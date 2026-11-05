"""Focused, computationally real laboratories: regression, ML, DL and NLP."""
from __future__ import annotations
import math,re
import numpy as np
from scipy.special import expit,softmax
from sklearn.datasets import make_moons,make_circles,make_blobs
from sklearn.metrics import (confusion_matrix,accuracy_score,precision_score,recall_score,f1_score,roc_curve,roc_auc_score,precision_recall_curve,average_precision_score)
from sklearn.tree import DecisionTreeClassifier,export_text
from sklearn.ensemble import RandomForestClassifier,GradientBoostingClassifier
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import TfidfVectorizer,CountVectorizer
from .maths import safe_evaluate,numerical_gradient,numerical_hessian,activation,activation_prime,BENCHMARKS
from .optimizers import update

def scatter(x,y,name='Данные',color='#0d9488',mode='markers',size=8,**kwargs):
    return {'type':'scatter','mode':mode,'name':name,'x':np.asarray(x).tolist(),'y':np.asarray(y).tolist(), 'marker':{'color':color,'size':size},**kwargs}

def heatmap(z,x=None,y=None,name='',colorscale='Viridis'):
    d={'type':'heatmap','z':np.asarray(z).tolist(),'colorscale':colorscale,'name':name,'colorbar':{'thickness':11}}
    if x is not None:d['x']=np.asarray(x).tolist()
    if y is not None:d['y']=np.asarray(y).tolist()
    return d

def chart(title,*traces,xlabel='',ylabel='',height=370,**opts):
    return {'title':title,'traces':list(traces),'layout':{'height':height,'margin':{'l':50,'r':18,'t':38,'b':50},'xaxis':{'title':xlabel},'yaxis':{'title':ylabel},**opts}}

def result(name,charts,stats=None,explain='',table=None,details=None):
    return {'name':name,'charts':charts,'stats':stats or {},'explain':explain,'table':table or [],'details':details or {}}

def make_data(cfg):
    typ=cfg.get('dataset','moons'); n=max(30,min(500,int(cfg.get('n',180))));noise=float(cfg.get('noise',.22));seed=int(cfg.get('seed',42))
    if typ=='circles':x,y=make_circles(n_samples=n,noise=noise/2,factor=.45,random_state=seed)
    elif typ=='blobs':x,y=make_blobs(n_samples=n,centers=3,cluster_std=max(.15,noise*3),random_state=seed)
    elif typ=='xor':
        rng=np.random.default_rng(seed);x=rng.uniform(-2,2,(n,2));y=(x[:,0]*x[:,1]>0).astype(int);x+=rng.normal(0,noise*.3,x.shape)
    elif typ=='spiral':
        rng=np.random.default_rng(seed);count=n//2;theta=np.linspace(0,3*np.pi,count);r=np.linspace(.05,1.2,count)
        a=np.column_stack((r*np.cos(theta),r*np.sin(theta)));b=-a;x=np.vstack((a,b))+rng.normal(0,noise*.25,(2*count,2));y=np.array([0]*count+[1]*count)
    else:x,y=make_moons(n_samples=n,noise=noise,random_state=seed)
    return x,np.asarray(y,dtype=int)

def boundaries(model,x,res=75):
    xx=np.linspace(float(x[:,0].min())-.65,float(x[:,0].max())+.65,res)
    yy=np.linspace(float(x[:,1].min())-.65,float(x[:,1].max())+.65,res)
    a,b=np.meshgrid(xx,yy);grid=np.c_[a.ravel(),b.ravel()];pred=model.predict(grid).reshape(a.shape)
    proba=model.predict_proba(grid)[:,1].reshape(a.shape) if hasattr(model,'predict_proba') and len(model.classes_)==2 else None
    return xx,yy,pred,proba

def classification_lab(c):
    x,y=make_data(c);kind=c.get('algorithm','logistic');C=float(c.get('C',1.));depth=int(c.get('depth',4))
    models={ 'logistic':lambda:LogisticRegression(C=max(.001,C),max_iter=500),
      'softmax':lambda:LogisticRegression(C=max(.001,C),max_iter=500),
      'tree':lambda:DecisionTreeClassifier(max_depth=depth,min_samples_leaf=int(c.get('min_leaf',2)),criterion=c.get('criterion','gini'),random_state=int(c.get('seed',42))),
      'forest':lambda:RandomForestClassifier(n_estimators=int(c.get('trees',35)),max_depth=depth,random_state=int(c.get('seed',42))),
            'boosting':lambda:GradientBoostingClassifier(n_estimators=int(c.get('trees',35)),learning_rate=float(c.get('lr',.1)),max_depth=min(depth,5),random_state=int(c.get('seed',42))),
      'svm':lambda:SVC(C=max(.001,C),kernel=c.get('kernel','rbf'),gamma=float(c.get('gamma',1.)),probability=True,random_state=int(c.get('seed',42))),
      'knn':lambda:KNeighborsClassifier(n_neighbors=int(c.get('k',7))),
      'naive_bayes':lambda:GaussianNB() }
    if kind not in models:raise ValueError('Классификатор не найден')
    if kind=='softmax':
        x,y=make_data({**c,'dataset':'blobs'})
    model=models[kind]();model.fit(x,y);xx,yy,z,pr=boundaries(model,x)
    threshold=float(c.get('threshold',.5));train_pr=model.predict_proba(x)[:,1] if len(np.unique(y))==2 else None
    prediction=(train_pr>=threshold).astype(int) if train_pr is not None else model.predict(x)
    cm=confusion_matrix(y,prediction,labels=np.unique(y));acc=float(accuracy_score(y,prediction))
    charts=[chart('Реальные границы решений',heatmap(z,xx,yy,colorscale='Cividis'),scatter(x[:,0],x[:,1],color=y.tolist(),size=9),xlabel='x₁',ylabel='x₂'),
        chart('Матрица ошибок',heatmap(cm,colorscale='Blues'),xlabel='Предсказано',ylabel='Истинный класс')]
    stats={'accuracy':round(acc,4),'n_samples':len(y),'classes':len(np.unique(y))}
    if train_pr is not None:
        stats.update(precision=round(float(precision_score(y,prediction,zero_division=0)),4),recall=round(float(recall_score(y,prediction,zero_division=0)),4),f1=round(float(f1_score(y,prediction,zero_division=0)),4))
        fpr,tpr,_=roc_curve(y,train_pr)
        charts.append(chart('ROC-кривая',scatter(fpr,tpr,'ROC',mode='lines'),scatter([0,1],[0,1],'Случайная модель',mode='lines'),xlabel='FPR',ylabel='TPR'))
        prec,rec,_=precision_recall_curve(y,train_pr)
        charts.append(chart('Precision–Recall',scatter(rec,prec,'PR',mode='lines'),xlabel='Recall',ylabel='Precision'))
        charts.append(chart('Вероятность положительного класса',heatmap(pr,xx,yy),scatter(x[:,0],x[:,1],color=y.tolist(),size=7),xlabel='x₁',ylabel='x₂'))
        stats['average_precision']=round(float(average_precision_score(y,train_pr)),4)
        stats['roc_auc']=round(float(roc_auc_score(y,train_pr)),4)
    if kind=='tree':
        tree=model.tree_;candidates=[]
        for j in range(min(tree.node_count,30)):
            candidates.append({'node':j,'feature':int(tree.feature[j]),'threshold':round(float(tree.threshold[j]),4),'samples':int(tree.n_node_samples[j]),'impurity':round(float(tree.impurity[j]),4)})
        stats['nodes']=int(tree.node_count);stats['depth']=int(tree.max_depth)
        def impurity(labels):
            counts=np.bincount(labels,minlength=len(np.unique(y))).astype(float);prob=counts/counts.sum()
            return float(1-np.sum(prob**2)) if model.criterion=='gini' else float(-np.sum(prob[prob>0]*np.log2(prob[prob>0])))
        parent=impurity(y);splits=[]
        for feature in (0,1):
            vals=np.unique(x[:,feature]);thresholds=(vals[1:]+vals[:-1])/2
            for threshold in thresholds:
                mask=x[:,feature]<=threshold
                if min(mask.sum(),(~mask).sum())<model.min_samples_leaf:continue
                score=parent-(mask.mean()*impurity(y[mask])+(~mask).mean()*impurity(y[~mask]))
                splits.append({'feature':f'x{feature+1}','threshold':round(float(threshold),4),'gain':round(float(score),7),'left':int(mask.sum()),'right':int((~mask).sum())})
        splits.sort(key=lambda row:-row['gain'])
        top=splits[:24]
        if top:
            charts.append(chart('Кандидаты split корневого узла',{'type':'bar','x':[f"{v['feature']} ≤ {v['threshold']}" for v in top[:15]],'y':[v['gain'] for v in top[:15]],'marker':{'color':'#8eb4f1'}},xlabel='Кандидат split',ylabel='Уменьшение impurity'))
        stats['root_feature']=int(tree.feature[0]);stats['root_threshold']=round(float(tree.threshold[0]),5)
        explanation='В таблице настоящие кандидаты порога корневого узла и уменьшение weighted impurity; дерево обучено алгоритмом sklearn CART.'
        return result(kind,charts,stats,explanation,top,{'tree_text':export_text(model,feature_names=['x1','x2']),'nodes':candidates})
    if kind=='forest':stats['trees']=len(model.estimators_)
    if kind=='svm':stats['support_vectors']=len(model.support_vectors_)
    if kind in ('logistic','softmax'):
        stats['w']=np.round(model.coef_,4).tolist();stats['bias']=np.round(model.intercept_,4).tolist()
    if kind=='softmax':
        probs=model.predict_proba(x)
        charts.append(chart('Softmax вероятности классов',heatmap(probs,model.classes_,range(len(x))),xlabel='Класс',ylabel='Объект'))
        stats['macro_f1']=round(float(f1_score(y,prediction,average='macro')),4)
    return result(kind,charts,stats,'Результат настоящего обучения выбранного классификатора на синтетическом наборе. Threshold влияет на метрики, не меняя вероятности.')

def clustering_lab(c):
    """Iterative K-Means only; unrelated unsupervised algorithms intentionally removed."""
    x,_=make_data({**c,'dataset':c.get('dataset','blobs')});k=max(2,min(9,int(c.get('k',3))))
    rng=np.random.default_rng(int(c.get('seed',42)))
    init=c.get('init','k-means++')
    if init=='random':centers=x[rng.choice(len(x),size=k,replace=False)].copy()
    elif init=='k-means++':
        ids=[int(rng.integers(len(x)))]
        while len(ids)<k:
            dist2=np.min(np.sum((x[:,None,:]-x[np.array(ids)][None,:,:])**2,axis=2),axis=1)
            if dist2.sum()<=1e-12:ids.append(int(rng.choice([j for j in range(len(x)) if j not in ids])))
            else:ids.append(int(rng.choice(len(x),p=dist2/dist2.sum())))
        centers=x[ids].copy()
    else:raise ValueError('Неизвестная инициализация K-Means')
    trajectories=[centers.copy()];inertias=[]
    for step in range(max(1,min(100,int(c.get('iterations',30))))):
        dist=np.sum((x[:,None,:]-centers[None,:,:])**2,axis=2);labels=np.argmin(dist,axis=1)
        inertias.append(float(np.min(dist,axis=1).sum()))
        new=np.array([x[labels==j].mean(axis=0) if np.any(labels==j) else centers[j] for j in range(k)])
        trajectories.append(new.copy())
        if np.linalg.norm(new-centers)<1e-6:centers=new;break
        centers=new
    dist=np.sum((x[:,None,:]-centers[None,:,:])**2,axis=2);labels=np.argmin(dist,axis=1)
    inertia=float(np.min(dist,axis=1).sum());inertias.append(inertia)
    traces=[scatter(x[:,0],x[:,1],color=labels.tolist(),size=9),scatter(centers[:,0],centers[:,1],'Центроиды',color='#0d9488',size=16,marker={'color':'#0d9488','size':16,'symbol':'x'})]
    for j in range(k):
        path=np.array(trajectories)[:,j,:];traces.append(scatter(path[:,0],path[:,1],f'Центроид {j+1}',mode='lines+markers',size=5,color='#64748b'))
    uniq,counts=np.unique(labels,return_counts=True)
    return result('clustering',[chart('Кластеры и путь центроидов',*traces,xlabel='x₁',ylabel='x₂'),chart('Размеры кластеров',{'type':'bar','x':uniq.astype(str).tolist(),'y':counts.tolist()},xlabel='Кластер',ylabel='Точки'),chart('Inertia по итерациям',scatter(range(len(inertias)),inertias,'Within-cluster SSE',mode='lines+markers'),xlabel='Шаг',ylabel='SSE')],{'inertia':round(inertia,3),'iterations':len(trajectories)-1,'k':k},'K-Means: показаны действительные assignment/update, центроиды и сумма квадратов расстояний. Инициализация K-Means++ или random; других методов кластеризации в учебной программе нет.')


def math_lab(c):
    expr=str(c.get('expression','sin(x)+0.15*x**2'));mode=c.get('dimension','1d');xmin=float(c.get('xmin',-5));xmax=float(c.get('xmax',5))
    if not xmin<xmax or xmax-xmin>50:raise ValueError('Некорректный диапазон')
    if mode=='1d':
        x=np.linspace(xmin,xmax,300);y=np.broadcast_to(safe_evaluate(expr,x=x),x.shape);at=float(c.get('at',1.));v=float(safe_evaluate(expr,x=at))
        d=float(numerical_gradient(lambda t:float(safe_evaluate(expr,x=t[0])),[at])[0]);tangent=v+d*(x-at)
        return result('math',[chart('Функция и касательная',scatter(x,y,'f(x)',mode='lines'),scatter(x,tangent,'Касательная',mode='lines',color='#ad8c68'),scatter([at],[v],'Текущая точка',color='#ad97ff',size=13),xlabel='x',ylabel='f(x)'),chart('Численная производная',scatter(x,np.gradient(y,x),'f′(x)',mode='lines'),xlabel='x',ylabel='df/dx')],{'f(x)':round(v,5),'f_prime':round(d,5)},'Центральная численная производная. Для негладких точек результат зависит от шага.')
    x=np.linspace(xmin,xmax,72);X,Y=np.meshgrid(x,x);Z=np.broadcast_to(safe_evaluate(expr,x=X,y=Y),X.shape)
    at=float(c.get('at',1.))
    fn=lambda z:float(safe_evaluate(expr,x=z[0],y=z[1]))
    grad=numerical_gradient(fn,[at,at]);hessian=numerical_hessian(fn,[at,at])
    return result('math',[chart('Линии уровня',heatmap(Z,x,x),xlabel='x',ylabel='y'),chart('Поверхность функции',{'type':'surface','x':x.tolist(),'y':x.tolist(),'z':Z.tolist(),'colorscale':'Viridis'},height=425)],{'min_on_grid':round(float(np.min(Z)),5),'max_on_grid':round(float(np.max(Z)),5),'gradient_norm_at_(t,t)':round(float(np.linalg.norm(grad)),5)},'Построен численный срез выбранной функции двух переменных. Градиент и симметризованный Hessian оценены центральными разностями в точке (t,t).',details={'point':[at,at],'gradient':np.round(grad,5).tolist(),'hessian':np.round(hessian,5).tolist()})

def optimizer_gallery(c):
    name=c.get('function','himmelblau');expr=c.get('expression','x*x+y*y');base=BENCHMARKS.get(name)
    fn=base[1] if base else lambda x,y:safe_evaluate(expr,x=x,y=y)
    start=np.array([float(c.get('x0',-1.5)),float(c.get('y0',2.5))]);steps=int(c.get('steps',75));lr=float(c.get('lr',.015));names=c.get('optimizers',['sgd','momentum','rmsprop','adam','adamw'])
    x=np.linspace(-3,3,65);xx,yy=np.meshgrid(x,x)
    with np.errstate(over='ignore',invalid='ignore'):zz=np.asarray(fn(xx,yy),dtype=float)
    if zz.shape!=xx.shape:zz=np.broadcast_to(zz,xx.shape)
    if not np.isfinite(zz).all():raise ValueError('Поверхность содержит NaN/Inf')
    contour=[{'type':'contour','x':x.tolist(),'y':x.tolist(),'z':zz.tolist(),'colorscale':'Viridis','ncontours':25,'showscale':False}];lines=[];surface=[];stats={}
    palette=['#0d9488','#8680a8','#bf986e','#72a58c','#ad7b88','#b2a075','#8799b0','#a594b1']
    for idx,opt in enumerate(names[:8]):
        color=palette[idx%len(palette)]
        theta=start.copy();state={};path=[theta.tolist()];losses=[float(fn(*theta))]
        for t in range(max(1,min(350,steps))):
            try:
                g=numerical_gradient(lambda z:float(fn(*z)),theta)
                if opt=='nesterov':
                    v=np.asarray(state.get('velocity',[0.,0.]));g=numerical_gradient(lambda z:float(fn(*z)),theta+.9*v)
                if opt=='projected':
                    radius=float(c.get('radius',1.8));raw=theta-lr*g
                    theta=raw*min(1.,radius/max(np.linalg.norm(raw),1e-12))
                else:theta,state,_=update(theta,g,state,name=opt,lr=lr,decay=.05)
                loss=float(fn(*theta))
                if not np.isfinite(loss):break
                losses.append(loss);path.append(theta.tolist())
            except (ValueError,FloatingPointError,OverflowError):break
        path=np.array(path);contour.append(scatter(path[:,0],path[:,1],opt,mode='lines+markers',size=4,color=color,line={'color':color,'width':2}));lines.append(scatter(range(len(losses)),losses,opt,mode='lines',color=color,line={'color':color,'width':2}));surface.append({'type':'scatter3d','mode':'lines+markers','x':path[:,0].tolist(),'y':path[:,1].tolist(),'z':losses,'name':opt,'line':{'color':color,'width':4},'marker':{'color':color,'size':2}})
        stats[opt]=round(losses[-1],5)
    charts=[chart('Траектории · линии уровня',*contour,xlabel='x',ylabel='y'),chart('Objective по шагам',*lines,xlabel='Шаг',ylabel='f(x,y)'),chart('3D-поверхность + траектории',{'type':'surface','x':x.tolist(),'y':x.tolist(),'z':zz.tolist(),'opacity':.80,'showscale':False},*surface,height=440)]
    charts[2]['wide']=True
    return result('optimizer_gallery',charts,stats,'Projected GD после градиентного шага проектирует точку на L2-шар радиуса R. Одинаковая стартовая точка. Траектории рассчитаны численно, не анимированы по шаблону. Сравнивайте с учётом гиперпараметров.')

def neural_lab(c):
    seed=int(c.get('seed',42));rng=np.random.default_rng(seed);hidden=int(c.get('hidden',6));hidden=max(2,min(hidden,30));steps=int(c.get('steps',500));lr=float(c.get('lr',.1))
    x,y=make_data({'dataset':c.get('dataset','xor'),'n':int(c.get('n',180)),'noise':float(c.get('noise',.08)),'seed':seed});y=y%2
    W1=rng.normal(0,np.sqrt(2/2),(2,hidden));b1=np.zeros(hidden);W2=rng.normal(0,np.sqrt(2/hidden),(hidden,1));b2=np.zeros(1)
    losses=[];activ=c.get('activation','tanh');detail={}
    for t in range(max(1,min(1200,steps))):
        z1=x@W1+b1;a1=activation(z1,activ);z2=a1@W2+b2;out=expit(z2).flatten()
        loss=float(np.mean(np.logaddexp(0,z2.flatten())-y*z2.flatten()));losses.append(loss)
        dz2=(out-y).reshape(-1,1)/len(x);dw2=a1.T@dz2;db2=dz2.sum(axis=0)
        dz1=(dz2@W2.T)*activation_prime(z1,activ);dw1=x.T@dz1;db1=dz1.sum(axis=0)
        if t==0:
            # Gradient check at the *pre-update* weights and biases.
            w=W1[0,0];eps=1e-5
            def check_loss(candidate):
                W1[0,0]=candidate
                pre=activation(x@W1+b1,activ)@W2+b2
                return float(np.mean(np.logaddexp(0,pre.flatten())-y*pre.flatten()))
            numeric=(check_loss(w+eps)-check_loss(w-eps))/(2*eps)
            W1[0,0]=w
            detail={'gradient_W1_first_step':np.round(dw1,6).tolist(),'gradient_W2_first_step':np.round(dw2,6).tolist(),'gradient_check_w1_00':{'analytic':float(dw1[0,0]),'numeric':float(numeric),'abs_diff':abs(float(dw1[0,0])-float(numeric))}}
        W1-=lr*dw1;b1-=lr*db1;W2-=lr*dw2;b2-=lr*db2
    gx=np.linspace(float(x[:,0].min())-.4,float(x[:,0].max())+.4,70);gy=np.linspace(float(x[:,1].min())-.4,float(x[:,1].max())+.4,70);X,Y=np.meshgrid(gx,gy);z=np.c_[X.ravel(),Y.ravel()];probs=expit(activation(z@W1+b1,activ)@W2+b2).reshape(X.shape)
    return result('neural',[chart('Нелинейная поверхность предсказания MLP',heatmap(probs,gx,gy),scatter(x[:,0],x[:,1],color=y.tolist()),xlabel='x₁',ylabel='x₂'),chart('Фактический BCE training loss',scatter(range(len(losses)),losses,'BCE',mode='lines'),xlabel='Шаг',ylabel='BCE'),chart('Распределение весов',{'type':'histogram','x':np.r_[W1.flatten(),W2.flatten()].tolist(),'marker':{'color':'#9390b9'}},xlabel='Значение веса')],{'final_bce':round(losses[-1],5),'hidden_neurons':hidden,'parameters':int(W1.size+b1.size+W2.size+b2.size),'train_accuracy':round(float(np.mean((expit(activation(x@W1+b1,activ)@W2+b2).flatten()>=.5)==y)),4)},'Небольшая 2→hidden→1 нейросеть. Forward, sigmoid BCE и аналитический backprop действительно выполняются в NumPy.',details=detail)

def neuron_lab(c):
    x=np.array([float(c.get('x1',1.)),float(c.get('x2',-1.))]);w=np.array([float(c.get('w1',.9)),float(c.get('w2',-.4))]);b=float(c.get('bias',.3));f=c.get('activation','sigmoid')
    z=float(w@x+b);a=float(activation(z,f));d=float(activation_prime(np.array([z]),f)[0]);grad=w*0 # grad output w.r.t. weights, not training loss
    v=np.linspace(-7,7,350);curve=activation(v,f)
    return result('neuron',[chart('Активация нейрона',scatter(v,curve,f,mode='lines'),scatter([z],[a],'Текущее значение',color='#ffd080',size=13),xlabel='z=w·x+b',ylabel='a=f(z)'),chart('Вклады линейной комбинации',{'type':'bar','x':['w₁x₁','w₂x₂','bias'],'y':[float(w[0]*x[0]),float(w[1]*x[1]),b],'marker':{'color':['#0d9488','#9090b0','#be9764']}},ylabel='Вклад')],{'z':round(z,6),'activation':round(a,6),'f_prime':round(d,6),'da_dw1':round(d*x[0],6),'da_dw2':round(d*x[1],6),'da_db':round(d,6)},'Forward: z=w₁x₁+w₂x₂+b; a=f(z). Производные выхода получены chain rule.')

def cnn_lab(c):
    side=12;x=np.zeros((side,side));x[3:9,4:8]=1.;x[5:7,2:10]=.6
    kernels={'sobel_x':[[-1,0,1],[-2,0,2],[-1,0,1]],'sobel_y':[[-1,-2,-1],[0,0,0],[1,2,1]],'blur':np.ones((3,3))/9,'sharpen':[[0,-1,0],[-1,5,-1],[0,-1,0]],'edge':[[-1,-1,-1],[-1,8,-1],[-1,-1,-1]],'identity':[[0,0,0],[0,1,0],[0,0,0]]}
    ker=np.asarray(kernels.get(c.get('kernel','sobel_x'),kernels['sobel_x']),dtype=float);stride=int(c.get('stride',1));pad=int(c.get('padding',0));xpad=np.pad(x,pad)
    out=np.array([[np.sum(xpad[i:i+3,j:j+3]*ker) for j in range(0,xpad.shape[1]-2,stride)] for i in range(0,xpad.shape[0]-2,stride)])
    return result('cnn',[chart('Исходное изображение',heatmap(x,colorscale='Greys')),chart('Ядро 3×3',heatmap(ker,colorscale='RdBu')),chart('Результат свёртки',heatmap(out,colorscale='RdBu')),chart('Receptive field: область первого выхода',heatmap(np.pad(np.ones((3,3)),((0,side-3),(0,side-3))),colorscale='Greys'),xlabel='Input pixel',ylabel='Input pixel')],{'input_shape':list(x.shape),'kernel_shape':[3,3],'output_shape':list(out.shape),'receptive_field':3,'stride':stride,'padding':pad},'Все пиксели вычислены непосредственным скалярным произведением input patch и kernel. В DL обычно это cross-correlation, а не переворот ядра.')

def nlp_lab(c):
    text=c.get('text','Машинное обучение учит модели. Машинное обучение работает с данными.');docs=c.get('documents','Машинное обучение полезно|Обучение моделей на данных|Данные и машинное обучение').split('|')
    tokens=re.findall(r"[\w]+|[^\w\s]",text.lower(),flags=re.UNICODE)
    vectorizer=TfidfVectorizer(token_pattern=r'(?u)\b\w+\b',lowercase=True);mat=vectorizer.fit_transform([d for d in docs if d.strip()])
    terms=vectorizer.get_feature_names_out();v=mat.toarray();sim=mat@mat.T
    counts={t:tokens.count(t) for t in sorted(set(tokens))};freq=sorted(counts.items(),key=lambda kv:-kv[1])
    return result('nlp',[chart('TF-IDF: документы × словарь',heatmap(v,terms,range(len(v))),xlabel='Термин',ylabel='Документ'),chart('Cosine similarity (TF-IDF нормализован)',heatmap(sim.toarray(),range(len(v)),range(len(v))),xlabel='Документ',ylabel='Документ'),chart('Частоты токенов',{'type':'bar','x':[z[0] for z in freq[:25]],'y':[z[1] for z in freq[:25]],'marker':{'color':'#76cafa'}})],{'tokens':len(tokens),'vocabulary':len(terms),'documents':len(v)},'Токенизация — Unicode regex; TF-IDF вычислен scikit-learn (smooth IDF, L2-нормировка).',table=[{'token':t,'count':n} for t,n in freq[:50]],details={'tokens':tokens,'terms':terms.tolist(),'matrix':np.round(v,4).tolist()})

def bpe_lab(c):
    corpus=str(c.get('text','кот котик коты кот котик собака')).lower().split();merges=max(0,min(30,int(c.get('merges',5))))
    words=[[ *list(w),'</w>'] for w in corpus];trace=[]
    for t in range(merges):
        freq={}
        for w in words:
            for pair in zip(w[:-1],w[1:]):freq[pair]=freq.get(pair,0)+1
        if not freq:break
        pair=max(freq,key=freq.get);trace.append({'step':t+1,'pair':' + '.join(pair),'frequency':freq[pair]});new=[]
        for w in words:
            out=[];i=0
            while i<len(w):
                if i<len(w)-1 and tuple(w[i:i+2])==pair:out.append(''.join(pair));i+=2
                else:out.append(w[i]);i+=1
            new.append(out)
        words=new
    lengths=[len(w) for w in words]
    return result('bpe',[chart('Длина токенизации после BPE',{'type':'bar','x':corpus,'y':lengths,'marker':{'color':'#9c88f0'}},xlabel='Слово',ylabel='Число токенов')],{'merges_done':len(trace),'unique_tokens':len({p for w in words for p in w})},'Реальные BPE merge-операции на данном учебном корпусе, начиная с символов.',table=trace,details={'encoded':words})

def attention_lab(c):
    tokens=str(c.get('text','кот видит свет')).split()[:12];n=len(tokens)
    if not n:raise ValueError('Требуется хотя бы один токен')
    d=max(2,min(12,int(c.get('d',4))));seed=int(c.get('seed',42));rng=np.random.default_rng(seed)
    X=rng.normal(0,.7,(n,d));Wq=rng.normal(0,1/np.sqrt(d),(d,d));Wk=rng.normal(0,1/np.sqrt(d),(d,d));Wv=rng.normal(0,1/np.sqrt(d),(d,d))
    Q=X@Wq;K=X@Wk;V=X@Wv;scale=np.sqrt(d)*max(.05,float(c.get('temperature',1.)));scores=Q@K.T/scale
    if c.get('causal',False):scores=np.where(np.triu(np.ones((n,n)),1)>0,-1e9,scores)
    A=softmax(scores,axis=1);output=A@V
    return result('attention',[chart('QKᵀ / √dₖ → Softmax',heatmap(A,tokens,tokens),xlabel='Key token',ylabel='Query token'),chart('Исходные embeddings',heatmap(X,list(range(d)),tokens),xlabel='Измерение',ylabel='Токен'),chart('Выход Attention = A·V',heatmap(output,list(range(d)),tokens),xlabel='Измерение',ylabel='Токен'),chart('Scaled scores до Softmax',heatmap(scores,tokens,tokens),xlabel='Key token',ylabel='Query token')],{'tokens':n,'head_dim':d,'max_row_sum_error':round(float(max(abs(A.sum(axis=1)-1))),12)},'Реальная цепь: Q=XWq, K=XWk, V=XWv, scores=QKᵀ/√d, A=softmax(scores), Out=AV. Матрицы учебные, случайно инициализированы.',details={'Q':np.round(Q,4).tolist(),'K':np.round(K,4).tolist(),'V':np.round(V,4).tolist(),'attention':np.round(A,4).tolist(),'output':np.round(output,4).tolist()})

def decoding_lab(c):
    words=['кот','идёт','спит','играет','в','саду','дома','быстро','медленно','!'];logits=np.array([1.6,2.,.5,1.2,.7,1.3,-.3,.1,-.5,.6]);temp=max(.05,float(c.get('temperature',1.)));k=max(1,min(len(words),int(c.get('top_k',10))));p=float(np.clip(float(c.get('top_p',1.)),.05,1))
    original=softmax(logits/temp);rank=np.argsort(-original);strategy=c.get('strategy','sampling')
    selected=rank[:k];cum=np.cumsum(original[selected]);keep=np.concatenate([[True],cum[:-1]<p]);selected=selected[keep]
    filtered=np.zeros(len(words));filtered[selected]=original[selected]/sum(original[selected])
    rng=np.random.default_rng(int(c.get('seed',42)))
    choice=words[int(rank[0])] if strategy=='greedy' else words[int(rng.choice(len(words),p=filtered))]
    return result('decoding',[chart('Распределение вероятностей токенов',{'type':'bar','x':words,'y':original.tolist(),'name':'Temperature','marker':{'color':'#7489fc'}},{'type':'bar','x':words,'y':filtered.tolist(),'name':'Top-k / Top-p','marker':{'color':'#63d2bb'}},barmode='group',ylabel='Вероятность')],{'sampled_token':choice,'entropy':round(float(-sum(original*np.log(original+1e-12))),4),'allowed_tokens':int((filtered>0).sum()),'strategy':strategy},'Учебный словарь и фиксированные logits; фильтрация и sampling математически настоящие, но это не обученная языковая модель.')

from .extras import algebra_lab,norm_lab,information_lab,schedulers_lab
LABS={
 'math':math_lab,'optimizer_gallery':optimizer_gallery,'classification':classification_lab,'clustering':clustering_lab,
 'neural':neural_lab,'neuron':neuron_lab,'cnn':cnn_lab,'nlp':nlp_lab,'bpe':bpe_lab,
 'attention':attention_lab,'decoding':decoding_lab,'algebra':algebra_lab,'norms':norm_lab,
 'information':information_lab,'schedulers':schedulers_lab
}
from .curriculum import CURRICULUM_LABS
LABS.update(CURRICULUM_LABS)

def run_lab(name,config=None):
    if name not in LABS:raise ValueError('Лаборатория не найдена: '+str(name))
    return LABS[name](config or {})
