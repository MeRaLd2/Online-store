# User service
Функции:
 - `post` -- `/groups` -- `Создает новую группу`
 - `get` -- `/groups` -- `Возвращает список групп`
 - `get` -- `/groups/{group_id}` -- `Возвращает информацию о группе`
 - `put` -- `/groups/{group_id}` -- `Обновляет информацию о группе`
 - `delete` -- `/groups/{group_id}` -- `Удаляет информацию о группе`


Для начала необходимо создать .env

# Запуск
Script: `source run.sh`\
Uvicorn: `uvicorn app:app --port 8003 --reload`

# Билд докера
```bash
docker build -t "user-service:1.0" .
```