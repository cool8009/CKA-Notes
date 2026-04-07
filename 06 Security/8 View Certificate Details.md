---
tags:
  - security
---
- We learn how to view certs in an existing cluster.
- The care different solutions to deploy a cluster with different solutions to creating certs.
- "The hard way" deploys components as services, and kubeadm deploys components as pods. ![The hard way deploys components as services, and kubeadm deploys components as pods](Images/Pasted%20image%2020260104202802.png)
- An example list of certs can be found here:
- https://github.com/mmumshad/kubernetes-the-hard-way/tree/master/tools
- Let's say for a kubeadm cluster this is what it looks like:
  ![8 View Certificate Details image 2](Images/Pasted%20image%2020260104202914.png)
- Start by finding the cert path. To do that, go to:
  `cat /etc/kubernetes/manifests/kube-apiserver.yaml`
- This will show the config of the apiserver and will show you where the certificates for it are located.
- ![8 View Certificate Details image 3](Images/Pasted%20image%2020260104203007.png)
- Then, take each cert and look inside it. For example the `--tls-cert-file`:
- ![8 View Certificate Details image 4](Images/Pasted%20image%2020260104203048.png)
- Use `openssl x509 -in *path* -text -noout` to look at cert info.
- These fields are important:
  ![8 View Certificate Details image 5](Images/Pasted%20image%2020260104203144.png)
- Issuer is the CA. Kubeadm names the default CA `kubernetes`.
- You can also look at logs with `journalctl -u etcd.service -l` for a cluster set up from scratch.
- ![8 View Certificate Details image 6](Images/Pasted%20image%2020260104203306.png)
- This shows bad cert.
- If you set up with kubeadm:
  `kubectl logs etcd-master` to give the same output.
- Sometimes, if a core components is down, kubectl won't function. You gotta go one level down to Docker to view logs.
  Use:
  `crtictl ps -a` to view all the logs.
- 