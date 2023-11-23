# Delivery Service
Функции:
 - `get` -- `/deliveries/{delivery_id}` -- `Получить доставку по ID`
 - `post` -- `/deliveries` -- `Добавить доставку в базу`
 - `delete` -- `/deliveries/{delivery_id}` -- `Удалить доставку по ID`
 - `put` -- `/deliveries/{delivery_id}` -- `Обновить информацию о доставке`
 - `get` -- `/deliveries` -- `Возвращает список точек доставок`

# Инструкция по установке и запуску сервиса

Перед запуском сервиса необходимо установить все зависимости. Для этого выполните следующие шаги:

1. Установите и активируйте виртуальное окружение Python.

2. Выполните команду pip install -r requirements.txt.

После установки зависимостей вы можете запустить сервис. Для этого выполните одну из следующих команд:

- uvicorn app:app --port 8001 --reload - запуск сервиса с помощью Uvicorn на порту 8001 с автоматической перезагрузкой при изменении кода.
- ./run.sh - запуск сервиса с помощью скрипта run.sh.
- Создать файл .env в Delivery service и написать в нём POSTGRES_DSN=postgresql://postgres:1023@localhost:5432/postgres
# Для сборки docker образа:
```bash
docker build -t "delivery-service:1.0" .
```

для запуска нужно перейти в Deploy:
```bash
docker compose up -d
```