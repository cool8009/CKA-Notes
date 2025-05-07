---
tags:
  - scheduling
aliases:
  - selector
  - selectors
  - Node Selectors
---
- You have a 3 node cluster, of which 2 are smaller nodes with lower hardware, and one with higher level of hardware.
- 3 different workloads running in your cluster, and you'd like to dedicate the data processing workloads that require higher horsepower to the stronger node.
- In the default setup, and pod can land on any node.
- We can set a limitation on the POD, so they will run on specific nodes only. The simplest way to do this is to use **node selectors.**
- Node selectors restrict pod placement by matching key-value pairs defined in the pod’s specification against the labels on the nodes.
- To ensure that a pod is restricted to run on a specific node, you can modify the pod's definition file using node selectors. Below is an example of a pod definition YAML file that deploys a data processing image exclusively on a node labeled as "Large":

```
apiVersion: v1
kind: Pod
metadata:
  name: myapp-pod
spec:
  containers:
    - name: data-processor
      image: data-processor
  nodeSelector:
    size: Large
```

- In this configuration, the Kubernetes scheduler identifies the appropriate node by matching the label with the key-value pair `size: Large`. Ensure that you pre-label the target node accordingly.
- **size: Large are labels (KV pair) assigned to the node. **
- To label a node, use:
   `kubectl label nodes <node-name> <label-key>=<label-value>`
- Kubernetes will then schedule your pod on the node that matches the selector—in this case, the larger node.

**This is fine for simple scenarios, but is limited for more complex scenarios like NOT logic, conditionals, etc. **

For instance, if you need to schedule a pod on a node that is either large or medium, or on any node that is not labeled as small, a basic node selector may not suffice. In these cases, consider using node affinity and anti-affinity features, which offer advanced scheduling capabilities to define more complex placement rules.