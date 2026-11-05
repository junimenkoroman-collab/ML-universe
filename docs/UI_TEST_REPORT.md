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

## Версия v0.8.1 — чистый интерфейс

- Убраны кнопки загрузки CSV, открытия/сохранения и экспорт PNG из Plotly UI. Старые API оставлены для совместимости.
- Modebar проверен браузером: только `Zoom in`, `Zoom out`, `Reset axes` на 2D; 3D настроен на `zoom3d` и `resetCameraDefault3d`. Наличие WebGL в этой Linux-среде не подтверждено.
- Проверены клики **Zoom in → Reset axes**, переключение тем, шаг регрессии, раскрытие математического инспектора, сворачиваемые группы параметров и переключение на классификацию.
- Повторный полный smoke-тест: 29/29 лабораторий, 0 ошибок JavaScript.
- Математические и API-тесты: 133 passed (`python -m pytest -q`).

## Версия v0.8.3 — модули параметров вместо стены настроек

- Для 29 разделов определены отдельные схемы: стартовые 1–3 поля и opt-in блоки «＋ Добавить блок».
- Переключение `SGD → Adam` отображает только β₁ и β₂, параметры RMSProp и Momentum скрыты. При удалении блока значения возвращаются к умолчаниям.
- Убрана дублирующая кнопка «Начать заново»: сброс остался в заголовке панели. Нет режимов «Эксперимент / Разобрать / Сравнить / Задание»: обучение и формулы доступны на одном экране, сравнение — в отдельной арене.
- Убраны нерелевантные поля SVM/kNN на страницах Decision Tree и ансамблей.
- Chromium smoke: 29/29 лабораторий, добавление/удаление блоков в регрессии, классификации и Attention, переключение Adam/L1, 2 темы, 0 JS ошибок.
- `python -m pytest -q`: 134 passed; `node --check ml_universe/static/app.js`: success.

Для ускорения проверки браузерного рендеринга можно запускать по диапазонам:

```bash
.venv/bin/python scripts/visual_smoke.py --chromium /usr/bin/chromium --nav-start 0 --nav-stop 10
.venv/bin/python scripts/visual_smoke.py --chromium /usr/bin/chromium --nav-start 10 --nav-stop 20
.venv/bin/python scripts/visual_smoke.py --chromium /usr/bin/chromium --nav-start 20 --nav-stop 29
```

Все три диапазона прошли последовательно без JavaScript-ошибок, каждый на реальных расчётах Python и локальном Plotly.
