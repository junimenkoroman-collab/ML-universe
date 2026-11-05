"""Small interactive linear-algebra, norms, information theory and LR schedulers."""
from __future__ import annotations
import numpy as np
from scipy.stats import entropy
from .labs import scatter,heatmap,chart,result
from .maths import regularization
from .optimizers import scheduler_lr

def algebra_lab(c):
    a=float(c.get('a',1.4));b=float(c.get('b',.4));cc=float(c.get('c',-.25));d=float(c.get('d',.8));M=np.array([[a,b],[cc,d]])
    grid=np.linspace(-2,2,8);lines=[];transformed=[]
    for value in grid:
        h=np.c_[grid,np.full(len(grid),value)];v=np.c_[np.full(len(grid),value),grid]
        for z in (h,v):
            lines.append(scatter(z[:,0],z[:,1],mode='lines',color='#818181',size=2))
            zz=z@M.T;transformed.append(scatter(zz[:,0],zz[:,1],mode='lines',color='#0d9488',size=2))
    vec=np.array([float(c.get('x',1.)),float(c.get('y',1.))]);mapped=M@vec
    return result('algebra',[chart('Исходная координатная сетка',*lines,xlabel='x',ylabel='y',height=350),chart('Линейное преобразование A·x',*transformed,scatter([0,mapped[0]],[0,mapped[1]],'A·v',mode='lines+markers',color='#be9764'),xlabel='x',ylabel='y',height=350)],{'det(A)':round(float(np.linalg.det(M)),4),'trace(A)':round(float(np.trace(M)),4),'dot_product':round(float(vec@mapped),4),'A·vector':np.round(mapped,4).tolist()},'Каждая точка сетки умножается на матрицу 2×2. Показан матрично-векторный продукт и скалярное произведение без SVD или спектральной теории.',details={'matrix':M.tolist()})

def norm_lab(c):
    lam=float(c.get('lam',1.));p=float(c.get('p',1.));theta=np.linspace(0,2*np.pi,300);ct=np.cos(theta);st=np.sin(theta)
    # Norm unit ball boundaries.
    l1x=ct/(abs(ct)+abs(st));l1y=st/(abs(ct)+abs(st))
    linfx=ct/np.maximum(abs(ct),abs(st));linfy=st/np.maximum(abs(ct),abs(st))
    w=np.array([float(c.get('w1',1.)),float(c.get('w2',1.))]);g1=regularization(w,'l1',lam);g2=regularization(w,'l2',lam)
    return result('norms',[chart('Геометрия единичных шаров',scatter(l1x,l1y,'L1 = 1',mode='lines',color='#be9764'),scatter(ct,st,'L2 = 1',mode='lines',color='#0d9488'),scatter(linfx,linfy,'L∞ = 1',mode='lines',color='#8987aa'),scatter([w[0]],[w[1]],'w',size=13),xlabel='w₁',ylabel='w₂')],{'L1(w)':round(float(np.sum(abs(w))),4),'L2(w)':round(float(np.linalg.norm(w)),4),'L∞(w)':round(float(np.max(abs(w))),4),'L1 penalty':round(g1[0],4),'L2 squared penalty':round(g2[0],4)},'L0 считается количеством ненулевых компонент (не настоящая норма). L1 — ромб, L2 — круг, L∞ — квадрат.')

def information_lab(c):
    p=float(c.get('p',.3));q=float(c.get('q',.65));p=np.clip(p,1e-5,1-1e-5);q=np.clip(q,1e-5,1-1e-5)
    P=np.array([p,1-p]);Q=np.array([q,1-q]);H=float(entropy(P,base=2));KL=float(entropy(P,Q,base=2));cross=float(-sum(P*np.log2(Q)))
    mixture=.5*(P+Q);js=.5*(entropy(P,mixture,base=2)+entropy(Q,mixture,base=2))
    x=np.linspace(.01,.99,180);curve=-x*np.log2(x)-(1-x)*np.log2(1-x)
    return result('information',[chart('Энтропия Bernoulli',scatter(x,curve,'H(p)',mode='lines'),scatter([p],[H],'Текущее p',size=13,color='#be9764'),xlabel='p',ylabel='Бит'),chart('P против Q',{'type':'bar','x':['событие 1','событие 2'],'y':P.tolist(),'name':'P'},{'type':'bar','x':['событие 1','событие 2'],'y':Q.tolist(),'name':'Q'},barmode='group')],{'Entropy H(P) bits':round(H,5),'Cross entropy H(P,Q) bits':round(cross,5),'KL(P||Q) bits':round(KL,5),'JS(P,Q) bits':round(float(js),5)},'H(P,Q)=H(P)+KL(P||Q). Логарифмы по основанию 2, результаты в битах.')

def schedulers_lab(c):
    steps=int(c.get('steps',200));base=float(c.get('lr',.1));warmup=int(c.get('warmup',15));which=['constant','step','exponential','inverse','polynomial','cosine','warmup_cosine','cyclic'];lines=[]
    for name in which:lines.append(scatter(range(steps+1),[scheduler_lr(k,base,name,steps,warmup) for k in range(steps+1)],name,mode='lines'))
    return result('schedulers',[chart('Learning Rate Schedules',*lines,xlabel='Optimizer step',ylabel='Learning rate',height=470)],{'base_lr':base,'steps':steps},'Значения lr рассчитаны по явным формулам; это учебные scheduler-функции. ReduceOnPlateau требует отдельной последовательности метрик.')
