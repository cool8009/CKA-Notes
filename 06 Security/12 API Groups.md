---
tags:
  - security
---
- We have been interacting with the API server in one way or another.
- We can access the API server in the master node address at port 6443:
```
curl https://kube-master:6443/version
```

- The response may look like:

```
{
  "major": "1",
  "minor": "13",
  "gitVersion": "v1.13.0",
  "gitCommit": "ddf47ac13c1a9483ea035a79cd7c1005ff21a6d",
  "gitTreeState": "clean",
  "buildDate": "2018-12-03T20:56:12Z",
  "goVersion": "go1.11.2",
  "compiler": "gc",
  "platform": "linux/amd64"
}
```

- Likewise, listing pods in the cluster involves accessing the `/api/v1/pods` endpoint.
- APIs in K8s are grouped into groups: 
- For instance, the `/version` endpoint provides cluster version data, while endpoints like `/metrics` and `/healthz` offer insights into the cluster’s performance and health.

![The image shows six colored labels with text: /metrics, /healthz, /version, /api, /apis, and /logs, each in a different color.](https://kodekloud.com/kk-media/image/upload/v1752869920/notes-assets/images/CKA-Certification-Course-Certified-Kubernetes-Administrator-API-Groups/frame_70.jpg)

This article focuses on two main API group categories:

1. **Core API Group:**  `/api`
    Contains the essential features of Kubernetes such as namespaces, pods, replication controllers, events, endpoints, nodes, bindings, persistent volumes, persistent volume claims, config maps, secrets, and services.
    
2. **Named API Groups:**  `/apis`
    Provides an organized structure for newer features. These groups include apps, extensions, networking, storage, authentication, and authorization. For example, under the apps group, you’ll find Deployments, ReplicaSets, and StatefulSets, whereas the networking group hosts resources such as Network Policies. Certificate-related resources like Certificate Signing Requests are also grouped under their relevant named groups.

- ![[Pasted image 20260106212615.jpg]]
- ![[Pasted image 20260106212622.jpg]]
- Each of these  resources has a set of actions associated with them.
- The K8s docs can tell you what API group for each object.\
- To retrieve the list of available API groups, access the API server's root endpoint on port 6443:

```
curl http://localhost:6443 -k
```

- The command returns a JSON response similar to:

```
{
  "paths": [
    "/api",
    "/api/v1",
    "/apis",
    "/apis/",
    "/healthz",
    "/logs",
    "/metrics",
    "/openapi/v2",
    "/swagger-2.0.0.json"
  ]
}
```

- When using `curl` without proper authentication, only selected endpoints (like `/version`) may be accessible. Unauthenticated requests to protected endpoints will result in a 403 Forbidden error.

- For example, an unauthenticated request may yield:

```
curl http://localhost:6443 -k
```

```
{
  "kind": "Status",
  "apiVersion": "v1",
  "metadata": {},
  "status": "Failure",
  "message": "forbidden: User \"system:anonymous\" cannot get path \"/\"",
  "reason": "Forbidden",
  "details": {},
  "code": 403
}
```

- To fully access the API server, use your certificate files with `curl`:

```
curl http://localhost:6443 -k \
  --key admin.key \
  --cert admin.crt \
  --cacert <your-ca-cert-file>
```

- You can start a `kubectl proxy` which starts a local HTTP proxy server on port 8001 and uses creds from your kubeconfig.
- The output confirms the proxy is running:

```
kubectl proxy
Starting to serve on 127.0.0.1:8001
```

- Now, you can access the API server through the proxy:

```
curl http://localhost:8001 -k
```

- The typical response should be:

```
{
  "paths": [
    "/api/",
    "/api/v1",
    "/apis",
    "/apis/",
    "/healthz",
    "/logs",
    "/metrics",
    "/openapi/v2",
    "/swagger-2.0.0.json"
  ]
}
```



- Remember that "kube proxy" and "kubectl proxy" serve different purposes. The former facilitates pod-to-pod and service communication within the cluster, while the latter is a local HTTP proxy for accessing the API server.