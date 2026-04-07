---
aliases:
  - kube-apiserver
  - kube-api server
  - kube-api
tags:
  - Controlplane
---

- Primary management components in K8s.
- When you run a `kubectl` command, the kubectl utility is in fact reaching to the kube-api, which runs [[3 Authentication|authentication]], [[13 Authorization|authorization]], and the [[14 Admissions Controllers (new 2025)|admission controller]] flow before responding to the request.
- You can also invoke the API directly with a POST request:
  ![04 kube api image 1](Images/Pasted%20image%2020250125163122.png)
  - During this time, the [[07 kube-scheduler]] consciously monitors the kube-api server, and realizes that there is a new pod with no node assigned. It updates the kube-api server, which then passes that info to the [[08 kubelet]] in the appropriate [[22 worker node]]. The kubelet creates the pod on the node, and instructs the CRE (container runtime engine) to deploy the app image. Once done, the kubelet updates the api, and the api updates the etcd.
  - This is how almost anything is done. The kube-api is at the center of all tasks being done.
  - The kube-api comes with [[00 kubeadm|kubeadm]], but when setting up the hard way, it needs to manually be downloaded, installed and configured in `kube-apiserver.service`
  - ![04 kube api image 2](Images/Pasted%20image%2020250125163959.png)
  - The important parts are highlighted - there are [[00 Certificates|certificates]] mostly.
  - `--etcd-servers:` is dictating which [[02 ETCD]] servers are connected to the API.
  - With [[00 kubeadm|kubeadm]], viewing the kube-api options is in:
    `cat /etc/kubernetes/manifests/kube-apiserver.yaml`
  - In a different setup, the service can be found at:
    `cat /etc/systemd/system/kube-apiserver.service`
- Or:
  `ps -aux | grep kube-apiserver`
