---
tags:
  - Controlplane
---

- [[Controllers]] are like offices/departments that manage certain things:
  - When a ship gets destroyed
  - When new ships arrives
- This means that they watch status, and remediate situation when something goes wrong
- In K8s terms, a controller is a process that continuously monitors the state of various components, and works towards **bringing the system to a desired functional state**.
- For example, the [[Node-Controller]] monitors the status of the nodes, and taking the actions to keep the apps running. It is done via the [[kube-api]].
	  - The [[Node-Controller]] checks the status of the nodes every five seconds (heartbeat).
	  - If heartbeat stops for **40** seconds, node is marked **unreachable** .
	  - It then gets **5 minutes** to get back up.
	  - If it doesn't, it removes that pod from the node, and provisions them on healthy ones if the pod is part of a [[ReplicaSet]].
- The next controller is a [[Replication-Controller]], which monitors the status of [[ReplicaSet]]s.
	  - Ensure the desired number of pods exist and work.
	  - If a pod dies, it creates another one.
- There are many more controllers in K8s:
  ![[Pasted image 20250125170324.png]]
- This is the brain behind a lot of things in K8s.
- They are packaged in a process called the [[Controller-Manager]]. When it's installed, the controllers are installed as well.
- You can download and install it, and then run as a service, with a lot of options provided:
  ![[Pasted image 20250125170505.png]]
- If you have [[kubeadm]], it's deployed as a pod in the master node, and you can view the option in the manifests folder.
- In a non-kubeadm setup, you can find the .service file in the `/etc/systemd/system/`
- Also listing the process with `ps -aux | grep kube-controller-manager`