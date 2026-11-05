# ML Universe — статус реализации на текущем этапе

## Действительно работающие вычислительные модули

- [x] Линейная регрессия: синтетический датасет, веса, bias, остатки, loss, регуляризация, поверхность ошибок, replay, save/load.
- [x] Loss: MSE, SSE, RMSE, MAE, Huber, Log-Cosh, Quantile, Weighted MSE (на уровне math API; weighted UI не выделен).
- [x] L1/L2/Elastic Net, математический градиент, bias исключён из штрафа.
- [x] GD/SGD/Mini Batch, Momentum, Nesterov, AdaGrad, RMSProp, Adam, AdamW, AMSGrad, Nadam, Adamax, Adadelta, Lion.
- [x] Численные benchmark оптимизации, 3D/2D контуры и траектории, LR scheduler.
- [x] Линейная алгебра: 2D grid transformation, matrix products, eigenvalues, SVD.
- [x] Нормы L1/L2/L∞, статистика CLT, информационная теория, кастомные функции, численные производные.
- [x] Logistic regression, softmax через scipy, SVM, kNN, Naive Bayes, деревья классификации, Random Forest, Extra Trees, AdaBoost, Gradient Boosting: *через обучаемые модели scikit-learn*, не полный ручной отладчик.
- [x] K-Means, DBSCAN, hierarchical, Gaussian Mixture Models; PCA и ручная ось проекции.
- [x] NumPy-нейрон и MLP с ручным backprop; CIF/численные операции CNN с пользовательским kernel.
- [x] TF-IDF/BoW через scikit-learn, Unicode tokens, учебный BPE, Q/K/V scaled dot-product attention, sampling decoding.
- [x] Q-learning Gridworld, Beta-Bernoulli, AR forecasting, Leakage demo, bias-variance, anomaly detection.
- [x] Feature scaling, NDCG, recommendations SVD, graph message passing, causal confounding, group fairness, permutation importance, forward diffusion.
- [x] Офлайн Plotly, JSON API, optional desktop webview, responsive UI, dark/light theme.
- [x] Unit/integration tests, Windows build script, Windows GitHub Actions workflow.

## Реализовано частично — текущая работа или ограничения

- [~] Внутренний отладчик по каждой компоненте: полностью в регрессии, частично в других лабораториях.
- [~] Визуальная геометрия деревьев: решения/список узлов, но нет полнофункционального редактируемого дерева.
- [~] CNN: реальные kernels/feature maps, пока без end-to-end обучения CNN.
- [~] Transformer: один scaled dot-product head и toy decoder, нет обученной полноценной архитектуры с несколькими слоями.
- [~] Нейросети: небольшой MLP и backprop, нет GPU-тренировки больших сетей.
- [~] Экспорт: JSON-regression; нет сохранения состояния всех дополнительных лабораторий.
- [~] Lessons/Challenge: пояснения и численная цель для регрессии, без редактора полноценных курсов и прогресса.
- [~] Windows: reproducible CI/build scripts подготовлены, Windows exe ещё НЕ собран и НЕ проверен в Linux окружении.
- [~] UI: offline dark/light theme; браузерное окно через pywebview, не чистые нативные Qt controls.

## Пока не реализовано в этой поставке (часть 124-главного мастер-ТЗ)

- [ ] полноценный мультислойный Transformer/LLM с trainable tokenizer/heads, предобученными весами, finetuning и KV cache;
- [ ] полноценные CNN/RNN/LSTM/GRU/GAN/VAE генеративные учебные тренировки;
- [ ] deep-learning GPU execution, mixed precision, DDP;
- [ ] расширенные байесовские методы MCMC/VI;
- [ ] RL среды за пределами маленького Gridworld;
- [ ] визуальный drag-and-drop конструктор моделей и совместимых pipelines;
- [ ] универсальный plugin SDK с изоляцией и версионированием;
- [ ] исследовательские модели Newton/BFGS/L-BFGS/coordinate/proximal/line search;
- [ ] крупный набор интерактивных учебных сценариев и система достижений;
- [ ] мультиязычная локализация, полноценная доступность, внешнее обновление;
- [ ] полное Windows E2E GUI тестирование и подписание исполняемого файла.

**Принцип:** «не сделано» здесь не означает декоративную страницу: недоделанные алгоритмы не представлены как готовые в интерфейсе.
