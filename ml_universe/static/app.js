/* ML Universe front-end: all plots use data from actual local scientific computations. */
'use strict';
const $=s=>document.querySelector(s), $$=s=>[...document.querySelectorAll(s)];
const NAV=[
 ['ОСНОВЫ И МАТЕМАТИКА',[
  ['regression','⌁','Линейная регрессия','Линейная регрессия в действии.','Параметры модели, регуляризация, GD/SGD/Adam, поверхность ошибки'],
  ['math','∿','Функции и производные','Математика под контролем.','Функции, численные производные, 2D/3D-поверхности'],
  ['optimizer_gallery','↗','Арена оптимизаторов','Оптимизаторы на одной карте.','Сравнивайте траектории и устойчивость алгоритмов'],
  ['pca','◇','PCA и проекции','Геометрия размерности.','Оси, собственные значения, реконструкция'],
  ['algebra','▤','Линейная алгебра','Матрицы меняют пространство.','Преобразования координатной сетки и SVD'],
  ['norms','◇','Нормы векторов','Геометрия регуляризации.','L0, L1, L2, L∞ и поверхности ограничений'],
  ['statistics','∑','Статистика и CLT','Случайность в формулах.','Распределения и центральная предельная теорема'],
  ['information','ℍ','Информация и KL','Сколько стоит неопределённость.','Энтропия, кросс-энтропия и KL-дивергенция'],
  ['schedulers','↝','Learning Rate Scheduler','Скорость обучения во времени.','Сравнение восьми расписаний LR']]],
 ['SUPERVISED LEARNING',[
  ['classification','◎','Классификация','Разделяйте пространство.','Вероятности, пороги и реальные границы решений'],
  ['trees','♧','Деревья решений','Как растут деревья.','Настройка разбиений и исследование структуры'],
  ['ensembles','♢','Леса и ансамбли','Сила многих моделей.','Random Forest, Extra Trees и градиентный бустинг'],
  ['validation','⌑','Bias–Variance','Почему модели переобучаются.','Полиномиальная регрессия, train и validation curves'],
  ['scaling','⌗','Масштабирование','Измеряйте признаки правильно.','Стандартизация, MinMax и геометрия данных'],
  ['interpretability','♧','Интерпретируемость','Какие признаки важны.','Настоящая permutation importance'],
  ['fairness','⚖','Групповые метрики','Справедливость модели.','Положительные решения, TPR, FPR и групповые разрывы'],
  ['ranking','↕','Learning to Rank','Порядок имеет значение.','Оценка ранжирования и NDCG']]],
 ['UNSUPERVISED LEARNING',[
  ['clustering','◈','Кластеризация','Скрытая структура данных.','K-Means, DBSCAN, GMM и иерархические методы'],
  ['anomaly','◇','Аномалии','Найдите необычное.','Isolation Forest и оценка нормальности']]],
 ['DEEP LEARNING',[
  ['neuron','◉','Один нейрон','Всё начинается с суммы.','Веса, смещение, нелинейности и аналитические производные'],
  ['neural','⬡','Нейронные сети','Backpropagation своими глазами.','NumPy MLP, реальные градиенты, XOR и loss'],
  ['cnn','▦','Свёрточные сети','Фильтры превращаются в признаки.','Свертка матриц и feature maps']]],
 ['NATURAL LANGUAGE PROCESSING',[
  ['nlp','≡','Текст и TF-IDF','Слова превращаются в числа.','Токены, частоты, матрицы и похожесть документов'],
  ['bpe','↔','BPE-токенизатор','Разберите слова на токены.','Обучающие слияния пар и словарь'],
  ['attention','⊞','Self-Attention','Посмотрите внутрь внимания.','Q, K, V, Softmax и матрицы внимания'],
  ['decoding','⌘','Генерация токенов','Случайность под контролем.','Temperature, Top-k и nucleus sampling']]],
 ['ПРОДВИНУТЫЕ ЛАБОРАТОРИИ',[
  ['rl','⚑','Reinforcement Learning','Агент учится действовать.','Настоящие обновления Q-table в Gridworld'],
  ['probability','◍','Байесовский вывод','Обновляйте убеждения.','Beta-Bernoulli prior → posterior'],
  ['timeseries','⌁','Временные ряды','Прогнозы из прошлого.','AR(1), оценка параметров и честный прогноз'],
  ['leakage','⚠','Утечка данных','Хорошая метрика может обманывать.','Покажите неправильную и правильную кросс-валидацию'],
  ['recommendations','★','Рекомендации','Что предложить пользователю.','Матричная SVD-реконструкция пользовательских оценок'],
  ['graph','⬢','Graph ML','Информация проходит по графу.','Смежность и настоящая агрегация сообщений'],
  ['causal','⋈','Причинность','Корреляция не равна причине.','Confounding и регрессия с контролем группы'],
  ['diffusion','◌','Диффузионные модели','От сигнала к шуму.','Forward diffusion и шаги зашумления']]]
];
const allNav=NAV.flatMap(x=>x[1]);
const CHOICES={
 optimizer:[['sgd','SGD'],['momentum','Momentum'],['nesterov','Nesterov'],['adagrad','AdaGrad'],['rmsprop','RMSProp'],['adam','Adam'],['adamw','AdamW'],['amsgrad','AMSGrad'],['nadam','NAdam'],['adamax','Adamax'],['adadelta','AdaDelta'],['lion','Lion']],
 loss:[['mse','MSE'],['sse','SSE'],['rmse','RMSE'],['mae','MAE'],['huber','Huber'],['logcosh','Log-Cosh'],['quantile','Quantile']],
 regularizer:[['none','Без штрафа'],['l1','L1'],['l2','L2'],['elastic','Elastic Net']],
 scheduler:[['constant','Постоянная'],['step','Step'],['exponential','Exponential'],['cosine','Cosine'],['warmup_cosine','Warmup + cosine'],['inverse','Inverse time'],['polynomial','Polynomial'],['cyclic','Cyclic']],
 dataset:[['moons','Two Moons'],['circles','Circles'],['blobs','Gaussian Blobs'],['xor','XOR'],['spiral','Spiral']],
 activation:[['sigmoid','Sigmoid'],['tanh','Tanh'],['relu','ReLU'],['leaky_relu','Leaky ReLU'],['softplus','Softplus'],['swish','SiLU/Swish'],['gelu','GELU'],['elu','ELU'],['linear','Linear']],
 classification:[['logistic','Logistic regression'],['tree','Decision tree'],['forest','Random forest'],['extra_trees','Extra Trees'],['boosting','Gradient Boosting'],['adaboost','AdaBoost'],['svm','SVM'],['knn','kNN'],['naive_bayes','Naive Bayes']],
 cluster:[['kmeans','K-Means'],['dbscan','DBSCAN'],['gmm','Gaussian Mixture'],['hierarchical','Agglomerative']],
 kernel:[['rbf','RBF'],['linear','Linear'],['poly','Polynomial'],['sigmoid','Sigmoid kernel']],
 cnnkernel:[['sobel_x','Sobel X'],['sobel_y','Sobel Y'],['blur','Blur'],['sharpen','Sharpen'],['edge','Edge Detection'],['identity','Identity']],
 benchmark:[['sphere','Sphere'],['rosenbrock','Rosenbrock'],['himmelblau','Himmelblau'],['rastrigin','Rastrigin'],['saddle','Saddle'],['anisotropic','Anisotropic'],['custom','Пользовательская']],
 dimension:[['1d','1D: функция и касательная'],['2d','2D: поверхность и уровни']],
 sampling:[['full','Full Batch'],['mini','Mini-batch'],['stochastic','Stochastic (1 sample)']]
};
const r=(key,label,min,max,step,value,group='ОСНОВНЫЕ')=>({key,label,min,max,step,value,group,type:'range'});
const s=(key,label,options,value,group='ОСНОВНЫЕ')=>({key,label,options,value,group,type:'select'});
const t=(key,label,value,group='ОСНОВНЫЕ',rows=2)=>({key,label,value,group,type:'text',rows});
const b=(key,label,value,group='ОСНОВНЫЕ')=>({key,label,value,group,type:'boolean'});
const SCHEMAS={
 regression:[s('optimizer','Оптимизатор',CHOICES.optimizer,'adam','ОПТИМИЗАТОР'),s('sampling','Режим градиента',CHOICES.sampling,'mini','ОПТИМИЗАТОР'),r('lr','Learning rate η',.0001,.5,.0001,.065,'ОПТИМИЗАТОР'),r('batch','Batch size',1,140,1,16,'ОПТИМИЗАТОР'),r('w','Weight w',-9,9,.05,-2.5,'ПАРАМЕТРЫ МОДЕЛИ'),r('b','Bias b',-9,9,.05,-3,'ПАРАМЕТРЫ МОДЕЛИ'),s('loss','Функция ошибки',CHOICES.loss,'mse','LOSS & REGULARIZATION'),s('regularizer','Регуляризация',CHOICES.regularizer,'none','LOSS & REGULARIZATION'),r('lam','Regularization λ',0,2,.005,0,'LOSS & REGULARIZATION'),r('ratio','Elastic Net L1 ratio',0,1,.01,.5,'LOSS & REGULARIZATION'),r('delta','Huber delta',.1,4,.05,1,'LOSS & REGULARIZATION'),r('momentum','Momentum coefficient',0,.999,.001,.9,'ВНУТРЕННЕЕ СОСТОЯНИЕ'),r('beta1','Adam β₁',.01,.999,.001,.9,'ВНУТРЕННЕЕ СОСТОЯНИЕ'),r('beta2','Adam β₂',.5,.9999,.0001,.999,'ВНУТРЕННЕЕ СОСТОЯНИЕ'),r('rho','RMSProp ρ',.01,.999,.001,.9,'ВНУТРЕННЕЕ СОСТОЯНИЕ'),r('weight_decay','Decoupled weight decay',0,.3,.001,.015,'ВНУТРЕННЕЕ СОСТОЯНИЕ'),r('clip','Gradient clip norm (0=off)',0,10,.1,0,'ВНУТРЕННЕЕ СОСТОЯНИЕ'),s('scheduler','LR Scheduler',CHOICES.scheduler,'constant','РАСПИСАНИЕ'),r('n','Количество точек',12,450,1,90,'ДАННЫЕ'),r('true_w','Истинный коэффициент',-5,5,.1,2.7,'ДАННЫЕ'),r('true_b','Истинный bias',-5,5,.1,1.3,'ДАННЫЕ'),r('noise','Уровень шума',0,3,.05,.65,'ДАННЫЕ'),r('outliers','Выбросы',0,35,1,0,'ДАННЫЕ'),r('seed','Random seed',1,999,1,42,'ДАННЫЕ')],
 math:[s('dimension','Размерность',CHOICES.dimension,'1d'),t('expression','Математическое выражение','sin(x)+0.15*x**2'),r('at','Текущий x',-5,5,.05,1),r('xmin','Левая граница',-10,0,.25,-5),r('xmax','Правая граница',0,10,.25,5)],
 optimizer_gallery:[s('function','Целевая функция',CHOICES.benchmark,'himmelblau'),t('expression','Custom f(x,y)','x*x+y*y'),r('lr','Learning rate',.0001,.25,.0001,.015),r('steps','Шагов',10,300,10,75),r('x0','Начальный x',-3,3,.1,-1.5),r('y0','Начальный y',-3,3,.1,2.5)],
 classification:[s('algorithm','Алгоритм',CHOICES.classification,'logistic'),s('dataset','Датасет',CHOICES.dataset,'moons'),r('n','Точки',40,440,10,180),r('noise','Шум',0,.65,.01,.22),r('threshold','Threshold',0,1,.01,.5),r('C','C / inverse regularization',.01,10,.05,1),r('depth','Max depth',1,12,1,4),s('criterion','Split criterion',[['gini','Gini'],['entropy','Entropy']],'gini'),r('min_leaf','Min samples leaf',1,20,1,2),r('trees','Number of trees',5,150,5,35),r('k','Число соседей',1,39,2,7),r('gamma','SVM gamma',.01,5,.05,1),s('kernel','SVM kernel',CHOICES.kernel,'rbf'),r('lr','Boosting learning rate',.01,.5,.01,.1),r('seed','Seed',1,999,1,42)],
 trees:[],ensembles:[],
 clustering:[s('algorithm','Алгоритм',CHOICES.cluster,'kmeans'),s('dataset','Датасет',CHOICES.dataset,'blobs'),r('n','Количество точек',40,460,10,180),r('noise','Шум',.01,.65,.01,.22),r('k','Кластеров / компонент',2,9,1,3),s('init','Инициализация центров',[['k-means++','K-Means++'],['random','Random']],'k-means++'),r('iterations','Max iterations',1,100,1,30),r('eps','DBSCAN ε',.05,1.5,.05,.35),r('min_samples','DBSCAN min_samples',2,20,1,5),r('seed','Random seed',1,999,1,42)],
 pca:[r('angle','Угол проекции (°)',0,180,1,30),r('n','Точки',30,400,10,160),r('seed','Seed',1,999,1,42)],
 neural:[s('dataset','Датасет',CHOICES.dataset,'xor'),s('activation','Скрытая активация',[['tanh','Tanh'],['relu','ReLU'],['sigmoid','Sigmoid'],['swish','SiLU']],'tanh'),r('hidden','Число нейронов',2,30,1,6),r('steps','Шаги обучения',20,1000,10,500),r('lr','Learning rate',.001,1,.001,.1),r('noise','Noise',0,.5,.01,.08),r('n','Samples',40,400,10,180),r('seed','Random seed',1,999,1,42)],
 neuron:[r('x1','Input x₁',-5,5,.1,1),r('x2','Input x₂',-5,5,.1,-1),r('w1','Weight w₁',-5,5,.05,.9),r('w2','Weight w₂',-5,5,.05,-.4),r('bias','Bias',-5,5,.05,.3),s('activation','Активация',CHOICES.activation,'sigmoid')],
 cnn:[s('kernel','Kernel',CHOICES.cnnkernel,'sobel_x'),r('stride','Stride',1,3,1,1),r('padding','Padding',0,2,1,0)],
 nlp:[t('text','Произвольный текст','Машинное обучение учит модели. Машинное обучение работает с данными.','ТЕКСТ',4),t('documents','Документы, разделитель |','Машинное обучение полезно|Обучение моделей на данных|Данные и машинное обучение','КОРПУС',4)],
 bpe:[t('text','Учебный корпус','кот котик коты кот котик собака','КОРПУС',4),r('merges','Операции BPE merge',0,25,1,5)],
 attention:[t('text','Токены через пробел','кот видит свет','ВХОД',3),r('d','Размерность ключа / value',2,12,1,4),r('temperature','Temperature',.1,3,.05,1),b('causal','Causal mask',false),r('seed','Seed',1,999,1,42)],
 decoding:[r('temperature','Температура',.05,3,.05,1),r('top_k','Top-k',1,10,1,10),r('top_p','Top-p',.05,1,.05,1),r('seed','Seed',1,999,1,42)],
 rl:[r('episodes','Эпизодов',10,800,10,150),r('lr','Q-learning α',.01,1,.01,.3),r('gamma','Discount γ',0,.999,.001,.9),r('epsilon','Epsilon-greedy ε',0,1,.01,.2),r('seed','Seed',1,999,1,42)],
 probability:[r('alpha','Prior α',.1,15,.1,2),r('beta','Prior β',.1,15,.1,5),r('heads','Успехи',0,100,1,12),r('tails','Неудачи',0,100,1,8)],
 timeseries:[r('phi','AR coefficient φ',-.95,.95,.05,.8),r('noise','Noise σ',.05,2,.05,.5),r('n','Наблюдений',40,300,10,160),r('seed','Seed',1,999,1,42)],
 anomaly:[r('contamination','Доля аномалий',.01,.35,.01,.1),r('n','Точек',40,400,10,170),r('seed','Seed',1,999,1,42)],
 leakage:[r('n','Наблюдений',50,250,10,120),r('features','Признаков',50,700,50,300),r('seed','Seed',1,999,1,42)],
 algebra:[r('a','Matrix a₁₁',-3,3,.05,1.4),r('b','Matrix a₁₂',-3,3,.05,.4),r('c','Matrix a₂₁',-3,3,.05,-.25),r('d','Matrix a₂₂',-3,3,.05,.8),r('x','Вектор x',-3,3,.1,1),r('y','Вектор y',-3,3,.1,1)],
 norms:[r('w1','Weight w₁',-3,3,.1,1),r('w2','Weight w₂',-3,3,.1,1),r('lam','Lambda λ',0,5,.05,1)],
 statistics:[s('distribution','Распределение',[['normal','Normal'],['uniform','Uniform'],['exponential','Exponential'],['poisson','Poisson']],'exponential'),r('samples','Выборок',100,1000,50,500),r('group','Наблюдений в среднем',1,50,1,8),r('seed','Seed',1,999,1,42)],
 information:[r('p','Вероятность P',.01,.99,.01,.3),r('q','Вероятность Q',.01,.99,.01,.65)],
 validation:[r('degree','Степень полинома',1,15,1,5),r('noise','Noise',0,2,.05,.3),r('n','Выборка',30,200,5,75),r('seed','Seed',1,999,1,42)],
 scaling:[r('scale','Дисбаланс масштабов',1,90,1,25),r('seed','Seed',1,999,1,42)],
 schedulers:[r('lr','Base LR',.001,.5,.001,.1),r('steps','Шагов',20,400,10,200),r('warmup','Warmup',1,90,1,15)],
 ranking:[r('weight','Вес scorer №1',0,1,.01,.5)],
 recommendations:[r('rank','Rank k',1,9,1,2),r('seed','Seed',1,999,1,42)],
 graph:[r('steps','Количество слоёв',1,8,1,2),r('seed','Seed',1,999,1,42)],
 causal:[r('confounding','Сила confounding',0,5,.1,2),r('seed','Seed',1,999,1,42)],
 fairness:[r('bias','Групповой сдвиг',-1.5,1.5,.05,.35),r('threshold','Порог',.05,.95,.05,.5),r('seed','Seed',1,999,1,42)],
 interpretability:[r('n','Точки',80,450,10,180),r('seed','Seed',1,999,1,42)],
 diffusion:[r('t','Уровень шума t',0,1,.02,.5),r('seed','Seed',1,999,1,42)]
};
SCHEMAS.trees=SCHEMAS.classification;SCHEMAS.ensembles=SCHEMAS.classification;
const ROOT=document.documentElement;
let page='regression',mode='explore',cfg={},reg=null,surface=null,labResult=null,playing=false,busy=false,playTimer=null,debounce=null,lastPlotTime=0,currentKey='';
const GENERATORS=new Set(['n','true_w','true_b','noise','outliers','seed']);
const HAS_WEBGL=(()=>{try{const c=document.createElement('canvas');return !!(c.getContext('webgl2')||c.getContext('webgl'));}catch(e){return false}})();
const NUM=x=>typeof x==='number'?(Math.abs(x)>=1e5||Math.abs(x)<1e-4&&x!==0?x.toExponential(3):parseFloat(x.toFixed(5)).toString()):String(x);
const ESC=x=>String(x).replace(/[&<>"']/g,s=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[s]));
const valueLabel=x=>Array.isArray(x)?x.map(NUM).join(', '):NUM(x);
function message(text,error=false){const n=$('#toast');n.textContent=text;n.classList.toggle('error',error);n.classList.add('show');clearTimeout(message._timer);message._timer=setTimeout(()=>n.classList.remove('show'),4000)}
async function api(path,payload={}){const response=await fetch('/api/'+path,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(payload)});const out=await response.json();if(!response.ok)throw Error(out.error||'Ошибка вычислений');return out;}
function heading(info){let label=info[2];$('#breadcrumb').textContent=label;$('#pageTitle').innerHTML=ESC(info[3].replace(/\.$/,''))+'<span class="title-highlight">.</span>';$('#pageDescription').textContent=info[4];$('#sectionLabel').textContent=(page==='regression'?'SUPERVISED LEARNING':page==='attention'?'NLP / TRANSFORMER':'ML UNIVERSE')+' / INTERACTIVE LAB';}
function buildNav(){const nav=$('#navigation');nav.innerHTML='';for(const [group,items] of NAV){const cap=document.createElement('div');cap.className='nav-caption';cap.textContent=group;nav.appendChild(cap);for(const info of items){const item=document.createElement('button');item.className='nav-item';item.dataset.page=info[0];item.innerHTML=`<span class="nav-icon">${info[1]}</span><span>${ESC(info[2])}</span>`;item.addEventListener('click',()=>navigate(info[0]));nav.appendChild(item);}}}
function defaults(key){return Object.fromEntries((SCHEMAS[key]||[]).map(s=>[s.key,s.value]));}
function navigate(next){stopPlay();page=next;cfg=defaults(page);if(page==='trees')cfg.algorithm='tree';if(page==='ensembles')cfg.algorithm='forest';if(page==='regression'&&reg)cfg={...cfg,...reg.config,w:reg.theta[0],b:reg.theta[1]};heading(allNav.find(x=>x[0]===page));$$('.nav-item').forEach(n=>n.classList.toggle('active',n.dataset.page===page));showControls();$('#timelineContainer').style.display=page==='regression'?'':'none';$('#runMainButton').innerHTML=page==='regression'?'▶ &nbsp; Запустить':'⟳ &nbsp; Вычислить';$('#csvButton').style.display=page==='regression'?'':'none';$('#saveButton').style.display=page==='regression'?'':'none';$('#loadButton').style.display=page==='regression'?'':'none';$('#modeLinks').style.display=page==='regression'?'':'none';if(page==='regression'){if(reg)drawRegression();else resetRegression();}else runLab();}
function formatInput(n){if(n.type==='select')return `<select class="field config-field" data-key="${n.key}">${n.options.map(([v,k])=>`<option value="${ESC(v)}" ${String(cfg[n.key])===String(v)?'selected':''}>${ESC(k)}</option>`).join('')}</select>`;
 if(n.type==='text')return `<textarea class="field field-text config-field" data-key="${n.key}" rows="${n.rows||2}">${ESC(cfg[n.key]||'')}</textarea>`;
 if(n.type==='boolean')return `<label><input class="config-field" data-key="${n.key}" type="checkbox" ${cfg[n.key]?'checked':''}> &nbsp; Включено</label>`;
 return `<div class="control-label"><span>${ESC(n.label)}</span><input class="field field-number config-field" data-key="${n.key}" type="number" min="${n.min}" max="${n.max}" step="${n.step}" value="${ESC(cfg[n.key])}"></div><input class="slider" type="range" data-range="${n.key}" min="${n.min}" max="${n.max}" step="${n.step}" value="${ESC(cfg[n.key])}"><div class="control-range"><span>${NUM(n.min)}</span><span>${NUM(n.max)}</span></div>`;}
function showControls(){const box=$('#parameters');box.innerHTML='';let group='';for(const n of SCHEMAS[page]){if(n.group!==group){group=n.group;box.insertAdjacentHTML('beforeend',`<div class="group-title">${ESC(group)}</div>`);}const block=document.createElement('div');block.className='control-group';block.innerHTML=(n.type==='range'?'':`<div class="control-label">${ESC(n.label)}</div>`)+formatInput(n);box.appendChild(block);}
 for(const node of $$('.config-field'))node.addEventListener(node.tagName==='TEXTAREA'||node.tagName==='SELECT'||node.type==='checkbox'?'change':'input',()=>{
    const key=node.dataset.key;let value=node.type==='checkbox'?node.checked:node.type==='number'?Number(node.value):node.value;
    if(node.type==='number'&&!Number.isFinite(value))return;
    cfg[key]=value;const sibling=$(`[data-range="${key}"]`);if(sibling)sibling.value=value;
    if(page==='regression')scheduleRegressionUpdate(key);
 });
 for(const node of $$('[data-range]'))node.addEventListener('input',()=>{const key=node.dataset.range;cfg[key]=Number(node.value);const paired=$(`.config-field[data-key="${key}"]`);if(paired)paired.value=cfg[key];if(page==='regression')scheduleRegressionUpdate(key);});
}
function scheduleRegressionUpdate(key){clearTimeout(debounce);stopPlay();debounce=setTimeout(async()=>{try{if(GENERATORS.has(key)){await resetRegression(true)}else if(key==='w'||key==='b'){reg=await api('set',{w:cfg.w,b:cfg.b});drawRegression();}else{reg=await api('set',{[key]:cfg[key]});if(['loss','regularizer','lam','ratio','delta','quantile'].includes(key))surface=(await api('surface')).surface;drawRegression();}}catch(e){message(e.message,true)}},key==='w'||key==='b'?130:280);}
async function resetRegression(quiet=false){try{stopPlay();setBusy(true);reg=await api('init',cfg);surface=reg.surface;delete reg.surface;cfg={...cfg,...reg.config};drawRegression();if(!quiet)message('Новый эксперимент создан');}catch(e){message(e.message,true)}finally{setBusy(false)}}
function setBusy(v){busy=v;$('#status-text').innerHTML=v?'<span class="online-dot"></span> Вычисление…':'<span class="online-dot"></span> Готово';}
function plotTheme(){const light=ROOT.classList.contains('light');return {paper_bgcolor:'rgba(0,0,0,0)',plot_bgcolor:'rgba(0,0,0,0)',font:{color:light?'#455c77':'#a7bdd7',family:'Segoe UI, Arial',size:10},xaxis:{gridcolor:light?'#e8edf4':'#2b3b54',zerolinecolor:'#3a4a61'},yaxis:{gridcolor:light?'#e8edf4':'#2b3b54',zerolinecolor:'#3a4a61'},legend:{orientation:'h',y:-.22,font:{size:9}},hovermode:'closest'};}
function renderCharts(charts){const host=$('#graphs');if(!charts||!charts.length){host.innerHTML='<div class="empty-panel">Пока нет данных.</div>';return;}const key=page+'_'+charts.length;const recreate=currentKey!==key||$$('.chart-card').length!==charts.length;currentKey=key;if(recreate){host.innerHTML='';charts.forEach((c,i)=>{const card=document.createElement('div');card.className='chart-card'+(c.wide?' wide':'');card.innerHTML=`<div class="chart-head"><strong>${ESC(c.title||'Визуализация')}${!HAS_WEBGL&&c.traces.some(t=>t.type==='surface'||t.type==='scatter3d')?' · 2D fallback':''}</strong><span class="chart-desc">ИНТЕРАКТИВНЫЙ ГРАФИК ${String(i+1).padStart(2,'0')}</span></div><div class="chart-body" id="plot-${i}"></div>`;host.appendChild(card);});}
 const theme=plotTheme();const time=performance.now();charts.forEach((c,i)=>{const original3d=c.traces.some(t=>t.type==='surface'||t.type==='scatter3d');
  let traces=c.traces;
  if(original3d&&!HAS_WEBGL)traces=traces.map(t=>t.type==='surface'?{type:'contour',x:t.x,y:t.y,z:t.z,colorscale:t.colorscale||'Viridis',showscale:false,opacity:t.opacity||1,ncontours:22}:t.type==='scatter3d'?{type:'scatter',x:t.x,y:t.y,mode:t.mode||'lines',name:t.name,line:t.line||{},marker:{...t.marker,size:Math.max(5,t.marker?.size||5)}}:t);
  const target=$(`#plot-${i}`),layout={...theme,...c.layout,margin:{l:48,r:12,t:18,b:48},height:target?.clientHeight||340,autosize:true};if(layout.xaxis)layout.xaxis={...theme.xaxis,...layout.xaxis};if(layout.yaxis)layout.yaxis={...theme.yaxis,...layout.yaxis};if(original3d&&HAS_WEBGL){layout.scene={xaxis:{title:'x'},yaxis:{title:'y'},zaxis:{title:'Objective'},bgcolor:'rgba(0,0,0,0)',...layout.scene};delete layout.xaxis;delete layout.yaxis;layout.margin={l:0,r:0,t:0,b:0};}
   Plotly.react(target,traces,layout,{responsive:true,displaylogo:false,scrollZoom:true,modeBarButtonsToRemove:['sendDataToCloud'],toImageButtonOptions:{format:'png',filename:'ML_Universe_'+page,scale:2}}).catch(e=>message('Ошибка графика: '+e.message,true));});
 $('#renderTime').textContent='ОБНОВЛЕНО ЗА '+(performance.now()-time).toFixed(0)+' МС';}
function setStats(items){let stats=Object.entries(items||{}).filter(([,v])=>typeof v==='number'||typeof v==='string');stats=stats.slice(0,8);if(!stats.length){$('#statsStrip').innerHTML='';return;}$('#statsStrip').innerHTML=stats.slice(0,4).map(([name,value])=>`<div class="stat-card"><div class="stat-label">${ESC(name.replaceAll('_',' ').toUpperCase())}</div><div class="stat-value" title="${ESC(valueLabel(value))}">${ESC(typeof value==='number'?NUM(value):value)}</div><div class="stat-small">Текущее вычисление <span class="stat-indicator">● LIVE</span></div></div>`).join('');}
function kvHtml(items){return Object.entries(items).slice(0,24).map(([k,v])=>`<div class="keyval"><span>${ESC(k.replaceAll('_',' '))}</span><strong>${ESC(valueLabel(v))}</strong></div>`).join('');}
function setExplanation(html){$('#explanation').innerHTML=html;}
function drawRegression(){if(!reg)return;const h=reg.history,last=reg.current,x=reg.x,y=reg.y,p=reg.prediction,w=reg.theta[0],b=reg.theta[1];const coords=h.map(q=>q.w),bias=h.map(q=>q.b),losses=h.map(q=>q.loss);const currentG=last.gradient;
 const segments=[];for(let i=0;i<x.length;i++){segments.push(x[i],x[i],null)}
 const ys=[];for(let i=0;i<x.length;i++)ys.push(y[i],p[i],null);
 const light=ROOT.classList.contains('light');
 const dataChart={title:'Модель и остаточные ошибки',traces:[{type:'scatter',mode:'markers',name:'Датасет',x,y,marker:{color:'#79d5ed',size:7,opacity:.86}}, {type:'scatter',mode:'lines',name:'Residuals',x:segments,y:ys,line:{color:'#ed879c',width:1},opacity:.7,hoverinfo:'skip'}, {type:'scatter',mode:'lines',name:'ŷ = '+NUM(w)+'x + '+NUM(b),x:[Math.min(...x),Math.max(...x)],y:[w*Math.min(...x)+b,w*Math.max(...x)+b],line:{color:'#fac07c',width:3}}],layout:{xaxis:{title:'Признак x'},yaxis:{title:'Целевая переменная y'}}};
 const s=surface;
 const path3={type:'scatter3d',x:coords,y:bias,z:losses,name:'Путь оптимизации',mode:'lines+markers',line:{color:'#ffbb66',width:5},marker:{size:2,color:'#ffc47d'}};
 const point3={type:'scatter3d',x:[w],y:[b],z:[last.loss],name:'Текущие θ',mode:'markers',marker:{size:7,color:'#a591ff'}};
 const surfChart={title:'3D · поверхность функции потерь',traces:s?[{type:'surface',x:s.w,y:s.b,z:s.z,opacity:.80,showscale:false,colorscale:'Viridis',hovertemplate:'w=%{x:.2f}<br>b=%{y:.2f}<br>Loss=%{z:.4f}<extra></extra>'},path3,point3]:[point3],layout:{scene:{xaxis:{title:'Weight w'},yaxis:{title:'Bias b'},zaxis:{title:'Loss'}}}};
 const contourChart={title:'Линии уровня и траектория',traces:s?[{type:'contour',x:s.w,y:s.b,z:s.z,showscale:false,colorscale:'Viridis',ncontours:24,contours:{coloring:'heatmap'},opacity:.89},{type:'scatter',x:coords,y:bias,mode:'lines+markers',name:'Траектория',line:{color:'#ffbc81',width:2.5},marker:{color:'#fff1e0',size:5}},{type:'scatter',x:[w],y:[b],mode:'markers',name:'Текущая точка',marker:{color:'#b9a6ff',size:14,symbol:'circle-open',line:{width:3}}}]:[],layout:{xaxis:{title:'Weight w'},yaxis:{title:'Bias b'}}};
 const lossChart={title:'История обучения · objective',traces:[{type:'scatter',x:h.map(q=>q.step),y:losses,mode:'lines',name:'Total objective',line:{color:'#64d7dc',width:2.5}},{type:'scatter',x:h.map(q=>q.step),y:h.map(q=>q.data_loss),mode:'lines',name:'Data loss',line:{color:'#a58cf4',width:1.5,dash:'dot'}}],layout:{xaxis:{title:'Шаг оптимизации'},yaxis:{title:'Loss'}}};
 renderCharts([dataChart,surfChart,contourChart,lossChart]);setStats({'TOTAL LOSS':last.loss,'WEIGHT w':w,'BIAS b':b,'GRADIENT NORM':Math.hypot(...currentG)});
 const d=reg.detail||{};const rows={'θ (w, b)':reg.theta,'∇L (full data)':currentG,'Data loss':last.data_loss,'Penalty':last.penalty,'RMSE':reg.score.rmse,'R²':reg.score.r2,'Optimizer':reg.config.optimizer,'Шаг':reg.steps};
 let html=kvHtml(rows)+`<div class="formula">θₜ₊₁ = Optimizer(θₜ, ∇L, stateₜ)</div>`;
 if(d.gradient)html+='<div class="group-title">ПОСЛЕДНИЙ ШАГ</div>'+kvHtml({Batch:d.batch_indices?.slice(0,18)||[],Gradient:d.gradient,Update:d.update,Before:d.before,After:d.after,LR:d.learning_rate});
 if(d.m_hat)html+='<div class="group-title">СОСТОЯНИЕ ADAM</div>'+kvHtml({m:d.first_moment,v:d.second_moment,m_hat:d.m_hat,v_hat:d.v_hat});
 if(d.velocity)html+='<div class="group-title">MOMENTUM</div>'+kvHtml({Velocity:d.velocity});
 if(d.second_moment&&!d.m_hat)html+='<div class="group-title">RMSPROP</div>'+kvHtml({EMA_squared:d.second_moment});
 $('#inspector').innerHTML=html;
 setExplanation(mode==='challenge'?`<b>Задание:</b> добейтесь Loss &lt; 0.5, подбирая learning rate и оптимизатор. <div class="formula">Текущий Loss = ${NUM(last.loss)} → ${last.loss<.5?'✓ Цель достигнута':'● Продолжайте эксперимент'}</div>`:mode==='learn'?'<b>Как читать графики?</b> Вверху слева исходные наблюдения, текущая прямая и ошибки. Вверху справа 3D-поверхность функции L(w,b). Внизу — контуры и настоящая история оптимизации. Измените η, алгоритм или регуляризатор.':'<b>Линейная регрессия:</b> ŷ = wx + b. Данные и штраф суммируются в objective. Градиент вычисляется аналитически по каждому batch. Воспроизведение сохраняет состояния и seed. L1 в точке нуля использует субградиент 0; AdamW реализует отдельный decoupled decay.');
 $('#timelineRange').max=h[h.length-1].step;$('#timelineRange').min=h[0].step;$('#timelineRange').value=reg.steps;$('#timelineStep').textContent='Шаг '+reg.steps;$('#timelineLoss').textContent='Loss '+NUM(last.loss);
}
async function stepRegression(){if(busy)return;try{setBusy(true);reg=await api('step');drawRegression()}catch(e){stopPlay();message(e.message,true)}finally{setBusy(false)}}
async function runRegression(n){if(busy)return;try{setBusy(true);reg=await api('run',{steps:n});drawRegression();message('Выполнено '+n+' шагов (или до условия остановки)');}catch(e){message(e.message,true)}finally{setBusy(false)}}
async function seek(step){if(busy)return;try{setBusy(true);reg=await api('seek',{step});drawRegression()}catch(e){message(e.message,true)}finally{setBusy(false)}}
function stopPlay(){playing=false;clearInterval(playTimer);playTimer=null;$('#toPlay').textContent='▶'}
function togglePlay(){if(playing){stopPlay();return}playing=true;$('#toPlay').textContent='Ⅱ';playTimer=setInterval(()=>{if(!busy)stepRegression()},330)}
async function compareRegression(){if(!reg)return;setBusy(true);try{const d=await api('compare',{steps:100,names:['sgd','momentum','rmsprop','adam','adamw','adagrad']});const colors=['#65dce9','#c1a0ff','#ffb677','#66d99a','#ed839e','#98b0ee'];const lines=d.runs.map((q,i)=>({type:'scatter',mode:'lines',name:q.name,x:q.history.map(h=>h.step),y:q.history.map(h=>h.loss),line:{color:colors[i],width:2}}));const tracks=d.runs.map((q,i)=>({type:'scatter',mode:'lines+markers',name:q.name,x:q.history.map(h=>h.w),y:q.history.map(h=>h.b),line:{color:colors[i],width:2},marker:{size:3}}));const contours=surface?[{type:'contour',x:surface.w,y:surface.b,z:surface.z,colorscale:'Viridis',ncontours:25,showscale:false}]:[];const stats=Object.fromEntries(d.runs.slice(0,4).map(q=>[q.name+'_loss',q.final.loss]));setStats(stats);renderCharts([{title:'Optimizer Arena · траектории',traces:[...contours,...tracks],layout:{xaxis:{title:'Weight w'},yaxis:{title:'Bias b'}}},{title:'Функции потерь по шагам',traces:lines,layout:{xaxis:{title:'Шаг'},yaxis:{title:'Total Objective'}}}]);$('#inspector').innerHTML=kvHtml(Object.fromEntries(d.runs.map(q=>[q.name+' · final loss',q.final.loss])))+'<div class="formula">Одна и та же функция, датасет и инициализация; разные правила обновления.</div>';setExplanation('Алгоритмы сравниваются на одинаковых данных и начальных весах. Learning rate общий, поэтому сравнение показывает поведение при этой конкретной настройке, а не универсального победителя. Вернитесь к экспериментам для продолжения основного run.');message('Сравнение шести оптимизаторов готово');}catch(e){message(e.message,true)}finally{setBusy(false)}}
function labName(){return ['trees','ensembles'].includes(page)?'classification':page;}
async function runLab(){if(busy)return;try{setBusy(true);const results=await api('lab',{name:labName(),config:cfg});labResult=results;setStats(results.stats);renderCharts(results.charts);const extra=Object.entries(results.details||{}).slice(0,10).map(([k,v])=>`<details class="detail-fold"><summary>${ESC(k.replaceAll('_',' '))}</summary><pre class="formula">${ESC(JSON.stringify(v,null,2).slice(0,5000))}</pre></details>`).join('');
 $('#inspector').innerHTML=kvHtml(results.stats)+extra+(results.table?.length?`<div class="group-title">ТАБЛИЦА РАСЧЁТОВ</div><div style="overflow:auto;max-height:260px"><table class="data-table"><thead><tr>${Object.keys(results.table[0]).map(k=>`<th>${ESC(k)}</th>`).join('')}</tr></thead><tbody>${results.table.slice(0,28).map(row=>`<tr>${Object.values(row).map(v=>`<td>${ESC(valueLabel(v))}</td>`).join('')}</tr>`).join('')}</tbody></table></div>`:'');setExplanation('<b>Как устроено вычисление:</b> '+ESC(results.explain));}catch(e){message(e.message,true);$('#inspector').textContent='Ошибка: '+e.message}finally{setBusy(false)}}
function saveFile(name,obj){const blob=new Blob([JSON.stringify(obj,null,2)],{type:'application/json'});const a=document.createElement('a');a.href=URL.createObjectURL(blob);a.download=name;a.click();setTimeout(()=>URL.revokeObjectURL(a.href),5000)}
async function saveExperiment(){try{const data=await api('save');saveFile('ML_Universe_Experiment.mluniverse',data);message('Эксперимент сохранён')}catch(e){message(e.message,true)}}
async function loadCsv(file){if(!file)return;try{const raw=await file.text();const delimiter=raw.includes(';')?';':raw.includes('\t')?'\t':',';const lines=raw.trim().split(/\r?\n/).filter(Boolean);const coords=[];for(let i=0;i<Math.min(lines.length,601);i++){const cells=lines[i].split(delimiter);if(cells.length<2)continue;const x=Number(cells[0].trim().replace(',','.')),y=Number(cells[1].trim().replace(',','.'));if(Number.isFinite(x)&&Number.isFinite(y)&&cells[0].trim()!==''&&cells[1].trim()!=='')coords.push([x,y]);}if(coords.length<4||coords.length>600)throw Error('CSV должен содержать 4–600 числовых строк с колонками x и y.');stopPlay();setBusy(true);reg=await api('import_csv',{config:cfg,x:coords.map(v=>v[0]),y:coords.map(v=>v[1])});surface=reg.surface;delete reg.surface;cfg={...cfg,...reg.config};showControls();drawRegression();message('Импортировано '+coords.length+' точек из CSV');}catch(e){message('Ошибка CSV: '+e.message,true)}finally{setBusy(false)}}
async function loadExperiment(file){if(!file)return;try{const text=await file.text();reg=await api('load',JSON.parse(text));surface=reg.surface;delete reg.surface;cfg={...cfg,...reg.config,w:reg.theta[0],b:reg.theta[1]};showControls();drawRegression();message('Эксперимент восстановлен');}catch(e){message('Ошибка импорта: '+e.message,true)}}
function changeMode(next){mode=next;$$('.mode').forEach(v=>v.classList.toggle('active',v.dataset.mode===next));$('#modeHint').textContent={explore:'Изменяйте параметры и наблюдайте',learn:'Объяснение каждого механизма',debug:'Пошаговый отладчик состояния',compare:'Сопоставление алгоритмов',challenge:'Достигните целевого loss'}[next];if(page==='regression'){if(next==='compare')compareRegression();else drawRegression()}}
function wire(){buildNav();$('#applyButton').onclick=()=>page==='regression'?resetRegression():runLab();$('#resetButton').onclick=()=>{cfg=defaults(page);if(page==='trees')cfg.algorithm='tree';if(page==='ensembles')cfg.algorithm='forest';showControls();page==='regression'?resetRegression():runLab()};$('#runMainButton').onclick=()=>page==='regression'?runRegression(50):runLab();$('#toStep').onclick=()=>stepRegression();$('#toBack').onclick=()=>seek(Math.max(0,reg.steps-1));$('#toStart').onclick=()=>seek(0);$('#toPlay').onclick=togglePlay;$('#run25').onclick=()=>runRegression(25);$('#run100').onclick=()=>runRegression(100);$('#timelineRange').addEventListener('change',e=>seek(Number(e.target.value)));$('#csvButton').onclick=()=>$('#csvInput').click();$('#csvInput').onchange=e=>loadCsv(e.target.files[0]);$('#saveButton').onclick=saveExperiment;$('#loadButton').onclick=()=>$('#loadInput').click();$('#loadInput').onchange=e=>loadExperiment(e.target.files[0]);$$('.mode').forEach(v=>v.onclick=()=>changeMode(v.dataset.mode));$('#themeButton').onclick=()=>{ROOT.classList.toggle('light');if(page==='regression')drawRegression();else if(labResult)renderCharts(labResult.charts);};$('#helpButton').onclick=()=>$('#modal').classList.remove('hidden');$('#closeModal').onclick=()=>$('#modal').classList.add('hidden');$('#modal').onclick=e=>{if(e.target===$('#modal'))$('#modal').classList.add('hidden')};window.addEventListener('keydown',e=>{if(e.key==='Escape'){$('#modal').classList.add('hidden');stopPlay()}if(e.key===' '&&!['INPUT','TEXTAREA','SELECT'].includes(document.activeElement.tagName)&&page==='regression'){e.preventDefault();togglePlay()}});window.addEventListener('resize',()=>{$$('.chart-body').forEach(n=>{if(n.data)Plotly.Plots.resize(n)})});navigate('regression');}
wire();
