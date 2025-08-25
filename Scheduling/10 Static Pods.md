---
tags:
  - scheduling
aliases:
  - static pod
  - static pods
---
- What happens if we don't have a control plane?
- No kube-api, no scheduler, no nothing
- We literally have a node, on its own, without any "connection to the outside world"
- How can we create PODs on said node, that only has a kubelet on it?
- We know that we need a **pod definition file** to create a POD.
- If we take a POD def file, and place it in the following dir on a node, the kubelet will create it:
  `/etc/kubernetes/manifests`
- kubelet will monitor this directory and create PODs based on the manifests.
- It will also make sure that the pod stays up and will restart it if it fails.
- If we delete the pod def file from that directory, the kubelet will delete the pod.
- This is called a **static POD**.
- You can only create PODs this way. No ReplicaSets, deployments, services or anything else. These require other control plane components. 
- The kubelet only works on the POD level, and only understands pods.
- **You can change the pod definition directory on the node. This directory is passed to the kubelet as a parameter when running the kubelet service.**
- You can also look at the **kubelet.config** file which by default is in `/var/lib/kubelet`
- Look at the --pod-manifest-path param in the kubelet.service file: 
```
ExecStart=/usr/local/bin/kubelet \\
--container-runtime-remote \\
--container-runtime-endpoint=unix:///var/run/containerd/containerd.sock \\
--pod-manifest-path=/etc/Kubernetes/manifests \\
--kubeconfig=/var/lib/kubelet/kubeconfig \\
--network-plugin=cni \\
--register-node=true \\
--v=2
```

- Or you can provide a config file with the `--config=kubeconfig.yaml` and provide the `staticPodPath: /etc/kubernetes/manifests` param in the config.
- Clusters set up with kubeadm use this approach.
- **Catch:**
	  - To view the static POD, use the `docker ps ` command or the relevant command for your runtime. 
	  - We can't use `kubectl` as we don't have the rest of the control plane, and this command works with the kube-api.
- If you **are** part of a control plane, you can still create a static pod, whether via placing a def file in the manifests folder on the node, or with the API (which is how the kubectl does it).
- **This means that in a full cluster, even if you create a static POD, kube-api is still aware of it. This means that running `get pods` you will still see the static POD if you are in a cluster. You can create both types of PODs at the same time. **
- This is how this works:
	  - When creating a static POD, the kubelet, if it is a part of the cluster, creates a mirror object in the kube-api server.
	  - It is just a readonly mirror of the POD.
	  - You can't edit or delete them via kube-api server (aka kubectl). Only by modifying the files in the manifests folder.
- POD name is automatically appended with the node name.
- **But what is the use case for this?**
	- Deploying control plane components as PODs on a node:
	  ![[Pasted image 20250824094353.png]]
	- This way, you don't have to download the binaries, configure services, or worry about the services crashing, as kubelet will restart any crashed PODs. These run as container images and not binaries.
	- This is how kubeadm does it. And this is why you see the control plane components as PODs when you set up that way.
- ## Static Pods vs. DaemonSets

A common question that arises is how static pods differ from DaemonSets. The table below summarizes the key differences between the two:

| Feature                    | Static Pods                                          | DaemonSets                                                 |
| -------------------------- | ---------------------------------------------------- | ---------------------------------------------------------- |
| Creation Source            | Directly managed by the kubelet                      | Managed by the DaemonSet controller via the kube-apiserver |
| Control Plane Involvement  | No API server interaction                            | Requires kube-apiserver communication                      |
| Use Case                   | Typically used for critical control plane components | Ensures a copy of a pod runs on every node                 |
| Interaction with Scheduler | Ignored by the kube-scheduler                        | Ignored by the kube-scheduler                              |

