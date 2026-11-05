/* ML Universe · focused ML → Deep Learning → NLP learning path. */
'use strict';
const $=s=>document.querySelector(s), $$=s=>[...document.querySelectorAll(s)];
const NAV=[
 ['01 · РЕГРЕССИЯ И ОПТИМИЗАЦИЯ',[
  ['regression','∿','Линейная регрессия','Линейная регрессия','Вес, bias, градиент, история шагов и 3D loss surface'],
  ['losses','≋','Функции потерь','Исследователь функций потерь','MSE, MAE, Smooth L1, Huber, Quantile, Log-Cosh и производные'],
  ['regularization_path','⌁','Регуляризация','Пути регуляризации','Ridge, Lasso, Elastic Net, влияние alpha на коэффициенты'],
  ['optimizer_gallery','↗','Арена оптимизаторов','Арена оптимизаторов','GD, SGD, Momentum, Nesterov, RMSProp, Adam, AdamW и Projected GD'],
  ['schedulers','◷','Learning Rate','Расписания learning rate','Warmup, cosine, step, exponential и cyclic'],
  ['sweep','▦','Hyperparameter Sweep','Подбор гиперпараметров','Тепловая карта 25 воспроизводимых обучений']],
 ],
 ['02 · КЛАССИФИКАЦИЯ',[
  ['classification','◎','Классификаторы','Классификация на плоскости','Logistic, Softmax, SVM, kernel SVM, kNN и Naive Bayes'],
  ['trees','♧','Decision Tree','Как строится дерево','Gini, entropy, кандидаты split и границы решений'],
  ['ensembles','⋈','Random Forest / Boosting','Ансамбли моделей','Random Forest и Gradient Boosting, ROC и PR']],
 ],
 ['03 · КЛАСТЕРИЗАЦИЯ',[
  ['clustering','◈','K-Means','K-Means пошагово','Assignment, update, траектории центроидов, inertia']],
 ],
 ['04 · НЕЙРОННЫЕ СЕТИ',[
  ['neuron','◉','Один нейрон','Один нейрон','Линейная комбинация, bias, activation и частные производные'],
  ['activation','∫','Activation Explorer','Функции активации','Sigmoid, Tanh, ReLU, GELU, SiLU и их производные'],
  ['neural','⬡','MLP / XOR','Нейросеть: Forward & Backprop','Полносвязная сеть, XOR, BCE и аналитические градиенты'],
  ['neural_dynamics','≍','Градиенты и Dropout','Как ведёт себя глубокая сеть','Weight initialization, vanishing gradients, dropout'],
  ['cnn','▦','CNN / Receptive Field','Свёртка и receptive field','Ядро 3×3, stride, padding, выходные карты признаков'],
  ['rnn','↻','RNN','Рекуррентная нейронная сеть','Токены → hidden states → рекуррентное преобразование']],
 ],
 ['05 · NLP И TRANSFORMERS',[
  ['nlp','≡','Препроцессинг / TF-IDF','Слова становятся числами','Unicode tokens, Bag of Words, TF-IDF и cosine similarity'],
  ['bpe','↔','Byte Pair Encoding','BPE по шагам','Статистика пар, слияния, новые токены'],
  ['text_classification','◇','Text Classification','Классификация текстов','Multinomial Naive Bayes и Bag of Words'],
  ['embeddings','∙','Word Embeddings','Контекстные embeddings','Co-occurrence, PPMI, SVD, cosine similarity'],
  ['attention','⊞','Q / K / V · Attention','Scaled Dot-Product Attention','Query, Key, Value и матрицы softmax'],
  ['multihead','▤','Multi-Head Attention','Несколько голов внимания','Независимые heads, concat и проекция'],
  ['decoding','⌘','Decoding / Sampling','Выбор следующего токена','Greedy, temperature, Top-K и Top-P'],
  ['rag','⌕','RAG · Retrieval','Поиск контекста для RAG','TF-IDF retrieval и top-k фрагментов без выдуманной генерации']],
 ],
 ['06 · REINFORCEMENT LEARNING',[
  ['bandits','⤴','Multi-Armed Bandit','Epsilon-Greedy Bandit','Выбор ручек, оценка наград и pseudo-regret']],
 ],
 ['07 · МАТЕМАТИЧЕСКАЯ БАЗА',[
  ['math','ƒ','Градиент / Hessian','Функции и производные','Производная, градиент, Hessian, численные поверхности'],
  ['algebra','⊞','Векторы и матрицы','Базовый линал','Dot product, матричные преобразования 2D'],
  ['norms','◇','Нормы','L1 / L2 / L∞','Геометрия единичных шаров и регуляризации'],
  ['information','ℍ','Entropy / KL / JS','Теория информации','Энтропия, cross-entropy, KL и JS divergence']],
 ]
];
const allNav=NAV.flatMap(x=>x[1]);
const CHOICES={
 optimizer:[['sgd','Gradient Descent / SGD'],['momentum','Momentum'],['nesterov','Nesterov'],['adagrad','AdaGrad'],['rmsprop','RMSProp'],['adam','Adam'],['adamw','AdamW']],
 loss:[['mse','MSE'],['sse','SSE'],['rmse','RMSE'],['mae','MAE'],['huber','Huber'],['smooth_l1','Smooth L1'],['logcosh','Log-Cosh'],['quantile','Quantile'],['weighted_mse','Weighted MSE']],
 regularizer:[['none','Без штрафа'],['l1','L1 / Lasso'],['l2','L2 / Ridge'],['elastic','Elastic Net']],
 weight_mode:[['uniform','Все равны'],['edge','Сильнее крайние x'],['center','Сильнее центральные x']],
 scheduler:[['constant','Constant'],['step','Step'],['exponential','Exponential'],['cosine','Cosine'],['warmup_cosine','Warmup + cosine'],['inverse','Inverse time'],['polynomial','Polynomial'],['cyclic','Cyclic']],
 dataset:[['moons','Two Moons'],['circles','Circles'],['blobs','Gaussian Blobs'],['xor','XOR'],['spiral','Spiral']],
 activation:[['sigmoid','Sigmoid'],['tanh','Tanh'],['relu','ReLU'],['leaky_relu','Leaky ReLU'],['softplus','Softplus'],['swish','SiLU / Swish'],['gelu','GELU'],['elu','ELU'],['linear','Linear']],
 classification:[['logistic','Logistic Regression'],['softmax','Softmax Regression · 3 класса'],['svm','Support Vector Machine'],['knn','k-Nearest Neighbors'],['naive_bayes','Naive Bayes'],['tree','Decision Tree'],['forest','Random Forest'],['boosting','Gradient Boosting']],
 kernel:[['rbf','RBF'],['linear','Linear'],['poly','Polynomial'],['sigmoid','Sigmoid kernel']],
 cnnkernel:[['sobel_x','Sobel X'],['sobel_y','Sobel Y'],['blur','Blur'],['sharpen','Sharpen'],['edge','Edge'],['identity','Identity']],
 benchmark:[['sphere','Sphere'],['rosenbrock','Rosenbrock'],['himmelblau','Himmelblau'],['rastrigin','Rastrigin'],['saddle','Saddle'],['anisotropic','Anisotropic'],['custom','Своя функция']],
 dimension:[['1d','1D: функция и касательная'],['2d','2D: поверхность и уровни']],
 sampling:[['full','GD · полный датасет'],['mini','Mini-batch SGD'],['stochastic','SGD · один пример']],
 path_kind:[['ridge','Ridge (L2)'],['lasso','Lasso (L1)'],['elastic','Elastic Net']],
 arena_mode:[['compare','Сравнить оптимизаторы'],['projected','Projected GD vs GD'],['adaptive','Adam / AdaGrad / RMSProp']],
 init:[['xavier','Xavier'],['he','He'],['small','Малые веса'],['zeros','Нулевые веса'],['large','Большие веса']]
};
const r=(key,label,min,max,step,value,group='НАСТРОЙКИ')=>({key,label,min,max,step,value,group,type:'range'});
const s=(key,label,options,value,group='НАСТРОЙКИ')=>({key,label,options,value,group,type:'select'});
const t=(key,label,value,group='НАСТРОЙКИ',rows=2)=>({key,label,value,group,type:'text',rows});
const b=(key,label,value,group='НАСТРОЙКИ')=>({key,label,value,group,type:'boolean'});
const SCHEMAS={
 regression:[
  s('optimizer','Оптимизатор',CHOICES.optimizer,'sgd','Обучение'),s('sampling','Выбор batch',CHOICES.sampling,'full','Обучение'),
  r('lr','Learning rate η',.0001,.5,.0001,.065,'Обучение'),r('batch','Batch size',1,140,1,16,'Обучение'),
  r('w','Weight w',-9,9,.05,-2.5,'Модель'),r('b','Bias b',-9,9,.05,-3,'Модель'),
  s('loss','Loss',CHOICES.loss,'mse','Loss и штраф'),s('weight_mode','Веса Weighted MSE',CHOICES.weight_mode,'uniform','Loss и штраф'),
  s('regularizer','Регуляризация',CHOICES.regularizer,'none','Loss и штраф'),r('lam','Lambda λ',0,2,.005,0,'Loss и штраф'),
  r('ratio','L1 ratio',0,1,.01,.5,'Loss и штраф'),r('delta','Huber / Smooth L1 δ',.1,4,.05,1,'Loss и штраф'),r('quantile','Quantile τ',.01,.99,.01,.5,'Loss и штраф'),
  r('momentum','Momentum',0,.999,.001,.9,'Оптимизатор'),r('beta1','Adam β₁',.01,.999,.001,.9,'Оптимизатор'),
  r('beta2','Adam β₂',.5,.9999,.0001,.999,'Оптимизатор'),r('rho','RMSProp ρ',.01,.999,.001,.9,'Оптимизатор'),
  r('weight_decay','AdamW weight decay',0,.3,.001,.015,'Оптимизатор'),r('clip','Gradient clip (0 = off)',0,10,.1,0,'Оптимизатор'),
  s('scheduler','LR Scheduler',CHOICES.scheduler,'constant','Расписание'),
  r('n','Количество точек',12,450,1,90,'Датасет'),r('true_w','Истинный w',-5,5,.1,2.7,'Датасет'),
  r('true_b','Истинный bias',-5,5,.1,1.3,'Датасет'),r('noise','Шум',0,3,.05,.65,'Датасет'),
  r('outliers','Выбросы',0,35,1,0,'Датасет'),r('seed','Random seed',1,999,1,42,'Датасет')],
 losses:[r('residual','Residual',-3,3,.05,1.4),r('delta','Huber / Smooth L1 δ',.1,3,.1,1),r('quantile','Quantile τ',.05,.95,.05,.7)],
 regularization_path:[s('kind','Метод',CHOICES.path_kind,'ridge'),r('ratio','Elastic Net L1 ratio',.05,.95,.05,.5),r('seed','Seed',1,999,1,42)],
 optimizer_gallery:[s('function','Функция',CHOICES.benchmark,'himmelblau'),s('arena_mode','Режим',CHOICES.arena_mode,'compare'),t('expression','Своя f(x, y)','x*x+y*y'),r('lr','Learning rate',.0001,.25,.0001,.015),r('steps','Шагов',10,300,10,75),r('radius','Радиус проекции L2',.2,4,.1,1.8),r('x0','Начальный x',-3,3,.1,-1.5),r('y0','Начальный y',-3,3,.1,2.5)],
 schedulers:[r('lr','Base LR',.001,.5,.001,.1),r('steps','Шагов',20,400,10,200),r('warmup','Warmup steps',1,90,1,15)],
 sweep:[s('optimizer','Оптимизатор',CHOICES.optimizer,'sgd'),r('steps','Шагов',10,150,10,60),r('seed','Seed',1,999,1,42)],
 classification:[s('algorithm','Алгоритм',CHOICES.classification,'logistic'),s('dataset','Данные',CHOICES.dataset,'moons'),r('n','Точки',40,440,10,180),r('noise','Шум',0,.65,.01,.22),r('threshold','Threshold',0,1,.01,.5),r('C','Inverse regularization C',.01,10,.05,1),r('depth','Max depth',1,12,1,4),s('criterion','Split criterion',[['gini','Gini'],['entropy','Entropy']],'gini'),r('min_leaf','Min samples leaf',1,20,1,2),r('trees','Number of trees',5,150,5,35),r('k','kNN neighbors',1,39,2,7),r('gamma','SVM gamma',.01,5,.05,1),s('kernel','SVM kernel',CHOICES.kernel,'rbf'),r('lr','Boosting learning rate',.01,.5,.01,.1),r('seed','Seed',1,999,1,42)],
 trees:[],ensembles:[],
 clustering:[s('dataset','Датасет',CHOICES.dataset,'blobs'),r('n','Количество точек',40,460,10,180),r('noise','Шум',.01,.65,.01,.22),r('k','Число кластеров',2,9,1,3),s('init','Инициализация',[['k-means++','K-Means++'],['random','Random']],'k-means++'),r('iterations','Итерации',1,100,1,30),r('seed','Seed',1,999,1,42)],
 neuron:[r('x1','Input x₁',-5,5,.1,1),r('x2','Input x₂',-5,5,.1,-1),r('w1','Weight w₁',-5,5,.05,.9),r('w2','Weight w₂',-5,5,.05,-.4),r('bias','Bias',-5,5,.05,.3),s('activation','Активация',CHOICES.activation,'sigmoid')],
 activation:[s('activation','Выделить функцию',CHOICES.activation,'relu'),r('at','Точка z',-5,5,.1,1)],
 neural:[s('dataset','Датасет',CHOICES.dataset,'xor'),s('activation','Hidden activation',[['tanh','Tanh'],['relu','ReLU'],['sigmoid','Sigmoid'],['swish','SiLU']],'tanh'),r('hidden','Нейронов',2,30,1,6),r('steps','Шаги обучения',20,1000,10,500),r('lr','Learning rate',.001,1,.001,.1),r('noise','Шум',0,.5,.01,.08),r('n','Samples',40,400,10,180),r('seed','Seed',1,999,1,42)],
 neural_dynamics:[s('init','Weight initialization',CHOICES.init,'xavier'),r('layers','Количество слоёв',2,14,1,6),r('width','Нейронов в слое',4,64,1,16),r('keep','Keep probability',.1,1,.05,.8),r('seed','Seed',1,999,1,42)],
 cnn:[s('kernel','Ядро',CHOICES.cnnkernel,'sobel_x'),r('stride','Stride',1,3,1,1),r('padding','Padding',0,2,1,0)],
 rnn:[t('text','Последовательность токенов','машина учится на тексте','Текст',3),r('hidden','Hidden size',2,24,1,6),r('recurrent_scale','Recurrent scale',.1,2,.05,.7),r('seed','Seed',1,999,1,42)],
 nlp:[t('text','Произвольный текст','Машинное обучение учит модели. Машинное обучение работает с данными.','Текст',4),t('documents','Документы через |','Машинное обучение полезно|Обучение моделей на данных|Данные и машинное обучение','Корпус',4)],
 bpe:[t('text','Обучающий корпус','кот котик коты кот котик собака','Текст',4),r('merges','Число BPE merge',0,25,1,5)],
 text_classification:[t('text','Проверяемый текст','нейросеть изучает данные','Текст',3),r('alpha','Сглаживание Naive Bayes',.05,5,.05,1)],
 embeddings:[t('text','Учебный корпус','кот ест рыбу. кот любит еду. собака ест мясо. собака любит прогулки. рыба живет в воде. мясо и рыба это еда.','Текст',5),r('window','Context window',1,5,1,2),t('word','Слово для ближайших соседей','кот')],
 attention:[t('text','Токены через пробел','кот видит свет','Вход',3),r('d','Размерность Q/K/V',2,12,1,4),r('temperature','Temperature',.1,3,.05,1),b('causal','Causal mask',false),r('seed','Seed',1,999,1,42)],
 multihead:[t('text','Токены через пробел','кот видит свет','Вход',3),r('heads','Количество heads',1,6,1,3),r('d','Head dimension',2,12,1,4),b('causal','Causal mask',false),r('seed','Seed',1,999,1,42)],
 decoding:[s('strategy','Стратегия',[['sampling','Sampling'],['greedy','Greedy (argmax)']],'sampling'),r('temperature','Temperature',.05,3,.05,1),r('top_k','Top-K',1,10,1,10),r('top_p','Top-P',.05,1,.05,1),r('seed','Seed',1,999,1,42)],
 rag:[t('query','Вопрос','Как работает Adam?','Поиск',3),t('documents','Документы через |','Градиентный спуск минимизирует функцию потерь.|Adam использует экспоненциальные оценки первого и второго моментов градиента.|TF-IDF представляет текст через взвешенные частоты слов.|Attention вычисляет веса между query и key.|Регуляризация L2 штрафует большие коэффициенты модели.','Корпус',5),r('top_k','Top-K документов',1,5,1,2)],
 bandits:[r('arms','Число ручек',2,10,1,5),r('steps','Шагов',10,1000,10,300),r('epsilon','Epsilon',0,1,.01,.15),r('seed','Seed',1,999,1,42)],
 math:[s('dimension','Размерность',CHOICES.dimension,'1d'),t('expression','Математическое выражение','sin(x)+0.15*x**2'),r('at','Текущий x',-5,5,.05,1),r('xmin','Левая граница',-10,0,.25,-5),r('xmax','Правая граница',0,10,.25,5)],
 algebra:[r('a','A₁₁',-3,3,.05,1.4),r('b','A₁₂',-3,3,.05,.4),r('c','A₂₁',-3,3,.05,-.25),r('d','A₂₂',-3,3,.05,.8),r('x','Вектор x',-3,3,.1,1),r('y','Вектор y',-3,3,.1,1)],
 norms:[r('w1','Weight w₁',-3,3,.1,1),r('w2','Weight w₂',-3,3,.1,1),r('lam','Lambda λ',0,5,.05,1)],
 information:[r('p','P(event)',.01,.99,.01,.3),r('q','Q(event)',.01,.99,.01,.65)]
};
SCHEMAS.trees=[s('algorithm','Алгоритм',[['tree','Decision Tree']],'tree'),...['dataset','depth','criterion','min_leaf','n','noise','seed'].map(k=>SCHEMAS.classification.find(x=>x.key===k))];
SCHEMAS.ensembles=[s('algorithm','Алгоритм',[['forest','Random Forest'],['boosting','Gradient Boosting']],'forest'),...['dataset','depth','trees','lr','n','noise','seed'].map(k=>SCHEMAS.classification.find(x=>x.key===k))];
// Progressive disclosure for every topic: core concepts first, advanced modules only on request.
// Every schema key must belong to exactly one group; values remain in cfg even if hidden.
const PARAM_LAYOUT={
 regression:{core:['w','b','lr'],modules:[
  ['optimizer','Оптимизатор',['optimizer','sampling','batch','momentum','beta1','beta2','rho','weight_decay','clip']],
  ['loss','Функция потерь',['loss','weight_mode','delta','quantile']],
  ['regularization','Регуляризация',['regularizer','lam','ratio']],
  ['schedule','Расписание learning rate',['scheduler']],
  ['dataset','Генератор данных',['n','true_w','true_b','noise','outliers','seed']]]},
 losses:{core:['residual'],modules:[['loss_settings','Форма функции потерь',['delta','quantile']]]},
 regularization_path:{core:['kind'],modules:[['path','Параметры регуляризации',['ratio','seed']]]},
 optimizer_gallery:{core:['function'],modules:[
  ['scenario','Сценарий сравнения',['arena_mode','expression','radius']],
  ['training','Шаги оптимизации',['lr','steps']],['start','Стартовая точка',['x0','y0']]]},
 schedulers:{core:['lr'],modules:[['scheduler_settings','Параметры расписания',['steps','warmup']]]},
 sweep:{core:['optimizer'],modules:[['sweep_config','Параметры поиска',['steps','seed']]]},
 classification:{core:['algorithm','dataset'],modules:[
  ['decision','Решение и регуляризация',['threshold','C']],
  ['model','Параметры модели',['depth','criterion','min_leaf','trees','k','gamma','kernel','lr']],
  ['data','Генератор данных',['n','noise','seed']]]},
 trees:{core:['algorithm','dataset'],modules:[
  ['tree','Параметры дерева',['depth','criterion','min_leaf']],
  ['data','Генератор данных',['n','noise','seed']]]},
 ensembles:{core:['algorithm','dataset'],modules:[
  ['ensemble','Настройки ансамбля',['depth','trees','lr']],
  ['data','Генератор данных',['n','noise','seed']]]},
 clustering:{core:['dataset','k'],modules:[
  ['init','Инициализация центроидов',['init','seed']],['data','Данные и итерации',['n','noise','iterations']]]},
 neuron:{core:['x1','x2'],modules:[
  ['weights','Веса и смещение',['w1','w2','bias']],['activation','Функция активации',['activation']]]},
 activation:{core:['activation'],modules:[['probe','Точка исследования',['at']]]},
 neural:{core:['dataset'],modules:[
  ['architecture','Архитектура',['hidden','activation']],['training','Обучение',['steps','lr']],
  ['data','Данные',['n','noise','seed']]]},
 neural_dynamics:{core:['init'],modules:[
  ['architecture','Архитектура',['layers','width']],['dropout','Dropout',['keep']],['seed','Воспроизводимость',['seed']]]},
 cnn:{core:['kernel'],modules:[['convolution','Параметры свёртки',['stride','padding']]]},
 rnn:{core:['text'],modules:[['recurrent','Размерности и веса',['hidden','recurrent_scale']],['seed','Воспроизводимость',['seed']]]},
 nlp:{core:['text'],modules:[['documents','Корпус документов',['documents']]]},
 bpe:{core:['text'],modules:[['merges','Число слияний',['merges']]]},
 text_classification:{core:['text'],modules:[['model','Сглаживание классификатора',['alpha']]]},
 embeddings:{core:['text'],modules:[['context','Контекстное окно',['window','word']]]},
 attention:{core:['text'],modules:[
  ['shape','Размерность внимания',['d','seed']],['mask','Маска и температура',['causal','temperature']]]},
 multihead:{core:['text'],modules:[
  ['heads','Количество голов и размерность',['heads','d']],['mask','Causal mask',['causal']],['seed','Воспроизводимость',['seed']]]},
 decoding:{core:['strategy'],modules:[
  ['sampling','Сэмплирование',['temperature','top_k','top_p']],['seed','Воспроизводимость',['seed']]]},
 rag:{core:['query'],modules:[['corpus','Поисковый корпус',['documents']],['retrieval','Количество документов',['top_k']]]},
 bandits:{core:['epsilon'],modules:[['experiment','Количество ручек и шагов',['arms','steps']],['seed','Воспроизводимость',['seed']]]},
 math:{core:['dimension','expression'],modules:[['domain','Область и точка',['at','xmin','xmax']]]},
 algebra:{core:['a','b'],modules:[['matrix','Остальные элементы матрицы',['c','d']],['vector','Вектор',['x','y']]]},
 norms:{core:['w1','w2'],modules:[['regularization','Сила штрафа',['lam']]]},
 information:{core:['p'],modules:[['comparison','Второе распределение',['q']]]}
};
const activeModules=new Map();
function modulesFor(key){return activeModules.get(key)||new Set();}
function getLayout(key){return PARAM_LAYOUT[key]||{core:[],modules:[]};}
function validateParameterLayouts(){for(const [key,fields] of Object.entries(SCHEMAS)){
 const layout=getLayout(key),used=[...layout.core,...layout.modules.flatMap(m=>m[2])],expected=fields.map(f=>f.key);
 if(used.length!==expected.length||new Set(used).size!==used.length||expected.some(k=>!used.includes(k)))throw Error('Неполная схема параметров '+key);
}}
validateParameterLayouts();
function relevantField(key){
 if(page==='regression'){
  if(key==='batch')return cfg.sampling==='mini';
  if(key==='momentum')return ['momentum','nesterov'].includes(cfg.optimizer);
  if(['beta1','beta2'].includes(key))return ['adam','adamw'].includes(cfg.optimizer);
  if(key==='rho')return cfg.optimizer==='rmsprop';
  if(key==='weight_decay')return cfg.optimizer==='adamw';
  if(key==='weight_mode')return cfg.loss==='weighted_mse';
  if(key==='delta')return ['huber','smooth_l1'].includes(cfg.loss);
  if(key==='quantile')return cfg.loss==='quantile';
  if(key==='lam')return cfg.regularizer!=='none';
  if(key==='ratio')return cfg.regularizer==='elastic';
 }
 if(['classification','trees','ensembles'].includes(page)){
  const a=cfg.algorithm;
  if(key==='threshold')return a!=='softmax';
  if(key==='C')return ['logistic','softmax','svm'].includes(a);
  if(key==='k')return a==='knn';
  if(['kernel','gamma'].includes(key))return a==='svm';
  if(['depth','min_leaf'].includes(key))return ['tree','forest','boosting'].includes(a);
  if(key==='criterion')return a==='tree';
  if(key==='trees')return ['forest','boosting'].includes(a);
  if(key==='lr')return a==='boosting';
 }
 if(page==='regularization_path'&&key==='ratio')return cfg.kind==='elastic';
 if(page==='optimizer_gallery'){
  if(key==='expression')return cfg.function==='custom';
  if(key==='radius')return cfg.arena_mode==='projected';
 }
 if(page==='schedulers'&&key==='warmup')return true;
 if(page==='decoding'&&['temperature','top_k','top_p'].includes(key))return cfg.strategy!=='greedy';
 return true;
}
const ROOT=document.documentElement;
let page='regression',cfg={},reg=null,surface=null,labResult=null,playing=false,busy=false,playTimer=null,debounce=null,lastPlotTime=0,currentKey='';
const GENERATORS=new Set(['n','true_w','true_b','noise','outliers','seed']);
let labUpdateTimer=null,labRequestSeq=0;
function scheduleLabUpdate(){clearTimeout(labUpdateTimer);labUpdateTimer=setTimeout(()=>runLab(),420);}
const HAS_WEBGL=(()=>{try{const c=document.createElement('canvas');return !!(c.getContext('webgl2')||c.getContext('webgl'));}catch(e){return false}})();
const NUM=x=>typeof x==='number'?(Math.abs(x)>=1e5||Math.abs(x)<1e-4&&x!==0?x.toExponential(3):parseFloat(x.toFixed(5)).toString()):String(x);
const ESC=x=>String(x).replace(/[&<>"']/g,s=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[s]));
const valueLabel=x=>Array.isArray(x)?x.map(NUM).join(', '):NUM(x);
function message(text,error=false){const n=$('#toast');n.textContent=text;n.classList.toggle('error',error);n.classList.add('show');clearTimeout(message._timer);message._timer=setTimeout(()=>n.classList.remove('show'),4000)}
async function api(path,payload={}){const response=await fetch('/api/'+path,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(payload)});const out=await response.json();if(!response.ok)throw Error(out.error||'Ошибка вычислений');return out;}
function heading(info){$('#breadcrumb').textContent=info[2];$('#pageTitle').textContent=info[3];$('#pageDescription').textContent=info[4];const group=NAV.find(g=>g[1].some(item=>item[0]===page));$('#sectionLabel').textContent=group?group[0].replace(/^\d+ · /,''):'';}
function buildNav(){const nav=$('#navigation');nav.innerHTML='';for(const [group,items] of NAV){const cap=document.createElement('div');cap.className='nav-caption';cap.textContent=group;nav.appendChild(cap);for(const info of items){const item=document.createElement('button');item.className='nav-item';item.dataset.page=info[0];item.innerHTML=`<span class="nav-icon">${info[1]}</span><span>${ESC(info[2])}</span>`;item.addEventListener('click',()=>navigate(info[0]));nav.appendChild(item);}}}
function defaults(key){return Object.fromEntries((SCHEMAS[key]||[]).map(s=>[s.key,s.value]));}
function navigate(next){if(!allNav.some(x=>x[0]===next))return;labRequestSeq++;clearTimeout(labUpdateTimer);clearTimeout(debounce);document.body.classList.remove('sidebar-open');stopPlay();page=next;cfg=defaults(page);if(page==='trees')cfg.algorithm='tree';if(page==='ensembles')cfg.algorithm='forest';if(page==='regression'&&reg)cfg={...cfg,...reg.config,w:reg.theta[0],b:reg.theta[1]};heading(allNav.find(x=>x[0]===page));$$('.nav-item').forEach(n=>n.classList.toggle('active',n.dataset.page===page));showControls();$('#timelineContainer').style.display=page==='regression'?'':'none';if(page==='regression'){if(reg)drawRegression();else resetRegression();}else runLab();}
function formatInput(n){if(n.type==='select')return `<select class="field config-field" data-key="${n.key}">${n.options.map(([v,k])=>`<option value="${ESC(v)}" ${String(cfg[n.key])===String(v)?'selected':''}>${ESC(k)}</option>`).join('')}</select>`;
 if(n.type==='text')return `<textarea class="field field-text config-field" data-key="${n.key}" rows="${n.rows||2}">${ESC(cfg[n.key]||'')}</textarea>`;
 if(n.type==='boolean')return `<label><input class="config-field" data-key="${n.key}" type="checkbox" ${cfg[n.key]?'checked':''}> &nbsp; Включено</label>`;
 return `<div class="control-label"><span>${ESC(n.label)}</span><input class="field field-number config-field" data-key="${n.key}" type="number" min="${n.min}" max="${n.max}" step="${n.step}" value="${ESC(cfg[n.key])}"></div><input class="slider" type="range" data-range="${n.key}" min="${n.min}" max="${n.max}" step="${n.step}" value="${ESC(cfg[n.key])}"><div class="control-range"><span>${NUM(n.min)}</span><span>${NUM(n.max)}</span></div>`;}
function showControls(){
 const host=$('#parameters'),layout=getLayout(page),active=modulesFor(page);
 host.innerHTML='';
 function createFields(keys,parent){for(const key of keys){
   const item=(SCHEMAS[page]||[]).find(x=>x.key===key);
   if(!item||!relevantField(key))continue;
   const control=document.createElement('div');control.className='control-group';
   control.innerHTML=(item.type==='range'?'':`<div class="control-label">${ESC(item.label)}</div>`)+formatInput(item);
   parent.appendChild(control);
 }}
 const essential=document.createElement('section');essential.className='essential-fields';
 essential.innerHTML='<div class="essentials-heading">Основное</div>';
 createFields(layout.core,essential);host.appendChild(essential);
 for(const [id,title,keys] of layout.modules){if(!active.has(id))continue;
   const wrap=document.createElement('section');wrap.className='added-module';wrap.dataset.module=id;
   const header=document.createElement('div');header.className='added-module-title';
   const heading=document.createElement('h4');heading.textContent=title;
   const remove=document.createElement('button');remove.type='button';remove.className='module-remove';remove.textContent='×';remove.title='Убрать блок и сбросить его параметры';remove.setAttribute('aria-label','Убрать блок '+title);
   remove.addEventListener('click',()=>removeModule(id));header.append(heading,remove);wrap.appendChild(header);
   const content=document.createElement('div');content.className='added-module-content';createFields(keys,content);
   if(!content.children.length)content.innerHTML='<p class="module-hint">Для текущего алгоритма дополнительные параметры не требуются.</p>';
   wrap.appendChild(content);host.appendChild(wrap);
 }
 const remaining=layout.modules.filter(m=>!active.has(m[0])&&m[2].some(relevantField));
 const addButton=$('#addModuleButton');addButton.hidden=!remaining.length;
 const picker=$('#modulePicker');picker.innerHTML='';picker.hidden=true;
 for(const [id,title] of remaining){const item=document.createElement('button');item.type='button';item.className='module-choice';item.textContent='+ '+title;item.addEventListener('click',()=>{
   activeModules.set(page,new Set([...active,id]));showControls();
   host.querySelector(`[data-module="${id}"]`)?.scrollIntoView({block:'nearest',behavior:'smooth'});
 });picker.appendChild(item);}
 addButton.setAttribute('aria-expanded','false');
 host.querySelectorAll('.config-field').forEach(node=>node.addEventListener(node.tagName==='TEXTAREA'||node.tagName==='SELECT'||node.type==='checkbox'?'change':'input',()=>{
   const key=node.dataset.key;const value=node.type==='checkbox'?node.checked:node.type==='number'?Number(node.value):node.value;
   if(node.type==='number'&&!Number.isFinite(value))return;
   cfg[key]=value;
   if(page==='classification'&&key==='algorithm'&&value==='softmax')cfg.dataset='blobs';
   const sibling=host.querySelector(`[data-range="${key}"]`);if(sibling)sibling.value=value;
   const dynamic=['optimizer','sampling','loss','regularizer','algorithm','kind','function','arena_mode','strategy'];
   if(dynamic.includes(key))showControls();
   if(page==='regression')scheduleRegressionUpdate(key);else scheduleLabUpdate();
 }));
 host.querySelectorAll('[data-range]').forEach(node=>node.addEventListener('input',()=>{
   const key=node.dataset.range;cfg[key]=Number(node.value);
   const paired=host.querySelector(`.config-field[data-key="${key}"]`);if(paired)paired.value=cfg[key];
   if(page==='regression')scheduleRegressionUpdate(key);else scheduleLabUpdate();
 }));
}
function removeModule(id){const module=getLayout(page).modules.find(m=>m[0]===id);if(!module)return;
 clearTimeout(debounce);clearTimeout(labUpdateTimer);stopPlay();
 const next=new Set(modulesFor(page));next.delete(id);activeModules.set(page,next);
 const defaultsMap=defaults(page);for(const key of module[2])cfg[key]=defaultsMap[key];
 showControls();if(page==='regression')resetRegression(true);else runLab();
}
function scheduleRegressionUpdate(key){clearTimeout(debounce);stopPlay();debounce=setTimeout(async()=>{try{if(GENERATORS.has(key)){await resetRegression(true)}else if(key==='w'||key==='b'){reg=await api('set',{w:cfg.w,b:cfg.b});drawRegression();}else{reg=await api('set',{[key]:cfg[key]});if(['loss','regularizer','lam','ratio','delta','quantile'].includes(key))surface=(await api('surface')).surface;drawRegression();}}catch(e){message(e.message,true)}},key==='w'||key==='b'?130:280);}
async function resetRegression(quiet=false){try{clearTimeout(debounce);stopPlay();setBusy(true);reg=await api('init',cfg);surface=reg.surface;delete reg.surface;cfg={...cfg,...reg.config};drawRegression();if(!quiet)message('Новый эксперимент создан');}catch(e){message(e.message,true)}finally{setBusy(false)}}
function setBusy(v){busy=v;$('#status-text').innerHTML=v?'<span class="online-dot"></span> Вычисление…':'<span class="online-dot"></span> Готово';}
function plotTheme(){
 const light=ROOT.classList.contains('light');
 const primary=light?'#27272a':'#ececec';const grid=light?'#e9e9eb':'#414141';
 return {paper_bgcolor:'rgba(0,0,0,0)',plot_bgcolor:'rgba(0,0,0,0)',
 font:{color:light?'#66666b':'#bdbdc2',family:'Inter, system-ui, Segoe UI, Arial',size:11},
 colorway:['#0d9488','#64748b','#e09b55','#7c84a6','#5caa83','#b17889','#a39980','#818cf8'],
 xaxis:{gridcolor:grid,zerolinecolor:grid},yaxis:{gridcolor:grid,zerolinecolor:grid},
 legend:{orientation:'h',y:-.22,font:{size:10}},hovermode:'closest'};
}
function renderCharts(charts){const host=$('#graphs');if(!charts||!charts.length){host.innerHTML='<div class="empty-panel">Пока нет данных.</div>';return;}const key=page+'_'+charts.length;const recreate=currentKey!==key||$$('.chart-card').length!==charts.length;currentKey=key;if(recreate){host.innerHTML='';charts.forEach((c,i)=>{const card=document.createElement('div');card.className='chart-card'+(c.wide?' wide':'');card.innerHTML=`<div class="chart-head"><strong>${ESC(c.title||'Визуализация')}${!HAS_WEBGL&&c.traces.some(t=>t.type==='surface'||t.type==='scatter3d')?' · 2D контуры':''}</strong></div><div class="chart-body" id="plot-${i}"></div>`;host.appendChild(card);});}
 const theme=plotTheme();charts.forEach((c,i)=>{const original3d=c.traces.some(t=>t.type==='surface'||t.type==='scatter3d');
  let traces=c.traces;
  if(original3d&&!HAS_WEBGL)traces=traces.map(t=>t.type==='surface'?{type:'contour',x:t.x,y:t.y,z:t.z,colorscale:t.colorscale||'Viridis',showscale:false,opacity:t.opacity||1,ncontours:22}:t.type==='scatter3d'?{type:'scatter',x:t.x,y:t.y,mode:t.mode||'lines',name:t.name,line:t.line||{},marker:{...t.marker,size:Math.max(5,t.marker?.size||5)}}:t);
  // Calm sequential scale for loss surfaces; preserve diverging scales for signed kernels.
  const calm=ROOT.classList.contains('light')?[[0,'#f0f4f4'],[.5,'#9abfba'],[1,'#316b66']]:[[0,'#263a39'],[.5,'#4f817a'],[1,'#a7c8b9']];
  traces=traces.map(t=>t.colorscale==='Viridis'?{...t,colorscale:calm}:t);
  const target=$(`#plot-${i}`),layout={...theme,...c.layout,margin:{l:48,r:12,t:18,b:48},height:target?.clientHeight||340,autosize:true};if(layout.xaxis)layout.xaxis={...theme.xaxis,...layout.xaxis};if(layout.yaxis)layout.yaxis={...theme.yaxis,...layout.yaxis};if(original3d&&HAS_WEBGL){layout.scene={xaxis:{title:'x'},yaxis:{title:'y'},zaxis:{title:'Objective'},bgcolor:'rgba(0,0,0,0)',...layout.scene};delete layout.xaxis;delete layout.yaxis;layout.margin={l:0,r:0,t:0,b:0};}
   // Focus on learning: only zoom and reset, without screenshot/export, lasso or 3D gimmicks.
   const buttons=original3d&&HAS_WEBGL?['zoom3d','resetCameraDefault3d']:['zoomIn2d','zoomOut2d','resetScale2d'];
   Plotly.react(target,traces,layout,{responsive:true,displaylogo:false,displayModeBar:'hover',scrollZoom:true,doubleClick:'reset',modeBarButtons:[buttons]}).catch(e=>message('Ошибка графика: '+e.message,true));});
}
function setStats(items){let stats=Object.entries(items||{}).filter(([,v])=>typeof v==='number'||typeof v==='string');stats=stats.slice(0,8);if(!stats.length){$('#statsStrip').innerHTML='';return;}$('#statsStrip').innerHTML=stats.slice(0,4).map(([name,value])=>`<div class="stat-card"><div class="stat-label">${ESC(name.replaceAll('_',' ').toUpperCase())}</div><div class="stat-value" title="${ESC(valueLabel(value))}">${ESC(typeof value==='number'?NUM(value):value)}</div></div>`).join('');}
function kvHtml(items){return Object.entries(items).slice(0,24).map(([k,v])=>`<div class="keyval"><span>${ESC(k.replaceAll('_',' '))}</span><strong>${ESC(valueLabel(v))}</strong></div>`).join('');}
function setExplanation(html){$('#explanation').innerHTML=html;}
function drawRegression(){if(!reg)return;const h=reg.history,last=reg.current,x=reg.x,y=reg.y,p=reg.prediction,w=reg.theta[0],b=reg.theta[1];const coords=h.map(q=>q.w),bias=h.map(q=>q.b),losses=h.map(q=>q.loss);const currentG=last.gradient;
 const segments=[];for(let i=0;i<x.length;i++){segments.push(x[i],x[i],null)}
 const ys=[];for(let i=0;i<x.length;i++)ys.push(y[i],p[i],null);
 const light=ROOT.classList.contains('light');
 const dataChart={title:'Модель и остаточные ошибки',traces:[{type:'scatter',mode:'markers',name:'Датасет',x,y,marker:{color:'#0d9488',size:7,opacity:.86}}, {type:'scatter',mode:'lines',name:'Residuals',x:segments,y:ys,line:{color:'#c58d85',width:1},opacity:.7,hoverinfo:'skip'}, {type:'scatter',mode:'lines',name:'ŷ = '+NUM(w)+'x + '+NUM(b),x:[Math.min(...x),Math.max(...x)],y:[w*Math.min(...x)+b,w*Math.max(...x)+b],line:{color:'#b78b56',width:3}}],layout:{xaxis:{title:'Признак x'},yaxis:{title:'Целевая переменная y'}}};
 const s=surface;
 const path3={type:'scatter3d',x:coords,y:bias,z:losses,name:'Путь оптимизации',mode:'lines+markers',line:{color:'#b78b56',width:5},marker:{size:2,color:'#b78b56'}};
 const point3={type:'scatter3d',x:[w],y:[b],z:[last.loss],name:'Текущие θ',mode:'markers',marker:{size:7,color:'#64748b'}};
 const surfChart={title:'3D · поверхность функции потерь',traces:s?[{type:'surface',x:s.w,y:s.b,z:s.z,opacity:.80,showscale:false,colorscale:'Viridis',hovertemplate:'w=%{x:.2f}<br>b=%{y:.2f}<br>Loss=%{z:.4f}<extra></extra>'},path3,point3]:[point3],layout:{scene:{xaxis:{title:'Weight w'},yaxis:{title:'Bias b'},zaxis:{title:'Loss'}}}};
 const contourChart={title:'Линии уровня и траектория',traces:s?[{type:'contour',x:s.w,y:s.b,z:s.z,showscale:false,colorscale:'Viridis',ncontours:24,contours:{coloring:'heatmap'},opacity:.89},{type:'scatter',x:coords,y:bias,mode:'lines+markers',name:'Траектория',line:{color:'#b78b56',width:2.5},marker:{color:'#eee2d2',size:5}},{type:'scatter',x:[w],y:[b],mode:'markers',name:'Текущая точка',marker:{color:'#8d89aa',size:14,symbol:'circle-open',line:{width:3}}}]:[],layout:{xaxis:{title:'Weight w'},yaxis:{title:'Bias b'}}};
 const lossChart={title:'История обучения · objective',traces:[{type:'scatter',x:h.map(q=>q.step),y:losses,mode:'lines',name:'Total objective',line:{color:'#0d9488',width:2.5}},{type:'scatter',x:h.map(q=>q.step),y:h.map(q=>q.data_loss),mode:'lines',name:'Data loss',line:{color:'#7c84a6',width:1.5,dash:'dot'}}],layout:{xaxis:{title:'Шаг оптимизации'},yaxis:{title:'Loss'}}};
 renderCharts([dataChart,surfChart,contourChart,lossChart]);setStats({'TOTAL LOSS':last.loss,'WEIGHT w':w,'BIAS b':b,'GRADIENT NORM':Math.hypot(...currentG)});
 const d=reg.detail||{};const rows={'θ (w, b)':reg.theta,'∇L (full data)':currentG,'Data loss':last.data_loss,'Penalty':last.penalty,'RMSE':reg.score.rmse,'R²':reg.score.r2,'Optimizer':reg.config.optimizer,'Шаг':reg.steps};
 let html=kvHtml(rows)+`<div class="formula">θₜ₊₁ = Optimizer(θₜ, ∇L, stateₜ)</div>`;
 if(d.gradient)html+='<div class="group-title">ПОСЛЕДНИЙ ШАГ</div>'+kvHtml({Batch:d.batch_indices?.slice(0,18)||[],Gradient:d.gradient,Update:d.update,Before:d.before,After:d.after,LR:d.learning_rate});
 if(d.m_hat)html+='<div class="group-title">СОСТОЯНИЕ ADAM</div>'+kvHtml({m:d.first_moment,v:d.second_moment,m_hat:d.m_hat,v_hat:d.v_hat});
 if(d.velocity)html+='<div class="group-title">MOMENTUM</div>'+kvHtml({Velocity:d.velocity});
 if(d.second_moment&&!d.m_hat)html+='<div class="group-title">RMSPROP</div>'+kvHtml({EMA_squared:d.second_moment});
 $('#inspector').innerHTML=html;
 setExplanation('<b>Линейная регрессия:</b> ŷ = wx + b. Вверху показаны наблюдения и 3D-поверхность L(w, b); ниже — контуры и фактическая история шагов. Меняйте параметры справа, а затем используйте кнопки истории для пошагового обучения. Раскройте математический инспектор для градиентов и состояний оптимизатора.');
 $('#timelineRange').max=h[h.length-1].step;$('#timelineRange').min=h[0].step;$('#timelineRange').value=reg.steps;$('#timelineStep').textContent='Шаг '+reg.steps;$('#timelineLoss').textContent='Loss '+NUM(last.loss);
}
async function stepRegression(){if(busy)return;try{setBusy(true);reg=await api('step');drawRegression()}catch(e){stopPlay();message(e.message,true)}finally{setBusy(false)}}
async function runRegression(n){if(busy)return;try{setBusy(true);reg=await api('run',{steps:n});drawRegression();message('Выполнено '+n+' шагов (или до условия остановки)');}catch(e){message(e.message,true)}finally{setBusy(false)}}
async function seek(step){if(busy)return;try{setBusy(true);reg=await api('seek',{step});drawRegression()}catch(e){message(e.message,true)}finally{setBusy(false)}}
function stopPlay(){playing=false;clearInterval(playTimer);playTimer=null;$('#toPlay').textContent='▶'}
function togglePlay(){if(playing){stopPlay();return}playing=true;$('#toPlay').textContent='Ⅱ';playTimer=setInterval(()=>{if(!busy)stepRegression()},330)}
function labName(){return ['trees','ensembles'].includes(page)?'classification':page;}
async function runLab(){const requestId=++labRequestSeq;const requestedPage=page;try{setBusy(true);const payload={...cfg};if(page==='optimizer_gallery'){payload.optimizers=cfg.arena_mode==='projected'?['sgd','projected']:cfg.arena_mode==='adaptive'?['adagrad','rmsprop','adam','adamw']:['sgd','momentum','nesterov','adagrad','rmsprop','adam','adamw'];}const results=await api('lab',{name:labName(),config:payload});if(requestId!==labRequestSeq||requestedPage!==page)return;labResult=results;setStats(results.stats);renderCharts(results.charts);const extra=Object.entries(results.details||{}).slice(0,10).map(([k,v])=>`<details class="detail-fold"><summary>${ESC(k.replaceAll('_',' '))}</summary><pre class="formula">${ESC(JSON.stringify(v,null,2).slice(0,5000))}</pre></details>`).join('');
 $('#inspector').innerHTML=kvHtml(results.stats)+extra+(results.table?.length?`<div class="group-title">ТАБЛИЦА РАСЧЁТОВ</div><div style="overflow:auto;max-height:260px"><table class="data-table"><thead><tr>${Object.keys(results.table[0]).map(k=>`<th>${ESC(k)}</th>`).join('')}</tr></thead><tbody>${results.table.slice(0,28).map(row=>`<tr>${Object.values(row).map(v=>`<td>${ESC(valueLabel(v))}</td>`).join('')}</tr>`).join('')}</tbody></table></div>`:'');setExplanation('<b>Как устроено вычисление:</b> '+ESC(results.explain));}catch(e){if(requestId===labRequestSeq){message(e.message,true);$('#inspector').textContent='Ошибка: '+e.message}}finally{if(requestId===labRequestSeq)setBusy(false)}}
function loadTheme(){try{return localStorage.getItem('ml-universe-theme')}catch(_){return null}}
function saveTheme(theme){try{localStorage.setItem('ml-universe-theme',theme)}catch(_){/* private/opaque origin */}}
function updateThemeIcon(){const light=ROOT.classList.contains('light');$('#themeButton').textContent=light?'☾':'☼';$('#themeButton').title=light?'Включить тёмную тему':'Включить светлую тему'}
function wire(){ROOT.classList.toggle('light',loadTheme()!=='dark');updateThemeIcon();buildNav();$('#resetButton').onclick=()=>{clearTimeout(debounce);clearTimeout(labUpdateTimer);activeModules.delete(page);cfg=defaults(page);if(page==='trees')cfg.algorithm='tree';if(page==='ensembles')cfg.algorithm='forest';showControls();page==='regression'?resetRegression():runLab()};$('#toStep').onclick=()=>stepRegression();$('#toBack').onclick=()=>seek(Math.max(0,reg.steps-1));$('#toPlay').onclick=togglePlay;$('#run25').onclick=()=>runRegression(25);$('#timelineRange').addEventListener('change',e=>seek(Number(e.target.value)));$('#themeButton').onclick=()=>{ROOT.classList.toggle('light');saveTheme(ROOT.classList.contains('light')?'light':'dark');updateThemeIcon();if(page==='regression')drawRegression();else if(labResult)renderCharts(labResult.charts);};$('#addModuleButton').onclick=()=>{const picker=$('#modulePicker');picker.hidden=!picker.hidden;$('#addModuleButton').setAttribute('aria-expanded',String(!picker.hidden));};$('#helpButton').onclick=()=>$('#modal').classList.remove('hidden');$('#closeModal').onclick=()=>$('#modal').classList.add('hidden');$('#modal').onclick=e=>{if(e.target===$('#modal'))$('#modal').classList.add('hidden')};window.addEventListener('keydown',e=>{if(e.key==='Escape'){$('#modal').classList.add('hidden');stopPlay()}if(e.key===' '&&!['INPUT','TEXTAREA','SELECT'].includes(document.activeElement.tagName)&&page==='regression'){e.preventDefault();togglePlay()}});window.addEventListener('resize',()=>{$$('.chart-body').forEach(n=>{if(n.data)Plotly.Plots.resize(n)})});$('#sidebarToggle').onclick=()=>document.body.classList.toggle('sidebar-open');navigate('regression');}
wire();
