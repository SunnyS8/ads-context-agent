@echo off
chcp 65001 >nul
title Агент контекстной рекламы — запуск
cd /d "%~dp0"

echo ============================================
echo  Агент контекстной рекламы
echo  Запуск сервера...
echo ============================================

echo.
echo [1/4] Запуск БД и Redis (Docker)...
docker compose -p ads_agent up -d

echo.
echo [2/4] Проверка/применение миграций БД...
cd backend
if exist "..\.venv\Scripts\python.exe" (
    ..\.venv\Scripts\python.exe -m alembic upgrade head
) else (
    echo ОШИБКА: не найдено виртуальное окружение .venv
    pause
    exit /b 1
)

echo.
echo [3/4] Заполнение демо-данными (безопасно, повторно не дублирует)...
..\.venv\Scripts\python.exe scripts\seed_mock.py

echo.
echo [4/4] Запуск API-сервера...
echo.
echo Сервер будет работать, пока открыто это окно.
echo Адрес: http://localhost:8000  (документация: http://localhost:8000/docs)
echo.
echo Чтобы остановить сервер, просто закройте это окно.
echo ============================================

..\.venv\Scripts\python.exe -m uvicorn src.main:app --host 0.0.0.0 --port 8000

pause