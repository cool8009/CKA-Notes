---
tags: 
aliases:
  - namespaces
  - namespace
  - Namespace
---
![[Pasted image 20250319204930.png]]
- There is the default namespace.
- To isolate K8s core components needed for it to run, they run under the `kube-system` ns.
- Another default created NS is called `kube-public`. This is where resources that should be available to all users are hosted.
- NS serve isolation:
	![[Pasted image 20250319205141.png]]
- Each NS has it's own set of policies, quota of resources, etc.
- Inside the NS, resources can refer to each other just by their names.
- Outside, they have to append the NS name to the service name, like so:
		`db-service.dev.svc.cluster.local `
		`service-name.namespace.svc.cluster.local`
- When the service is created, a DNS entry is automatically created. This allows us to use this url.
	- ![[Pasted image 20250319205414.png]]
- `kubectl get pods` only lists pods in the default namespace. add `--namespace`.
- Same with creation: `kubectl create -f resource.yaml --namespace=myns`
- Or do this in the yaml:
	![[Pasted image 20250319205533.png]]
- Creating a namespace is done with a namespace definition file:
```
apiVersion: v1
kind: Namespace
metadata:
	name: dev
```
- Or by running `kubectl create namespace nsname`
- To change ns, as in, don't have to add `--namespace` for every command, use
  `kubectl config set-context $(kubectl config current-context) --namespace=dev `
- Now, when you run `get pods`, you won't have to specify ns for dev pods.
- To create a **resource quota** for a namespace, do this:
```
apiVersion: v1
kind: ResourceQuota
metadata:
	name: compute-quota
	namespace: dev
spec:
	hard:
		pods: 10
		requests.cpu: 4
		requests.memory: 5Gi
		...
```
`spec ` provides the limits.