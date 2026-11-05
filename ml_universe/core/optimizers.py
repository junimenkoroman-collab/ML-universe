"""Numerically transparent optimizers and learning-rate schedules."""
import math
import numpy as np
SUPPORTED=['sgd','momentum','nesterov','adagrad','rmsprop','adam','adamw','amsgrad','nadam','adamax','adadelta','lion']
def update(theta,grad,state,name='adam',lr=.03,beta1=.9,beta2=.999,eps=1e-8,momentum=.9,rho=.9,decay=0.,clip=0.):
    p=np.asarray(theta,dtype=float);g=np.asarray(grad,dtype=float).copy()
    if p.shape!=g.shape or not np.isfinite(g).all():raise ValueError('Некорректный градиент')
    norm=float(np.linalg.norm(g))
    if clip and norm>clip:g*=clip/max(norm,1e-20)
    t=int(state.get('t',0))+1;s={'t':t};detail={'gradient':g.tolist(),'gradient_norm':norm,'learning_rate':float(lr)}
    old=lambda k:np.asarray(state.get(k,np.zeros_like(p)),dtype=float)
    if name=='sgd':delta=-lr*g
    elif name in ('momentum','nesterov'):
        v=momentum*old('velocity')-lr*g;s['velocity']=v.tolist();delta=v;detail['velocity']=v.tolist()
    elif name=='adagrad':
        a=old('sumsq')+g*g;s['sumsq']=a.tolist();delta=-lr*g/(np.sqrt(a)+eps);detail['accumulated_squared_gradient']=a.tolist()
    elif name=='rmsprop':
        v=rho*old('v')+(1-rho)*g*g;s['v']=v.tolist();delta=-lr*g/(np.sqrt(v)+eps);detail['second_moment']=v.tolist()
    elif name in ('adam','adamw','amsgrad','nadam'):
        m=beta1*old('m')+(1-beta1)*g;v=beta2*old('v')+(1-beta2)*g*g
        mh=m/(1-beta1**t);vh=v/(1-beta2**t);s.update(m=m.tolist(),v=v.tolist())
        detail.update(first_moment=m.tolist(),second_moment=v.tolist(),m_hat=mh.tolist(),v_hat=vh.tolist())
        if name=='amsgrad':
            vmax=np.maximum(old('vmax'),vh);s['vmax']=vmax.tolist();vh=vmax;detail['vmax']=vmax.tolist()
        if name=='nadam':mh=beta1*m/(1-beta1**(t+1))+(1-beta1)*g/(1-beta1**t)
        delta=-lr*mh/(np.sqrt(vh)+eps)
        if name=='adamw':delta-=lr*decay*p;detail['decoupled_decay']=(-lr*decay*p).tolist()
    elif name=='adadelta':
        eg=rho*old('eg')+(1-rho)*g*g;d=-np.sqrt(old('edx')+eps)/np.sqrt(eg+eps)*g;edx=rho*old('edx')+(1-rho)*d*d
        s.update(eg=eg.tolist(),edx=edx.tolist());delta=lr*d;detail.update(grad_ema=eg.tolist(),update_ema=edx.tolist())
    elif name=='adamax':
        m=beta1*old('m')+(1-beta1)*g;u=np.maximum(beta2*old('u'),abs(g));delta=-lr*m/((1-beta1**t)*(u+eps));s.update(m=m.tolist(),u=u.tolist());detail.update(first_moment=m.tolist(),infinity_ema=u.tolist())
    elif name=='lion':
        c=beta1*old('m')+(1-beta1)*g;delta=-lr*np.sign(c)-lr*decay*p;m=beta2*old('m')+(1-beta2)*g;s['m']=m.tolist();detail['signed_direction']=np.sign(c).tolist()
    else:raise ValueError('Оптимизатор не поддерживается')
    result=p+delta
    if not np.isfinite(result).all() or max(abs(result))>1e12:raise FloatingPointError('Расходимость — веса слишком велики')
    detail.update(update=delta.tolist(),before=p.tolist(),after=result.tolist())
    return result,s,detail

def scheduler_lr(step,base,kind='constant',total=200,warmup=10,gamma=.97):
    t=max(0,int(step));total=max(1,int(total))
    if kind=='constant':return base
    if kind=='step':return base*gamma**(t//max(1,total//5))
    if kind=='exponential':return base*gamma**t
    if kind=='cosine':return base*.5*(1+math.cos(math.pi*min(t,total)/total))
    if kind=='warmup_cosine':
        if t<warmup:return base*(t+1)/max(1,warmup)
        return base*.5*(1+math.cos(math.pi*min(t-warmup,total-warmup)/max(1,total-warmup)))
    if kind=='inverse':return base/(1+.02*t)
    if kind=='polynomial':return base*max(0,1-t/total)**2
    if kind=='cyclic':return base*(.1+.9*(1-abs(2*((t%max(2,total//3))/max(2,total//3))-1)))
    raise ValueError('Неизвестный scheduler')
