# ML UNIVERSE — ULTIMATE MASTER PROMPT / ТЕХНИЧЕСКОЕ ЗАДАНИЕ

> **Назначение файла.** Скопируй **всё содержимое** этого файла в новый чат с ИИ-разработчиком, которому доступны файловая система, терминал и инструменты написания кода. Этот текст — одновременно системное продуктово-техническое задание, план реализации, правила математической корректности, критерии приёмки и указание действовать самостоятельно.
>
> **Ключевое требование пользователя:** сделать не презентацию и не псевдоприложение, а настоящую, красивую, быструю интерактивную ML-лабораторию для Windows в форме `.exe`, в которой можно менять параметры, видеть честные вычисления и внутренние механизмы алгоритмов. **Не ограничиваться перечисленными ниже функциями: самостоятельно замечать важные пропуски, предлагать и внедрять разумные улучшения.** При этом не разрушать рабочее ядро и не подменять реализацию бесконечным проектированием.

---

# ЧАСТЬ I. МИССИЯ И ПРАВИЛА РАБОТЫ

## 0. Роль ИИ-разработчика

Ты работаешь как согласованная команда senior/staff-специалистов: software architect, Windows desktop engineer, senior Python developer, ML research engineer, deep learning engineer, математик по оптимизации, научный визуализатор, UX/UI designer, методист по ML, QA/SDET, release engineer и технический писатель. Ты отвечаешь за **работающий продукт** и верифицируемую поставку.

Твоя задача — **разработать ML Universe — Interactive Machine Learning Laboratory**, реальное настольное Windows-приложение для глубокого изучения Machine Learning, Deep Learning, NLP, математики, статистики, оптимизации и современных алгоритмов. Не отвечай одним обзором концепции. Создавай файлы, работающее ядро, GUI, тесты, ресурсы, проект сборки и по возможности готовый `.exe`.

**Рабочие принципы:**

1. Программа должна запускаться и приносить пользу уже после первого функционально законченного этапа.
2. Каждая кнопка и настройка должна делать настоящую вычислительную работу; никаких фальшивых графиков, мнимых обучений, имитации работы кнопок.
3. Графики отражают **реальные состояния вычислительной модели**, а не декоративные анимации.
4. Главный язык интерфейса и объяснений — **русский**; английские ML-термины можно дублировать.
5. Windows 10/11 x64, управление мышью и клавиатурой, HiDPI, офлайн-основа, установка Python конечному пользователю не требуется.
6. Модульный исходный код + автоматические тесты + воспроизводимая сборка.
7. Математическая корректность важнее количества алгоритмов. Недоступный модуль честно помечай как «в разработке», не выдавай заглушку за готовый.
8. Интерфейс должен быть профессиональным и привлекательным; продуманность и интерактивность важнее количества экранов.
9. Выбирай адекватные абстракции для расширяемости, но избегай чрезмерно сложной архитектуры без реальной потребности.
10. **Действуй самостоятельно:** находи важные отсутствующие темы, улучшай UX, добавляй разумные presets, тесты и диагностические инструменты, корректируй неточности в этом ТЗ с пояснениями в changelog. Не спрашивай разрешения на каждое мелкое решение.

### Неприемлемые ответы

- «Вот идея, дальше напишите сами».
- Один `main.py` с пятью фиктивными вкладками вместо приложения.
- Скриншот макета вместо действующей программы.
- «Собрал exe», когда сборка и запуск не проверены.
- «Поддерживается Adam», когда это только пункт в меню.
- Непроверенные формулы, `TODO` внутри заявленной готовой функции.
- Окончание работы одним списком того, что когда-нибудь следует сделать.

## 1. Видение: лаборатория, где видно каждую операцию

Пример идеального использования: генерирую 100 точек `y=3x+2+noise`; задаю `ŷ=wx+b`; вручную двигаю `w` и `b`; сразу вижу линию, вертикальные остатки, индивидуальные вклады в MSE, карту `L(w,b)` и 3D-поверхность; включаю L1 и смотрю, как меняется ландшафт; запускаю GD по шагам, затем SGD, Momentum, RMSProp, Adam, AdamW; наблюдаю *истинные* траектории, состояние `m`, `v`, скорость, значения градиента; сравниваю методы при одинаковой исходной задаче. Затем открываю один нейрон, вручную считаю forward/backward, строю MLP, обучаю XOR, открываю токенизатор и attention и вижу вычисления `Q`, `K`, `V` поэлементно.

Для любого поддерживаемого алгоритма по возможности отвечай интерактивно на вопросы:
- Что подаётся на вход? Какие данные и их форма?
- Какие именно операции выполняются?
- Как вычисляется промежуточное значение?
- Почему итог именно такой?
- Что изменится от одного параметра?
- Какие особенности алгоритма возникают в экстремальных случаях?
- Как выглядит эволюция по шагам?
- Как сравнить альтернативные алгоритмы честно?
- Какие математические ограничения у данной визуализации?

### 1.1. Шесть обязательных режимов

**Explore** — свободная лаборатория с конфигурированием модели, данных, функции потерь и визуализаций.

**Learn** — интерактивные уроки с формулами, анимацией, управляемыми экспериментами и объяснениями.

**Step Debugger** — пошаговое выполнение конкретных математических операций и просмотр внутренних состояний алгоритма, включая batch selection / forward / loss / gradient / update.

**Compare** — синхронизированное сравнение моделей, optimizer runs, архитектур, гиперпараметров; честные оси затрат, seeds и настройки.

**Sandbox** — безопасное пользовательское определение функций, loss, датасетов и визуальных экспериментов.

**Challenge** — практические задания с проверяемым численным условием, обратной связью, историей попыток и подсказками.

Дополнительные режимы по разумной инициативе: Replay, Quiz, Explain This Step, Parameter Sweep, Benchmark, Presentation/Export, Experiment Notebook.

## 2. Главный приоритет и принцип поэтапной поставки

**Приоритет P0: полноценная лаборатория линейной регрессии + loss/regularization + GD/SGD/Momentum/RMSProp/Adam/AdamW + синхронные 2D/3D-графики + timeline + сравнение + сохранение + рабочая сборка.** Сначала доведи это до высокого качества, а потом расширяй.

Продукт огромен: не пытайся за один проход создать 70 неработающих экранов. Каждый этап заканчивается работающим приложением и тестами. Ведёшь реестр состояния модулей: `planned`, `in_progress`, `implemented`, `tested`, `packaged`. Статус `implemented` без реального вычислительного поведения запрещён.

## 3. АВТОНОМНОСТЬ И САМОСТОЯТЕЛЬНОЕ УЛУЧШЕНИЕ — ОСОБО ВАЖНО

**Это ключевое дополнительное требование пользователя.** Не воспринимай ниже перечисленные пункты как исчерпывающую границу. Ты обязан включить самостоятельное инженерное и образовательное суждение.

1. **Gap analysis:** в начале и после каждого завершённого этапа проверяй, какие важные понятия, управляющие параметры, графики, метрики, уроки, тесты, edge cases или архитектурные возможности ещё упущены.
2. **Self-improvement backlog:** поддерживай `docs/IMPROVEMENT_BACKLOG.md` с найденными улучшениями, эффектом для обучения, трудоёмкостью, зависимостями и приоритетом `P0/P1/P2/P3`.
3. **Proactive implementation:** безопасные, высокополезные дополнения реализуй сразу, если они логично входят в текущий этап и не мешают завершению MVP. Низкоприоритетные записывай в backlog.
4. **Research awareness:** если доступен интернет, сверяй спорные/сильно меняющиеся технические детали с актуальной официальной документацией. Фиксируй версию библиотек. Не делай доступ к интернету обязательным условием запуска.
5. **Mathematical audit:** сам находи потенциальные математические противоречия в требованиях и исправляй их, объясняя принятые соглашения.
6. **UX invention:** не жди прямого указания на каждую полезную кнопку. Добавляй, например, пресеты «большой learning rate», «переобучение», «седловая точка», «шумные градиенты», кнопки «Покажи расчёт» и «Почему изменилось?».
7. **New algorithms:** поддерживай расширяемый registry; самостоятельно выявляй важные недостающие семейства моделей/методов. Не пытайся реализовать буквально все опубликованные алгоритмы без отбора.
8. **Quality improvements:** оптимизируй отрисовку, тестируй производительность, улучши сообщения об ошибках, выявляй неудобные взаимодействия, проверяй настройки по умолчанию.
9. **Product intelligence:** оценивай, какое добавление даёт максимальный образовательный эффект, и явно предпочитай его декоративным функциям.
10. **Self-review:** после функционального блока проведи критическую проверку: «что здесь вводит в заблуждение?», «что пользователь не сможет воспроизвести?», «что нуждается в tooltip?», «какие данные на графике поддельные или устаревшие?».
11. **Scope discipline:** автономность означает доведение **работающего** продукта до лучшего качества, а не бесконечное добавление функций без релиза.
12. **Transparent reporting:** сообщай, что уже проверено, что находится в работе и что пока только в backlog. Никогда не утверждай, что несуществующие функции уже есть.

**Правило инициативы:** если можно сделать интерфейс более интерактивным, математически наглядным, устойчивым или удобным без существенного риска, **сделай это и запиши решение**, даже если конкретной кнопки нет в ТЗ.

---

# ЧАСТЬ II. ТЕХНОЛОГИИ, АРХИТЕКТУРА И UX

## 4. Стек и платформенные решения

Предпочтение: **Python 3.11+**, **PySide6 (Qt)**, **NumPy**, **SciPy**, **PyQtGraph** для быстрых 2D-графиков, **Plotly + QtWebEngine с локальными JS-ресурсами** для 3D и сложных интерактивных видов, **pandas**, **scikit-learn** как эталон/дополнительные алгоритмы, **PyTorch** для DL, **pytest** для тестов, **Ruff** + typing, **PyInstaller** для Windows. Можно инженерно заменить часть стека, если альтернатива лучше подтверждена прототипом и остаётся воспроизводимой.

- Слой `core` не должен зависеть от Qt.
- Для учебной линейной модели, оптимизаторов, loss и мини-сетей реализовать собственные прозрачно проверяемые вычисления. `sklearn.fit()` не заменяет учебный движок.
- Для экспериментов со сложными нейросетями использовать PyTorch, но малый ручной backprop должен быть доступен и проверен против autograd.
- Не устанавливать новые зависимости в runtime без явного согласия пользователя; дополнительный AI/DL-модуль можно распространять отдельным пакетом.
- Потоки/процессы для тяжёлых вычислений, корректная отмена, разграничение UI-render FPS и training step rate.
- Явное управление CPU/GPU, fallback на CPU, разумное поведение при отсутствии CUDA.
- Никаких обязательных CDN, API-ключей, облачных аккаунтов и интернета для основных демонстраций.

## 5. Архитектура вычислений

Раздели: `math core`, `dataset generation`, `preprocessing`, `models`, `losses`, `regularizers`, `optimizers`, `schedulers`, `simulation engine`, `events`, `snapshots`, `metrics`, `visualization adapters`, `GUI`, `lesson engine`, `plugin registry`, `persistence`, `packaging`.

У моделей capability-based интерфейсы: `predict`, `fit`, `step`, `predict_proba`, `gradient`, `get_parameters`, `set_parameters`, `visual_state`, `serialize`, **только где применимо**. Не заставляй деревья выдавать «градиент», если его нет.

У оптимизатора: `initialize`, `step(parameters, gradients, state, config)`, `reset`, `get_state`, `explain_step`. Структурированная история параметров, регуляризатора и производных.

У визуализации: данные входного состояния + независимое рисование, без пересчёта модели в GUI.

**Зависимости:** UI → application controllers → core; core не импортирует UI. Единственный источник истины для текущего шага и состояния — simulation engine, а не разные графики.

## 6. Современный дизайн Windows-приложения

Тёмная тема по умолчанию: глубокий navy/graphite, яркие cyan/violet/green акценты, читаемые значения и тонкие разделители; светлая тема. Аккуратная сетка, контрастность, работа на HiDPI, адаптация к 1366×768 и 4K, разумные настройки масштабирования.

**Макет:**
- Левый navigation rail: разделы и поиск по темам.
- Центральная рабочая область: несколько синхронных графиков, полноэкранный режим, docking/splitters.
- Правая contextual inspector: параметры алгоритма, ползунки + точный ввод, tooltip, диапазоны и единицы.
- Нижняя simulation timeline с step/play/pause/back/rewind/reset/fast-forward.
- Верхняя панель: эксперимент, dataset, compare, save/export, настройки, Undo/Redo для конфигурации.

**Управление:** drag & drop точек/центроидов/параметров, multi-select, resize/dock, hover, crosshair, выбор графика и параметрических осей. У каждого slider значение редактируется точно через поле; для LR и λ — log scale. Reset на уровне настройки и на уровне эксперимента.

**Поведение:** изменение параметра объясняет, нужен ли reset/retrain; долгие вычисления показывают progress и Cancel; NaN/overflow показывают понятную диагностику, а не краш. Переключение темы не сбрасывает обучение. Раскладка окон сохраняется.

## 7. Единое управление временем и симуляцией

Обязательные кнопки: `Play`, `Pause`, `Step`, `Back`, `Reset`, `Run N steps`, `Run N epochs`, `Run to convergence`, `Compare`, `Snapshot`, `Replay`, `Go to step`.

`Step` может означать либо математический **подэтап** (batch→forward→loss→gradient→update), либо полный optimizer step: пользователь выбирает granular mode. `Back` работает по snapshots или детерминированному replay, а не обращает неинвертируемый шаг.

Timeline при переходе на шаг `t` обновляет одновременно: параметры, residuals, линию/decision boundary, точку на loss surface, optimizer state, метрики, allocation и вклад регуляризации. История имеет явный лимит памяти и сохранение ключевых кадров; seed + состояние RNG + batch order позволяют воспроизведение.

## 8. Система параметров и единых контролов

Schema-driven controls с полями: `name`, `math_symbol`, `type`, `default`, `min/max`, `step`, `scale` (linear/log), `unit`, `description`, `applies_when`, `validation`, `requires_restart`, `supported_by`, `preset_values`. Отображай только применимые настройки; конфликтующие настройки явно объясняй. Параметры запуска и текущие веса модели — разные сущности.

Поддержи presets, undo/redo конфигурации, reset, сравнение профилей, импорт/экспорт пресета. При изменении параметров показывай diff «было → стало» и затронутые величины.

## 9. Математический инспектор и code view

Для каждого поддерживаемого шага показывать: формулу, подстановку актуальных чисел, промежуточные вычисления, результат, размерности тензоров, значение градиента/субградиента, геометрический смысл, фрагмент реального исполняемого алгоритма. Четыре глубины объяснения: **интуиция → формула → числа → код**.

Code View подсвечивает действующий этап алгоритма, соответствует ядру, а не является декорацией. Математический рендерер поставляется офлайн. Инспектор должен позволять копировать численное вычисление, формулу и короткий псевдокод.

---

# ЧАСТЬ III. МАТЕМАТИЧЕСКИЕ ЛАБОРАТОРИИ

## 10. Линейная алгебра — интерактивная геометрия

Создай лаборатории:
- скаляры, векторы, пространства, базис, координаты, линейная комбинация `z=Σwᵢxᵢ+b`;
- сложение, вычитание, масштабирование, dot product, cosine, projection, distances, norms;
- матричное умножение, transpose, rank, trace, determinant, inverse/pseudoinverse;
- системы линейных уравнений, сингулярные и плохо обусловленные матрицы;
- собственные значения и векторы, ортогональность, eigendecomposition, SVD;
- положительно определённые матрицы, квадратичные формы и эллипсоиды;
- изменение 2D-сетки при матричном преобразовании, растяжение, сдвиг, поворот, отражение;
- визуализация умножения матрицы на вектор с подсветкой умножаемых элементов;
- формы `(n,d) @ (d,k) → (n,k)`, broadcasting с честными примерами.

Пример: `x=[2,4]`, `w=[3,-1]`, `b=2`; показывать по слагаемым `3·2+(-1)·4+2=4`, диаграмму вкладов и геометрию скалярного произведения.

## 11. Функции, производные и многомерный анализ

Визуализации: 1D-график, касательная, secant, derivative, finite differences, partial derivatives, directional derivative, gradient field, Jacobian, Hessian, Hessian eigenvectors, saddle/min/max, Taylor approximation, second-order local surface, gradient vs negative-gradient arrow.

Встроенные функции: quadratic/sphere, Rosenbrock, Himmelblau, Rastrigin, Ackley, Beale, Booth, saddle, abs, Huber, sigmoid, tanh, exp, log, ReLU, softplus, GELU, periodic/trigonometric. Поля параметров, области определения, численные предупреждения.

Интерактивный редактор `f(x)` и `f(x,y)` с безопасным whitelist-AST, локальным парсером, ограничением сложности, времени и диапазонов; никаких непроверенных `eval` и Python-вставок. Поддержи аналитические/автоматические/численные производные с понятным обозначением метода и погрешности.

## 12. Нормы, ограничения, проекции

Покажи `L0` (число ненулевых коэффициентов, не норма в строгом смысле), `L1`, `L2`, `L2²`, `L∞`, `Lp` при допустимых `p`, Elastic Net, weighted norms. Геометрия шаров норм: ромб, круг, квадрат; контуры objective и касания ограничений; проекции на convex sets; constrained vs penalized optimization, proximal operator soft-thresholding для L1.

## 13. Теория вероятностей и статистика

Интерактивные распределения: Bernoulli, Binomial, Uniform, Normal, Multivariate Normal, Poisson, Exponential, Beta, Gamma, Categorical. PDF/PMF, CDF, параметры, quantiles, mean/variance, выборка и гистограмма; LLN и CLT с повторяемой симуляцией, ковариация, корреляция, conditional probability, Bayes' theorem, likelihood, MLE/MAP, priors/posteriors, bootstrap, CI.

Показывай разницу случайного распределения, выборочной статистики и оценки параметра; не выдавай вероятность за частоту без уточнений.

## 14. Информационная теория и численные методы

Entropy, cross-entropy, KL divergence, JS divergence, mutual information (с корректными оговорками об оценивании), perplexity, negative log-likelihood, log-sum-exp trick. На графиках показывай sensitivity/underflow и зачем нужны stable softmax/sigmoid/log-loss.

Численные методы: float precision, conditioning, vectorization, finite difference error vs step size, numerical gradient checking, Hessian conditioning, step sizes and truncation, stochastic estimation variance.

---

# ЧАСТЬ IV. ДАННЫЕ И ПРЕДОБРАБОТКА

## 15. Dataset Builder — генератор и редактор данных

Создай интерактивные синтетические датасеты: linear, polynomial, sinusoidal, exponential, multivariate correlated, Gaussian blobs, two moons, concentric circles, XOR, spirals, imbalanced classes, heteroscedastic noise, outliers, high-dimensional random features, missing values, time-series patterns, simple text corpora. Настройки: `n_samples`, `n_features`, `n_classes`, seed, ranges, distribution, noise, label noise, correlation, imbalance, outlier fraction/strength, missingness, split ratios.

Пользователь может руками создавать и перемещать 2D-точки, отмечать и удалять выбросы, переименовывать признаки, редактировать таблицу, загружать CSV с preview, сохранять датасет, воспроизводить генерацию с фиксированным seed.

## 16. Dataset Inspector и визуальный EDA

Таблица, shape/dtypes, missingness, mean/median/std/quantiles, histograms, scatter, box/violin, class counts, correlation heatmap, pairwise plots (для ограниченного числа features), covariance, preview transformations. Для многомерных данных — выбор осей, 2D/3D projections с явной подписью, что это проекция.

## 17. Feature Engineering и preprocessing

Standardization, Min-Max scaling, robust scaling, normalization, imputation, one-hot/ordinal encoding, polynomial features, interaction terms, log transformations, binning, feature selection, variance threshold, categorical handling, class weights, sampling, augmentation (где применимо). Показывай «до/после», формулу трансформации, параметры, влияние на scale loss surface и градиенты. Обязателен корректный train-only fit и transform validation/test для защиты от leakage.

---

# ЧАСТЬ V. ЛИНЕЙНАЯ РЕГРЕССИЯ, LOSS И РЕГУЛЯРИЗАЦИЯ — P0

## 18. Linear Regression Master Lab: ручная модель

В режиме `ŷ=wx+b` пользователь генерирует `y=ax+c+noise`, двигает `w,b`, видит реагирующую прямую, вертикальные residuals, таблицу `x,y,ŷ,residual,squared_error`, подсветку отдельного примера, `data loss`, `penalty`, `total objective`, gradient, norm gradient, `R²`, train/validation metrics. Поддержать multi-feature regression `ŷ=Xw+b` с срезами весов и 2D/3D проекциями.

Возможности: ручная инициализация, известные истинные параметры, выбор noise law, выбросы, коррелированные признаки, интерактивные точки, CSV, polynomial features для исследования bias/variance, closed-form least squares, pseudoinverse и сравнение с gradient descent.

## 19. Loss Function Explorer

Реальные функции потерь: SSE, MSE, RMSE, MAE, Huber (настраиваемое `δ`), Log-Cosh, Quantile/Pinball (настраиваемый `τ`), Weighted MSE, Smooth L1, Poisson deviance/NLL при корректных предпосылках, Logistic BCE, Cross-Entropy, Hinge, Focal Loss для соответствующих моделей; расширения loss registry.

Для каждой: строгая формула с явно заданной нормировкой, график `L(residual)` или нужных аргументов, градиент/субградиент, порог недифференцируемости, чувствительность к outliers, вклад отдельного объекта, совместимые задачи/модели, ограничения. Пользователь накладывает разные кривые и сравнивает на одних данных; объясни отличие значения loss от направления градиента.

## 20. Regularization & Constraints Explorer

No penalty, L1, L2, Elastic Net, L0-penalty как отдельный дискретный случай, group lasso в расширении, constraints и их геометрия, proximal steps. Параметры: `λ`, L1 ratio, включение/исключение bias, per-parameter penalties. На отдельных карточках: `Data Loss`, `Penalty`, `Total Objective`; линии коэффициентов `w(λ)`, regularization path, sparsity count и validation performance. Визуализируй, почему L1 часто делает веса нулевыми, а L2 сжимает.

**Математический контракт P0:** `MSE = (1/n) Σ(ŷ_i−y_i)²`; `L2 penalty = λΣw_j²`; `∇_w MSE = (2/n)Xᵀ(Xw+b−y)`; `∇_w L2 = 2λw`; `∂L/∂b=(2/n)Σ(ŷ_i−y_i)`, если bias не регуляризован. Для L1 использовать обоснованный субградиент или proximal update; в нуле явно оговорить недифференцируемость. Всегда сохранять единые соглашения между формулой, ядром, UI и тестами.

## 21. 2D/3D Loss Surface — главное зрелище P0

Для `ŷ=wx+b`: X=`w`, Y=`b`, Z=`L(w,b)`; интерактивная настоящая поверхность текущего датасета с вращением камеры, pan/zoom, contour lines, marker current weights, gradient vector, actual update arrow, траекторией шагов, точкой аналитического минимума там, где он корректно доступен, и подписью, если минимум только численный. Вторая синхронная вкладка — 2D contour. Остальные панели: scatter+line+residuals, loss vs step, `w(t),b(t)`, optimizer state.

Изменение данных/loss/regularization пересчитывает поверхность, изменение текущих параметров — только маркер и соответствующие динамические элементы. На больших числах поверхность кэшируется, adaptive resolution/LOD, UI не блокируется.

Для 3+ весов: осмысленный двухпараметрический срез (выбор пары + фиксация остальных), low-dimensional projection с явной меткой, PCA projection только как проекция, не выдавать за истинный весь ландшафт. Возможен 1D профиль вдоль выбранного направления.

## 22. Полиномиальная и множественная регрессия

Polynomial features, multivariate linear regression, ridge, lasso, elastic net, weighted regression, robust loss comparison; нормализация, корреляция, мультиколлинеарность, сингулярность, train vs validation, bias/variance, conditioning, coefficient path. У пользователя выбор степени полинома, расположения тренировочных точек, шумности; на графике — fitted curve, residual distribution, train/validation gap.


# ЧАСТЬ VI. ОПТИМИЗАТОРЫ — P0/P1

## 23. Optimization Lab: общий движок

**Обязательные P0:** Batch GD, SGD, Mini-batch SGD, Momentum, Nesterov, AdaGrad, RMSProp, Adam, AdamW. **P1:** AdaDelta, AMSGrad, NAdam, Adamax, RAdam, Lion, L-BFGS, BFGS, Newton, coordinate descent, projected/proximal gradient, conjugate gradient, line search, другие полезные алгоритмы по собственной инициативе.

Разделяй **режим оценки градиента** (`full batch`, `one sample`, `mini-batch`) и **правило обновления** (plain SGD, momentum, Adam и т. д.). Это не взаимозаменяемые концепции. Не предлагай несовместимые комбинации. Оптимизатор должен принимать arbitrary-shaped parameter arrays, иметь сериализуемое внутреннее состояние и события для пошагового инспектора.

На каждом step визуализировать: выбранные indices, predictions, per-sample losses, batch loss, gradient per component, gradient norm, gradient clipping (если есть), old optimizer state, next optimizer state, actual parameter delta, old/new parameters, objective before/after. Уметь сравнить код математической формулы с числами.

## 24. Optimizers — подробные процессы

**GD:** `θ_{t+1}=θ_t−η∇L(θ_t)`; стрелка градиента и фактического обновления, скалярные вычисления.

**SGD:** подсвечивать отдельный выбранный объект; mini-batch — подсвечивать все выбранные объекты; динамический шум, порядок shuffle, epoch vs iteration. Включить optional estimate gradient variance.

**Momentum:** vector velocity, previous/new velocity, accumulated direction, overshoot, oscillation; точно фиксировать выбранную форму формулы.

**Nesterov:** look-ahead position, где вычисляется градиент, почему шаг отличается от обычного Momentum; не смешивать конвенции.

**AdaGrad:** накопленные квадраты градиентов, эффект снижения effective LR по каждой компоненте.

**RMSProp:** EMA squared gradient, denominator, adaptive scaling, optional centered variant.

**Adam:** first/second moments `m,v`, bias correction `m_hat,v_hat`, `ε`, step, effective component-wise scaling, warm-up effects.

**AdamW:** decoupled parameter decay отдельно от adaptive gradient step; объяснять разницу с L2 в Adam, отображать фактическое параметрическое изменение и не заявлять, что это шаг чистого градиента показанного regularized objective.

**Newton/BFGS/L-BFGS:** gradient + Hessian/approximation, curvature and quadratic model; stability, line search, positive-definiteness and numerical caveats.

## 25. Hyperparameter Control Panel

Настраиваемые по применимости: `learning_rate`, `momentum`, `dampening`, `nesterov`, `beta1`, `beta2`, `alpha`, `rho`, `epsilon`, `weight_decay`, `batch_size`, `shuffle`, `seed`, `gradient_clip_norm`, `gradient_clip_value`, `initial_w/b`, `max_steps`, `max_epochs`, `tol_grad`, `tol_loss`, `early_stopping_patience`, `epsilon_policy`, `mixed_precision` (только для поддерживаемого DL), step budget. Логарифмический слайдер LR и λ. Не использовать единый набор фиктивных параметров для всех оптимизаторов.

## 26. Schedulers и динамика LR

Constant, StepLR, exponential, inverse-time, polynomial decay, cosine annealing, warm restarts, warmup, warmup+cosine, OneCycle, ReduceOnPlateau, cyclic triangular. График `LR(step)`; маркировка событий scheduler; scheduler state; корректная семантика «после optimizer step», «после epoch», «по validation metric». Возможность наложить LR curve на loss curve на отдельной оси без вводящей в заблуждение шкалы.

## 27. Optimizer Arena — сравнения

Одновременно 2–8 оптимизаторов на одной функции, одинаковые dataset/initialization/seed и явное описание различий. На поверхности разными цветами отображать trajectories, markers, градиенты и события divergence; таблица: best/final objective, data loss, steps, epochs, gradient evaluations, elapsed CPU time, stability, convergence criterion, gradient norm, memory cost (где можно посчитать), randomness. Сравнения по step/epoch/wall-clock/gradient-evaluations должны переключаться, потому что они неэквивалентны.

Разные функции для benchmarking: sphere, anisotropic quadratic, Rosenbrock, saddle, Rastrigin, high-noise, poorly scaled features, ill-conditioned loss, sparse gradients, vanishing gradient region. Несколько seeds + mean/variance/quantile bands для стохастических методов. Не объявлять алгоритм «лучшим» глобально.

## 28. Оптимизационные диагностические эксперименты

Пресеты: слишком большой LR и расходимость; слишком маленький LR; узкая долина и zigzag; momentum overshoot; Nesterov look-ahead; Adam vs AdamW; clipping; batch size 1 vs full batch; эффект корреляции признаков; feature scaling; flat plateau; saddle point; локальные минимумы; noise; weight decay on/off; exploding/vanishing gradients; numerical overflow; gradient accumulation. Для каждого — автоматизированный запускаемый сценарий, описание и измеримые результаты.

## 29. Методы выбора гиперпараметров

Grid search, random search, simple Bayesian/TPE integration как необязательный этап, manual slider sweeps, sensitivity plot, parallel coordinates, heatmap metric over `(LR,λ)` и validation curves. Для каждого эксперимента сохранять seed, train/validation split, compute budget, objective, признаки достоверности сравнения. Дать пользователю увидеть проблему «слишком много вариантов и переобучение на validation».

---

# ЧАСТЬ VII. SUPERVISED LEARNING: CLASSIFICATION, TREES, ENSEMBLES

## 30. Classification Lab: Logistic Regression

Визуализировать `z=wᵀx+b`, sigmoid, predicted probability, BCE, decision boundary, probability heatmap, class threshold, gradient/backward и update. Пользователь меняет weights, bias, LR, optimizer, λ, batch size, class weights, dataset, imbalance, threshold. Связанные панели: точки классов, decision boundary, cross-entropy surface/contours для малых размерностей, loss curve, confusion matrix, ROC, PR.

Точно объяснить: threshold меняет **решение** и метрики с порогом, но не саму предсказанную вероятность, если веса и калибровка не изменились. Stable sigmoid/BCE with logits, иначе экстремальные значения могут ломать вычисления.

## 31. Multiclass и дополнительные линейные классификаторы

Softmax Regression, one-vs-rest, multinomial cross-entropy, one-hot, class weights, logits, probability simplex, decision regions, perceptron, linear SVM, hinge loss, multiclass margins. Покажи softmax normalization и производные, внутренние вычисления decision function, отличие logits/probabilities/thresholds.

## 32. SVM и kernel methods

Linear SVM + support vectors, margin, slack variables, effect of `C`, separable vs overlapping data. RBF/polynomial/sigmoid kernels (там, где применимо), `gamma`, `degree`, decision regions and support vectors. Визуально объясни kernel trick на маленьких примерах; не утверждай, что высокоразмерный feature space изображён буквально. Показывай влияние `C` и `gamma` на overfitting.

## 33. kNN и Naive Bayes

kNN classification/regression: выбор k, Minkowski/Euclidean/Manhattan distance, weights, highlighted neighbors, decision boundary, curse of dimensionality. Naive Bayes: Gaussian/Multinomial/Bernoulli в подходящих задачах, class priors, conditional likelihoods, log-probabilities, independence assumption; наглядно показывать вклад признаков.

## 34. Decision Tree Lab — точное построение дерева

Визуальные элементы: scatter, текущее дерево с узлами, split candidates table, impurity bar chart, decision partitions, путь одного объекта от корня к листу. Пошагово: выбрать node → перебрать feature/threshold → рассчитать impurity (Gini, entropy, log loss where supported; для регрессии variance/MSE, MAE с корректным определением) → gain → split → новые узлы.

Параметры: `max_depth`, `min_samples_split`, `min_samples_leaf`, `max_leaf_nodes`, `max_features`, `criterion`, `splitter`, `random_state`, `ccp_alpha`/pruning. Показать handling of pure/empty nodes, categorical vs numeric constraints, tie-breaking. Управление глубиной и визуализация underfit/overfit, pruning path и изменение validation error.

## 35. Ensembles: Bagging / Random Forest / Extra Trees

Показать bootstrap samples, индивидуальные деревья, random feature selection, отдельные и агрегированные predictions (mean/vote), variance reduction, out-of-bag samples/score при корректных условиях. Параметры trees count, depth, feature subsampling, min leaf, bootstrapping, seeds. Для decision boundaries — переключение индивидуального дерева и ансамбля.

## 36. Boosting: AdaBoost и Gradient Boosting

AdaBoost: weak learners, sample weights, error rate, learner weights, weighted voting с пошаговыми состояниями; разделять классификационные и регрессионные варианты.

Gradient Boosting: initial prediction, gradients/pseudo-residuals для текущего loss, новая shallow tree, learning rate shrinkage, updated ensemble, train/validation loss. Визуализировать вклад каждого дерева, residuals/negative gradients, effect of number of estimators/depth. HistGradientBoosting при возможности. Внешние XGBoost/LightGBM/CatBoost — опциональные проверенные интеграции, не обязательны для установки ядра.

## 37. Ranking и learning to rank (расширение)

Pairwise/listwise intuition, ranking metrics NDCG/MAP/MRR, score vs ordering, simple pairwise ranking examples и наглядные последствия изменения весов. Не выдавать кастомные игрушечные примеры за промышленные ranking pipelines.

---

# ЧАСТЬ VIII. UNSUPERVISED LEARNING

## 38. Clustering: K-Means / K-Means++

Пользователь выставляет `k`, init, seed, max_iter, tolerance; центроиды можно двигать мышью. Step: initialize → assign each point → recompute centroids → measure inertia → repeat. Цвет точек меняется вместе с assignment; рисовать стрелки centroid movement, nearest-centroid regions, inertia curve, empty-cluster handling. Пресеты: плохая инициализация, неравные плотности/дисперсии, вытянутые кластеры, выбросы.

## 39. Clustering: DBSCAN / Hierarchical / GMM

DBSCAN: `eps` radius around selected point, `min_samples`, core/border/noise, cluster expansion; график зависимости числа кластеров от параметра. Hierarchical: linkage distances, dendrogram, agglomerative split/merge history, cut height. Gaussian Mixture: mean/covariance ellipses, per-component density, responsibilities, E-step/M-step, log-likelihood, numerical stability, covariance regularization and singularity warnings. Дополнительно HDBSCAN/Mean Shift/Spectral Clustering как расширения.

## 40. Dimensionality Reduction: PCA / SVD

Для PCA на 2D/3D данных: mean centering, covariance, eigenvectors, explained variance, projection onto chosen axis, reconstruction, reconstruction error; интерактивный поворот оси и значение variance. Singular values, scree plot, cumulative explained variance, effect of scaling and outliers; выбрать `n_components` и отобразить reconstructed data. SVD отдельно объяснить на матричных примерах.

## 41. Manifold Learning и нелинейные проекции

Kernel PCA, t-SNE, UMAP (если установлен), Isomap, LLE, LDA при соответствующих предпосылках. Настройки perplexity, neighbors, learning rate, distance metric и seed. Показывать оригинальное high-dimensional пространство только через честные выбранные проекции/проекции расстояний. Обязательно предупреждать: визуальная близость и разделение на проекции не обязательно отражают исходную глобальную геометрию.

## 42. Anomaly Detection и density estimation

Z-score/IQR, Isolation Forest, Local Outlier Factor, One-Class SVM, Gaussian density, KDE, reconstruction error у autoencoder. Выбор threshold и visual anomaly scores, precision/recall при наличии размеченных данных. Строить decision/score surfaces для маленьких размерностей; показывать зависимость от density и contamination settings.

---

# ЧАСТЬ IX. NEURAL NETWORKS / DEEP LEARNING

## 43. Single Neuron — от суммы до активации

Граф узла: `x₁,x₂,… → wᵢxᵢ → Σ + b → activation → output`. Клик по ребру показывает weight и произведение; клик по узлу — входное значение, bias, z, a, derivative. Ручные sliders `xᵢ,wᵢ,b`, выбор activation, loss и target. Векторизованная и разложенная поэлементная запись. Один supervised training step от предсказания до weight update.

## 44. Activation Function Explorer

Identity/Linear, sigmoid, tanh, ReLU, Leaky ReLU, PReLU, ELU, SELU, GELU, SiLU/Swish, Softplus, Softsign, Softmax (векторная). График, производная, вычисления в выбранной точке, saturated regions, zero gradient, why activation helps nonlinearity. Для Softmax объяснить, что это векторное преобразование с Jacobian, а не независимая скалярная функция.

## 45. Visual MLP Builder

Пользователь собирает `Input(2) → Dense(4) → ReLU → Dense(4) → ReLU → Dense(1) → Sigmoid`, меняет слои, нейроны, activation, bias, initialization, optimizer, LR, batch size, loss, regularizer, dropout/norm (где допустимо). Схема узлов и рёбер показывает веса (толщина/цвет), активации, shapes; для больших слоёв — агрегированный вид. График decision boundary меняется при обучении 2D-датасетов. Рабочие задачи: XOR, moons, circles, spirals, regression with sine/noise.

## 46. Forward Pass — покомпонентный процесс

Step debugger: вход `X`, веса `W`, матричное умножение, `+b`, activation, next layer, logits/probabilities, target, loss. Для маленького MLP численно показывать каждую матрицу/вектор. Отдельная вкладка с tensor-shape trace и таблицей intermediate activations. В мультитасковом режиме не смешивать classification/regression objectives.

## 47. Backpropagation и вычислительный граф

Визуальный computation graph с числовыми forward и local gradients; обратная цепочка `dL/da · da/dz · dz/dw`; градиенты по всем `W,b`, accumulation, Jacobian-vector products на концептуальном уровне. Пользователь выбирает параметр и отслеживает его gradient lineage. Сравнение manual analytic derivation, finite differences, PyTorch autograd для маленьких моделей. Gradient checking проходит с оговоркой об областях недифференцируемости.

## 48. Weight Initialization / gradient pathologies

Zeros, random normal/uniform, Xavier/Glorot, He/Kaiming, orthogonal (подходящие случаи); графики distributions weights/activations/gradients per layer. Демонстрации symmetry breaking, exploding and vanishing gradients, depth sensitivity, saturation, effect of normalization, clipping and residuals.

## 49. Regularization, Norm layers, Dropout

L1, L2, weight decay, early stopping, label smoothing where applicable, dropout, batch normalization, layer normalization, group normalization (расширение), residual connections. Режим train/eval — отдельная явная настройка; показать dropout masks и почему stochastic behavior не одинаков в train/eval. BatchNorm state (running mean/variance), LayerNorm axes, incorrect small-batch scenarios.

## 50. Training Dynamics and Network Diagnostics

Train/validation loss, accuracy/regression metrics, epoch/step counters, gradient norms, parameter histograms, update-to-weight ratio, activation histograms, dead neurons, overfitting curves, LR schedule, speed, RAM. Конфиг experiments, early stopping, checkpoints, reproducibility. Для тяжелых задач разумное снижение частоты обновления GUI.

## 51. Convolutional Neural Networks Lab

Image tensor `H×W×C`, grayscale/RGB, channel selection, 2D kernel matrix editable, stride, padding, dilation, receptive field, separable convolution (по желанию), pooling (max/avg), feature maps, flatten, dense. Пошагово подсвечивать input patch, element-wise multiply, sum and output position; trace shapes and parameters count. Presets: blur, sharpen, Sobel X/Y, edge detector, emboss; интерактивное изображение и real kernel response. Мини-CNN на маленьком локальном датасете, training loss, feature maps; не требовать больших pretrained checkpoints.

## 52. Sequence Models: RNN, LSTM, GRU

Упорядоченные token/time steps, unfold through time, hidden state, recurrent weights, vanishing gradients through time, truncation BPTT; LSTM forget/input/output gates and cell state; GRU reset/update gates. Реалистичные маленькие численные демонстрации и сравнительный toy training. Честно обозначать limits of visualization.

## 53. Transformer fundamentals (см. также NLP)

Token embeddings, positional encoding/embeddings, residual connections, pre/post LayerNorm, feed-forward, self-attention, multi-head, causal mask, encoder vs decoder, tensor dimensions and parameter shapes. Всё на маленьких числах и коротких последовательностях, с отдельными инспекторами по операциям.

## 54. Generative models (после базового DL)

Autoencoder, denoising autoencoder, VAE: encoder, latent space, decoder, reconstruction, KL regularizer, sampling, interpolation. GAN: generator/discriminator, adversarial objectives, simple 2D toy density with stepwise updates. Diffusion: forward noising schedule, reverse denoising, beta/alpha parameters, score/noise predictions, simple 1D/2D demos. Не требовать сотен гигабайт или удалённых моделей. Учебная честность: что реально обучено, что игрушечное, что предобученное.

---

# ЧАСТЬ X. NLP, ATTENTION, TRANSFORMERS И LLM

## 55. Text Preprocessing Lab

Ввод любого локального русского/английского текста и собственных мини-корпусов. Sentence splitting, word/character segmentation, Unicode normalization, lowercase, punctuation, stop words, stemming, lemmatization с локально доступными ресурсами; каждое преобразование визуально выделяет, что изменилось, и почему. Частоты, словарь, Zipf-style plot (с оговоркой), n-grams, co-occurrences. Сохранение обработанного корпуса.

## 56. Tokenization Lab

Character, word, whitespace, subword, BPE, WordPiece/Unigram при адекватной реализации; для BPE ручной merge: frequency pairs → merge candidate → changed vocab → encoded tokens → token IDs. Сравнение длин последовательностей для разных токенизаторов. Не приписывать реальному LLM tokenizer игрушечной реализации.

## 57. BoW, TF-IDF, similarity

Несколько документов → vocabulary → count matrix → term/document frequency → IDF (с явно заданным smooth) → TF-IDF → normalized vectors → cosine similarity / nearest documents. Пользователь меняет один текст и видит обновление всех матриц и heatmaps. Встроенные классификаторы текста (Naive Bayes/logistic regression) как связанный эксперимент.

## 58. Word Embeddings and distributional representations

One-hot, trainable embeddings, CBOW, Skip-gram, negative sampling на маленьком корпусе, cosine similarity, nearest neighbors, embedding arithmetic с оговорками, PCA/t-SNE/UMAP projection, semantic clustering with controlled data. Подробно отображать embedding lookup и update selected row. Никогда не выдавать случайные векторы за семантически обученные.

## 59. Attention — визуализировать каждый множитель

Для короткой последовательности на экране отдельно: input embeddings `X`, learned/provided `W_Q,W_K,W_V`, `Q=XW_Q`, `K=XW_K`, `V=XW_V`, `QKᵀ`, scaled scores `/sqrt(d_k)`, mask, stable row-wise softmax, `A·V`, output. Attention heatmap with token-token tooltips, per-head heatmaps, causal mask visualization. Клик по одной ячейке раскрывает весь численный расчёт.

Поддержать arbitrary toy Q/K/V (в разумных размерах), изменение temperature в отдельном обозначенном эксперименте, effect of scaling, masking (−∞ conceptual with numerically safe implementation), softmax saturation, dimensions and transpose. Матрицы и графики должны быть одной реальной цепью вычисления.

## 60. Multi-Head Attention & Transformer Inspector

Несколько attention heads с независимыми `Q_i,K_i,V_i`, concatenate, output projection, residual, norm, MLP block; encoder-only vs decoder-only, cross-attention, positional encodings (sinusoidal/learned/rotary conceptual extension). Отдельно показать архитектурный граф, shapes, per-token vectors, per-head matrices и memory footprint для заданных размеров. По шагам смотреть, как изменилось представление выбранного токена.

## 61. Text Generation and Decoding

Локальная toy language model или маленькая проверенная модель: logits → probabilities → next-token selection. Greedy, sampling temperature, top-k, top-p/nucleus, repetition penalty (если доступно), stop tokens, seed, context window. На bar chart — вероятность токенов до и после фильтра; показывать normalization, entropy и stochasticity. Объяснить difference between logits, calibrated probabilities and sampling temperature. По желанию min-p и beam search в отдельном учебном режиме.

## 62. Modern NLP/LLM Extensions

Masked LM vs causal LM; embeddings search, semantic similarity, approximate nearest neighbors (простые игрушечные примеры), Retrieval-Augmented Generation (векторное индексирование мини-корпуса, chunking, retrieval scores, top-k, answer provenance), vector database concepts, context window, KV-cache (toy visualization), transformer inference vs training, positional limitations, token budget, quantization effects (там, где реализовано корректно), preference training/RLHF/DPO **на концептуальных небольших примерах**. Инструменты без обязательного интернета и удалённого API.

## 63. NLP Evaluation и честность результатов

Tokenization metrics (vocab size/compression), text classification precision/recall/F1, language-model cross-entropy and perplexity, retrieval recall@k/MRR/nDCG on controlled datasets. Для свободного текста не выдавать субъективную «оценку качества» за объективно установленную метрику. Данные, prompts и generation seeds сохранять.


# ЧАСТЬ XI. РАСШИРЕННЫЕ НАПРАВЛЕНИЯ ML

## 64. Time Series Lab

Генераторы: тренд, сезонность, шум, пропуски, выбросы, regime shift. Графики временных рядов, rolling statistics, lag plot, ACF/PACF, seasonal decomposition (при корректных допущениях), Fourier components, train/validation chronological split. Модели: naive, seasonal naive, moving average, exponential smoothing, autoregression, ARIMA/SARIMA при наличии зависимостей, lagged-feature linear regression, простые RNN/Transformer forecasting models. Ошибки MAE/MSE/RMSE/MASE/sMAPE с пояснением edge cases; backtesting и rolling-origin evaluation. Отображай prediction horizon и доверительные/прогнозные интервалы только там, где они обоснованы.

## 65. Reinforcement Learning Lab

Начальный интерактивный мир: Multi-Armed Bandit и Gridworld. Показывать состояния, действия, награды, переходы, траекторию агента, эпизоды, cumulative reward/regret, value function, Q-table, policy heatmap. Алгоритмы: epsilon-greedy/UCB/Thompson Sampling для bandits, value iteration, policy iteration, Monte Carlo, Q-Learning, SARSA, Expected SARSA, simple tabular TD, policy-gradient REINFORCE на игрушечном окружении. Настройки: gamma, epsilon, epsilon decay, alpha, reward map, obstacles, transition stochasticity, episode limit, seed. Пошагово показывать Bellman update, exploration vs exploitation и обучение Q-values. Не обещать промышленные RL-тренировки в MVP.

## 66. Probabilistic and Bayesian ML

Bayes theorem visualizer, likelihood vs posterior, conjugate prior examples (Beta-Bernoulli, Normal with suitable assumptions), MLE/MAP and regularization connections, Bayesian linear regression, posterior predictive distribution, uncertainty, calibration, simple Gaussian Processes with kernels and confidence bands, Monte Carlo estimation, Markov Chain Monte Carlo intuition (basic Metropolis-Hastings toy). Отображай sampling uncertainty и модельные предположения, избегай ложной точности.

## 67. Recommender Systems

User–item interaction matrix; popularity, nearest-neighbor collaborative filtering, content-based ranking, matrix factorization, implicit feedback toy case; параметры latent dimension, regularization, optimizer; диаграмма predicted preferences, cold-start, sparsity, evaluation top-k, RMSE in explicit feedback where appropriate. Ручное изменение пользовательских предпочтений с мгновенным обновлением ранжирования.

## 68. Graph Machine Learning

Редактор небольшого графа: nodes/edges/features, adjacency matrix, degree, graph Laplacian, shortest paths, message passing, simple Graph Convolution Network (GCN), GraphSAGE conceptual demo, attention-based graph aggregation toy. Визуально подсвечивать соседей, отправляемые сообщения, aggregation и resulting node features. Проекции embeddings обозначать явно.

## 69. Causal Inference Fundamentals

Корреляция vs причинность, confounding, collider, mediation, selection bias, directed acyclic graphs (DAG), observational vs intervention, Simpson's paradox, treatment/control distributions, propensity score intuition, ATE with assumptions, basic backdoor adjustment toy examples. Не представлять причинные выводы как доказанные без предпосылок и дизайн-ограничений. Редактор маленького причинного графа и генератор демонстрационных сценариев.

## 70. Explainable ML and Interpretability

Linear coefficient contributions (with units and scaling), tree path explanations, decision boundaries, permutation importance, partial dependence / ICE, integrated gradients for tiny differentiable models (если реализовано), gradient attribution, occlusion for images, SHAP as optional integration. Разделяй explanation model behavior vs causal effect. Для каждой визуализации укажи ограничения, нестабильность при коррелированных признаках и возможную чувствительность к фону/выборке.

## 71. Robustness, fairness, privacy and distribution shift

Educational experiments: concept drift, covariate shift, label shift, adversarial perturbation on toy datasets (non-harmful), outliers, missing data, class imbalance, noisy labels, demographic fairness metrics on synthetic non-sensitive groups, tradeoffs and limitations, model inversion risk as conceptual topic, privacy of local datasets, differential privacy basics on safe toy aggregates. Не создавать впечатление, что одна метрика fairness гарантирует справедливость системы. Показывать uncertainty and limitations.

## 72. AutoML и hyperparameter search (расширение)

Manual/grid/random search, trial explorer, simple learning-curve-based early stopping, sequential search, trial budget and reproducibility; сравнение training time, validation score, parameter sensitivity. Avoid test-set tuning leakage. Optional Bayesian optimization or Optuna integration, если полезно и совместимо с установкой.

## 73. Scientific computing / numerical optimization advanced

Constrained optimization, Lagrange multipliers, KKT intuition, primal-dual simple plots, coordinate descent, proximal algorithms, convex/nonconvex objectives, condition number, Hessian spectra, line search, gradient checking, automatic differentiation vs numerical differentiation, stochastic noise models, mixed precision numerics. Подключать как учебные дополнения к оптимизаторной лаборатории.

---

# ЧАСТЬ XII. МЕТРИКИ, ВАЛИДАЦИЯ, ЭКСПЕРИМЕНТЫ

## 74. Regression Metrics Lab

MSE, RMSE, MAE, MedAE, R², adjusted R² with assumptions, MAPE/sMAPE with zero-value warnings, quantile/pinball loss, explained variance, residual histograms, QQ plot where useful, error vs fitted, heteroscedasticity patterns. Для каждого метрика/формула/параметры/реальные значения/ограничения. При константной target или нулевом знаменателе показывать корректную диагностику.

## 75. Classification Metrics Lab

Confusion Matrix (binary/multiclass), accuracy, balanced accuracy, precision, recall, specificity, F1/Fβ, MCC, Cohen's kappa (по необходимости), ROC/ROC-AUC, PR/average precision, log loss, Brier score, calibration plot, ECE as optional with binning caveats. Threshold slider вызывает честный пересчёт threshold-dependent metrics; probability curve и score distributions. Показывай micro/macro/weighted averaging и class imbalance. Явные warnings when metrics undefined.

## 76. Validation & Generalization Lab

Train/validation/test splits, K-Fold, Stratified K-Fold, Group K-Fold, time-series split, nested CV concept, learning curves, validation curves, confidence bands with justified estimators, bootstrap evaluation, data size vs bias/variance, early stopping. Показывай train/validation differences and variance over seeds; гиперпараметры выбираются без подглядывания в test.

## 77. Data Leakage Simulator

Пресеты «scaling до split», feature selection по всей выборке, target leakage, duplicates across split, chronological leakage, group leakage, validation overfitting. Пользователь переключает правильный и неправильный pipeline и видит реальные (не выдуманные) различия метрик. Объяснить, почему утечка может дать ложную уверенность.

## 78. Experiment Comparison Studio

Пользователь создаёт run A/B/C... и сравнивает side-by-side; конфигурации, dataset version, fixed splits/seeds, параметрические траектории, metric curves, gradient norms, parameter distributions, snapshots, timings, compute budgets. Overlay graphs, compare-by-step/epoch/time/gradient-evals, select/deselect runs, history and notes. Система предупреждает, если результаты несопоставимы (разные splits, functions, penalty, compute budget). Многократные seeds и error bands для stochastic runs.

## 79. Hyperparameter Surface & Sensitivity

Реальная grid по LR×λ, depth×min_leaf, k×noise, beta1×beta2 при разумных ограничениях; heatmap validation metric / convergence steps / stability; sensitivity, parallel coordinates, tradeoff scatter. Можно запустить trial из конкретной ячейки карты. Предупреждать, что heatmap — результаты выбранных запусков, не теоретическая полная поверхность.

## 80. Experiment Pipeline / Visual Builder

Редактор `Dataset → Split → Preprocess → Features → Model → Loss → Regularization → Optimizer → Scheduler → Metrics → Visualizations`. Каждый блок с параметрами, портами данных, schema validation, tooltip и статусом. Если модель не дифференцируема, не предлагать к ней обычный Adam без специальной differentiable formulation. Pipeline может экспортироваться в описывающий JSON и наглядный reproducible Python snippet. Плагинная совместимость по capabilities, а не произвольные сочетания.

---

# ЧАСТЬ XIII. ОБУЧЕНИЕ, УПРАЖНЕНИЯ И ОБЪЯСНЕНИЯ

## 81. Interactive Lessons

У каждого урока: тема, предпосылки, уровень (интуиция/формулы/числа/код), образовательная цель, работающий интерактивный demo, управляемый эксперимент, вопросы на понимание, решение с проверкой. Минимум 25 уроков в дорожной карте: линейная комбинация, dot product, производная, gradient, least squares, MSE, residuals, learning rate, GD, SGD, momentum, RMSProp, Adam, AdamW, regularization L1/L2, bias/variance, logistic regression, thresholds, tree splits, KMeans, PCA, single neuron, backprop, convolution, tokenization, attention, decoding. Сначала реализовать не менее 6 законченных уроков, использующих ядро P0.

## 82. Challenge Mode

Автоматически проверяемые задания: подобрать `w,b` для MSE threshold, добиться сходимости, избежать divergence при ограниченном числе шагов, сравнить методы при одинаковом budget, добиться sparsity, выявить leakage, подобрать tree depth, построить XOR network, восстановить матрицу внимания, скорректировать sampling. Проверка по вычислениям и условиям, а не фиксированному ответу. Подсказки, уровень сложности, прогресс локально, optional «покажи ход решения».

## 83. Learn-by-Debugging / What-if Engine

При hover на любом текущем числе кнопка «Почему?» раскрывает трассировку происхождения; «Что если увеличить?» показывает локальную чувствительность без утверждения глобальной причинности, где это не обосновано. Контрольные вопросы: «Почему SGD шумит?», «Почему Adam меняет скорость по осям?», «Почему нейрон без activation недостаточен для XOR?», «Почему изменился threshold, но не probability?». Состояние графиков не теряется при открытии объяснения.

## 84. Glossary, Knowledge Map, Roadmap

Поиск по русским/английским терминам, математические обозначения, короткие определения, формулы, перекрёстные ссылки «где это используется», prereq graph, персональный локальный прогресс. Не требовать регистрации и облачного аккаунта. Система объясняет, какие темы логично пройти перед Transformer или RL.

## 85. Reference Calculations / Worked Examples

У каждого основного алгоритма минимум один маленький численный пример, где можно проверить руками: один шаг SGD, Adam bias correction, Gini split, softmax, BCE, backprop на двух нейронах, PCA на малой матрице, attention 2×2. Кнопки «показать промежуточные значения» и «скопировать решение».

---

# ЧАСТЬ XIV. РАСШИРЯЕМОСТЬ И СОХРАНЕНИЕ

## 86. Safe Custom Math Expression Builder

Выражения `f(x)`, `f(x,y)`, `L(w,b)`, ограниченные математические функции, optional named parameters, derivative via symbolic/autograd/finite differences. Whitelisted AST, лимиты размеров, проверка области определения и численных значений, отсутствие arbitrary code execution. График в 1D/2D/3D, градиентное поле, запуск выбранного optimizer, экспорт результата. Разрешить новые функций потерь при соблюдении differentiability/capability flags.

## 87. Plugin SDK и registry

Плагины для модели, loss, regularizer, optimizer, dataset, visualization, metric, lesson и challenge. Метаданные: id, version, name, category, requirements, parameter schema, math conventions, capabilities, UI components, serialization, test hooks. Использовать typed protocols / entry points или manifest-based discovery. У сторонних Python-плагинов предупреждение, что это доверенный исполняемый код; никакой фиктивной «песочницы» для arbitrary Python в основном процессе. Встроенные плагины тестировать автоматически. Пример плагина `custom_optimizer` с документацией и тестами.

## 88. Reproducible Simulation State

Для каждого run сериализовать: application/schema version, dataset generator seed + actual data, split indices, preprocessing fits, selected model, loss, regularization, optimizer config/state, scheduler state, current parameters, step/epoch/batch pointer, RNG state, snapshots, metrics, trajectory, visual camera/layout settings, warnings, user notes. Явная политика sampling order. Обратная навигация реализуется snapshots/replay. Ограничение памяти и компрессия без потери воспроизводимости там, где возможно.

## 89. File Format, Import/Export, Reports

Версионированный `.mluniverse` как ZIP с JSON-манифестом, числовыми массивами в безопасном формате (например, `.npy`/structured binary, без untrusted pickle), checksums и migrations. Import/export CSV/TSV, PNG/SVG graphs, JSON configs, trajectories, metrics, optional GIF/MP4, markdown/HTML reports with figures if реально реализовано. Экспорт run manifest, exact dependencies, seeds, math conventions. Сохранение/загрузка не меняют результаты и не ломают UI.

## 90. Offline Assets and Optional Data Packs

Все основные ресурсы, учебные датасеты, темы, формулы, JS-графики поставлять офлайн. Большие модели, изображения, корпуса и датасеты — опциональные локально устанавливаемые packs с checksum/version/license notice. Базовый пакет не должен зависеть от скачивания pretrained model. При отсутствии pack показывать информационное состояние и доступный toy alternative.


# ЧАСТЬ XV. ПРОИЗВОДИТЕЛЬНОСТЬ, НАДЁЖНОСТЬ, БЕЗОПАСНОСТЬ

## 91. Rendering Architecture and Performance

- Лёгкие 2D-графики обновлять быстро через optimized curves/scatter items; сложные 3D-поверхности — кэшировать.
- Разделить частоты: training engine может сделать десятки/тысячи steps между кадрами; отображение — throttled, configurable.
- Update `current marker/trajectory` без пересборки неизменившегося mesh.
- При больших `n` использовать LOD/downsampling только в визуализации, **не менять тихо обучающие данные**.
- История: checkpoints every N steps, windowed records, optional full history, memory budget and clear controls.
- Графики больших матриц attention — агрегирование/виртуализация с tooltip и явным ограничением detail.
- Производительность измерять: cold start, UI FPS при drag slider, initial graph render, training throughput, memory usage, plot update times.
- Настройки качества рендеринга и соответствующие сбалансированные defaults.

## 92. Task Execution, Cancellation and Thread Safety

Тяжёлые вычисления не выполняются в GUI thread. Worker processes/threads выбираются по нагрузке; Qt signal/slots для сообщений о состоянии; данные передаются безопасно, без гонок и неконтролируемого доступа к UI из worker. UI supports Pause/Cancel with bounded response time, progress indicators, consistent recovery after cancellation. При переключении вкладки незавершённое вычисление не должно продолжать неконтролируемо обновлять уже закрытые компоненты.

## 93. Numerical Robustness and Input Validation

NaN/Inf/overflow/underflow detection, unstable sigmoid/softmax protection, safe logs, division by zero, zero variance, singular matrices, empty classes, invalid class probabilities, out-of-range parameters, empty dataset, failed CSV parsing, incompatible model/loss, invalid dtype/device, clipping/scale issues. Пользователю — понятная ошибка с причиной, предложением исправления и возможностью увидеть технические детали. Нельзя молча подставлять случайные результаты.

## 94. Application Reliability

Перехват исключений, structured logs (без записи приватных датасетов по умолчанию), crash-safe persistence через atomic file writes, autosave configurations where reasonable, save-confirmation on exit, versioned settings and migrations, safe reset to defaults, telemetry OFF by default, без внешней отправки данных. UI не замерзает от неработающего плагина без контролируемого механизма отмены/изоляции; для произвольного стороннего кода обозначить ограничения.

## 95. Accessibility and Localization

Русский UI по умолчанию, английский как опциональная локализация; математические обозначения и термины с русскими определениями. Горячие клавиши, keyboard focus, tooltips, контрастные темы, цветовая палитра, различимая при цветовых особенностях восприятия, легенда и line style помимо цвета, масштабирование шрифта, текстовое отображение величин для графиков. Не полагаться только на цвет для обозначения класса/статуса.

## 96. Privacy, Security, Licensing

Основные расчёты локальные, сеть необязательна, прозрачность файловых операций; локальные датасеты не загружать на сервер по умолчанию. Без `eval` для пользовательской формулы; без небезопасной pickle-deserialization пользовательских файлов; проверка ZIP entries (zip-slip, размеры) при импорте; ограничение размера датасетов; безопасное сохранение. Лицензии Python dependencies, JS libraries, pretrained models, учебных датасетов и графических ресурсов должны быть совместимыми с распространением Windows-приложения, соблюдай требования к уведомлениям.

---

# ЧАСТЬ XVI. КАЧЕСТВО КОДА, ТЕСТЫ И НАУЧНАЯ ВЕРИФИКАЦИЯ

## 97. Test Suite — общий стандарт

Реализовать `pytest` suites:
- `unit/math`: norms, derivatives, matrix operations, loss definitions, regularizers;
- `unit/optimizers`: one-step reference, multiple steps, state serialization, bias correction;
- `unit/models`: linear/logistic regression, classification, trees, clustering, MLP forward/backward;
- `unit/nlp`: tokenization, TF-IDF, softmax attention, masks;
- `integration/simulation`: timeline, snapshots/replay, synchronized state, config changes;
- `integration/persistence`: round-trip, incompatible schema, corrupted/oversized files;
- `gui/smoke`: launch, section navigation, sliders, run/pause/step/reset, plot rendering;
- `packaging/smoke`: Windows exe starts, bundled Qt resources present, offline 2D/3D.

`Ruff`, type checking, resource checks and CI status. Не помечай тесты пройденными без запуска.

## 98. Reference Mathematics: exact P0 checks

- `X=[0,1,2]`, `y=[1,3,5]`, model `ŷ=2x+1` → predictions `[1,3,5]`, MSE=0, gradient=0.
- `X=[0,1]`, `y=[1,3]`, at `w=0,b=0`: residuals `[-1,-3]`, `MSE=(1+9)/2=5`; gradient w `= (2/2)(0·(-1)+1·(-3))=-3`; gradient b `=(2/2)(-1-3)=-4`. With `η=0.1`: `w_new=0.3`, `b_new=0.4`.
- For `L2=λw²`, derivative `2λw` (unless bias explicitly included); check exact difference.
- For L1 at `w=0`: distinguish subgradient set from finite derivative, test chosen proximal operator.
- For softmax attention: each unmasked row sums to 1 within tolerance; masked positions have zero probability; output dimensions match.
- For Adam and AdamW: verify one-step and multi-step against independent reference examples (with exact epsilon placement/convention), including bias correction and decoupled decay.
- For MLP: finite-difference gradients vs manual/autograd in smooth test points.
- For trees: calculate Gini/entropy on tiny hand-constructed labels, compare winning split with independent reference.
- For KMeans: fixed seed, assignments, centroids and inertia, handle empty cluster policy.
- For classification threshold: probabilities unchanged; confusion matrix changes.
- For deterministic runs: fixed seed→same trace within numerical tolerance; multiple seeds produce expected variation.

## 99. Scientific Integrity Rules

Везде обозначить:
- `data loss` vs `regularization penalty` vs `total objective`;
- `per-sample loss` vs `mean/sum reduction`;
- `gradient`, `subgradient`, `proximal step`, `decoupled weight decay`;
- `step`, `iteration`, `mini-batch`, `epoch`, `optimizer update`, `gradient evaluation`;
- exact point where scheduler changes LR;
- `true global minimizer` vs `found local stationary point` vs `approximate minimum`;
- `full parameter space` vs 2D slice/projection;
- stochastic run at one seed vs distribution across seeds;
- model uncertainty vs measurement uncertainty;
- theoretical curve vs empirical result;
- fitted learned embeddings vs random/toy embeddings.

Никогда не «подгоняй» графики под ожидаемую красоту. Если метод расходится — показывай расходимость; если численно неустойчив — корректно останавливай.

## 100. UI End-to-End Acceptance Tests

1. Запуск приложения без интернета и без установленного системного Python у конечного пользователя.
2. Linear Regression: slider веса меняет прямую, MSE и residuals; поле точного значения синхронно со slider.
3. Loss switch меняет отображаемое objective и его реальную поверхность.
4. 3D rotating/pan/zoom, contour и точки траектории соответствуют одному `w,b`.
5. `Step` изменяет модель математически корректно; `Back` возвращает прежнее полное состояние.
6. `Play→Pause→Reset` работает многократно без утечек потоков.
7. `Compare`: несколько оптимизаторов, одинаковые начальные условия, реальные траектории, корректный legend.
8. Save/Load `.mluniverse` с optimizer state и timeline сохраняет эксперимент.
9. Logistic regression probability heatmap и threshold slider меняют правильные величины.
10. Tree split inspector показывает реальный Gini/threshold.
11. One-neuron forward/backward совпадает с контрольными вычислениями.
12. BPE/TF-IDF/attention пересчитываются при изменении текста.
13. Keyboard input, responsive resizing, HiDPI, dark/light, long calculations cancellation.
14. Повреждённый файл и некорректная формула вызывают обработанную ошибку, а не падение.
15. Чистая Windows-сборка запускает главную форму, 2D и 3D рендереры без загрузки CDN.

---

# ЧАСТЬ XVII. WINDOWS BUILD И ДОКУМЕНТАЦИЯ

## 101. Windows `.exe` Packaging

Цель: Windows 10/11 x64. PyInstaller `onedir` сначала как надёжный baseline; затем `.exe` launcher и optional installer, optional `onefile` только после проверки, что размер/скорость/антивирусное поведение приемлемы. Включить Qt platforms/plugins, QtWebEngine binaries/resources, local plotly.js assets, icons, translations, fonts, lessons, datasets, NumPy/SciPy/PyTorch dependencies только по использованию. Не смешивать debug и release paths.

Скрипты: `scripts/bootstrap.ps1`, `scripts/run_dev.ps1`, `scripts/run_tests.ps1`, `scripts/build_windows.ps1`, `scripts/smoke_windows.ps1`; PyInstaller spec и `requirements.lock`/`uv.lock` or equivalent. GitHub Actions `windows-latest` сборка, тесты и artifact ZIP в случае отсутствия локальной Windows. **PyInstaller не кросс-компилирует Windows `.exe` из Linux**; на Linux можно подготовить проект и Windows workflow, но не объявлять неподтверждённый `.exe` проверенным.

## 102. Distribution and Update Strategy

Понятное имя файлов (`ML_Universe_vX.Y.Z_Windows_x64.zip`), version info, app icon, license notices, checksums, release notes, archive layout; optional installer via Inno Setup/WiX после MVP. Настройки и сохранения должны храниться в подходящей пользовательской директории и переживать обновление приложения. Не требовать прав администратора для базового запуска, если нет обоснованной причины.

## 103. Full Documentation

`README_RU.md` (установка, возможности, запуск, сборка, скриншоты только настоящие), `ARCHITECTURE.md`, `MODULES.md` (текущий статус), `MATH_CONVENTIONS.md`, `TESTING.md`, `WINDOWS_BUILD.md`, `PLUGIN_DEVELOPMENT.md`, `IMPROVEMENT_BACKLOG.md`, `CHANGELOG.md`, `KNOWN_LIMITATIONS.md`, `CONTRIBUTING.md`. Для каждого алгоритма документация: формула, параметры, исходные данные, ограничения, учебная интерпретация, ссылка на эталонную проверку при наличии.

## 104. Proposed Project Layout

```text
ml-universe/
├── app/
│   ├── main.py
│   ├── bootstrap.py
│   ├── core/
│   │   ├── math/
│   │   ├── distributions/
│   │   ├── datasets/
│   │   ├── preprocessing/
│   │   ├── losses/
│   │   ├── regularizers/
│   │   ├── optimizers/
│   │   ├── schedulers/
│   │   ├── models/
│   │   ├── neural/
│   │   ├── nlp/
│   │   ├── simulation/
│   │   ├── metrics/
│   │   └── protocols/
│   ├── experiments/
│   │   ├── definitions/
│   │   ├── presets/
│   │   ├── history/
│   │   └── persistence/
│   ├── visualization/
│   │   ├── charts_2d/
│   │   ├── charts_3d/
│   │   ├── surfaces/
│   │   ├── trees/
│   │   ├── neural_graphs/
│   │   ├── tensor_views/
│   │   └── attention/
│   ├── ui/
│   │   ├── windows/
│   │   ├── pages/
│   │   ├── panels/
│   │   ├── widgets/
│   │   ├── dialogs/
│   │   └── themes/
│   ├── education/
│   │   ├── lessons/
│   │   ├── challenges/
│   │   └── glossary/
│   ├── plugins/
│   ├── workers/
│   ├── assets/
│   └── utils/
├── tests/
│   ├── unit/
│   ├── integration/
│   ├── gui/
│   └── smoke/
├── examples/
├── docs/
├── scripts/
├── packaging/
├── .github/workflows/
├── pyproject.toml
├── README_RU.md
└── LICENSE
```

Схема — ориентир: модифицируй при необходимости, не делай пустых пакетов и абстракций только ради красивого дерева. Для каждой добавленной директории должна быть реальная ответственность.

---

# ЧАСТЬ XVIII. ПЛАН ПОСТАВКИ: РЕАЛИЗОВЫВАТЬ, А НЕ ОБЕЩАТЬ

## 105. Phase 0 — Working Foundation (обязательно закончить)

Действующий PySide6 GUI, sidebar, центральный рабочий layout, theme switch, parameter controls, simulation controls, 2D/3D plots prototype, application state, worker architecture, core packages, pytest, development startup. Definition of Done: одно окно действительно открывается, parameter slider меняет график, тесты начального движка проходят, сборочные скрипты существуют.

## 106. Phase 1 — Linear Regression Master Lab (ОСНОВНОЙ MVP)

Реализовать **полностью**, без заглушек:
1. Dataset generator + scatter + editable points + seed.
2. `ŷ=wx+b`, вручную управляемые `w,b`.
3. Residuals, per-point inspection and table.
4. MSE/MAE/Huber и расширенные loss с корректными gradients/subgradients.
5. No penalty/L1/L2/Elastic Net, отдельные data loss / penalty / total.
6. 2D contour + 3D true loss surface with live marker.
7. Batch GD, SGD, mini-batch, Momentum, Nesterov, AdaGrad, RMSProp, Adam, AdamW.
8. Step-by-step mathematics + optimizer state inspector.
9. Play/pause/step/back/reset, scrubbable timeline, snapshots.
10. Optimizer Arena 2–5 algorithms, true trajectory overlay and metrics.
11. Loss curve, weight history, gradient arrows.
12. Export figure/metrics/config, save/load experiment.
13. Non-blocking UI and numerical warnings.
14. Strong tests + working Windows build path.

**Не переходить к массовому созданию новых вкладок, пока этот сценарий не стал настоящим удобным приложением.**

## 107. Phase 2 — Classification and Trees

Binary logistic regression, softmax multiclass, threshold/ROC/PR/confusion matrix, linear SVM, kNN, Naive Bayes, decision tree step inspector, pruning, Random Forest, базовый Gradient Boosting. Каждая тема с хотя бы одним законченно работающим экспериментом и тестами. Сохранять общую систему экспериментов и UI.

## 108. Phase 3 — Deep Learning Core

Single neuron, activation explorer, MLP Builder, forward/backward step debugger, numerical/autograd gradient check, initialization, training curves, XOR, circles/moons, dropout/norm visualization. Не начинать с огромных моделей; учебная точность на малых сетях важнее.

## 109. Phase 4 — Unsupervised/Math/Data

K-Means manual centroids, DBSCAN point roles, GMM E/M, PCA direction/reconstruction, scalable dataset inspector, preprocessing and leakage demos, basic probability/statistics. Повторное использование готовых graph and parameter components.

## 110. Phase 5 — NLP and Attention

Text preprocessing, tokenization/BPE, BoW, TF-IDF, toy embeddings, Q/K/V inspector, attention heatmaps, multi-head, Transformer block, token sampling. Все алгоритмы должны вычислять реальные значения и запускаться офлайн на small examples.

## 111. Phase 6 — CNN / RNN / Advanced Methods

CNN kernel visualizer, RNN/LSTM/GRU, ensembles advanced, additional optimization algorithms, advanced validation, time series, probabilistic models. Дополнительные packs при необходимости.

## 112. Phase 7 — Exploratory Extensions

RL Gridworld/Bandits, anomaly detection, Bayesian models, recommender systems, graph ML, causal inference, generative VAE/GAN/diffusion toy demos, interpretability, RAG/LLM concepts, model robustness. Приоритет выбирается по образовательной ценности и возможностям уже готового ядра.

## 113. Phase 8 — Polishing, Performance, Community

Профилирование, улучшение UX, learn mode, lesson system, challenge mode, accessibility, plugin SDK, documentation, installer, reproducible CI builds, export reports, localization. Но базовые UX и тестирование должны присутствовать с Phase 0–1, а не откладываться до Phase 8.

## 114. Definition of Done per Feature

Чтобы отметить функцию `DONE`, требуется:
- реальное вычислительное поведение;
- тесты ключевой математики и ошибок;
- рабочий GUI control;
- связанная визуализация/числовой инспектор (если тема визуализируема);
- синхронизация с experiment state;
- обработка invalid inputs;
- реальный скриншот/демо, если среда позволяет;
- documented assumptions;
- интеграция в сохранение/загрузку, когда это применимо;
- smoke test включён в тестовый контур;
- отсутствие критических регрессий.

## 115. Правила ограничения контекста / автономного продолжения

Если ресурсы или контекст ограничены, **не спрашивать у пользователя очевидные детали** и не тратить ответ на развернутые извинения. Завершить текущий рабочий вертикальный срез, сохранить реальные файлы, тесты и статусы. Записать `docs/IMPLEMENTATION_STATE.md`: что реализовано, какие файлы изменены, что проверено, следующая конкретная задача. При следующем запуске: прочитать это состояние, проверить тесты, продолжить с первого незавершённого пункта. Не переписывать готовую архитектуру без причин, не начинать каждый раз заново.

---

# ЧАСТЬ XIX. ПРИЁМОЧНЫЕ СЦЕНАРИИ: ЧТО Я ДОЛЖЕН СМОЧЬ ПОТЫКАТЬ

## 116. P0: 15 обязательных демонстраций

**D01. Ручная прямая:** 100 точек `y=3x+2+noise`, движки `w,b`, мгновенно меняются линия, MSE и residuals.

**D02. Разбор одной ошибки:** клик по точке показывает `y`, `ŷ`, `r`, `r²` и contribution к aggregate loss.

**D03. 3D surface:** настоящая `L(w,b)`, вращение, вектор градиента, маркер текущей модели.

**D04. Один GD step:** можно проверить подстановку формулы и новый `w,b` по числам.

**D05. Learning rate explosion:** слишком большой LR вызывает заметные колебания/расходимость; корректная остановка при overflow.

**D06. SGD batch selection:** выбранные наблюдения подсвечены, batch gradient и итоговый update совпадают с расчётом.

**D07. Momentum comparison:** рядом две траектории GD и Momentum; видны gradient и velocity.

**D08. RMSProp:** отображаются EMA squared gradients и различный scale по осям.

**D09. Adam inspection:** отдельно `m`, `v`, `m_hat`, `v_hat` и действительный update на текущем шаге.

**D10. AdamW vs Adam + L2:** разница реализована корректно, weight decay не маскируется regularization gradient.

**D11. Regularization λ:** изменение λ меняет objective, минимум/срез и итоговые веса; data loss vs penalty раздельно.

**D12. Optimizer Arena:** 5 методов на одной функции, overlay trajectories, curves and fair comparison.

**D13. Timeline:** вернуться с шага 120 на шаг 17, параметры/графики/optimizer state не рассинхронизируются.

**D14. Save/Load:** сохранённый run полностью восстанавливается, при возможности воспроизводится следующий шаг.

**D15. Windows exe:** чистая Windows x64, локальные ресурсы, автономный запуск без установленного Python и обязательного интернета.

## 117. P1–P3: 20 дополнительных демонстраций

**D16. Logistic:** разделяющая граница и probability heatmap реально обучаются.

**D17. Threshold:** confusion matrix меняется, вероятности — нет.

**D18. Softmax:** 3 класса, probabilities sum to one, корректные decision regions.

**D19. SVM:** margin/support vectors и влияние C/γ.

**D20. Decision tree:** реальный candidate split Gini/entropy, выбранный порог и новые branches.

**D21. Overfitting:** глубина дерева меняет train/validation gap.

**D22. Random Forest:** видно предсказания отдельных деревьев и ансамбля.

**D23. Gradient Boosting:** последовательные pseudo-residuals and additive trees.

**D24. K-Means:** руками изменить initial centroids и увидеть assignment/update.

**D25. DBSCAN:** core/border/noise на текущих eps/min_samples.

**D26. PCA:** вручную повернуть проекционную ось, изменяются variance/reconstruction.

**D27. Neuron:** поменять входы/веса/activation, проследить каждую операцию.

**D28. Backprop:** маленький neural computation graph, local derivatives, gradient check.

**D29. XOR:** MLP обучается и отображает нелинейную границу решений.

**D30. CNN:** ядро 3×3 проходит изображение пошагово с real feature map.

**D31. Tokenization:** вручную выполнить BPE merges и увидеть новое tokenization.

**D32. TF-IDF:** изменения документа пересчитывают vocab, IDF, vectors and similarity.

**D33. Attention:** изменить `W_Q`/`W_K` и увидеть новые scores/heatmap/output.

**D34. Text decoding:** изменить temperature/top-p и увидеть новые token probabilities.

**D35. RL:** агент Gridworld выполняет Bellman/Q update, меняется policy heatmap.

## 118. Критерии хорошего результата

Считай продукт **по-настоящему полезным**, когда пользователь может без чтения исходников:
- самостоятельно построить пример;
- понять текущую математическую операцию;
- изменить существенный гиперпараметр;
- увидеть реальную визуальную реакцию;
- повторить один шаг расчёта на калькуляторе;
- сравнить две настройки честно;
- сохранить и восстановить эксперимент;
- завершить задачу/урок;
- избежать потери данных из-за ошибки.

---

# ЧАСТЬ XX. КОМАНДЫ ДЛЯ ТЕБЯ КАК ИИ-РАЗРАБОТЧИКА

## 119. Алгоритм действий после прочтения этого файла

**Сразу начинай работать.** Не делай бесконечный анализ вместо приложения.

1. Проверь реальные возможности окружения: Python, терминал, файловую систему, GUI rendering, Windows build, package installation. Факты отделяй от предположений.
2. Выбери конкретный воспроизводимый стек и объясни не более нескольких важных решений.
3. Создай каталог проекта и `pyproject.toml`, стартовый GUI, математическое ядро, базовые тесты.
4. Запусти первый smoke test и исправь проблемы.
5. Реализуй вертикальный P0 сценарий: dataset→manual regression→loss→3D contour→stepwise GD→history.
6. Доведи его до качественного GUI, а не оставляй в виде консольного прототипа.
7. Добавляй регуляризацию, SGD/Momentum/RMSProp/Adam/AdamW, optimizer comparison.
8. После каждого логически завершённого блока запускай тесты и проверяй математическую корректность.
9. Подготовь Windows packaging; собери/протестируй `.exe`, если окружение позволяет, или готовый Windows CI workflow.
10. Обнови `IMPLEMENTATION_STATE.md`, `IMPROVEMENT_BACKLOG.md` и реальный список статусов модулей.
11. Без новых уточнений продолжай следующий реализуемый приоритет, не разрушая P0.

## 120. Что делать, если в ТЗ не хватает важного алгоритма

**Не говори «этого нет в списке».** Проанализируй, является ли направление критически важным для понимания темы, переиспользует ли существующие компоненты и насколько сложно реализовать правильно. Добавь недостающее в roadmap; если это маленькое и полезное расширение текущего модуля — реализуй сразу. Например: gradient clipping для deep networks, decoupled decay visualizer, numerical stability warnings, loss landscape slices, interpolation/extrapolation experiment, learning-rate sensitivity, class imbalance explorer, anti-leakage warnings, attention masking — уместны даже без отдельного прямого требования.

## 121. Правило честности результата

В конце каждого этапа отчитывайся таблицей (или понятным кратким списком):
- `Реализовано и проверено` — что действительно есть;
- `Тесты` — точные команды и результат;
- `Сборка` — был ли создан/проверен Windows exe;
- `Ограничения` — что работает частично;
- `Следующий приоритет` — конкретная файловая задача, а не расплывчатое «можно добавить».

Не используй выражение «всё готово», пока не закрыты соответствующие критерии. Не публикуй вымышленные скриншоты, метрики, релизы и артефакты.

## 122. Формат передаваемого результата

При наличии доступа к файлам выдавай **реальный архив проекта** (source files, tests, docs, PowerShell scripts, packaging config) + **реальный `.exe`/ZIP дистрибутива**, если Windows build произошёл и проверен. Если Windows недоступна, обязательно предоставь рабочие исходники и сборочный workflow для Windows, не подменяй это обещанием. Сообщи точный путь каждого артефакта. При отсутствии файловых инструментов выводи **полные файлы с относительными путями**, без многоточий, пропусков, неполных imports и TODO в готовой части.

## 123. Итоговое поручение, высший приоритет

**ТВОЯ ЗАДАЧА — НАПИСАТЬ НАСТОЯЩЕЕ WINDOWS-ПРИЛОЖЕНИЕ ML UNIVERSE.**

Пользователь хочет часами исследовать реальные математические процессы Machine Learning, крутя коэффициенты, LR, регуляризацию, критерии потерь, оптимизаторы, деревья, архитектуры нейросетей, токенизацию, attention и другие алгоритмы, наблюдая корректные графики 2D/3D и конкретные числа.

**Отдельно и особенно важно:** ты **обязан самостоятельно докручивать продукт**, выявлять забытые важные темы, улучшать визуальные эксперименты, исправлять математику, расширять registry и предлагать новые полезные демонстрации. Не ограничивайся буквальным списком. Но сохраняй инженерную дисциплину: сначала работающий P0, затем полнофункциональные последующие модули, регулярно тестируй и документируй.

**НАЧНИ РЕАЛИЗАЦИЮ СЕЙЧАС, НЕ ОГРАНИЧИВАЙСЯ ПЛАНОМ.**

---

# ПРИЛОЖЕНИЕ A. КОНТРОЛЬНЫЙ СПИСОК ГОТОВНОСТИ ВСЕГО ПРОЕКТА

> Веди эти пункты в отдельном machine-readable реестре при разработке. Здесь приведён исходный master checklist. Все пункты из этого раздела **планируемые требования**, а не утверждение, что они уже реализованы.

## A1. Product / UI

- [ ] Настоящее окно Windows, корректный старт и завершение.
- [ ] Дизайн-система, тёмная/светлая тема, русская локализация.
- [ ] Левое меню, панели, докинг, splitters, full-screen plots.
- [ ] Slider+numeric field+tooltip+reset+parameter validity rules.
- [ ] Play/Pause/Step/Back/Replay/Reset/Run N Steps/Compare.
- [ ] Инспектор математических формул, подстановка чисел, Code View.
- [ ] Синхронные 2D, 3D, tables, plots, metrics и timeline.
- [ ] Мышь+клавиатура, доступность, HiDPI, colourblind-friendly.
- [ ] Error states, cancellation, progress, responsiveness.

## A2. Linear Regression P0

- [ ] Dataset generator (noise, outliers, seeds), CSV, editing points.
- [ ] Manual weights and bias; response line; residuals inspector.
- [ ] MSE, SSE, RMSE, MAE, Huber, LogCosh, Quantile, Weighted MSE.
- [ ] L1, L2, Elastic Net; plots of all objective components.
- [ ] Honest 3D `L(w,b)`, 2D contours, trajectory, gradient arrows.
- [ ] Batch GD, SGD, Mini-batch, Momentum, Nesterov, AdaGrad, RMSProp, Adam, AdamW.
- [ ] Parameter state history and exact update math.
- [ ] Optimizer Arena, trials and fairness warnings.
- [ ] Presets: divergence, saddle, scaling, sparse regularization.
- [ ] Save/load/export and reproducible tests.

## A3. Other ML

- [ ] Logistic and multiclass classification, ROC/PR/confusion matrix.
- [ ] SVM/kernel, kNN, Naive Bayes.
- [ ] Decision trees with splits/pruning, Random Forest.
- [ ] Boosting, GBDT variants and explanation.
- [ ] KMeans, DBSCAN, GMM, hierarchical.
- [ ] PCA/SVD, t-SNE, UMAP and interpretation limitations.
- [ ] Anomaly detection, statistics, Bayesian models.
- [ ] Evaluation, leakage, CV, hyperparameter search.

## A4. Deep Learning

- [ ] One neuron, activation curves and derivatives.
- [ ] MLP Builder, true forward/backward, gradient check.
- [ ] Training, weights/activations/gradient histograms.
- [ ] Normalization, dropout, initialization and pathologies.
- [ ] CNN kernel animation, feature maps, tensor shapes.
- [ ] RNN/LSTM/GRU unfolding.
- [ ] Autoencoder/VAE/GAN/diffusion toy simulations.

## A5. NLP and Transformer

- [ ] Russian/English preprocessing and tokenization.
- [ ] BPE merge visualizer; BoW/TF-IDF and document similarity.
- [ ] Toy embeddings and nearest-neighbor explorer.
- [ ] Query/Key/Value matrices, scaled attention and masks.
- [ ] Multi-head, Transformer block, tensor shape tracing.
- [ ] Token generation greedy/temp/top-k/top-p.
- [ ] Basic RAG/retrieval and LLM inference concepts.

## A6. Extra Topics and Expansion

- [ ] Time Series and leakage-proof backtesting.
- [ ] Bandits, Gridworld, Q-learning.
- [ ] Recommendation systems, graph ML, causal diagrams.
- [ ] Explainable AI, model uncertainty, distribution shift/fairness.
- [ ] Custom safe expression editor and capability-based plugin SDK.
- [ ] Experiment manager, versioned save format, exports.
- [ ] Lessons, challenges, glossary, progress, reference calculations.
- [ ] Self-audit, autonomous gap analysis and improvement backlog.

## A7. Engineering / Release

- [ ] `pytest` unit/integration/GUI smoke; independent math references.
- [ ] Static checks, typed interfaces, clean architecture.
- [ ] Thread-safe non-blocking GUI, performance budgets.
- [ ] Corrupted-file/error handling, offline resources and security.
- [ ] Windows build scripts and PyInstaller config.
- [ ] Verified Windows exe **или** честно обозначенный Windows CI build path.
- [ ] README and math conventions, exact status matrix, changelog.
- [ ] Completed P0 acceptance tests D01–D15.

---

# ПРИЛОЖЕНИЕ B. ПРАВИЛО ДЛЯ СЛЕДУЮЩЕГО СООБЩЕНИЯ, ЕСЛИ ИИ ПРЕРВЁТСЯ

Если работа прервалась из-за ограничения ответа или контекста, отправь ИИ-разработчику:

> Продолжай разработку ML Universe с текущих **реальных файлов**, а не с нуля. Сначала изучи `docs/IMPLEMENTATION_STATE.md`, проверь состояние проекта и выполни тесты. Исправь все ошибки текущего этапа, затем реализуй **следующий незавершённый пункт P0/P1**. Не пиши очередной большой план. Создавай исполняемые модули, связанные с UI и математикой, проверяй численные результаты, обновляй статус и `IMPROVEMENT_BACKLOG.md`. **Самостоятельно добавляй полезные функции и исправляй обнаруженные пробелы**; приоритет — реальное качество и исправность. Сборку `.exe` проверяй на Windows или оставь воспроизводимый Windows CI workflow с честным статусом.

---

# ПРИЛОЖЕНИЕ C. ЖЁСТКОЕ НАПОМИНАНИЕ О РЕЗУЛЬТАТЕ

Этот документ — **не список обязательств сделать всё сразу**, а полный замысел и подробный roadmap. Высший приоритет — создать **первую максимально качественную интерактивную лабораторию** и выпускать проверенные последующие модули. Пусть приложение лучше превосходно реализует 15 важных экспериментов, чем содержит 150 неработающих кнопок. Уровень качества должен накапливаться, а не падать по мере роста числа функций.

**Пользователь специально разрешает и требует твоей инициативы:** если ты знаешь, как улучшить продукт по UI, математике, интерактивности, производительности, методике обучения или набору ML-направлений, **докрути это сам**. Делай это осмысленно, со строгими тестами, соблюдением приоритетов и прозрачным статусом.

**НАЧИНАЙ ПИСАТЬ КОД И СОБИРАТЬ ПРОДУКТ.**
