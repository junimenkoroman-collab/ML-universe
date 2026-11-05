# GitHub, Linux и CI для ML Universe

Этот репозиторий уже хранит исходники ML Universe. **Не нужно импортировать ZIP в GitHub заново.** Linux — основная платформа, Windows workflow сохранён.

## Запуск и обновление

```bash
git clone https://github.com/junimenkoroman-collab/ML-universe.git
cd ML-universe
./scripts/run_linux.sh
```

Первый запуск установит Python-зависимости в `.venv`. Нужен Python 3.11 или новее и `python3-venv`. В обычном режиме сервер запускается только на `127.0.0.1` и открывает приложение в браузере. Если браузер не запустился:

```bash
.venv/bin/python -m ml_universe --no-open --port 8765
```

Открой `http://127.0.0.1:8765` на том же компьютере. При последующих изменениях в GitHub:

```bash
git pull --ff-only
./scripts/run_linux.sh
```

Если есть локальные незакоммиченные изменения, сначала сохрани их в своей ветке, не перезаписывай.

## Тесты на Linux

```bash
./scripts/test_linux.sh
```

Либо, если уже установил тестовые зависимости:

```bash
.venv/bin/python -m pytest -q
node --check ml_universe/static/app.js  # когда Node.js установлен
```

## GitHub Actions

- [Linux quality checks](https://github.com/junimenkoroman-collab/ML-universe/actions/workflows/linux-ci.yml) автоматически запускается при каждом push в `main` и в Pull Requests.
- Внутри есть проверки на **Python 3.11 и Python 3.12**, unit/API tests, JavaScript syntax check и проверка HTTP `/api/health`.
- Для запуска вручную: вкладка Actions → Linux quality checks → **Run workflow** → main → Run workflow.
- Чтобы прочитать результат, открой последний workflow run: зелёный ✔ означает успешные проверки, красный ✖ — смотри шаги с ошибками.
- GitHub CI не выполняет полноценный GUI-тест Chromium. Для него локально есть `python scripts/visual_smoke.py --chromium /usr/bin/chromium`, если установлен Playwright и Chromium. Этот тест запускается **отдельно и не обязателен** для базового Linux CI.
- Windows workflow сохранён, но Windows `.exe` не является приоритетом.

## Изменение кода

Для собственных изменений удобно создать ветку `feature/<тема>`, сделать commit и открыть Pull Request; CI проверит ветку автоматически. Если изменения в GitHub вносит ChatGPT, для обычного использования тебе достаточно `git pull --ff-only`.

## Доступ с удалённого Linux-сервера

Этот проект **не готов для публичного хостинга**: у него единое состояние симуляции и нет аутентификации. Не открывай API на публичном интерфейсе.

На своём VPS запусти:

```bash
.venv/bin/python -m ml_universe --no-open --port 8765
```

Со своего компьютера организуй SSH-туннель:

```bash
ssh -L 8765:127.0.0.1:8765 USER@SERVER
```

Тогда `http://127.0.0.1:8765` на твоём компьютере безопасно подключится к loopback-серверу. Для публичного доступа понадобятся сессии, ограничения ресурсов, аутентификация и изоляция экспериментов.
