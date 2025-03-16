---
tags:
  - yaml
  - pods
---

- K8s uses YAML files for defining objects. They follow a similar structure:
		```apiVersion: v1 #version of K8s API to create the object.
		kind: Pod #object type
		metadata: #metadata of the pod. Note the indentation.
		  name: myapp-pod
		  labels: #dictionary with any KV you want.
			  app: myapp
			  type: front-end 
		
		spec: #specifies what we need for the object
			containers: #list/array
			 - name: nginx-container
			 image: nginx
- They are required.
- `kubectl describe pod myapp-pod` to view info on specific pod.