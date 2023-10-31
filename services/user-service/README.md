# User service
Для начала необходимо создать .env

# Запуск
Script: `source run.sh`\
Uvicorn: `uvicorn app:app --port 8003 --reload`

# Билд докера
```bash
docker build -t "user-service:1.0" .
```