@echo off
echo ====================================
echo   PortfolioHub - Запуск сервера
echo ====================================
echo.

:: Проверка наличия виртуального окружения
if not exist "venv\Scripts\activate.bat" (
    echo [!] Виртуальное окружение не найдено
    echo [*] Создание виртуального окружения...
    python -m venv venv
    echo [+] Виртуальное окружение создано
    echo.
)

:: Активация виртуального окружения
echo [*] Активация виртуального окружения...
call venv\Scripts\activate.bat

:: Установка зависимостей
echo [*] Проверка зависимостей...
pip install -q -r requirements.txt

:: Запуск приложения
echo.
echo [+] Запуск Flask приложения...
echo [+] Откройте браузер: http://localhost:5000
echo.
python app.py

pause

