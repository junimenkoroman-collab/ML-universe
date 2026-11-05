# Проверка интерфейса ML Universe v0.8

Проверены: **29 пунктов меню** в Chromium с встроенными ресурсами HTML/CSS/JS, локальным Plotly и API-ответами настоящего Python Controller. Это UI integration smoke test с in-memory API transport, а не внешнее E2E в публичном интернете.

Результат: 29/29 страниц создали графики, доступны светлая и тёмная темы; JavaScript pageerror: 0. Скриншоты: `docs/ui-light.png`, `docs/ui-dark.png`.

Среда ограничивает сетевую навигацию Chromium (`URLBlocklist=*`), поэтому скриншоты и smoke test выполнены через `page.set_content` и проксирование вызовов к тому же `Controller.handle`, который обслуживает HTTP. Реальный HTTP API независимо проверяется в `tests/test_server.py`.

Ограничения: Chromium в этой среде не имеет WebGL, поэтому проверен корректный fallback 3D в 2D контуры. Полный GUI E2E в пользовательской системе Linux ещё рекомендуется. Автозапуск этого визуального теста в GitHub Actions не настроен: он опционален и требует Playwright + Chromium.

Повторить на Linux после установки `pip install playwright` и наличия `/usr/bin/chromium`:

```bash
.venv/bin/python scripts/visual_smoke.py --chromium /usr/bin/chromium
```

Отдельно запускать `./scripts/test_linux.sh` для unit/API проверок.
