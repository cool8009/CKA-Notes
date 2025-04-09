---
tags:
  - scheduling
aliases:
  - manual scheduling
  - Manual Scheduling
---
- What if we don't have a scheduler in our cluster? We probably don't want to rely on a built in one, and do it manually.
- 
- POD manifest files have an extra property we can provide called `nodeName`:
```
	apiVersion: v1 
	kind: Pod
	metadata: 
	  name: nginx
	  labels: 
		  name: nginx
	
	spec:
		containers:
		-  name: nginx
		   image: nginx
		   ports:
		     - containerPort: 8080
	nodeName:
```
- If you don't specify this field, K8s will add it automatically.
- The scheduler looks through all the PODs, and looks for those that don't have this property set.
- When it finds them, those are the candidates for scheduling.
- ![[Pasted image 20250324203039.png]]
- If there's not scheduler, PODs won't be assigned and will be stuck in a Pending state. To fix this, you can manually set the `nodeName` field to the name of the node you want to schedule the [[10 POD]] on. The POD then gets assigned to the specified node.
- You can do it only at creation time. 
- What happens if the POD is already created? K8s won't allow you to modify the property.
- Another way is to create a **binding object** and send **a POST request to the PODs binding API**. This will mimic what the actual scheduler does. 
- ```
```
apiVersion: v1 
kind: Binding
metadata: 
  name: nginx
  target: 
	  apiVersion: v1
	  kind: Node
	  name: The name of the node you wanna bind to.
```

- Send it as a JSON format.
- **The scheduler runs as a POD in the kube-system namespace.**

