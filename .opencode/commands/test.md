# Запуск тестов

Запускает тестовый набор бэкенда и фронтенда.

## Использование

```
/test [backend|frontend|all]
```

## Бэкенд

```powershell
cd backend
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
pytest -v
```

## Фронтенд

```powershell
cd frontend
npm install
npm run lint
npm run build
```

## Что проверяют тесты

- Расчеты KPI (CTR, CPC, CPA, ДРР, ROAS).
- Обнаружение аномалий.
- Формирование рекомендаций.
- Работу mock-адаптера.