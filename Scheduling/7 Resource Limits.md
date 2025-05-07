---
tags:
  - scheduling
aliases: []
---
- Let's look at a 3 node cluster. Each node has a set of CPU and RAM resources available.
- ![[Pasted image 20250507215022.png]]
- Every POD requires resources to run. When a pod is placed on a node, it consumes the resources available on that node.
- The decisions to place which pod where is done by the [[07 kube-scheduler|kube-scheduler]].
- The Kubernetes scheduler decides which node will host the pod by evaluating the requested resources against what each node can offer. If, for example, Node 2 has sufficient capacity, the scheduler assigns the pod there. Otherwise, if no node meets the requirements, the pod remains in a pending state. You can inspect pod events using the command `kubectl describe pod`, which may reveal messages like this when resources (such as CPU) are insufficient:

```
NAME              READY   STATUS    RESTARTS   AGE
Nginx             0/1     Pending   0          7m
Events:
  Reason           Message
  ------           -------
  FailedScheduling  No nodes are available that match all of the following predicates: insufficient cpu.
```
- You can define the minimum resources required for a POD in the definition file:
  Below is an example snippet of a pod definition with resource requests set to 4 Gi of memory and 2 CPU cores:

```
apiVersion: v1
kind: Pod
metadata:
  name: simple-webapp-color
  labels:
    name: simple-webapp-color
spec:
  containers:
  - name: simple-webapp-color
    image: simple-webapp-color
    ports:
    - containerPort: 8080
    resources:
      requests:
        memory: "4Gi"
        cpu: 2
```

- When a pod gets placed on a node, it gets **guaranteed** that amount of resources for it.
- **Remember, it is possible to use fractional CPU values. For example, 0.1 CPU is equivalent to 100m (where "m" denotes milli, meaning 0.001 of a CPU). One CPU core is typically equivalent to one vCPU in cloud environments like AWS, GCP, or Azure.**
- **Note these differences:**
  ![[Pasted image 20250507215615.png]]
- By default a container has no limit on the resources it will consume if it has the space. You can also specify an upper **maximum limit**.
- Note that while CPU usage is throttled when a pod reaches its limit, **memory usage is not**. If a pod exceeds its memory limit, it may be terminated due to an Out Of Memory (OOM) error.
- Below is an example of a pod definition that includes both resource requests and limits for memory and CPU:

```
apiVersion: v1
kind: Pod
metadata:
  name: simple-webapp-color
  labels:
    name: simple-webapp-color
spec:
  containers:
  - name: simple-webapp-color
    image: simple-webapp-color
    ports:
    - containerPort: 8080
    resources:
      requests:
        memory: "1Gi"
        cpu: 1
      limits:
        memory: "2Gi"
        cpu: 2
```

- ## Default Behavior and Scenarios

- By default, Kubernetes does not enforce CPU or memory requests and limits. This means a pod without specified limits can consume all available resources on its node, potentially affecting other pods and system processes.

- Below are several scenarios for CPU configurations:

1. **No Requests or Limits:**  
    A container can utilize all available CPU, potentially starving other pods.
2. **Limits Specified Without Requests:**  
    Kubernetes assumes the request value is equal to the limit (e.g., setting a limit of 3 vCPUs results in a request of 3 vCPUs).
3. **Both Requests and Limits Defined:**  
    The container is guaranteed its requested amount (e.g., 1 vCPU) but can use additional CPU up to its defined limit (e.g., 3 vCPUs).
4. **Requests Defined Without Limits:**  
    The container is guaranteed its requested CPU value, with access to additional cycles if available, which allows for efficient utilization of idle resources.

- Similar configurations apply for memory:

- Without any resource configurations, a single pod may monopolize node memory.
- When only limits are specified, Kubernetes sets the memory request equal to the limit.
- With both requests and limits, the pod is allocated a guaranteed memory amount and can burst up to the limit.
- Only specifying requests guarantees the pod a base amount of memory but might let it consume more, potentially leading to termination if memory usage becomes excessive.
![[Pasted image 20250507220956.png]]![[Pasted image 20250507221001.png]]

- By default, Kubernetes does not enforce resource requests or limits on pods. To ensure that every pod in a namespace receives default resource settings, you can define a LimitRange. **LimitRanges** are namespace-level objects that **automatically assign default resource values** to containers that do not specify them.
- For example, you can create a LimitRange to enforce CPU constraints:

```
# limit-range-cpu.yaml
apiVersion: v1
kind: LimitRange
metadata:
  name: cpu-resource-constraint
spec:
  limits:
    - default:
        cpu: 500m
      defaultRequest:
        cpu: 500m
      max:
        cpu: "1"
      min:
        cpu: 100m
      type: Container
```

- Likewise, to set memory constraints, use the following configuration:

```
# limit-range-memory.yaml
apiVersion: v1
kind: LimitRange
metadata:
  name: memory-resource-constraint
spec:
  limits:
    - default:
        memory: 1Gi
      defaultRequest:
        memory: 1Gi
      max:
        memory: 1Gi
      min:
        memory: 500Mi
      type: Container
```

**Keep in mind that changes to a LimitRange affect only new pods created after the LimitRange is applied or updated.**


- **To restrict the total amount of resources consumed by the entire namespace, use Resource Quotas. **
- Resource Quotas allow you to restrict the overall resource consumption for all applications within a namespace. By setting a Resource Quota, you can define hard limits on the aggregate consumption—such as restricting total CPU requests to 4 vCPUs and total memory to 4 GB, while also defining maximum limits (for example, 10 vCPUs and 10 GB) across all pods.

- This approach helps maintain balanced resource allocation within a namespace even if individual pods lack explicit limits.
- ![[Pasted image 20250507221801.png]]