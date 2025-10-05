---
tags:
  - Controlplane
aliases:
  - etcd
  - ETCD
---

- is a KV store
- Installing is simple: downloading and executing the binary.
- 
	1. **Download Binaries**
	`curl -L https://github.com/etcd-io/etcd/releases/download/v3.3.11/etcd-v3.3.11-linux-amd64.tar.gz -o etcd-v3.3.11-linux-amd64.tar.gz`
	
	2. **Extract**
	`tar xzvf etcd-v3.3.11-linux-amd64.tar.gz`
	
	3. **Run ETCD Service**
	`./etcd`
- It starts a svc that listening on port 2379 by default.
- Comes with a [[03 etcdctl]] client:
  `etcdctl set key1 value1`
  `etcdctl view key1`
- There are different releases and versions of etcd. Between v2 and v3 there were some command changes.
- etcd is **not** only for k8s. It's a KV store that is used also in k8s.
- It stores a bunch of info about different things such as:
  - [[20 nodes]]
  - [[10 POD]]s
  - [[Configs]]
  - [[Secrets]]
  - [[Accounts]]
  - [[Roles]]
  - [[Binding]]
  - and more
- Every change you make to a cluster are updated on the [[02 ETCD]] server.
- Only once it is updated, change is considered complete.
- Depending on your setup, from scratch or with [[kubeadm]], [[02 ETCD]] is deployed differently.
- If you deploy from scratch, you download and install [[02 ETCD]] by yourself, and configure it.
- [[kubeadm]] deploys etcd as a pod in the kube-system [[namespace]]. 
- the `--advertise-client-urls` option in `etcd.service` is where [[02 ETCD]] is listening on. This is the url you later set up on your worker nodes.
- etcd stores k8s data in a specific structure:
  ![[Pasted image 20250125162609.png]]
- In a HA environment, because you have multiple master nodes and therefore multiple etcd clusters, you need to specify the `--initial-cluster controller-0={urltocontroller0}:2380 {urltocontroller1}:2380` in `etcd.service`
  This will ensure that the different etcd instances will know about each other.
- 
  
  
