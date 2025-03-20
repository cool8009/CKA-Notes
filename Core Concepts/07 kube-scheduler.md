---
tags:
  - Controlplane
aliases:
  - kube-scheduler
  - scheduler
---

- Scheduler is responsible **only** on deciding which POD goes on which [[20 nodes]]. 
- It doesn't actually place them there, that's the job of the [[08 kubelet]].
- You need a scheduler to make sure that the right container ends up on the right ship (node), with regard to capacity, performance, policy etc.
- The scheduler looks at each pod and tries to find the best node for it in 2 phases:
	  - **Filtering** nodes that don't fit the requirements of the pod.
	  - **Ranks** the nodes via a priority function, which assigns a **score** for each POD based on where will be a better fit.
- To install the scheduler, download the binary, extract and run as a service.
- Like the previous components, [[kubeadm]] deploys it on the master node.
- If not, you can find it in the `systemd/system` folder or using `ps -aux | grep kube-scheduler`