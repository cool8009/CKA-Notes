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
  - NodePort
  - nodeport
  - nodeports
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

- If you don't provide a `targetPort`, it's assumed to be the same as `port`.
- If you don't provide a `nodePort`, a free port in the range 30000 - 32767 will be selected.
- You can have multiple such mappings within a single service.
- One thing is missing. We specified a targetPort, but didn't tell it which POD is the target. There could be infinite PODs with port 80 listening.
- As we did previously and how do a lot in K8s, we will use **labels and selectors** to link these together in the  `spec`:
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
- Use the same selectors from the pod definition file. This links the service to the POD.
- `kubectl create -f service-def.yaml`
- `kubectl get services`
- In a prod environment, you will have multiple PODs running the same application for HA and load balancing. What do you do then?
- The service automatically selects the amount of PODs relevant, based on the selectors, and forwards requests to them. No additional configuration needed!
- The algorithm it uses to decide to which POD to forward traffic to, it's random.
- This makes the NodePort service a built in load balancer:
	![[Pasted image 20250319200809.png]]
- If we have our application running on PODs across **different nodes**, K8s automatically creates a service that spans all the nodes in the cluster, **and maps the TargetPort to the same NodePort as all the nodes in the cluster:**
	- ![[Pasted image 20250319201039.png]]
- This way, you can access your app using the IP of any node in the cluster, and with the same port number.
- No matter the cluster configuration, the service is created and behaves exactly the same, without having to do any additional steps during the service creation.
- When PODs are removed or created, the service adapts automatically.
- **Once created, you typically won't have to make any additional configuration changes.**