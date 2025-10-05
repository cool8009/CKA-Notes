---
tags:
  - scheduling
aliases:
  - priority class
---
- We know the K8s runs different applications as PODs with different priorities.
- We know that the control plane components are the highest priority and need to always be up and running.
- Similarly, we might have high importance databases, critical apps and maybe lower priority background jobs running as well:
  
- ![[Pasted image 20250825085931.png]]
- We need a way to make sure that higher priority workloads will take precedence over lower priority ones. This is **priority classes**.
- Priority classes help us define priorities for different workloads, so that higher priority workloads always get priority over lower ones. **If a higher priority pod can't be scheduled, the scheduler will terminate a lower priority one to make it happen.**
- PC's (priority classes) are non-namespaced object. 
- Once they're created they're able to be configured on any POD in any namespace.
- We define priority using a **range of numbers**, between 1 billion and negative 2 billion. This is the range for **application deployed on the cluster.**
- There is a separate range: between **1 billion and 2 billion** which is reserved for **system applications only** - like control plane stuff.
- ![[Pasted image 20250825090530.png]]
- Run `kubectl get priorityclass` to view them, incl. the system ones.
- The output may appear as follows:

```
NAME                      VALUE          GLOBAL-DEFAULT   AGE     PREEMPTIONPOLICY
system-cluster-critical   2000000000     false            7m33s   PreemptLowerPriority
system-node-critical      2000010000     false            7m33s   PreemptLowerPriority
```
- To create a new priority class, define an object with the API version `scheduling.k8s.io/v1`, set the kind to `PriorityClass`, and include metadata with a name, numerical value, and an optional description. For example:

```
apiVersion: scheduling.k8s.io/v1
kind: PriorityClass
metadata:
  name: high-priority
value: 1000000000
description: "Priority class for mission critical pods"
```
- To use the PC in your POD def file, use the name you gave in the PC yaml in your POD def file like so:

```
# priority-class.yaml
apiVersion: scheduling.k8s.io/v1
kind: PriorityClass
metadata:
  name: high-priority
value: 1000000000
description: "Priority class for mission critical pods"
globalDefault: true


# pod-definition.yaml
apiVersion: v1
kind: Pod
metadata:
  name: nginx
  labels:
    app: nginx
spec:
  containers:
    - name: nginx
      image: nginx
      ports:
        - containerPort: 8080
  priorityClassName: high-priority
```

- If you don't specify a priority for a POD, the default is 0.
- To change the default priority for Pods, create a priority class with the **`globalDefault` property set to `true`**. Note that only one priority class can be marked as the global default.
## POD Priority and Preemption
- Let's look at the effect of POD Priority:
	 Consider a scenario where there are two workloads waiting to be scheduled: a critical application with a priority of 7 and a job with a priority of 5. With available resources, the higher priority critical application is scheduled first. If resources remain, the lower priority job is also scheduled.

![The image illustrates the concept of pod priority, showing a comparison between "Jobs" with priority 5 and "Critical Apps" with priority 7, distributed across three servers.](https://kodekloud.com/kk-media/image/upload/v1752869898/notes-assets/images/CKA-Certification-Course-Certified-Kubernetes-Administrator-Priority-Classes/pod-priority-comparison-jobs-apps.jpg)

- Now, what if a new job with a priority of **6** gets scheduled with no resources left? The lower prio workflow will get kicked and 6 will get scheduled.
- This behavior can be overwritten by the **`PreemptionPolicy`** prop defined in the PC's definition file. (preemption=eviction) .
- By default, or if not defined, the policy is **`PreemptLowerPriority`** - kick lower priority in order to schedule a workload.
- The following YAML snippet demonstrates setting the preemption policy to `PreemptLowerPriority`:

```
apiVersion: scheduling.k8s.io/v1
kind: PriorityClass
metadata:
  name: high-priority
value: 1000000000
description: "Priority class for mission critical pods"
preemptionPolicy: PreemptLowerPriority
```

- If you prefer that a higher priority Pod waits for resources rather than preempting lower priority Pods, set the `preemptionPolicy` to `Never`. This change ensures the Pod remains in the scheduling queue without evicting any existing Pods:

```
apiVersion: scheduling.k8s.io/v1
kind: PriorityClass
metadata:
  name: high-priority
value: 1000000000
description: "Priority class for mission critical pods"
preemptionPolicy: Never
```