"""Replayable linear regression simulator; all charts derive from the same state."""
from __future__ import annotations
import copy
import time
import numpy as np
from .maths import loss_and_grad,regularization
from .optimizers import update,scheduler_lr

DEFAULT={'n':90,'true_w':2.7,'true_b':1.3,'noise':.65,'outliers':0,'seed':42,'w':-2.5,'b':-3.,
 'loss':'mse','weight_mode':'uniform','regularizer':'none','lam':0.,'ratio':.5,'delta':1.,'quantile':.5,'optimizer':'adam',
 'lr':.065,'batch':16,'sampling':'mini','momentum':.9,'beta1':.9,'beta2':.999,'rho':.9,'epsilon':1e-8,
 'weight_decay':.015,'clip':0.,'scheduler':'constant','total':200,'warmup':10}

class RegressionExperiment:
    def __init__(self,cfg=None,x=None,y=None):
        self.cfg=copy.deepcopy(DEFAULT);self.cfg.update(cfg or {})
        c=self.cfg; n=int(c['n'])
        if not 4<=n<=600:raise ValueError('Число точек должно быть 4–600')
        self.rng=np.random.default_rng(int(c['seed']))
        if x is None:
            self.x=np.sort(self.rng.uniform(-3,3,n))
            self.y=float(c['true_w'])*self.x+float(c['true_b'])+self.rng.normal(0,float(c['noise']),n)
            out=min(n,max(0,int(c.get('outliers',0))))
            if out:
                ids=self.rng.choice(n,out,replace=False);self.y[ids]+=self.rng.choice([-1,1],out)*self.rng.uniform(3,8,out)
        else:
            self.x=np.asarray(x,dtype=float);self.y=np.asarray(y,dtype=float)
            if self.x.ndim!=1 or self.y.ndim!=1 or len(self.x)!=len(self.y) or not 4<=len(self.x)<=600 or not np.isfinite(self.x).all() or not np.isfinite(self.y).all():raise ValueError('Некорректные данные: две числовые колонки, 4–600 точек')
            self.cfg['n']=len(self.x)
        self.theta=np.array([float(c['w']),float(c['b'])]);self.optstate={};self.step_count=0;self.cursor=0
        self.order=self.rng.permutation(len(self.x)).tolist();self.history=[];self.last={};self.record()

    def objective(self,theta,idx=None):
        ids=np.arange(len(self.x)) if idx is None else np.asarray(idx,dtype=int)
        p=theta[0]*self.x[ids]+theta[1]
        weights=None
        if self.cfg['loss']=='weighted_mse':
            mode=self.cfg.get('weight_mode','uniform')
            if mode=='edge':weights=1+abs(self.x[ids])
            elif mode=='center':weights=1/(1+abs(self.x[ids]))
            elif mode!='uniform':raise ValueError('Неизвестный режим весов примеров')
        data,der=loss_and_grad(self.y[ids],p,self.cfg['loss'],self.cfg['delta'],self.cfg['quantile'],weights)
        pen,pg=regularization(theta[:1],self.cfg['regularizer'],self.cfg['lam'],self.cfg['ratio'])
        grad=np.array([np.dot(der,self.x[ids])+pg[0],np.sum(der)])
        return float(data+pen),float(data),float(pen),grad

    def record(self):
        total,data,pen,grad=self.objective(self.theta)
        snap={'step':self.step_count,'w':float(self.theta[0]),'b':float(self.theta[1]),
              'loss':total,'data_loss':data,'penalty':pen,'gradient':grad.tolist(),
              'optimizer_state':copy.deepcopy(self.optstate),'detail':copy.deepcopy(self.last),
              'cursor':self.cursor,'order':list(self.order),'rng':copy.deepcopy(self.rng.bit_generator.state)}
        self.history.append(snap)
        if len(self.history)>1500:self.history.pop(0)
        return snap

    def _batch(self):
        c=self.cfg;n=len(self.x);mode=c.get('sampling','mini')
        if mode=='full':return np.arange(n)
        batch=1 if mode=='stochastic' else min(n,max(1,int(c['batch'])))
        ids=[]
        while len(ids)<batch:
            take=min(batch-len(ids),n-self.cursor)
            ids.extend(self.order[self.cursor:self.cursor+take]);self.cursor+=take
            if self.cursor>=n:
                self.cursor=0;self.order=self.rng.permutation(n).tolist()
        return np.array(ids,dtype=int)

    def step(self):
        ids=self._batch();c=self.cfg;lr=scheduler_lr(self.step_count,float(c['lr']),c['scheduler'],int(c['total']),int(c['warmup']))
        before=self.theta.copy();batch_loss,_,_,g=self.objective(before,ids)
        name=c['optimizer']
        if name=='nesterov':
            velocity=np.asarray(self.optstate.get('velocity',[0.,0.]));look=before+float(c['momentum'])*velocity
            _,_,_,g=self.objective(look,ids)
        else:look=None
        new,state,detail=update(before,g,self.optstate,name=name,lr=lr,beta1=float(c['beta1']),beta2=float(c['beta2']),
                eps=float(c['epsilon']),momentum=float(c['momentum']),rho=float(c['rho']),decay=float(c['weight_decay']),clip=float(c['clip']))
        self.theta=new;self.optstate=state;self.step_count+=1
        self.last={'batch_indices':ids.tolist(),'batch_loss_before':batch_loss,'gradient_at':look.tolist() if look is not None else before.tolist(),**detail}
        self.record();return self.history[-1]

    def run(self,steps=50):
        steps=max(0,min(500,int(steps)))
        for _ in range(steps):
            self.step()
            if np.linalg.norm(self.history[-1]['gradient'])<1e-9:break
        return self.state()

    def seek(self,step):
        found=next((h for h in self.history if h['step']==int(step)),None)
        if found is None:raise ValueError('Шаг отсутствует в истории')
        self.theta=np.array([found['w'],found['b']]);self.step_count=found['step'];self.optstate=copy.deepcopy(found['optimizer_state'])
        self.cursor=found['cursor'];self.order=list(found['order']);self.rng.bit_generator.state=copy.deepcopy(found['rng']);self.last=copy.deepcopy(found['detail'])
        self.history=[h for h in self.history if h['step']<=step]
        return self.state()

    def set_params(self,params):
        if any(k in params for k in ('w','b')):
            self.theta=np.array([float(params.get('w',self.theta[0])),float(params.get('b',self.theta[1]))]);self.cfg.update(w=float(self.theta[0]),b=float(self.theta[1]))
            self.history=[];self.step_count=0;self.optstate={};self.last={};self.record()
        else:
            keys=set(DEFAULT)-{'seed','n','true_w','true_b','noise','outliers','w','b'}
            for k,v in params.items():
                if k in keys:self.cfg[k]=v
            self.history=[];self.step_count=0;self.optstate={};self.last={};self.record()
        return self.state()

    def surface(self,resolution=52):
        c=self.cfg;w0,b0=self.theta;ww=np.linspace(min(-4,w0-2,float(c['true_w'])-2),max(5,w0+2,float(c['true_w'])+2),resolution)
        bb=np.linspace(min(-5,b0-2,float(c['true_b'])-2),max(5,b0+2,float(c['true_b'])+2),resolution)
        W,B=np.meshgrid(ww,bb);z=np.zeros_like(W)
        # Vectorized over sample axis; share exactly the same loss definition as objective().
        for i in range(len(bb)):
            for j in range(len(ww)):
                z[i,j]=self.objective(np.array([ww[j],bb[i]]))[0]
        return {'w':ww.tolist(),'b':bb.tolist(),'z':z.tolist()}

    def state(self,with_surface=False):
        last=self.history[-1]; p=self.theta[0]*self.x+self.theta[1]; residual=p-self.y
        result={'config':self.cfg,'x':self.x.tolist(),'y':self.y.tolist(),'prediction':p.tolist(),
            'residual':residual.tolist(),'theta':self.theta.tolist(),'current':last,
            'history':[{k:h[k] for k in ('step','w','b','loss','data_loss','penalty','gradient')} for h in self.history],
            'detail':self.last,'steps':self.step_count,'score':{'rmse':float(np.sqrt(np.mean(residual**2))),'mae':float(np.mean(abs(residual))),'r2':float(1-np.sum(residual**2)/(np.sum((self.y-np.mean(self.y))**2)+1e-12))}}
        if with_surface:result['surface']=self.surface()
        return result

    def export(self):
        return {'format':'mluniverse-experiment','version':1,'config':self.cfg,'x':self.x.tolist(),'y':self.y.tolist(),
                'full_history':copy.deepcopy(self.history)}

    @classmethod
    def load(cls,obj):
        if obj.get('format')!='mluniverse-experiment' or obj.get('version')!=1:raise ValueError('Неизвестный формат эксперимента')
        e=cls(obj['config'],obj['x'],obj['y']);hs=obj['full_history']
        if not hs or len(hs)>1500:raise ValueError('Неверная история')
        e.history=hs;e.seek(hs[-1]['step']);return e

def compare(config,names,steps=100):
    if len(names)>9:raise ValueError('Не более 9 алгоритмов')
    base=RegressionExperiment(config);result=[]
    for name in names:
        c={**config,'optimizer':name};e=RegressionExperiment(c,base.x,base.y)
        # Same RNG behavior between runs, including batch permutations.
        for _ in range(min(400,max(1,int(steps)))):
            try:e.step()
            except (ValueError,FloatingPointError):break
        result.append({'name':name,'history':[{k:h[k] for k in ('step','w','b','loss')} for h in e.history],
            'final':e.history[-1],'steps':e.step_count})
    return {'runs':result,'x':base.x.tolist(),'y':base.y.tolist()}
