# ML Universe — Interactive Machine Learning Laboratory

**ML Universe** — работающее офлайн-приложение с интерактивными визуализациями и математическими вычислениями по машинному обучению. Исходный код открыт, все учебные расчёты выполняются локально.

> **Статус:** действующий расширяемый прототип v0.7.0, а не полностью завершённая реализация всех 124 глав мастер-ТЗ. Сейчас реализовано более 30 отдельных вычислительных лабораторий и 12 правил обновления оптимизатора. Включены 2D/3D-срезы и визуализации, многократные эксперименты, сохранение регрессии и воспроизведение шагов. Часть расширенных технологий и polish пока в backlog.

## Linux — основная платформа проекта

**Для Linux запускайте в браузере:**

```bash
# Из корня репозитория; требуется Python >= 3.11 и модуль venv
./scripts/run_linux.sh
```

Скрипт создаст `.venv`, установит зависимости при первом запуске и откроет офлайн-приложение через `127.0.0.1`. Нативный оконный движок не нужен. Для запуска тестов: `python -m pytest -q` (после установки `pytest`) или `./scripts/test_linux.sh`.

Подробно: [GitHub и Linux](docs/GITHUB_LINUX_SETUP.md). В репозитории добавлен `.github/workflows/linux-ci.yml` для автоматической проверки при изменениях. **Windows сборка остаётся доступна**, но не является основной платформой.

**Не открывайте существующий локальный HTTP API напрямую в публичный интернет** — используйте SSH-туннель для личной удалённой работы, см. инструкцию.

## Запуск из исходников

Требуется Python 3.11+ и Windows 10/11 x64 (также работает на Linux/macOS через браузер).

```powershell
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -e '.[desktop]'
python -m ml_universe
```

Если системный WebView2 недоступен или возникли проблемы с 3D-графиками, запустите интерфейс в обычном браузере:

```powershell
python -m ml_universe --browser
```

На Linux:

```bash
python -m pip install -e .
python -m ml_universe --browser
```

Приложение поднимает локальный HTTP-сервер **только** на `127.0.0.1` на случайном свободном порту. Все JS-графики поставляются локально, внешний интернет не требуется. Дополнительный оконный движок — `pywebview` (на Windows работает через совместимый WebView). Без него откроется системный браузер.

## Сборка настоящего Windows `.exe`

**Сборка PyInstaller под Windows должна запускаться на Windows.** Linux-сборка не является Windows `.exe` и не должна им называться.

Способ 1: в PowerShell в корне проекта:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\build_windows.ps1
```

После тестов и smoke-test готовый архив:

`dist\ML_Universe_Windows_x64.zip`

Распакуйте **всю папку** и запустите `ML_Universe\ML_Universe.exe`. Пользователю не требуется устанавливать Python. Предпочтителен современный Windows WebView2 runtime; при его отсутствии передайте аргумент `--browser` и используйте установленный браузер.

Способ 2: загрузите проект в GitHub, откройте **Actions → Build Windows EXE → Run workflow**, затем скачайте artifact `ML_Universe_Windows_x64`. Workflow на Windows устанавливает зависимости, запускает тесты, собирает `.exe`, проверяет локальный API и архивирует переносимый дистрибутив.

## Что можно делать сейчас

В главной лаборатории: синтезировать данные `y=wx+b+noise`, двигать веса и смещение, измерять residuals/MSE/MAE/Huber/RMSE/Log-Cosh/Quantile, включать L1/L2/Elastic Net, смотреть настоящую 3D loss surface и contour, наблюдать SGD/Momentum/Nesterov/AdaGrad/RMSProp/Adam/AdamW/AMSGrad/NAdam/Adamax/AdaDelta/Lion, включать LR scheduler, просматривать градиенты и состояния, двигаться по timeline, сравнивать оптимизаторы, сохранять/загружать результаты.

В других лабораториях можно изменять параметры и запускать реальные вычисления: пользовательские функции, линейная алгебра, нормы, статистика/CLT, информационная теория, LR schedules, PCA, classification (logistic, SVM, kNN, Naive Bayes), деревья, леса и бустинг, кластеризация (K-Means, DBSCAN, GMM, Agglomerative), anomaly detection, leakage, scaling, bias-variance, permutation importance, group fairness, ранжирование NDCG, рекомендации/SVD, graph message passing, confounding, single neuron, NumPy-MLP с backprop на XOR, CNN kernel maps, TF-IDF, BPE, scaled dot-product attention, sampling temperature/top-k/top-p, Q-learning Gridworld, Bayesian update, AR forecasting, forward diffusion.

Все страницы научно вычислительные, но глубина интерактивного пошагового инспектора различается. Полный ручной step/debug/seek реализован сейчас для linear regression; многие другие лаборатории выполняют выбранный расчёт целиком.

## Горячие клавиши

- `Space` — воспроизведение/пауза главного эксперимента, если фокус не в поле ввода.
- `Esc` — закрыть справку / остановить playback.

## Тесты

```bash
python -m pytest -q
node --check ml_universe/static/app.js
```

## Структура

- `ml_universe/core/maths.py` — безопасный AST, loss functions и аналитические производные.
- `ml_universe/core/optimizers.py` — настоящие правила оптимизаторов и schedulers.
- `ml_universe/core/regression.py` — воспроизводимая симуляция с сохранением RNG/optimizer state.
- `ml_universe/core/labs.py`, `core/extras.py` — другие ML/DS вычислительные лаборатории.
- `ml_universe/static/` — офлайн-интерфейс и локальный Plotly JS.
- `ml_universe/server.py` — HTTP API на loopback, запуск окна.
- `tests/` — тесты математических инвариантов и API.
- `scripts/build_windows.ps1` — сборка и smoke-test Windows exe.
- `.github/workflows/windows-exe.yml` — воспроизводимая сборка через GitHub Actions.
- `docs/MASTER_PROMPT.md` — полный исходный мастер-промпт (124 раздела).
- `docs/IMPLEMENTATION_MATRIX.md` — точная картина реализованного и отсутствующего.

## Научные соглашения

Основной objective: `MSE = mean((ŷ−y)²)`. При L2 используется `λ Σwⱼ²`, при L1 — `λ Σ|wⱼ|`; смещение не штрафуется. При Elastic Net: `λ [ratio·L1+(1-ratio)·Σwⱼ²]`. В точке недифференцируемости L1 выбран нулевой субградиент. AdamW выполняет decoupled decay отдельно от указанного objective, не выдаётся за L2-градиент. Training step / sample selection отличаются от epoch. Примеры генерации NLP явно показывают, какие веса случайны и какие не обучались.

## Безопасность и ограничения

- AST не позволяет произвольные Python-вызовы.
- HTTP прослушивает только loopback; сеть для вычислений не используется.
- Импортируются структурированные JSON-эксперименты, а не произвольные pickle.
- Очень большие матрицы ограничены с целью устойчивой отзывчивости.
- Классификаторы и ансамбли вне основной лаборатории используют scikit-learn, а не переписанные вручную пошаговые движки.
- Подробная проверка отображения GUI на Windows и готового `.exe` должна быть проведена на Windows после сборки.
