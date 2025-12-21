---
tags:
  - ALM
---
- With a lot of pod def files, managing env variables becomes difficult across all of them.
- We can use yoink the env vars from the pod def files and put them into a **ConfigMap.**
- 2 Phases:
  1. Configure ConfigMap
  2. Inject the vars into the pod.

- Use `kubectl create ConfigMap` or an apply command with a ConfigMap definition file.
- 
`kubectl create configmap app-config --from-literal=APP_COLOR=blue --from-literal=APP_MOD=prod`

- Or from a file:
`kubectl create configmap app-config --from-file=app_config.properties`
- With a declarative approach, you define your ConfigMap in a YAML file and apply it with kubectl. Here is an example ConfigMap definition:

```
apiVersion: v1
kind: ConfigMap
metadata:
  name: app-config
data:
  APP_COLOR: blue
  APP_MODE: prod
```
- For larger deployments, consider organizing multiple ConfigMaps by logical grouping, such as for your application, MySQL, and Redis:

|ConfigMap Name|Description|Sample Data|
|---|---|---|
|app-config|Application configuration|APP_COLOR: blue, APP_MODE: prod|
|mysql-config|MySQL database configuration|port: 3306, max_allowed_packet: 128M|
|redis-config|Redis server configuration|port: 6379, rdb-compression: yes|

- Naming ConfigMaps appropriately is essential because you will reference these names when associating them with pods.
- Once a ConfigMap is created, you can list it using:

```
kubectl get configmaps
```

- To check the stored configuration data, use the describe command:

```
kubectl describe configmaps
```

- The output will detail the key–value pairs stored in the ConfigMap, for example:

```
Name:           app-config
Namespace:      default
Labels:         <none>
Annotations:    <none>
Data
====
APP_COLOR:
----
blue
APP_MODE:
----
prod
Events:        <none>
```

- After creating a ConfigMap, configure your pod to use the configuration data. Below is an example pod definition that injects the `app-config` ConfigMap into the container as environment variables:

```
# pod-definition.yaml
apiVersion: v1
kind: Pod
metadata:
  name: simple-webapp-color
  labels:
    name: simple-webapp-color
spec:
  containers:
    - name: simple-webapp-color
      image: simple-webapp-color
      ports:
        - containerPort: 8080
  envFrom: #this is what injects the env vars from the configmap to the webapp
    - configMapRef:
        name: app-config
```

- The corresponding ConfigMap definition might look like this:

```
# config-map.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: app-config
data:
  APP_COLOR: blue
  APP_MODE: production
```

- When you create the pod with this configuration, your web application receives the configured environment variables automatically.
- ## Alternative Injection Methods

- In addition to using `envFrom`, there are other methods to inject configuration data from ConfigMaps into your pods. You can inject a single environment variable using the `valueFrom` property or mount the entire ConfigMap as a volume. For example:

```
envFrom:
  - configMapRef:
      name: app-config


env:
  - name: APP_COLOR
    valueFrom:
      configMapKeyRef:
        name: app-config
        key: APP_COLOR


volumes:
  - name: app-config-volume
    configMap:
      name: app-config
```

- Each method provides flexibility to fit the design of your application, whether you need specific environment variables or a complete set of configuration files mounted as volumes.
