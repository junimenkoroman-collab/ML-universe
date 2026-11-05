"""Additional mathematically grounded interactive educational laboratories."""
from __future__ import annotations
import math
import numpy as np
from scipy.stats import binom,norm,poisson,entropy,pearsonr
from sklearn.datasets import make_regression,make_classification
from sklearn.preprocessing import StandardScaler,MinMaxScaler,PolynomialFeatures
from sklearn.pipeline import make_pipeline
from sklearn.linear_model import Ridge,LinearRegression
from sklearn.metrics import mean_squared_error,ndcg_score,precision_score,recall_score,accuracy_score
from sklearn.model_selection import train_test_split,KFold,cross_val_score
from sklearn.ensemble import RandomForestRegressor,RandomForestClassifier
from sklearn.inspection import permutation_importance
from .labs import scatter,heatmap,chart,result
from .optimizers import scheduler_lr
from .maths import regularization,numerical_gradient


def algebra_lab(c):
    a=float(c.get('a',1.4));b=float(c.get('b',.4));cc=float(c.get('c',-.25));d=float(c.get('d',.8));M=np.array([[a,b],[cc,d]])
    grid=np.linspace(-2,2,8);lines=[];transformed=[]
    for value in grid:
        h=np.c_[grid,np.full(len(grid),value)];v=np.c_[np.full(len(grid),value),grid]
        for z in (h,v):
            lines.append(scatter(z[:,0],z[:,1],mode='lines',color='#5a7397',size=2))
            zz=z@M.T;transformed.append(scatter(zz[:,0],zz[:,1],mode='lines',color='#6fd0e0',size=2))
    eigen=np.linalg.eigvals(M);S=np.linalg.svd(M)[1];vec=np.array([float(c.get('x',1.)),float(c.get('y',1.))]);mapped=M@vec
    return result('algebra',[chart('Исходная координатная сетка',*lines,xlabel='x',ylabel='y',height=350),chart('Линейное преобразование A·x',*transformed,scatter([0,mapped[0]],[0,mapped[1]],'A·v',mode='lines+markers',color='#f4b772'),xlabel='x',ylabel='y',height=350)],{'det(A)':round(float(np.linalg.det(M)),4),'trace(A)':round(float(np.trace(M)),4),'singular_values':np.round(S,3).tolist(),'A·vector':np.round(mapped,4).tolist()},'Каждая точка сетки умножается на матрицу [[a,b],[c,d]]. Детерминант отражает масштаб ориентированной площади; SVD определяет растяжения.',details={'matrix':M.tolist(),'eigenvalues':[str(round(v.real,4))+'+'+str(round(v.imag,4))+'i' for v in eigen]})

def norm_lab(c):
    lam=float(c.get('lam',1.));p=float(c.get('p',1.));theta=np.linspace(0,2*np.pi,300);ct=np.cos(theta);st=np.sin(theta)
    # Norm unit ball boundaries.
    l1x=ct/(abs(ct)+abs(st));l1y=st/(abs(ct)+abs(st))
    linfx=ct/np.maximum(abs(ct),abs(st));linfy=st/np.maximum(abs(ct),abs(st))
    w=np.array([float(c.get('w1',1.)),float(c.get('w2',1.))]);g1=regularization(w,'l1',lam);g2=regularization(w,'l2',lam)
    return result('norms',[chart('Геометрия единичных шаров',scatter(l1x,l1y,'L1 = 1',mode='lines',color='#f6b17a'),scatter(ct,st,'L2 = 1',mode='lines',color='#65d6dc'),scatter(linfx,linfy,'L∞ = 1',mode='lines',color='#ae99ff'),scatter([w[0]],[w[1]],'w',size=13),xlabel='w₁',ylabel='w₂')],{'L1(w)':round(float(np.sum(abs(w))),4),'L2(w)':round(float(np.linalg.norm(w)),4),'L∞(w)':round(float(np.max(abs(w))),4),'L1 penalty':round(g1[0],4),'L2 squared penalty':round(g2[0],4)},'L0 считается количеством ненулевых компонент (не настоящая норма). L1 — ромб, L2 — круг, L∞ — квадрат.')

def stats_lab(c):
    rng=np.random.default_rng(int(c.get('seed',42)));samples=int(c.get('samples',500));group=max(1,int(c.get('group',8)));dist=c.get('distribution','exponential')
    if dist=='uniform':random=rng.uniform(size=(samples,group))
    elif dist=='normal':random=rng.normal(size=(samples,group))
    elif dist=='poisson':random=rng.poisson(2,(samples,group))
    else:random=rng.exponential(size=(samples,group))
    samplemeans=random.mean(axis=1);raw=random.ravel();mu=float(raw.mean());sd=float(raw.std())
    return result('statistics',[chart('Распределение исходных наблюдений',{'type':'histogram','x':raw.tolist(),'histnorm':'probability density','marker':{'color':'#69c8ed'}},xlabel='x',ylabel='Плотность'),chart('Распределение средних по группам',{'type':'histogram','x':samplemeans.tolist(),'histnorm':'probability density','marker':{'color':'#a590f9'}},xlabel='Среднее',ylabel='Плотность')],{'sample_mean':round(mu,4),'sample_std':round(sd,4),'std_of_sample_means':round(float(samplemeans.std()),4),'CLT_target_std':round(sd/np.sqrt(group),4)},'Центральная предельная теорема: при росте размера группы выборочные средние приближаются к нормальному распределению при выполнении условий теоремы.')

def information_lab(c):
    p=float(c.get('p',.3));q=float(c.get('q',.65));p=np.clip(p,1e-5,1-1e-5);q=np.clip(q,1e-5,1-1e-5)
    P=np.array([p,1-p]);Q=np.array([q,1-q]);H=float(entropy(P,base=2));KL=float(entropy(P,Q,base=2));cross=float(-sum(P*np.log2(Q)))
    x=np.linspace(.01,.99,180);curve=-x*np.log2(x)-(1-x)*np.log2(1-x)
    return result('information',[chart('Энтропия Bernoulli',scatter(x,curve,'H(p)',mode='lines'),scatter([p],[H],'Текущее p',size=13,color='#f8b57f'),xlabel='p',ylabel='Бит'),chart('P против Q',{'type':'bar','x':['событие 1','событие 2'],'y':P.tolist(),'name':'P'},{'type':'bar','x':['событие 1','событие 2'],'y':Q.tolist(),'name':'Q'},barmode='group')],{'Entropy H(P) bits':round(H,5),'Cross entropy H(P,Q) bits':round(cross,5),'KL(P||Q) bits':round(KL,5)},'H(P,Q)=H(P)+KL(P||Q). Логарифмы по основанию 2, результаты в битах.')

def validation_lab(c):
    rng=np.random.default_rng(int(c.get('seed',42)));n=int(c.get('n',75));noise=float(c.get('noise',.3));degree=int(c.get('degree',5))
    x=rng.uniform(-3,3,n);y=np.sin(1.6*x)+rng.normal(0,noise,n)
    train_idx,test_idx=train_test_split(np.arange(n),test_size=.3,random_state=42)
    model=make_pipeline(PolynomialFeatures(degree,include_bias=False),Ridge(alpha=.1));model.fit(x[train_idx,None],y[train_idx]);predict=model.predict(x[:,None]);gx=np.linspace(-3,3,300);gy=model.predict(gx[:,None]);trainerr=mean_squared_error(y[train_idx],predict[train_idx]);testerr=mean_squared_error(y[test_idx],predict[test_idx])
    degrees=list(range(1,16));trainloss=[];testloss=[]
    for d in degrees:
        m=make_pipeline(PolynomialFeatures(d,include_bias=False),Ridge(alpha=.1));m.fit(x[train_idx,None],y[train_idx]);trainloss.append(float(mean_squared_error(y[train_idx],m.predict(x[train_idx,None]))));testloss.append(float(mean_squared_error(y[test_idx],m.predict(x[test_idx,None]))))
    return result('validation',[chart('Недообучение vs переобучение',scatter(x[train_idx],y[train_idx],'Train',color='#6dcfec'),scatter(x[test_idx],y[test_idx],'Validation',color='#f3ac74'),scatter(gx,gy,'Полиномиальная модель',mode='lines',color='#b39cfc'),xlabel='x',ylabel='y'),chart('Training/validation curves',scatter(degrees,trainloss,'Train MSE',mode='lines+markers'),scatter(degrees,testloss,'Validation MSE',mode='lines+markers',color='#f9b672'),xlabel='Степень полинома',ylabel='MSE')],{'degree':degree,'train_MSE':round(float(trainerr),5),'validation_MSE':round(float(testerr),5),'generalization_gap':round(float(testerr-trainerr),5)},'Полиномиальные признаки + Ridge. Большая степень способна переобучаться; для выбора гиперпараметров не используйте финальный test как validation.')

def scaling_lab(c):
    rng=np.random.default_rng(int(c.get('seed',42)));n=150
    x=np.c_[rng.normal(size=n)*.5,rng.normal(size=n)*float(c.get('scale',25))];standard=StandardScaler().fit_transform(x);mm=MinMaxScaler().fit_transform(x)
    return result('scaling',[chart('Исходные масштабы',scatter(x[:,0],x[:,1],color='#f4b46b'),xlabel='feature1',ylabel='feature2'),chart('StandardScaler (μ=0, σ=1)',scatter(standard[:,0],standard[:,1],color='#68dbcd'),xlabel='z₁',ylabel='z₂'),chart('MinMaxScaler [0,1]',scatter(mm[:,0],mm[:,1],color='#a995f4'),xlabel='z₁',ylabel='z₂')],{'original_stdev':np.round(x.std(axis=0),3).tolist(),'scaled_stdev':np.round(standard.std(axis=0),3).tolist()},'Скейлинг меняет геометрию признаков и численную обусловленность оптимизации. Нормализаторы обучаются только на train при наличии split.')

def schedulers_lab(c):
    steps=int(c.get('steps',200));base=float(c.get('lr',.1));warmup=int(c.get('warmup',15));which=['constant','step','exponential','inverse','polynomial','cosine','warmup_cosine','cyclic'];lines=[]
    for name in which:lines.append(scatter(range(steps+1),[scheduler_lr(k,base,name,steps,warmup) for k in range(steps+1)],name,mode='lines'))
    return result('schedulers',[chart('Learning Rate Schedules',*lines,xlabel='Optimizer step',ylabel='Learning rate',height=470)],{'base_lr':base,'steps':steps},'Значения lr рассчитаны по явным формулам; это учебные scheduler-функции. ReduceOnPlateau требует отдельной последовательности метрик.')

def ranking_lab(c):
    true=np.array([3,0,2,3,1,0,2,1],dtype=float);w=float(c.get('weight',.5));score1=np.array([.8,.2,.7,.9,.4,.1,.3,.5]);score2=np.array([.3,.6,.4,.1,.5,.7,.9,.2]);score=w*score1+(1-w)*score2
    ndcg=float(ndcg_score(true[None,:],score[None,:],k=5));order=np.argsort(-score)
    return result('ranking',[chart('Оценки объектов и релевантность',{'type':'bar','x':order.astype(str).tolist(),'y':true[order].tolist(),'name':'Истинная релевантность'},{'type':'bar','x':order.astype(str).tolist(),'y':score[order].tolist(),'name':'Rank score'},barmode='group',xlabel='Объект (в ранжированном порядке)')],{'NDCG_at_5':round(ndcg,4),'top_item_id':int(order[0])},'Ранжирование определяется score; NDCG нормирует Discounted Cumulative Gain на идеальную сортировку.')

def recommendation_lab(c):
    rng=np.random.default_rng(int(c.get('seed',42)));users=12;items=10;k=int(c.get('rank',2));user_true=rng.normal(size=(users,3));item_true=rng.normal(size=(3,items));R=3+user_true@item_true*.7+rng.normal(0,.2,(users,items))
    U,S,Vt=np.linalg.svd(R-R.mean(),full_matrices=False);recon=R.mean()+(U[:,:k]*S[:k])@Vt[:k,:];err=float(np.sqrt(np.mean((R-recon)**2)))
    return result('recommendations',[chart('Исходные оценки пользователей',heatmap(R,list(range(items)),list(range(users))),xlabel='Item',ylabel='User'),chart('Низкоранговая SVD реконструкция',heatmap(recon,list(range(items)),list(range(users))),xlabel='Item',ylabel='User')],{'rank':k,'RMSE':round(err,4),'users':users,'items':items},'Низкоранговая матричная реконструкция SVD на синтетических оценках. Это не production collaborative filtering с пропусками.')

def graph_lab(c):
    rng=np.random.default_rng(int(c.get('seed',42)));n=9;A=np.zeros((n,n));edges=[(0,1),(0,2),(1,3),(1,4),(2,5),(2,6),(5,7),(6,8),(4,7)];
    for i,j in edges:A[i,j]=A[j,i]=1
    X=rng.normal(size=(n,3));steps=int(c.get('steps',2));H=X.copy();W=np.eye(3)
    for t in range(steps):
        At=A+np.eye(n);D=np.diag(1/np.sqrt(At.sum(axis=1)));H=np.tanh(D@At@D@H@W)
    return result('graph',[chart('Матрица смежности',heatmap(A,list(range(n)),list(range(n))),xlabel='Узел',ylabel='Узел'),chart('Признаки после message passing',heatmap(H,list(range(3)),list(range(n))),xlabel='Feature',ylabel='Node')],{'nodes':n,'edges':len(edges),'layers':steps},'Реальное message passing: Hₜ₊₁=tanh(D⁻¹/²(A+I)D⁻¹/²HₜW), с единичной матрицей W. Это фиксированное преобразование, не обученная GNN.')

def causal_lab(c):
    rng=np.random.default_rng(int(c.get('seed',42)));n=150;strength=float(c.get('confounding',2));group=rng.integers(0,2,n);X=rng.normal(size=n)+strength*group;Y=.7*X-1.8*strength*group+rng.normal(0,.4,n)
    naive=LinearRegression().fit(X[:,None],Y);adjusted=LinearRegression().fit(np.column_stack([X,group]),Y)
    return result('causal',[chart('Смешение (confounding)',scatter(X[group==0],Y[group==0],'Группа 0'),scatter(X[group==1],Y[group==1],'Группа 1',color='#efac7c'),xlabel='X',ylabel='Y')],{'naive_slope':round(float(naive.coef_[0]),4),'adjusted_slope':round(float(adjusted.coef_[0]),4),'true_within_group_slope':.7},'Демонстрация confounding: переменная группы влияет на X и Y. Контроль группы меняет оценённый коэффициент. Нельзя автоматически трактовать регрессионный коэффициент как причинный эффект.')

def fairness_lab(c):
    rng=np.random.default_rng(int(c.get('seed',42)));n=700;group=rng.integers(0,2,n);ability=rng.normal(size=n);truth=(ability+.25*group+rng.normal(0,.65,n)>0).astype(int);bias=float(c.get('bias',.35));score=1/(1+np.exp(-(ability-bias*group)));threshold=float(c.get('threshold',.5));prediction=(score>=threshold).astype(int)
    tab=[]
    for g in (0,1):
        m=group==g;pred=prediction[m];y=truth[m];tn=((pred==0)&(y==0)).sum();fp=((pred==1)&(y==0)).sum();fn=((pred==0)&(y==1)).sum();tp=((pred==1)&(y==1)).sum()
        tab.append({'group':g,'accuracy':round(float(accuracy_score(y,pred)),3),'positive_rate':round(float(pred.mean()),3),'TPR':round(float(tp/max(1,tp+fn)),3),'FPR':round(float(fp/max(1,fp+tn)),3)})
    return result('fairness',[chart('Групповые показатели',{'type':'bar','x':['Group 0','Group 1'],'y':[r['positive_rate'] for r in tab],'name':'Positive rate'},{'type':'bar','x':['Group 0','Group 1'],'y':[r['TPR'] for r in tab],'name':'TPR'},{'type':'bar','x':['Group 0','Group 1'],'y':[r['FPR'] for r in tab],'name':'FPR'},barmode='group')],{'demographic_parity_gap':round(abs(tab[0]['positive_rate']-tab[1]['positive_rate']),4),'equal_opportunity_gap':round(abs(tab[0]['TPR']-tab[1]['TPR']),4)},'Групповые метрики на синтетической симуляции. Несколько критериев справедливости могут конфликтовать, а измерения сами по себе не решают нормативные вопросы.',table=tab)

def interpretability_lab(c):
    n=int(c.get('n',180));rng=np.random.default_rng(int(c.get('seed',42)));X=rng.normal(size=(n,6));y=2*X[:,0]-1.5*X[:,3]+rng.normal(0,.45,n);tr,te=train_test_split(np.arange(n),random_state=11,test_size=.32)
    model=RandomForestRegressor(n_estimators=45,random_state=10).fit(X[tr],y[tr]);perm=permutation_importance(model,X[te],y[te],n_repeats=6,random_state=2)
    return result('interpretability',[chart('Feature importance по permutation',{'type':'bar','x':['x'+str(i) for i in range(6)],'y':perm.importances_mean.tolist(),'marker':{'color':'#79cde8'}},xlabel='Признак',ylabel='Decrease in R²')],{'test_R2':round(float(model.score(X[te],y[te])),4),'top_feature':int(np.argmax(perm.importances_mean))},'Permutation importance рассчитана на отложенной части данных: случайная перестановка признака измеряет падение R². Коррелированные признаки усложняют интерпретацию.')

def diffusion_lab(c):
    rng=np.random.default_rng(int(c.get('seed',42)));n=220;ang=rng.uniform(0,2*np.pi,n);X=np.column_stack([np.cos(ang),np.sin(ang)])+rng.normal(0,.12,(n,2));t=float(c.get('t',.5));alpha=(1-t)**2;noise=rng.normal(size=X.shape);noisy=np.sqrt(alpha)*X+np.sqrt(1-alpha)*noise
    return result('diffusion',[chart('Начальное распределение X₀',scatter(X[:,0],X[:,1],size=6),xlabel='x',ylabel='y'),chart('Forward diffusion Xₜ',scatter(noisy[:,0],noisy[:,1],color='#bd9fff',size=6),xlabel='x',ylabel='y')],{'alpha_bar':round(alpha,5),'noise_std':round(math.sqrt(1-alpha),5)},'Фактическая прямая диффузия xₜ=√ᾱₜ·x₀+√(1−ᾱₜ)·ε. Обратная генерация не моделируется: для неё нужен обученный denoiser.')

EXTRA_LABS={
 'algebra':algebra_lab,'norms':norm_lab,'statistics':stats_lab,'information':information_lab,
 'validation':validation_lab,'scaling':scaling_lab,'schedulers':schedulers_lab,
 'ranking':ranking_lab,'recommendations':recommendation_lab,'graph':graph_lab,'causal':causal_lab,'fairness':fairness_lab,
 'interpretability':interpretability_lab,'diffusion':diffusion_lab}
