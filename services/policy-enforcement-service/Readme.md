# Policy enforcement service

## Настройки

Порядок загрузки настроек:
1) Файл .env
2) Переменные среды
3) Значения по умолчанию

# Запуск
В автономном режиме:

```bash
source run.sh
```

или

```bash
uvicorn app.app:app --port 5100 --reload
```

# Docker:

```bash
docker build -t "policy-enforcement-service:1.0" .
```

```bash
docker-compose up -d
```