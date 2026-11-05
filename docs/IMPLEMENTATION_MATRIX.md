# ML Universe v0.8 — что реально реализовано

Эта версия целенаправленно оставляет только учебный путь **базовый линал → классический ML → DL → NLP** и маленький бонус по RL. Не путать интерактивную демонстрацию операции с обучением полноценной сети.

## Входящий в scope функционал

**Регрессия и оптимизация:** `ŷ = wx+b`, residuals, MSE, SSE, RMSE, MAE, Huber, Smooth L1, Log-Cosh, Quantile, Weighted MSE (3 вида весов наблюдений), L1/L2/ElasticNet, Ridge/Lasso/ElasticNet regularization path, GD/SGD/Mini-batch, Momentum, Nesterov, AdaGrad, RMSProp, Adam, AdamW, LR schedulers, 25-точечный grid sweep, Projected GD (на L2-шар), Optimizer Arena, 2D/3D loss surface, history/replay. Программный API импорта CSV и сохранения остался для совместимости, но файловые кнопки удалены из учебного UI.

**Классификация:** Logistic Regression, Softmax Regression (3 класса, Gaussian Blobs), линейный/kernel SVM, kNN, Gaussian Naive Bayes, дерево и критерии split, Random Forest, Gradient Boosting, ROC, PR, confusion matrix и метрики. Модели scikit-learn; показатели на учебной выборке, не независимый тест качества обобщения.

**K-Means:** инициализация random/K-means++, assignment/update, фактические центроиды, inertia и путь обновлений. Убраны DBSCAN/GMM/hierarchical.

**DL:** одиночный нейрон, 9 активаций, MLP/XOR с аналитическим forward/backprop и численной проверкой градиента, выбор weight initialization, нормы обратных градиентов в глубокой ReLU-сети, inverted dropout, свёртка 3×3 и receptive field, простая Elman RNN. CNN/RNN в текущем модуле не обучаются end-to-end — здесь показаны математические операции.

**NLP:** Unicode-токенизация, CountVectorizer/Bag of Words, TF-IDF, BPE, текстовый MultinomialNB на встроенном маленьком корпусе, co-occurrence→PPMI→SVD embeddings, scaled dot-product attention Q/K/V, multi-head attention и выходная проекция, fixed-logits decoding (greedy, temperature, top-K, top-P), RAG retrieval (TF-IDF + cosine + top-K; генерация LLM отсутствует).

**RL:** Bernoulli Multi-Armed Bandit, epsilon-greedy, эмпирические оценки, подсчёт pulls, среднего reward и pseudo-regret. Gridworld Q-learning удалён.

**Математика:** вектор и matrix 2×2, dot product, линейное преобразование сетки, L1/L2/L∞, производная, градиент и Hessian через центральные разности, энтропия/cross entropy/KL/JS для Бернулли.

## Глубина реализации и ограничения

- Ручное `step/back/seek` сохраняющее RNG и состояние оптимизатора реализовано **для линейной регрессии**. Остальные лаборатории пересчитывают полный выбранный эксперимент.
- Для Nesterov и AdamW используются явные выбранные соглашения, а не обещание универсальной эквивалентности всех реализаций.
- Классификация через scikit-learn (не реализован полноценный ручной пошаговый CART или обучение через собственный backprop).
- Многомерная регрессия в path lab существует, но основная интерактивная loss surface использует два параметра `w,b`.
- Отдельные RNN/CNN/Attention/Embeddings не используют предобученную модель. Математика настоящая, параметры учебные.
- Retrieval RAG не подменяется фиктивным ответом от LLM.
- В офлайн Chromium без WebGL включается 2D contour fallback; настоящий 3D возможен при доступном WebGL.
- Windows workflow и скрипты не удалены, но на Linux `.exe` не собирается.
- Локальное API доступно только одному доверенному пользователю и **не годится для публичного хостинга без защиты**.

## Удалённые направления

PCA, advanced spectral algebra, DBSCAN, GMM, hierarchical, Extra Trees, AdaBoost, статистика CLT, anomaly, time series, leakage demo, bias-variance, feature scaling demo, fairness, causal inference, graph ML, diffusion, ranking, recommendations, probability/Bayes и Gridworld Q-learning — вне текущей программы. Их нет в навигации и реестре `run_lab`.

## Качество

- Новые математические тесты сверяют аналитический градиент с central finite differences и проверяют invariants внимания/PGD/softmax.
- Chromium smoke test проходит по 29 пунктам меню и проверяет обе темы с результатами вычислительного `Controller`.
- Источники фронтенда: `/ml_universe/static`; тесты и docs сопровождают изменения.
