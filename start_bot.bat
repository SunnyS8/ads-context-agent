@echo off
chcp 65001 >nul
title Агент контекстной рекламы — Telegram-бот
cd /d "%~dp0"

if not exist ".venv\Scripts\python.exe" (
    echo ОШИБКА: не найдено виртуальное окружение .venv
    pause
    exit /b 1
)

prompt $G
echo Запуск Telegram-бота (остановка — закрыть окно)...

.venv\Scripts\python.exe bot\bot.py

pause
