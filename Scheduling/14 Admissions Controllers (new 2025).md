---
aliases:
  - Admission Controllers
  - Admission Controller
  - admission controllers
  - admission controller
tags:
  - scheduling
---
- We have been using the `kubectl` util to run commands.
- We know that every time we use it, the request goes to the api server, the pod is created, and the information is persisted in the etcd database.
- When a request happens, it is also authenticated, usually via certificates.
- If it was sent through kubectl, we know the kubeconfig has the certificates already configured, and the **authn** process is responsible on making sure the user who sent the requests is valid.
  Consider the following configuration:

```
> cat ~/.kube/config
apiVersion: v1
clusters:
- cluster:
    certificate-authority-data: LS0tCIlRjdG......BQyMjAwFURs9tCg==
    server: https://example.com
  name: example-cluster
```
- Afterwards, the req goes through an **authz** process, to make sure that the user has the required **premissions** to do the task. This perms are governed via RBAC.
  For instance, if a user is assigned the following role:

```
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: developer
rules:
- apiGroups: [""]
  resources: ["pods"]
  verbs: ["list", "get", "create", "update", "delete"]
```

- The user is permitted to list, get, create, update, or delete pods. RBAC can also restrict access to specific resource names or namespaces:

```
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: developer
rules:
- apiGroups: [""]
  resources: ["pods"]
  verbs: ["create"]
  resourceNames: ["blue", "orange"]
```
- ![[Pasted image 20250922154351.png]] These are the rules from the yaml.
- These RBAC rules are enforced at the API level and determine which API operations a user can access.

## The Role of Admission Controllers

- While RBAC handles basic authorization, it does not offer advanced validations or mutations. Admission controllers step in to provide additional security by:

	- Validating pod specifications (e.g., ensuring that images are not from a public Docker Hub registry or enforcing the prohibition of the "latest" tag).
	- Rejecting pods running containers as the root user, or enforcing specific Linux capabilities.
	- Ensuring required metadata like labels is included.
	  ![[Pasted image 20250922154552.png]]


- **Admissions Controllers** are a step after **authn & authz** in the request. Some come prebuilt in K8s:
  ![[Pasted image 20250922154724.png]]
	 - **AlwaysPullImages:** Forces image pulling on each pod creation.
	- **DefaultStorageClass:** Automatically assigns a default storage class to PVCs if none is specified.
	- **EventRateLimit:** Limits the number of concurrent API server requests to prevent overload.
	- **NamespaceExists:** Rejects requests to operate in non-existent namespaces.

- And many more.
- An in depth example:
	 - Say we wanna create a pod in a namespace called `blue` that doesn't exist.
	 - If I run `kubectl run nginx --image nginx --namespace blue`, this will throw an error.
	 - In this example, my req gets **authn, authz** but doesn't pass the **admission controller**, specifically the `NamespaceExists` one.
	 - Alternatively, Kubernetes offers the NamespaceAutoProvision admission controller (not enabled by default) to automatically create a missing namespace.

- To check the enabled admission controllers, run:

```
kube-apiserver -h | grep enable-admission-plugins
```

 - This command lists the active admission plugins, including defaults such as NamespaceLifecycle, LimitRanger, ServiceAccount, among others.
 - If running with a kubeadm based setup, this command must be ran inside the control plane pod:
   `kubectl exec kube-apiserver-controlplane -n kube-system -- kube-apiserver -h | grep enable-admission-plugins


## Adding an Admission Controller

- To add an AC, update the `--enable-adminssion-plugins` flag on the Kube API server service. For a kubeadm-based setup, modify the kube-apiserver manifest file.
- Traditional Kube API Server Service

```
ExecStart=/usr/local/bin/kube-apiserver \
    --advertise-address=${INTERNAL_IP} \
    --allow-privileged=true \
    --apiserver-count=3 \
    --authorization-mode=Node,RBAC \
    --bind-address=0.0.0.0 \
    --enable-swagger-ui=true \
    --etcd-servers=https://127.0.0.1:2379 \
    --event-ttl=1h \
    --runtime-config=api/all \
    --service-cluster-ip-range=10.32.0.0/24 \
    --service-node-port-range=30000-32767 \
    --v=2 \
    --enable-admission-plugins=NodeRestriction,NamespaceAutoProvision
```

- Kubeadm-Based Setup (API Server as a Pod)

```
apiVersion: v1
kind: Pod
metadata:
  creationTimestamp: null
  name: kube-apiserver
  namespace: kube-system
spec:
  containers:
  - command:
    - kube-apiserver
    - --authorization-mode=Node,RBAC
    - --advertise-address=172.17.0.107
    - --allow-privileged=true
    - --enable-bootstrap-token-auth=true
    - --enable-admission-plugins=NodeRestriction,NamespaceAutoProvision
    image: k8s.gcr.io/kube-apiserver-amd64:v1.11.3
    name: kube-apiserver
```
- To disable specific admission controllers, use the `disable-admission-plugins` flag in a similar manner.
- ### Auto-Provisioning a Namespace

- Once the admission controller is correctly configured, executing the pod creation command in a previously non-existent namespace "blue" will trigger the NamespaceAutoProvision controller, which will automatically create the namespace and allow the pod creation to succeed. For example:

```
kubectl run nginx --image nginx --namespace blue
Pod/nginx created!
```

- Listing the namespaces confirms the creation of "blue":

```
kubectl get namespaces
NAME         STATUS   AGE
blue         Active   3m
default      Active   23m
kube-public  Active   24m
kube-system  Active   24m
```

## Transition from Deprecated Controllers

It is important to note that the **NamespaceAutoProvision** and **NamespaceExists** admission controllers have been deprecated. They have been replaced by the **NamespaceLifecycle** admission controller, which:

- Rejects requests to non-existent namespaces.
- Protects default namespaces (default, kube-system, kube-public) from deletion.

This ensures a robust and consistent namespace management mechanism.