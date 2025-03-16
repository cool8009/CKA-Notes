---
aliases:
  - pod
  - pods
  - POD
  - PODS
  - PODs
tags:
  - pod
  - pods
---
- Before we understand pods, we have to assume the app is developed and built into a docker image.
- We also assume the cluster is set up and working.
- All the [[services]] need to be in a running state. Single node or multi node, doesn't matter.
- Our ultimate aim with K8s, as discussed before, is to deploy our app in the form of containers in a cluster, on the worker nodes. However, K8s doesn't actually deploy the containers directly on the nodes.
- They are instead encapsulated in PODs, which is **a single instance of an application.**
- This is the smallest object you can create in K8s.
- This is the simplest example:
	![[Pasted image 20250316105459.png]]
- A single instance of my application, inside a container, inside a pod, inside a single node K8s cluster.
- What if we need to scale up for new users of our app? Where do we create an additional container? We don't create it in the same POD, as a POD is a single application. Instead, we create a new POD in the [[nodes]], or a new node entirely:
- ![[Pasted image 20250316110356.png]]
- PODs usually have a 1:1 relationship with the containers. 
- **Multi container PODs** are possible, just usually it's not for containers of the same kind. If our intention is to scale our application, then putting 2 of the same app in one POD is not the way to go.
- Sometimes we might have a scenario when we need a helper container, such as something that provides a service for our web application, like processing user data. In that case, we might place 2 of the containers in the same POD to live alongside each other:
	![[Pasted image 20250316110650.png]]
- This ensure that when we spin up the POD, these 2 containers will spin up together. They can also access each other via localhost.
- They share network and storage space and fate.
- Multi container pods are usually a niche use case.
- To deploy PODS use `kubectl run nginx --image <url-to-image or image name>`.
- To see a list of PODS use `kubectl get pods`.
- 