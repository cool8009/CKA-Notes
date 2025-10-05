---
tags:
  - service
  - services
  - pods
  - yaml
aliases:
  - Cluster IP
  - cluster ip
  - CIP
  - cip
---

- A full stack web app, typically has different kinds of PODs, hosting different kinds of apps. Front end, back end, database, etc. They all need to communicate.
- What is the right way to establish connectivity between the tiers?
- All PODs have IP addresses, but these addresses are **not** static. PODs are created and destroyed all the time, so you can't rely on a POD's IP address for comms.
- Also, how does a front end POD know which backend POD to communicate with? Which BE pod does it go to, and who makes that decision?
- A service can help us group all the PODs in a tier, and allow access to them as a single group via an interface. This will allow external PODs to access the group via the service.
- Requests are forwarded randomly inside the group to one of the PODs.
- This allows us to easily and effectively deploy microservices.
- Each layer, or tier, can move and scale as much as it needs to, without affecting other layers. Each pod can access a different layer by just accessing the service.
- This service is known as a **Cluster IP**.
	- ![[Pasted image 20250319201820.png]]
- Use a service def file to create this service:

```
apiVersion: v1
kind: Service
metadata:
  name: backend
spec:
	type: ClusterIP #the default type
	ports:
	  - targetPort: 80 #list/array 
		port: 80
```
- `targetPort` is the port where the backend is exposed, and `port` is where the service is exposed.
- Again, to link the service to a set of pods, we will use a `selector`:
```
spec:
	type: NodePort #service type
	ports:
	
	  - targetPort: 80 #list/array 
		port: 80
		nodePort: 30008
	selector:
		app: myapp
		type: front-end
```
- `kubectl create -f def.yaml`
- `kubectl get services`