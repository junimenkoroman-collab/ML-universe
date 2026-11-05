# Как собрать Windows .exe

**Условия:** Windows 10/11 x64, Python 3.11 x64, доступ к PyPI при сборке, PowerShell. Для основной работы приложения интернет не нужен.

1. Распакуйте архив проекта.
2. Откройте PowerShell в корне `ML_Universe_App`.
3. Выполните `powershell -ExecutionPolicy Bypass -File scripts/build_windows.ps1`.
4. Скрипт создаёт виртуальное окружение, ставит зависимости, выполняет unit/integration tests, собирает PyInstaller one-folder, запускает созданный exe с `--no-open --port 18765`, проверяет `http://127.0.0.1:18765/api/health`, затем готовит ZIP.
5. Отправляйте полученный `dist/ML_Universe_Windows_x64.zip`; конечный пользователь распаковывает папку и запускает `ML_Universe.exe`.

**GitHub Actions:** добавьте проект в свой репозиторий, затем `Actions → Build Windows EXE → Run workflow`, скачайте артефакт с названием `ML_Universe_Windows_x64`.

**WebView2:** Native window через pywebview использует системный webview; если компонент не работает, fallback — браузер по умолчанию. Для принудительного браузера: `ML_Universe.exe --browser`. Он подходит для 3D и сохраняет работу офлайн.

**Почему не создан exe в текущей среде:** исходная среда Linux; PyInstaller не производит Windows-PE бинарник из Linux. Установить PyInstaller дополнительно не удалось из-за отсутствия сетевого DNS-доступа. Windows workflow заготовлен, но не выполнялся в этой среде. Не следует выдавать подготовленный скрипт за проверенный exe.
