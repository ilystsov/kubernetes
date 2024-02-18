[Вернуться][main]

---

# Использование Minikube для создания кластера

## Цели

- Узнай, что такое кластер Kubernetes.
- Узнай, что такое Minikube.
- Запусти кластер Kubernetes на локальной машине.

## Кластеры Kubernetes

Kubernetes координирует высокодоступный кластер компьютеров, которые соединены для работы как единое целое. Абстракции
Kubernetes позволяют разворачивать контейнерные приложения на кластере, не привязывая их к отдельным машинам. Чтобы
использовать эту новую модель развёртывания, приложения должны быть упакованы таким образом, чтобы отделить их от
отдельных узлов: они должны быть контейнеризированы. Контейнерные приложения более гибкие и доступные, чем моделях
развёртывания в прошлом, когда приложения устанавливались непосредственно на конкретные машины в виде пакетов, глубоко
интегрированных в хост. Kubernetes автоматизирует распределение и планирование контейнеров приложений по кластеру более
эффективным способом. Kubernetes - это платформа с открытым исходным кодом, готовая к промышленной разработке.

Кластер Kubernetes состоит из двух типов ресурсов:

- **Control Plane** - координирует работу кластера.
- **Узлы (Nodes)** - рабочие (workers), на которых запускаются приложения

> :eight_spoked_asterisk: Примечание: Kubernetes - это платформа производственного уровня с открытым исходным кодом,
> которая организует размещение (планирование) и выполнение контейнеров приложений внутри и между компьютерными
> кластерами.

### Кластерная диаграмма

![](https://kubernetes.io/docs/tutorials/kubernetes-basics/public/images/module_01_cluster.svg)

**Control Plane** отвечает за управление кластером. Control Plane координирует все действия в кластере, такие как
планирование работы приложений, поддержание желаемого состояния приложений, масштабирование приложений и выпуск новых
обновлений.

**Узел (Node)** - это виртуальная машина или физический компьютер, который служит рабочей машиной в кластере Kubernetes.
Каждый узел имеет Kubelet, который является агентом для управления узлом и взаимодействия с плоскостью управления
Kubernetes. На узле также должны быть установлены инструменты для работы с контейнерами, такие как `containerd`
или `CRI-O`. Кластер Kubernetes, обрабатывающий производственный трафик, должен состоять как минимум из трех узлов,
поскольку если один узел выходит из строя, то теряется и `etcd`, и инстанс control plane, и резервирование нарушается.
Снизить этот риск можно, добавив больше узлов control plane.

> :eight_spoked_asterisk: Примечание: Control Plane управляет кластером и узлами, на которых размещаются запущенные
> приложения.

Когда разворачиваешь приложения на Kubernetes, "говоришь" Control Plane запустить контейнеры приложений. Control Plane
планирует запуск контейнеров на узлах кластера. Компоненты на уровне узлов, такие как kubelet, взаимодействуют с Control
Plane с помощью [Kubernetes API](https://kubernetes.io/docs/concepts/overview/kubernetes-api/), который раскрывает
Control Plane. Конечные пользователи могут напрямую использовать Kubernetes API для взаимодействия с кластером.

Кластер Kubernetes может быть развёрнут как на физических, так и на виртуальных машинах. Чтобы начать разработку
Kubernetes, можешь использовать Minikube. Minikube - это облегченная реализация Kubernetes, которая создает виртуальную
машину на локальной машине и разворачивает простой кластер, содержащий только один узел. Minikube доступен для систем
Linux, macOS и Windows. Minikube CLI обеспечивает базовые операции загрузки для работы с кластером, включая запуск,
остановку, состояние и удаление.

## Привет, Minikube

Запустим приложение на Kubernetes с помощью minikube. Будем использовать образ контейнера, который использует NGINX для
обратной передачи всех запросов.

### Задачи

- Разверуть приложение на minikube.
- Запустить приложение.
- Просмотр логов приложения.

> :eight_spoked_asterisk: Примечание: Должны быть установлены minikube и kubectl

### Создание кластера minikube

```sh
minikube start
```

### Просмотр приборной панели (Dashboard)

Открой Dashboard Kubernetes. Это можно сделать двумя разными способами:

- Скопировать и вставить URL-адрес

```sh
minikube dashboard --url
```

- Запустить и дождаться пока страница откроется:

```sh
minikube dashboard
```

Теперь переключись обратно в терминал, в котором запустили `minikube start`.

### Создание развёртывания (Deployment)

Kubernetes Pod - это группа из одного или нескольких контейнеров, связанных между собой для целей администрирования и
работы в сети. В нашем случае Pod имеет только один контейнер. Развёртывание (Deployment) Kubernetes проверяет состояние
Pod и перезапускает контейнер Pod-а, если он завершает работу. Развёртывания (Deployments) - это рекомендуемый способ
управления созданием и масштабированием Pod-ов.

1. Используй команду kubectl create, чтобы создать развёртывание (Deployment), управляющее Pod. Pod запускает контейнер
   на основе предоставленного образа Docker.

```sh
# Запусти образ тестового контейнера, включающий веб-сервер
kubectl create deployment hello-node --image=registry.k8s.io/e2e-test-images/agnhost:2.39 -- /agnhost netexec --http-port=8080
```

2. Просмотри на Deployment:

```sh
kubectl get deployments
```

Вывод будет примерно таким:

```sh
NAME         READY   UP-TO-DATE   AVAILABLE   AGE
hello-node   1/1     1            1           40s
```

3. Просмотр узла:

```sh
kubectl get pods
```

Вывод будет примерно таким:

```sh
NAME                         READY   STATUS    RESTARTS   AGE
hello-node-ccf4b9788-7jdrm   1/1     Running   0          10m
```

4. Просмотр событий кластера:

```sh
kubectl get events
```

5. Просмотр конфигурации kubectl:

```sh
kubectl config view
```

6. Просмотр логов приложений для контейнера в pod.

```sh
kubectl logs hello-node-ccf4b9788-7jdrm
```

Вывод будет примерно таким:

```sh
I0214 04:36:59.263917       1 log.go:195] Started HTTP server on port 8080
I0214 04:36:59.264070       1 log.go:195] Started UDP server on port  8081
```

> :eight_spoked_asterisk: Примечание: Более подробную информацию о командах kubectl можно найти
> по [ссылке](https://kubernetes.io/docs/reference/kubectl/).

### Создай сервис

По умолчанию Pod доступен только по своему внутреннему IP-адресу внутри кластера Kubernetes. Чтобы сделать hello-node
Container доступным извне виртуальной сети Kubernetes, необходимо выставить Pod в
качестве [сервиса](https://kubernetes.io/docs/concepts/services-networking/service/) Kubernetes.

1. Выведи Pod в публичный интернет с помощью команды `kubectl expose`:

```sh
kubectl expose deployment hello-node --type=LoadBalancer --port=8080
```

Флаг `--type=LoadBalancer` указывает на то, что мы хотим выставить свой сервис за пределы кластера.

Код приложения в тестовом образе прослушивает только TCP-порт 8080. Если бы мы использовали `kubectl expose` для
выставления другого порта, клиенты не смогли бы подключиться к этому другому порту.

2. Просмотри на созданный сервис:

```sh
kubectl get services
```

Вывод будет примерно таким:

```sh
hello-node   LoadBalancer   10.108.38.168   <pending>     8080:30600/TCP   5m17s
kubernetes   ClusterIP      10.96.0.1       <none>        443/TCP          75m
```

На облачных провайдерах, поддерживающих балансировщики нагрузки, для доступа к сервису будет предоставлен внешний
IP-адрес.
В minikube тип LoadBalancer делает сервис доступным через команду minikube service.

3. Выполни следующую команду:

```sh
minikube service hello-node
```

Откроется окно браузера, которое обслуживает приложение и показывает его ответ.

### Включение аддонов

Инструмент minikube включает в себя набор встроенных аддонов, которые можно включать, отключать и открывать в локальной
среде Kubernetes.

1. Список поддерживаемых в настоящее время аддонов:

```sh
minikube addons list
```

Вывод будет примерно таким:

```sh
|-----------------------------|----------|--------------|--------------------------------|
|         ADDON NAME          | PROFILE  |    STATUS    |           MAINTAINER           |
|-----------------------------|----------|--------------|--------------------------------|
| ambassador                  | minikube | disabled     | 3rd party (Ambassador)         |
| auto-pause                  | minikube | disabled     | minikube                       |
| cloud-spanner               | minikube | disabled     | Google                         |
| csi-hostpath-driver         | minikube | disabled     | Kubernetes                     |
| dashboard                   | minikube | enabled ✅   | Kubernetes                     |
| default-storageclass        | minikube | enabled ✅   | Kubernetes                     |
| efk                         | minikube | disabled     | 3rd party (Elastic)            |
| freshpod                    | minikube | disabled     | Google                         |
| gcp-auth                    | minikube | disabled     | Google                         |
| gvisor                      | minikube | disabled     | minikube                       |
| headlamp                    | minikube | disabled     | 3rd party (kinvolk.io)         |
| helm-tiller                 | minikube | disabled     | 3rd party (Helm)               |
| inaccel                     | minikube | disabled     | 3rd party (InAccel             |
|                             |          |              | [info@inaccel.com])            |
| ingress                     | minikube | disabled     | Kubernetes                     |
| ingress-dns                 | minikube | disabled     | minikube                       |
| inspektor-gadget            | minikube | disabled     | 3rd party                      |
|                             |          |              | (inspektor-gadget.io)          |
| istio                       | minikube | disabled     | 3rd party (Istio)              |
| istio-provisioner           | minikube | disabled     | 3rd party (Istio)              |
| kong                        | minikube | disabled     | 3rd party (Kong HQ)            |
| kubeflow                    | minikube | disabled     | 3rd party                      |
| kubevirt                    | minikube | disabled     | 3rd party (KubeVirt)           |
| logviewer                   | minikube | disabled     | 3rd party (unknown)            |
| metallb                     | minikube | disabled     | 3rd party (MetalLB)            |
| metrics-server              | minikube | disabled     | Kubernetes                     |
| nvidia-device-plugin        | minikube | disabled     | 3rd party (NVIDIA)             |
| nvidia-driver-installer     | minikube | disabled     | 3rd party (Nvidia)             |
| nvidia-gpu-device-plugin    | minikube | disabled     | 3rd party (Nvidia)             |
| olm                         | minikube | disabled     | 3rd party (Operator Framework) |
| pod-security-policy         | minikube | disabled     | 3rd party (unknown)            |
| portainer                   | minikube | disabled     | 3rd party (Portainer.io)       |
| registry                    | minikube | disabled     | minikube                       |
| registry-aliases            | minikube | disabled     | 3rd party (unknown)            |
| registry-creds              | minikube | disabled     | 3rd party (UPMC Enterprises)   |
| storage-provisioner         | minikube | enabled ✅   | minikube                       |
| storage-provisioner-gluster | minikube | disabled     | 3rd party (Gluster)            |
| storage-provisioner-rancher | minikube | disabled     | 3rd party (Rancher)            |
| volumesnapshots             | minikube | disabled     | Kubernetes                     |
|-----------------------------|----------|--------------|--------------------------------|
```

2. Включи аддон, например, metrics-server:

```sh
minikube addons enable metrics-server
```

Вывод будет примерно таким:

```sh
💡  metrics-server is an addon maintained by Kubernetes. For any concerns contact minikube on GitHub.
You can view the list of minikube maintainers at: https://github.com/kubernetes/minikube/blob/master/OWNERS
    ▪ Using image registry.k8s.io/metrics-server/metrics-server:v0.6.4
🌟  The 'metrics-server' addon is enabled
```

3. Просмотри Pod и Service, созданные при установке этого аддона:

```sh
kubectl get pod,svc -n kube-system
```

Вывод будет примерно таким:

```sh
NAME                                   READY   STATUS    RESTARTS   AGE
pod/coredns-5dd5756b68-dmhm5           1/1     Running   0          81m
pod/etcd-minikube                      1/1     Running   0          82m
pod/kube-apiserver-minikube            1/1     Running   0          82m
pod/kube-controller-manager-minikube   1/1     Running   0          82m
pod/kube-proxy-kkqpj                   1/1     Running   0          81m
pod/kube-scheduler-minikube            1/1     Running   0          82m
pod/metrics-server-7c66d45ddc-wvmrd    0/1     Running   0          68s
pod/storage-provisioner                1/1     Running   0          82m

NAME                     TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)                  AGE
service/kube-dns         ClusterIP   10.96.0.10      <none>        53/UDP,53/TCP,9153/TCP   82m
service/metrics-server   ClusterIP   10.99.236.151   <none>        443/TCP                  68s
```

4. Проверь вывод от metrics-server:

```sh
kubectl top pods
```

Вывод будет примерно таким:

```sh
NAME                         CPU(cores)   MEMORY(bytes)   
hello-node-ccf4b9788-7jdrm   1m           8Mi
```

Если увидим следующее сообщение, подожди и повтори попытку:

```sh
error: Metrics API not available
```

5. Отключи metrics-server:

```sh
minikube addons disable metrics-server
```

Вывод будет примерно таким:

```sh
🌑  "The 'metrics-server' addon is disabled
```

### Приберёмся за собой

Теперь можно очистить ресурсы, созданные в кластере:

```sh
kubectl delete service hello-node
kubectl delete deployment hello-node
```

Останови кластер Minikube:

```sh
minikube stop
```

По желанию удали виртуальную машину Minikube:

```sh
minikube delete
```

### Заключение

Рассмотрели основные аспекты создания и запуска кластера minikube. Теперь ты готов к развёртыванию приложений.

---

[Вернуться][main]


[main]: ../../README.md "содержание"
