
- Within a cluster, every POD can reach every other POD.
- This is accomplished by deploying a [[POD]] networking solution. This is a virtual network that spans across all nodes in the cluster to which all the pods connect.
- Through this network, they're able to communicate.
- There are many solution available for that.
- For example, a web app deployed on a node and a DB deployed on a different node. They can reach each other by using the IP of the POD.
- There is though, **no guarantee** that the IP won't change. 
- Therefore, a better way to expose the database is to use a service, let's call it **db**.
- The service also gets an IP, and whenever a POD tries to reach the service, it forwards the request to the backend POD, in this case, the database itself.
- But what is this service?
- It's not a container or something that lives in the network. It doesn't have a listener or something. It's a **virtual component that lives in K8s memory, and doesn't actually "exist".**
- But how is it accessible across the cluster from any node? This is where **kube-proxy** comes in.
- It's a process that runs on each node in the cluster. It's job is to look for new services, and once those are created, it creates the **appropriate rules on each node to forward traffic to those services, to the backend [[POD]]s:**
  ![[Pasted image 20250125182342.png]]
- One way it does this is using **IPTABLES** rules. In this case, it creates a rule on each node to forward traffic heading to the IP of the service, to the IP of the actual POD:
  ![[Pasted image 20250125182504.png]]
- That's how kube-proxy configures a service. We will discuss this later in the course.
- To install kube-proxy is the same, run as a service.
- With [[kubeadm]], it is deployed as a [[daemonset]], so it will be deployed on each node in the cluster.  