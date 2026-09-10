# Агент контекстной рекламы

Автоматизация управления, анализа и оптимизации контекстной рекламы
на площадках **Яндекс.Директ** (через eLama API) и **VK Ads (TARGETING)**.

## Возможности

- Загрузка статистики кампаний (показы, клики, расход, конверсии).
- Расчет KPI: CTR, CPC, CPA, CPL, ДРР, ROAS.
- Обнаружение аномалий и формирование рекомендаций.
- Генерация текстов объявлений через LLM.
- Веб-панель на Next.js и Telegram-бот на aiogram.
- Журнал всех действий (`audit_log`).
- Режим `DRY_RUN` по умолчанию.

## Структура

```
backend/     # FastAPI + SQLAlchemy + Alembic
frontend/    # Next.js 14 (App Router, TypeScript, Tailwind)
bot/         # Telegram-бот (aiogram 3.x)
prompts/     # Промпты для LLM
.opencode/   # Агенты и команды OpenCode
```

## Быстрый старт

### 1. Запустить инфраструктуру

```bash
docker compose up -d
```

### 2. Настроить окружение

```bash
cp .env.example .env
# заполнить реальные токены
```

### 3. Запустить бэкенд

```bash
cd backend
python -m venv .venv
.venv\Scripts\Activate.ps1   # Windows
pip install -r requirements.txt
alembic upgrade head
uvicorn src.main:app --reload
```

### 4. Запустить фронтенд

```bash
cd frontend
npm install
npm run dev
```

### 5. Запустить Telegram-бот

```bash
cd bot
pip install -r requirements.txt
python bot.py
```

## KPI по умолчанию

```
Целевой CPL: 1 500 ₽
Минимум конверсий для решения: 5
Период анализа: последние 7 дней
Максимальное изменение ставки: 15%
Максимальная ставка: 250 ₽
Автоизменение бюджета: запрещено
```

## Безопасность

- Изменения ставок — только после подтверждения пользователя.
- Секреты — только в `.env`, не в Git.
- Все действия — в `audit_log`.
- Тесты используют mock API.
- `DRY_RUN=true` по умолчанию.

## Тесты

```bash
cd backend
pytest -v
```

## Планы

- [ ] eLama API: список кампаний
- [ ] eLama API: Aggregated Reports
- [ ] VK Ads: кампании и статистика
- [ ] Подтверждение ставок через Telegram
- [ ] Автоматические отчеты по расписанию