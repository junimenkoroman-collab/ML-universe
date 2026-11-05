"""Focused, reproducible teaching labs for the ML -> DL -> NLP curriculum.

Every graph is generated from a numerical computation. Demos that do not train
models say so explicitly. Keep this file independent of GUI and network access.
"""
from __future__ import annotations
import re
import numpy as np
from scipy.special import softmax
from sklearn.linear_model import Ridge, Lasso, ElasticNet
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.decomposition import TruncatedSVD
from sklearn.metrics.pairwise import cosine_similarity
from .maths import loss_and_grad, activation, activation_prime
from .regression import RegressionExperiment
from .labs import result, chart, scatter, heatmap


def loss_lab(c):
    """Per-sample losses vs residual with independently evaluated gradients."""
    delta=max(.05,float(c.get('delta',1.)))
    q=float(np.clip(float(c.get('quantile',.7)),.01,.99))
    r=np.linspace(-3,3,251)
    kinds=['mse','sse','rmse','mae','huber','smooth_l1','logcosh','quantile','weighted_mse']
    names={'mse':'MSE','sse':'SSE','rmse':'RMSE','mae':'MAE','huber':'Huber','smooth_l1':'Smooth L1','logcosh':'Log-Cosh','quantile':'Quantile','weighted_mse':'Weighted MSE'}
    curves=[];derivatives=[];rows=[]
    for kind in kinds:
        vals=[];grads=[]
        for v in r:
            # One-point datasets make MSE/MAE/Huber comparable pointwise.
            loss,gradient=loss_and_grad(np.array([0.]),np.array([v]),kind,delta,q,np.array([2.]))
            vals.append(loss);grads.append(float(gradient[0]))
        curves.append(scatter(r,vals,names[kind],mode='lines'))
        derivatives.append(scatter(r,grads,names[kind],mode='lines'))
        point=float(c.get('residual',1.4));value,g=loss_and_grad(np.array([0.]),np.array([point]),kind,delta,q,np.array([2.]))
        rows.append({'loss':names[kind],'value':round(value,5),'d_loss/d_prediction':round(float(g[0]),5)})
    return result('losses',[chart('Штраф за ошибку предсказания',*curves,xlabel='Residual: prediction − target',ylabel='Loss'),chart('Производные по предсказанию',*derivatives,xlabel='Residual',ylabel='Gradient')],{'residual':float(c.get('residual',1.4)),'delta':delta,'quantile':q},'Одна точка, target = 0, prediction = residual. Для одной точки SSE=MSE=Weighted MSE, а RMSE=MAE. Smooth L1 и Huber совпадают при δ=1; при других δ отличаются масштабом. В точках излома показан выбранный субградиент.',table=rows)


def regularization_path_lab(c):
    rng=np.random.default_rng(int(c.get('seed',42)));n=150
    x=rng.normal(size=(n,4));x[:,1]=.85*x[:,0]+.35*x[:,1]
    y=3*x[:,0]-1.5*x[:,2]+.35*rng.normal(size=n)
    # Scale of alpha follows sklearn's documented objective, not the raw λ*||w||².
    alphas=np.geomspace(.002,4,34);model_type=c.get('kind','ridge')
    cls={'ridge':Ridge,'lasso':Lasso,'elastic':ElasticNet}
    if model_type not in cls:raise ValueError('Неизвестный вид пути')
    lines=[];coef=[]
    for alpha in alphas:
        kwargs={'alpha':float(alpha)}
        if model_type!='ridge':kwargs.update(max_iter=12000,tol=1e-7,random_state=42)
        if model_type=='elastic':kwargs['l1_ratio']=float(c.get('ratio',.5))
        model=cls[model_type](**kwargs).fit(x,y);coef.append(model.coef_.tolist())
    coef=np.asarray(coef)
    for j in range(4):lines.append(scatter(alphas,coef[:,j],f'w{j+1}',mode='lines+markers'))
    return result('regularization_path',[chart('Коэффициенты при росте регуляризации',*lines,xlabel='Alpha (log scale)',ylabel='Weight',height=400),chart('Число ненулевых коэффициентов',scatter(alphas,np.sum(abs(coef)>1e-5,axis=1),'Non-zero',mode='lines+markers'),xlabel='Alpha',ylabel='Количество коэффициентов')],{'algorithm':model_type,'alpha_min':float(alphas[0]),'alpha_max':float(alphas[-1]),'features':4},'Путь Ridge / Lasso / ElasticNet вычислен повторным обучением на одинаковых признаках. Alpha соответствует определениям scikit-learn; bias не штрафуется. В признаках x₁ и x₂ есть корреляция.',details={'alpha':np.round(alphas,5).tolist(),'coefficients':np.round(coef,5).tolist()})


def sweep_lab(c):
    optimizer=c.get('optimizer','sgd');steps=int(np.clip(c.get('steps',60),10,150))
    learning_rates=[.003,.01,.03,.07,.14];penalties=[0.,.001,.01,.1,.5]
    base={'n':75,'true_w':2.4,'true_b':.5,'noise':.45,'seed':int(c.get('seed',42)),'optimizer':optimizer,'sampling':'full','regularizer':'l2','w':-2.5,'b':-1.5}
    values=[];rows=[]
    for lam in penalties:
        line=[]
        for lr in learning_rates:
            experiment=RegressionExperiment({**base,'lr':lr,'lam':lam})
            try:experiment.run(steps);val=experiment.history[-1]['loss']
            except (FloatingPointError,ValueError,OverflowError):val=float('nan')
            line.append(float(val) if np.isfinite(val) else None)
            rows.append({'lr':lr,'lambda':lam,'objective':round(float(val),6) if np.isfinite(val) else 'Diverged'})
        values.append(line)
    finite=[row for row in rows if isinstance(row['objective'],float)]
    best=min(finite,key=lambda r:r['objective']) if finite else {}
    return result('sweep',[chart('Grid search: objective после одинакового числа шагов',heatmap(values,learning_rates,penalties),xlabel='Learning rate',ylabel='L2 lambda')],{'optimizer':optimizer,'steps':steps,'best_lr':best.get('lr','—'),'best_lambda':best.get('lambda','—')},'25 независимых запусков одного датасета и фиксированного старта. Цвет — итоговый training objective, а не validation score. Разные λ означают разные objective, поэтому минимум здесь не доказывает лучшую обобщающую способность.',table=rows)


def activation_lab(c):
    functions=['linear','sigmoid','tanh','relu','leaky_relu','elu','gelu','softplus','swish']
    x=np.linspace(-5,5,241);select=c.get('activation','relu');at=float(c.get('at',1.))
    names={'linear':'Linear','sigmoid':'Sigmoid','tanh':'Tanh','relu':'ReLU','leaky_relu':'Leaky ReLU','elu':'ELU','gelu':'GELU','softplus':'Softplus','swish':'SiLU / Swish'}
    vals=[scatter(x,activation(x,f),names[f],mode='lines',line={'width':3 if f==select else 1.2}) for f in functions]
    der=[scatter(x,activation_prime(x,f),names[f],mode='lines',line={'width':3 if f==select else 1.2}) for f in functions]
    return result('activation',[chart('Активационные функции',*vals,xlabel='z',ylabel='f(z)'),chart('Производные активаций',*der,xlabel='z',ylabel="f'(z)")],{'selected':names.get(select,select),'f(at)':round(float(activation(at,select)),5),"f'(at)":round(float(activation_prime(np.array([at]),select)[0]),5)},'Влияние нелинейностей на forward и локальную производную. В точке излома ReLU принят градиент 0; отображаемые производные GELU вычисляются численно.')


def neural_dynamics_lab(c):
    rng=np.random.default_rng(int(c.get('seed',42)));layers=int(np.clip(c.get('layers',6),2,14));width=int(np.clip(c.get('width',16),4,64));method=c.get('init','xavier');keep=float(np.clip(c.get('keep',.8),.1,1));
    methods={'zeros':0.,'small':.01,'xavier':np.sqrt(1/width),'he':np.sqrt(2/width),'large':2.0}
    if method not in methods:raise ValueError('Неизвестная инициализация')
    weights=[rng.normal(0,methods[method],(width,width)) for _ in range(layers)]
    a=rng.normal(size=(80,width));values=[float(np.std(a))];preacts=[]
    for W in weights:
        z=a@W;preacts.append(z);a=np.maximum(z,0);values.append(float(np.std(a)))
    # Derivative of sum of outputs, through the actual ReLU masks and matrices.
    grad=np.ones_like(a)/a.size;grad_norm=[]
    for z,W in zip(reversed(preacts),reversed(weights)):
        grad=(grad*(z>0))@W.T;grad_norm.insert(0,float(np.linalg.norm(grad)))
    mask=(rng.random(a.shape)<keep).astype(float);train_output=a*mask/keep
    return result('neural_dynamics',[chart('Стандартное отклонение активаций по слоям',scatter(range(layers+1),values,'Activation std',mode='lines+markers'),xlabel='Layer',ylabel='Std'),chart('Норма обратного градиента',scatter(range(1,layers+1),grad_norm,'Backprop norm',mode='lines+markers'),xlabel='Layer (input → output)',ylabel='Gradient norm'),chart('Dropout: train vs eval',{'type':'histogram','x':train_output.flatten().tolist(),'name':'Train (inverted dropout)'},{'type':'histogram','x':a.flatten().tolist(),'name':'Inference (dropout off)'},barmode='overlay')],{'init':method,'layers':layers,'dropout_rate':round(1-keep,3),'final_activation_std':round(values[-1],7)},'Нефиттированная глубокая ReLU-сеть. Весовые матрицы и маски действительно создаются; backprop проводится через ReLU. Dropout с inverted scaling используется только в режиме train. Графики не являются результатом обучения модели.')


def rnn_lab(c):
    words=str(c.get('text','машина учится на тексте')).split()[:20]
    if not words:raise ValueError('Введите последовательность токенов')
    d=int(np.clip(c.get('hidden',6),2,24));rng=np.random.default_rng(int(c.get('seed',42)))
    Wx=rng.normal(size=(d,d))*.35;Wh=rng.normal(size=(d,d))*float(c.get('recurrent_scale',.7))/np.sqrt(d);h=np.zeros(d);states=[]
    for word in words:
        # Stable per-token embedding for repeated tokens inside this experiment.
        code=sum((i+1)*ord(ch) for i,ch in enumerate(word));r=np.random.default_rng(code);x=r.normal(0,.5,d)
        h=np.tanh(x@Wx+h@Wh);states.append(h.copy())
    H=np.asarray(states)
    return result('rnn',[chart('Hidden state hₜ',heatmap(H,list(range(d)),words),xlabel='Dimension',ylabel='Token'),chart('Норма скрытого состояния',scatter(range(1,len(words)+1),np.linalg.norm(H,axis=1),'||h||',mode='lines+markers'),xlabel='Time step',ylabel='L2 norm')],{'tokens':len(words),'hidden_size':d,'final_state_norm':round(float(np.linalg.norm(h)),5)},'Учебная Elman RNN: hₜ=tanh(xₜWx+hₜ₋₁Wh). Показаны реальные состояния фиксированной случайной сети без обучения. При повторении токена его embedding повторяется.',details={'hidden_states':np.round(H,4).tolist()})


def embeddings_lab(c):
    corpus=str(c.get('text','кот ест рыбу. кот любит еду. собака ест мясо. собака любит прогулки. рыба живет в воде. мясо и рыба это еда.'))
    tokens=re.findall(r'[^\W_]+',corpus.lower(),re.UNICODE)[:700];vocab=sorted(set(tokens));m=len(vocab)
    if m<3:raise ValueError('Нужно хотя бы три различных слова')
    idx={word:i for i,word in enumerate(vocab)};counts=np.zeros((m,m));window=int(np.clip(c.get('window',2),1,5))
    for i,word in enumerate(tokens):
        for j in range(max(0,i-window),min(len(tokens),i+window+1)):
            if i!=j:counts[idx[word],idx[tokens[j]]]+=1
    total=counts.sum();pij=counts/max(total,1);pi=counts.sum(axis=1)/max(total,1);pj=counts.sum(axis=0)/max(total,1)
    with np.errstate(divide='ignore',invalid='ignore'):
        ppmi=np.maximum(0,np.log(np.where(counts>0,pij/(pi[:,None]*pj[None,:]+1e-12),1.)))
    if np.max(ppmi)==0:ppmi=counts
    # SVD produces deterministic distributional embeddings (up to axis sign).
    u,s,_=np.linalg.svd(ppmi,full_matrices=False);coords=u[:,:min(2,m)]*s[:min(2,m)]
    cosine=cosine_similarity(ppmi);np.fill_diagonal(cosine,-1)
    word=str(c.get('word',vocab[0])).lower();i=idx.get(word,0)
    nearest=np.argsort(-cosine[i])[:5]
    return result('embeddings',[chart('PPMI: контекстные связи',heatmap(ppmi,vocab,vocab),xlabel='Слово-контекст',ylabel='Слово'),chart('Проекция распределительных векторов SVD',scatter(coords[:,0],coords[:,1],color='#0d9488',mode='markers+text',text=vocab,textposition='top center',size=10),xlabel='SVD1',ylabel='SVD2')],{'vocabulary':m,'context_window':window,'query_word':vocab[i]},'Контекстная матрица co-occurrence → PPMI → SVD. Сходство вычислено по PPMI-строкам; это учебные distributional embeddings, не pretrained Word2Vec. Маленький корпус даёт шумное семантическое пространство.',table=[{'word':vocab[j],'cosine_similarity':round(float(cosine[i,j]),4)} for j in nearest])


_TRAIN_DOCS=[
 ('спорт','Команда выиграла матч и забила гол'),('спорт','Тренер готовит футболистов к матчу'),('спорт','Игрок проводит тренировку на поле'),('спорт','Победа в спортивном соревновании'),
 ('технологии','Алгоритм обрабатывает данные на сервере'),('технологии','Программист пишет код на Python'),('технологии','Нейросеть обучается на текстах'),('технологии','Компьютер выполняет модель машинного обучения'),
 ('кулинария','Повар готовит вкусный суп на кухне'),('кулинария','Рецепт блюда включает свежие овощи'),('кулинария','Запекаем хлеб и готовим обед'),('кулинария','Вкусный ужин из рыбы и риса')]

def text_classification_lab(c):
    docs=[a[1] for a in _TRAIN_DOCS]; labels=[a[0] for a in _TRAIN_DOCS];query=str(c.get('text','нейросеть изучает данные'))
    vec=CountVectorizer(token_pattern=r'(?u)\b\w+\b');X=vec.fit_transform(docs)
    model=MultinomialNB(alpha=max(.01,float(c.get('alpha',1.)))).fit(X,labels)
    counts=vec.transform([query]);prob=model.predict_proba(counts)[0]
    return result('text_classification',[chart('Вероятности классов',{'type':'bar','x':model.classes_.tolist(),'y':prob.tolist(),'marker':{'color':'#0d9488'}},ylabel='P(class | text)'),chart('Bag of Words: обучающий корпус',heatmap(X.toarray(),vec.get_feature_names_out(),list(range(len(docs)))),xlabel='Термин',ylabel='Документ')],{'prediction':str(model.classes_[np.argmax(prob)]),'training_examples':len(docs),'vocabulary':len(vec.vocabulary_)},'Multinomial Naive Bayes обучен на 12 встроенных предложениях. Вероятности аппроксимируют P(class | document), не являются хорошо откалиброванными. Новых моделей/LLM не загружаем.',details={'tokens_in_vocabulary':{w:int(v) for w,v in zip(vec.get_feature_names_out(),counts.toarray()[0]) if v}})


def multihead_lab(c):
    tokens=str(c.get('text','кот видит свет')).split()[:10]
    if not tokens:raise ValueError('Введите токены')
    heads=int(np.clip(c.get('heads',3),1,6));d=int(np.clip(c.get('d',4),2,12));n=len(tokens)
    rng=np.random.default_rng(int(c.get('seed',42)));X=rng.normal(size=(n,heads*d))*.4
    matrices=[];outputs=[];plots=[]
    for i in range(heads):
        Wq=rng.normal(size=(heads*d,d))/np.sqrt(heads*d);Wk=rng.normal(size=(heads*d,d))/np.sqrt(heads*d);Wv=rng.normal(size=(heads*d,d))/np.sqrt(heads*d)
        Q=X@Wq;K=X@Wk;V=X@Wv;score=Q@K.T/np.sqrt(d)
        if c.get('causal',False):score=np.where(np.triu(np.ones((n,n)),1)>0,-1e9,score)
        A=softmax(score,axis=1);matrices.append(A);outputs.append(A@V)
        plots.append(chart(f'Head {i+1}: attention weights',heatmap(A,tokens,tokens),xlabel='Key',ylabel='Query'))
    cat=np.concatenate(outputs,axis=1);Wo=rng.normal(size=(heads*d,heads*d))/np.sqrt(heads*d);final=cat@Wo
    plots.append(chart('Concat(heads) · Wₒ',heatmap(final,list(range(heads*d)),tokens),xlabel='Dimension',ylabel='Token'))
    return result('multihead',plots,{'heads':heads,'head_dim':d,'model_dim':heads*d,'max_row_sum_error':round(float(max(np.max(abs(a.sum(axis=1)-1)) for a in matrices)),12)},'Multi-head Attention: каждая голова имеет собственные Q/K/V-проекции, затем concat и выходная линейная проекция. Параметры случайные, это математическая демонстрация, не обученный Transformer.',details={'attention_matrices':[np.round(m,4).tolist() for m in matrices]})


def rag_lab(c):
    docs=[item.strip() for item in str(c.get('documents','Градиентный спуск минимизирует функцию потерь.|Adam использует экспоненциальные оценки первого и второго моментов градиента.|TF-IDF представляет текст через взвешенные частоты слов.|Attention вычисляет веса между query и key.|Регуляризация L2 штрафует большие коэффициенты модели.')).split('|') if item.strip()][:20]
    query=str(c.get('query','Как работает Adam?')).strip();top=int(np.clip(c.get('top_k',2),1,5))
    if len(docs)<2 or not query:raise ValueError('Введите запрос и минимум два документа')
    tf=TfidfVectorizer(token_pattern=r'(?u)\b\w+\b',ngram_range=(1,2));M=tf.fit_transform(docs+[query]);scores=cosine_similarity(M[-1],M[:-1])[0];order=np.argsort(-scores)[:top]
    rows=[{'rank':i+1,'document':int(j+1),'score':round(float(scores[j]),4),'text':docs[j]} for i,j in enumerate(order)]
    return result('rag',[chart('Retrieval: cosine similarity с запросом',{'type':'bar','x':[f'Doc {i+1}' for i in range(len(docs))],'y':scores.tolist(),'marker':{'color':'#0d9488'}},xlabel='Документ',ylabel='Cosine similarity')],{'documents':len(docs),'top_k':top,'top_score':round(float(scores[order[0]]),4)},'Учебный retrieval-этап RAG: TF-IDF → cosine similarity → top-k. Найденные фрагменты показаны с индексами. Генерация ответа LLM намеренно не имитируется и не включена в офлайн-демо.',table=rows,details={'retrieved_context':[docs[j] for j in order]})


def bandits_lab(c):
    rng=np.random.default_rng(int(c.get('seed',42)));k=int(np.clip(c.get('arms',5),2,10));steps=int(np.clip(c.get('steps',300),10,3000));eps=float(np.clip(c.get('epsilon',.15),0,1))
    probabilities=rng.uniform(.12,.88,size=k);est=np.zeros(k);counts=np.zeros(k,dtype=int);actions=[];reward_history=[];regrets=[];r=0;regret=0.
    for t in range(steps):
        if rng.random()<eps:arm=int(rng.integers(k))
        else:arm=int(np.argmax(est))
        reward=float(rng.random()<probabilities[arm]);counts[arm]+=1;est[arm]+=(reward-est[arm])/counts[arm]
        r+=reward;regret+=float(np.max(probabilities)-probabilities[arm]);actions.append(arm);reward_history.append(r/(t+1));regrets.append(regret)
    return result('bandits',[chart('Истинные p успеха и их оценки',{'type':'bar','x':[str(i+1) for i in range(k)],'y':probabilities.tolist(),'name':'True probability'},{'type':'bar','x':[str(i+1) for i in range(k)],'y':est.tolist(),'name':'Estimated reward'},barmode='group',xlabel='Arm',ylabel='P(reward=1)'),chart('Накопленный pseudo-regret',scatter(range(1,steps+1),regrets,'Expected regret',mode='lines'),xlabel='Step',ylabel='Expected regret'),chart('Средняя фактическая награда',scatter(range(1,steps+1),reward_history,'Mean reward',mode='lines'),xlabel='Step',ylabel='Reward')],{'epsilon':eps,'steps':steps,'best_arm':int(np.argmax(probabilities))+1,'total_reward':int(r),'pseudo_regret':round(regret,3)},'Bernoulli Multi-Armed Bandit. Epsilon-greedy выбирает случайную ручку с вероятностью ε, иначе лучшую по среднему наград. Истинные вероятности фиксированы seed; pseudo-regret считается относительно лучшей ручки.',table=[{'arm':i+1,'true_probability':round(float(probabilities[i]),3),'estimate':round(float(est[i]),3),'pulls':int(counts[i])} for i in range(k)])

CURRICULUM_LABS={
 'losses':loss_lab,'regularization_path':regularization_path_lab,'sweep':sweep_lab,
 'activation':activation_lab,'neural_dynamics':neural_dynamics_lab,'rnn':rnn_lab,
 'embeddings':embeddings_lab,'text_classification':text_classification_lab,
 'multihead':multihead_lab,'rag':rag_lab,'bandits':bandits_lab
}
