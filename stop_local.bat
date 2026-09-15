@echo off
chcp 65001 >nul
title Агент контекстной рекламы — остановка
cd /d "%~dp0"

echo Останавливаю БД и Redis (Docker)...
docker compose -p ads_agent stop

echo.
echo Готово. API-сервер остановите, закрыв его окно.
echo (Если окно сервера уже закрыто — всё выключено.)
pause