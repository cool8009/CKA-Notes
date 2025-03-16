---
aliases:
  - kube-apiserver
  - kube-api server
tags:
  - Controlplane
---

- Primary management components in K8s.
- When you run a `kubectl` command, the kubectl utility is in fact reaching to the kube-api, which auths, validates and responds to the request.
- You can also invoke the API directly with a POST request:
  ![[Pasted image 20250125163122.png]]
  - During this time, the [[kube-scheduler]] consciously monitors the kube-api server, and realizes that there is a new pod with no node assigned. It updates the kube-api server, which then passes that info to the [[kubelet]] in the appropriate [[worker node]]. The kubelet creates the pod on the node, and instructs the CRE (container runtime engine) to deploy the app image. Once done, the kubelet updates the api, and the api updates the etcd.
  - This is how almost anything is done. The kube-api is at the center of all tasks being done.
  - The kube-api comes with [[kubeadm]], but when setting up the hard way, it needs to manually be downloaded, installed and configured in `kube-apiserver.service`
  - ![[Pasted image 20250125163959.png]]
  - The important parts are highlighted - there are [[Certificates]] mostly.
  - `--etcd-servers:` is dictating which [[etcd]] servers are connected to the API.
  - With [[kubeadm]], viewing the kube-api options is in:
    `cat /etc/kubernetes/manifests/kube-apiserver.yaml`
  - In a different setup, the service can be found at:
    `cat /etc/systemd/system/kube-apiserver.service`
- Or:
  `ps -aux | grep kube-apiserver`