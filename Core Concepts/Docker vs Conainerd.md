---
tags:
  - clitools
  - runtime
---

- There a few CLI tools like ctr, nerdctl, crictl.
- **Docker** is the pioneer of the container era and it's the most dominant container tool. 
- Kubernetes was made for docker, and was at first tightly coupled.
- KB introduced an interface called the **Container Runtime Interface** which allows any container tech to work with KB, as long as they adhere to the OCI (Open Container Initiative). 
- OCI consists of a runtimespec and imagespec, which are specs on how an image should be built and a how a runtime should be developed. 
- Anyone can be a container runtime that can work with KB.
- rkt and other runtimes that adhere to OCI standard, can now work with KB. However, docker was build before OCI and still is supported.
- **dockershim** is a hacky way to support docker outside of OCI. Docker isn't a runtime alone, it's also a CLI, API, build tools. The container runtime is called **runc** and it is managed by **containerd** daemon. 
- **containerd** is CRI compatible. It can be used as a runtime by itself, separate from docker.
- It was decided in KB 1.24 to remove docker shim completely, so docker support was removed.
- All the docker images built before, continue to work with containerd, since they do follow the imagespec. 
- You can install containerd by itself, ideally. If you don't need docker features especially.
- How do you run containers without "docker run"?
- containerd comes with ctr, a non-user friendly CLI tool with limited features. The other way is just making API calls directly. You can pull images and run them, and other rudimentary things. Used mostly for debugging, and not for production.
- A good alternative is nerdctl:
- ![[Pasted image 20250125160342.png]]
- nerdctl vs docker:
    `$ docker run --name redis redis:alpine 
  `$ nerdctl run --name redis redis:alpine
- **crictl** is a cli used to interact with CRI compatible runtimes. 
  ![[Pasted image 20250125160747.png]]
  
- Since it's aware of [[Certified Kubernetes Administrator/Core Concepts/POD]], as opposed to docker, crictl is the go to solution to debug and view containers running in K8s.


  ``