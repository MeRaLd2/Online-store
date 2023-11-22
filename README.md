# Online-store

Для запуска Trivy необходимо писать:

```
docker run --rm -v /var/run/docker.sock:/var/run/docker.sock aquasec/trivy image 
```
И имя образа (например deploy-product-service)
