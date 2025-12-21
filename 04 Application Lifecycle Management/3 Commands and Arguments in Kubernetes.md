---
tags:
  - ALM
---
- We created a simple docker image in the prev lecture.
- We will now create a pod with this image:
- ```
  apiVersion: v1
  kind: Pod
  metadata:
	  name: ubuntu-sleeper-pod
	spec:
		containers:
		  - name: ubuntu-sleeper
		    image: ubuntu-sleeper
		    command: ["sleep2.0"] this is the ENTRYPOINT instruction
		    args: ["10"] #this is appended to the container as an arg
	#additional args in the pod def file
  ```
- `kubectl create -f pod-definition.yml` will cause the `args` field to override the `CMD` field in the docker command, and the `command` field will override the `ENTRYPOINT`
- 
- 