# Онлайн-магазин

# Сервисы

Basket service | [Click](/services/basket-service/)

Delivery service | [Click](/services/delivery-service/)

Feedback service | [Click](/services/feedback-service/)

Notification service | [Click](/services/notification-service/)

Policy enforcement service | [Click](/services/policy-enforcement-service)

Product service | [Click](/services/product-service/)

User service | [Click](/services/user-service/)

# Тесты
e2e tests - [Click](/tests/) \

# Trivy
Для запуска Trivy необходимо писать:

```
docker run --rm -v /var/run/docker.sock:/var/run/docker.sock aquasec/trivy image 
```
И имя образа (например deploy-product-service)


# Bandit
Для запуска Bandit Нужно напиать:

```
bandit -r ./dir
```
