- So far we have deployed our application in various ways. 
- We have used ReplicaSets and Deployments to ensure our app is available across various different worker nodes:
  ![[Pasted image 20250805225244.png]]
- A DaemonSet is like a ReplicaSet, but it helps you run **exactly one copy of your pod per node.**
- Whenever a new node is added to the cluster, a **replica of the pod is added to it automatically.**
- ![[Pasted image 20250805225359.png]]
- Same with when a node is removed: the pod is automatically removed.
- Use cases are logs viewer, monitoring solution, etc.
- This is perfect as a DS will deploy the monitoring agent exactly once per node on every node in the cluster.
  ![[Pasted image 20250805225519.png]]
- The kube-proxy is also deployed as a DaemonSet.
- Networking solutions like weave-net also require an agent on each node.
- Creating a DS is similar to the ReplicaSet creation process:
```
# daemon-set-definition.yaml
apiVersion: apps/v1
kind: DaemonSet
metadata:
  name: monitoring-daemon
spec:
  selector:
    matchLabels:
      app: monitoring-agent
  template:
    metadata:
      labels:
        app: monitoring-agent
    spec:
      containers:
        - name: monitoring-agent
          image: monitoring-agent
```

- This def file also has a nested pod template spec in the spec section. 
- Also, it has selectors to link the DaemonSet to the pods.
- ## How DaemonSets Schedule Pods

	Prior to Kubernetes version 1.12, scheduling a pod on a specific node was often achieved by manually setting the `nodeName` property within the pod specification. However, since version 1.12, DaemonSets leverage the default scheduler in conjunction with node affinity rules. This improvement ensures that a pod is automatically scheduled on every node without manual intervention.

![The image explains Kubernetes node scheduling, showing default behavior till v1.12 and changes with NodeAffinity from v1.12, featuring nodes labeled node01 to node06.](https://kodekloud.com/kk-media/image/upload/v1752869890/notes-assets/images/CKA-Certification-Course-Certified-Kubernetes-Administrator-DaemonSets/frame_240.jpg)

**DaemonSets are an ideal solution for deploying services that must run on every node, such as monitoring agents and essential networking components. Leveraging node affinity simplifies management as your cluster scales.** 


- Tip: You can create a DaemonSet via the CLI by creating a deployment with --dry-run to get the yaml and then change the **kind** field.