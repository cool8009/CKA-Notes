---
tags:
  - Workernode
  - pods
---

- Like the captain, leads all activities on the [[worker node]]
- Load or unload containers on the ship (node)
- Sole point of contact on the node, as instructed by the [[kube-scheduler]]
- Send back status reports at regular intervals
- Registers the node in the cluster. 
- When it gets a request to load a container, it instructs the current container runtime (docker for example) to pull the image and run an instance.
- Continues to monitor the POD and reports to the [[kube-api]] on a timely basis.
- In contrast with other services, when deploying a cluster with [[kubeadm]] it **doesn't** automatically deploy kubelet.
- Instead, you must always manually install kubelet on the worker nodes.
- Download, extract and run as a service.
- `ps -aux | grep kubelet` to view on the **worker node**.