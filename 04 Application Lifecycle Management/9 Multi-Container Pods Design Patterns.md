---
tags:
  - ALM
---
- There are different patterns for multi container pods.
- The basic one, that we spoke about in prev lesson is called co-located containers. Both containers are meant to continue to run during the pod lifecycle.
- The next one is **init containers** - when there's init steps to be taken by one container before the other one, like an init container that waits for the database to be ready before starting the main app. **The init container does its job, ends it, and then the main app starts**.
- Sidecar containers is like an init container, but the sidecar keeps running throughout the lifecycle of the pod. This is useful for like a log shipper, that both needs to start before the main app and also run during it.
- ![[Pasted image 20251201220959.png]]
- **The difference between the 1st pattern and the 3rd pattern, is that despite they both share the pod lifecycle, the 1st pattern has NO way to control startup order.
- To create a multi-container pod, add the configuration for the new container under the `containers` array in your pod definition file. For instance, you can incorporate a container named "log-agent" alongside an existing web application container. The following YAML snippet demonstrates how to configure a pod that contains both a web application and its corresponding logging agent:

```
apiVersion: v1
kind: Pod
metadata:
  name: simple-webapp
  labels:
    name: simple-webapp
spec:
  containers:
    - name: simple-webapp
      image: simple-webapp
      ports:
        - containerPort: 8080
    - name: log-agent
      image: log-agent
```
- In order to create a init container:
- 

```
	apiVersion: v1
	kind: Pod
	metadata:
	  name: simple-webapp
	  labels:
	    name: simple-webapp
	spec:
	  containers:
	    - name: simple-webapp
	      image: simple-webapp
	      ports:
	        - containerPort: 8080
	    initContainers:
	    - name: db-checker
	      image: busybox
	      command: 'waitforstart.sh'
	      #Note the initContainers field.
	      
	    - name: api-checker
	      image: busybox
	      command: 'waitforstart.sh'
	      #Note that you can have multiple.
```
- In order to create a sidecar:
```
	apiVersion: v1
	kind: Pod
	metadata:
	  name: simple-webapp
	  labels:
	    name: simple-webapp
	spec:
	  containers:
	    - name: simple-webapp
	      image: simple-webapp
	      ports:
	        - containerPort: 8080
	    initContainers:
	    - name: logshipper
	      image: busybox
	      command: 'waitforstart.sh'
	      restartPolicy: always
	      #Note the initContainers field WITH the restartpolicy.
    
```
- irl example:
- ![[Pasted image 20251201221748.png]]
- In this case, we add a Filebeat sidecar so that the main app startup and shutdown logs are always caught, and sent to ES.