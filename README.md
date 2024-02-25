## Документация о проделанной работе
### Используемые приложения
Перед началом работы с Kubernetes был разработан 
сервис **Message Board** с использованием базы данных,
к которому подключен инструмент 
мониторинга Prometheus.
**Message Board**
позволяет отправлять и просматривать
сообщения через HTML-форму.
### Подготовка к развертыванию в Kubernetes
Приложение является stateful и требует
использования множества объектов kubernetes, 
поэтому необходимо создать конфигурационные 
файлы (манифесты) для описания используемых ресурсов.
Манифесты для каждого компонента находятся в 
каталоге `/manifests`.
> **Примечание:** так как в ходе создания сервиса
> был написан `docker-compose.yml`, можно было использовать
> `kompose convert` для автоматического создания манифестов,
> однако, для лучшего осознания k8s манифесты были написаны вручную.

### Создание кластера, сервисов Pods и Deployments
Создание кластера:
```
minikube start
```

Так как для сервера используется
локальный докер-образ,
необходимо выполнить следующую команду:
```
eval $(minikube docker-env)
```
Эта команда настраивает текущую сессию терминала для работы с Docker-демоном внутри Minikube.

Сборка образа сервера: 
```
docker build -t server-message-board:latest -f docker/server/Dockerfile .
```

Образы Prometheus и Postgres используются из DockerHub.

Применение манифестов:
```
kubectl apply -k ./manifests
```

Проверка созданных ресурсов Deployments и Pods:
```
kubectl get pods

kubectl get deployments
```
### Подключение и работа с приложениями 
После применения манифестов были созданы ресурсы
типа Service,
в чём можно удостовериться следующим образом:
```
kubectl get services 
```
Подключение к сервису `server`:
```
minikube service server --url
```
Теперь можно добавить к URL `/messages` и перейти по итоговому 
URL в браузере.
### Присвоение меток и версионирование
В манифестах использовались метки, поэтому можно
получить Pod сервера по его метке:
```
kubectl get pods -l app=server
```

В манифестах также указывались метки версий.
Все Pod'ы версии `v1`:
```
kubectl get pods -l version=v1
```
Применение метки версии `v2` к Pod'у Prometheus и проверка:
```
export POD_NAME=$(kubectl get pods -l app=prometheus -o go-template='{{range .items}}{{.metadata.name}}{{"\n"}}{{end}}')
kubectl label pods "$POD_NAME" version=v2 --overwrite
kubectl get pods -l version=v2
```
### Масштабирование приложения
В манифесте сервера указано 2 реплики Pod,
в чем можно убедиться, выполнив команду: 
```
kubectl get rs
```
Масштабирование Deployment сервера до 5 реплик и проверка:
```
kubectl scale deployment/server --replicas=5
kubectl get rs
```
### Обновление приложения
Обновление `Postgres` с версии 13 до версии 13.14:
```
kubectl set image deployment/db postgres=postgres:13.14
```
Проверка статуса обновления:
```
kubectl rollout status deployment/db
```