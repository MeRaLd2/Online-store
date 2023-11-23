# Product Service
Функции:

 - `post` -- `/products/` -- `Создает продукт`
 - `get` -- `/products/{product_id}` -- `Получить информацию о продукте по id`
 - `get` -- `/products/` -- `Получить информацию о всех продуктах`
 - `put` -- `/products/{product_id}` -- `Обновляет продукт по id`
 - `delete` -- `/products/{product_id}` -- `Удаляет продукт по id`


# Инструкция по установке и запуску сервиса

Перед запуском сервиса необходимо установить все зависимости. Для этого выполните следующие шаги:

1. Установите и активируйте виртуальное окружение Python.

2. Выполните команду pip install -r requirements.txt.

После установки зависимостей вы можете запустить сервис. Для этого выполните одну из следующих команд:

- uvicorn app:app --port 8001 --reload - запуск сервиса с помощью Uvicorn на порту 8001 с автоматической перезагрузкой при изменении кода.
- ./run.sh - запуск сервиса с помощью скрипта run.sh.
- Создать файл .env в Product service и написать в нём POSTGRES_DSN=postgresql://postgres:1023@localhost:5432/postgres
# Для сборки docker образа:
```bash
docker build -t "product-service:1.0" .
```

для запуска нужно перейти в Deploy:
```bash
docker-compose up -d
```