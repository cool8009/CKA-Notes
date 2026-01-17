---
tags:
  - security
---
- We talked about Authn. 
- We saw how to get access to the cluster: certs, CAs etc.
- But once you get access, WHAT can you do?
- Once a user gains access, authorization ensures they only have the appropriate permissions for their role. For example, a cluster administrator can view various objects such as Pods, Nodes, and Deployments:

```
kubectl get pods
NAME    READY   STATUS    RESTARTS   AGE
nginx   1/1     Running   0          53s


kubectl get nodes
NAME        STATUS   ROLES     AGE     VERSION
worker-1    Ready    <none>    5d21h   v1.13.0
worker-2    Ready    <none>    5d21h   v1.13.0


kubec
```

- Administrators have full control, allowing them to create or delete objects like Pods or Nodes. As the cluster scales and more users—including administrators, developers, testers, or external applications like monitoring tools and [Jenkins](https://learn.kodekloud.com/user/courses/jenkins) —access the system, it is critical to provide only the access level necessary for each user’s role. 
- For instance, developers might be limited to deploying applications without the ability to modify the overall cluster configuration.
- Below is an example demonstrating operations executed with limited permissions:

```
kubectl get pods
NAME    READY   STATUS    RESTARTS   AGE
nginx   1/1     Running   0          53s


kubectl get nodes
NAME       STATUS   ROLES     AGE     VERSION
worker-1   Ready    <none>    5d21h   v1.13.0
worker-2   Ready    <none>    5d21h   v1.13.0


kubectl delete node worker-2
Node worker-2 Deleted!
```

- In contrast, attempting similar operations without sufficient privileges results in the following responses:

```
kubectl get pods
Error from server (Forbidden): pods is forbidden: User "Bot-1" cannot list "pods"


kubectl get nodes
Error from server (Forbidden): nodes is forbidden: User "Bot-1" cannot get "nodes"


kubectl delete node worker-2
Error from server (Forbidden): nodes "worker-2" is forbidden: User "developer" cannot delete resource "nodes"
```

- When sharing a cluster across different organizations or teams using namespaces, authorization restricts users to their designated namespaces. Kubernetes supports multiple authorization mechanisms, including:

	- Node Authorization
	- Attribute-Based Authorization (ABAC)
	- Role-Based Access Control (RBAC)
	- Webhook Authorization

-  We know that both users and kubelets access the API server.
- The kubelet accesses the server for R/W operations. ![[Pasted image 20260110201612.jpg]]
- Requests from kubelets—typically using certificates with names prefixed by "system: node" as part of the `system:nodes` group—are authorized by a special component known as the **node authorizer**. The following diagram explains the authorization process for kubelet requests:
- ![[Pasted image 20260110201645.jpg]]
- This is an example of **node authorization.** Access from within the cluster, via the `system:node` prefix in the cert CN (common name).
- **An example of ABAC (attribute based authz):**
	- ABAC associates a user or a group a set of permissions.
	- For example, you can grant a user called "dev-user" permissions to view, create, and delete pods. 
	- This is achieved by creating a policy file in JSON format and passing it to the API server. Consider the following example policy file:
	
	```
	{"kind": "Policy", "spec": {"user": "dev-user", "namespace": "*", "resource": "pods", "apiGroup": "*"}}
	{"kind": "Policy", "spec": {"user": "dev-user-2", "namespace": "*", "resource": "pods", "apiGroup": "*"}}
	{"kind": "Policy", "spec": {"group": "dev-users", "namespace": "*", "resource": "pods", "apiGroup": "*"}}
	{"kind": "Policy", "spec": {"user": "security-1", "namespace": "*", "resource": "csr", "apiGroup": "*"}}
	```
	
	- Each time security requirements change, you must manually update this policy file and restart the Kube API Server. This manual process can be tedious and set the stage for more streamlined methods such as Role-Based Access Control (RBAC).

- **An example of RBAC:**
	- Instead of directly associating a user or a group a set of perms, we define a **role**.
	- The role has a set of perms, and we assign all the relevant people to that role.
	- ![[Pasted image 20260110201949.jpg]]
	- RBAC is considered the standard method for managing access within a Kubernetes cluster. The diagram below provides a visual representation of RBAC across different roles.
	- For example, you can create a "developer" role that encompasses only the necessary permissions for application deployment. Developers are then associated with this role, and modifications in user access can be handled by updating the role, affecting all associated users immediately.

- **External Authz Mechanisms:**
	- If you prefer managing authorization externally rather than with built-in Kubernetes mechanisms, third-party tools like [Open Policy Agent (OPA)](https://www.openpolicyagent.org/) are an excellent choice. OPA can handle both admission control and authorization by processing user details and access requirements sent via API calls from Kubernetes. Based on OPA’s response, access is either granted or denied.
- **AlwaysAllow and AlwaysDeny**:
	- AA allows all request w/o checks, and AD denies all requests w/o checks.
	- These modes are configured using the authorization-mode option on the Kube API Server and are crucial when determining which authorization mechanism is active. 
	- In cases where no mode is specified, AlwaysAllow is used by default.

	- Below is an example configuration using AlwaysAllow:
	
	```
	ExecStart=/usr/local/bin/kube-apiserver \\
	  --advertise-address=${INTERNAL_IP} \\
	  --allow-privileged=true \\
	  --apiserver-count=3 \\
	  --authorization-mode=AlwaysAllow \\
	  --bind-address=0.0.0.0 \\
	  --enable-swagger-ui=true \\
	  --etcd-cafile=/var/lib/kubernetes/ca.pem \\
	  --etcd-certfile=/var/lib/kubernetes/apiserver-etcd-client.crt \\
	  --etcd-keyfile=/var/lib/kubernetes/apiserver-etcd-client.key \\
	  --etcd-servers=https://127.0.0.1:2379 \\
	  --event-ttl=1h \\
	  --kubelet-certificate-authority=/var/lib/kubernetes/ca.pem \\
	  --kubelet-client-certificate=/var/lib/kubernetes/apiserver-etcd-client.crt \\
	  --kubelet-client-key=/var/lib/kubernetes/apiserver-etcd-client.key \\
	  --service-node-port-range=30000-32767 \\
	  --client-ca-file=/var/lib/kubernetes/ca.pem \\
	  --tls-cert-file=/var/lib/kubernetes/apiserver.crt \\
	  --tls-private-key-file=/var/lib/kubernetes/apiserver.key \\
	  -v=2
	```
	
	- You can also specify a comma-separated list of multiple authorization modes. For example, to configure node authorization, RBAC, and webhook authorization, set the parameter as follows:
	
	```
	ExecStart=/usr/local/bin/kube-apiserver \\
	  --advertise-address=${INTERNAL_IP} \\
	  --allow-privileged=true \\
	  --apiserver-count=3 \\
	  --authorization-mode=Node,RBAC,Webhook \\
	  --bind-address=0.0.0.0 \\
	  --enable-swagger-ui=true \\
	  --etcd-cafile=/var/lib/kubernetes/ca.pem \\
	  --etcd-certfile=/var/lib/kubernetes/apiserver-etcd-client.crt \\
	  --etcd-keyfile=/var/lib/kubernetes/apiserver-etcd-client.key \\
	  --etcd-servers=https://127.0.0.1:2379 \\
	  --event-ttl=1h \\
	  --kubelet-certificate-authority=/var/lib/kubernetes/ca.crt \\
	  --tls-cert-file=/var/lib/kubernetes/apiserver.crt \\
	  --tls-private-key-file=/var/lib/kubernetes/apiserver.key \\
	  --v=2
	```
	
	- **When multiple modes are configured, each request is processed sequentially in the order specified.** For example, a user’s request is first evaluated by the node authorizer. If the request does not pertain to node-specific actions and is consequently denied, it is then passed to the next module, such as RBAC. Once a module approves the request, further checks are bypassed and the user is granted access.
	- **For each request, the authz is determined by the order of the types of authz modes. If a request fails, the next authz mode is checking the request, until it is succesful.**