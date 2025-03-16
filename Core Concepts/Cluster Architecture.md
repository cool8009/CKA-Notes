Best analogy for Kubernetes is like ships.
The purpose of Kubernetes is to manage and host your containers in an automated fashion, so you can easily deploy as many as you need, and easily enable communication between [[services]]

- A cluster contains of [[nodes]]. There are the cargo ships which host the applications as containers, called [[worker nodes]]. There are also the [[master nodes]]. They are in charge of managing the worker nodes - managing, planning. monitoring, etc. There are different components called the [[control plane]].
- **[[ETCD]]** Cluster is a KV database that stores info about the current status, the different ships and what container is on each ship.
- **[[kube-scheduler]]** is like the crane: what container is loaded on each ship, what can and can't be, and when. Identifies based on resource requirements, node capacity or any other policy - [[taints]] and [[tolerations]], [[node affinity]] rules, etc.
- **[[Controllers]]** are like the offices, that take care of different areas. [[Node-Controller]] is responsible for onboarding new node to the [[cluster]], and [[Replication-Controller]] ensures that the desired amount of containers is running at all times. etc. take care of different responsibilities in cluster management.
- **[[kube-api]]** orchestrates this whole thing, and exposes the API which is used by external users to perform management operations on the cluster and controllers, to monitor and make necessary changes. Also for the worker nodes to communicate with the server.
- Everything can be a container. That's why we use a container runtime engine, like docker. 
- [[kubelet]] is the captain of a [[worker node]]. Every ship (worker node) has a captain, which manages all operations on the [[worker nodes]], incl. but not limited to: managing existing containers, loading new ones, relaying info to the master ([[kube-api]] and [[control plane]]). It's basically an agent that runs on the nodes. The [[kube-api]] server periodically fetches status updates from the [[kubelet]].
- [[kube-proxy]] is a service that runs on the [[worker node]], which allows different nodes and different services (like an application that needs to talk to a DB) to talk to each other.

![[Pasted image 20250125150243.png]]![[Pasted image 20250125150301.png]]