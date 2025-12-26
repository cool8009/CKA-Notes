---
tags:
  - maintenance
---
- Taking down nodes from the cluster, for maintenance like security updates or OS upgrades.
- You have a cluster with a few nodes and pods. What happens when a node goes down? The pods go down with it.
- This might affect your users.
- Kubernetes offers mechanisms to handle such situations:
- If a node comes back online quickly, the pods are simply restarted.
- If a node remains down for more than five minutes, Kubernetes marks the pods on that node as dead. Those five minutes are know as **pod eviction timeout** and is set like so:
  `kube-controller-manager --pod-eviction-timeout=5m0s`
- For pods managed by a ReplicaSet, new pods are automatically created on other nodes. In contrast, pods that are not part of a ReplicaSet will not be restarted, potentially leading to downtime.
- **Draining a node** involves gracefully terminating the pods running on that node so they are recreated on other nodes. This is used when the recovery time is uncertain, as is it safer to drain a node beforehand.
- `kubectl drain node-1`
- The node is also **cordoned.** This means that the node is marked unschedule-able, until your purposefully remove the restriction (the cordon).
- To perform these operations, run the following commands:

```
kubectl drain node-1
kubectl uncordon node-1
```
- ## Cordon vs. Drain

- In addition to draining and uncordoning, Kubernetes provides the cordon command. Unlike drain, cordon only marks a node as unschedulable without terminating or relocating the currently running pods. This ensures that no new pods will be scheduled on the node.

- Warning

- Be cautious when using cordon on a node with critical workloads. Since existing pods remain and new pods cannot be scheduled, your application might become overloaded or experience unexpected behavior.