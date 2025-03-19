---
tags:
  - service
  - services
  - yaml
aliases:
  - service
  - services
  - Services
  - Service
---
- Enable comms between various components within or outside the application.
- Helps us connect apps together with other apps or users.
- For example, our app has groups of pods running various section: for serving front end loads, for back end, and for connecting to an external data source.
- Services enable connectivity between the groups of PODs:
	![[Pasted image 20250317202314.png]]
- Thus, they enable **loose coupling** between microservices in our app.
- Let's talk about one use case, external communication. The node has an IP address, my laptop is on the same network, but the internal POD has it's own network with it's own IP. I can't currently ping or access the POD at it's IP address:
	![[Pasted image 20250317202456.png]]
- How do we see the webpage? We can:
	- SSH to the node and view the website, but this is from inside the node.
	- Or something between our laptop to the node and the POD to help us make this connection.

- This is where the Service comes in to play. This is an **object**, and one of it's use cases is to listen on a port and forward traffic from that port, to the port on the POD running the web app.
- This service is known as a **NodePort** service:
	![[Pasted image 20250317202739.png]]
- There are other kinds of services available.
- **Cluster IP** is also a service, which creates a **virtual IP** in the cluster to enable communication.
- **Load Balancer** is also a service, which provisions an LB.
- ![[Pasted image 20250317202938.png]]
- We will discuss NodePort for now.
- It's basically a virtual server inside the node. Inside the cluster, it has it's own IP address which is called **cluster IP of the service.**
- Let's take a closer look at the service. There are 3 ports involved (these are referred from the viewpoint of the service itself): 
		- **Target port**: the port running on the node, the service forwards the requests to this.
		- **Port**: the port of the service itself.
		- **NodePort**: The port on the node itself, used to access the web server externally. Can only be in a valid range, which is 30000 - 37k something,.
		-![[Pasted image 20250317203313.png]]
- To create the service, we use a definition file:
```
apiVersion: v1
kind: Service
metadata:
  name: myapp-service
spec:
	type: NodePort #service type
	ports:
	
	  - targetPort: 80 #list/array 
		port: 80
		nodePort: 30008
		
	```