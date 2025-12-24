---
tags:
  - ALM
---
- You can resize pods in place.
- As of K8s 1.3.2 if you change resource req. of a pod while its alive, K8s will delete the pod and spin up a new one, therefore it doesn't happen in place.
- This can be disruptive for stateful workloads.
- In Place Resizing is a feature in progress, and is in alpha. 
- To enable:
- `FEATURE_GATES=InPlacePodVerticalScaling=true`
- This allows us to provide a `resizePolicy ` in the pod def file:
  
  The following manifest demonstrates a resize policy for the CPU resource, allowing an update without restarting the Pod:

```
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-app
spec:
  replicas: 1
  selector:
    matchLabels:
      app: my-app
  template:
    metadata:
      labels:
        app: my-app
    spec:
      containers:
      - name: my-app
        image: nginx
        resizePolicy: #here
          - resourceName: cpu
            restartPolicy: NotRequired
        resources:
          requests:
            cpu: "250m"
            memory: "256Mi"
          limits:
            cpu: "500m"
            memory: "512Mi"
```

When the in-place update feature is active, increasing the CPU resource value (for example, from "250m" to "1") updates the running Pod directly without termination, ensuring smooth scalability and minimal service interruption.
## Limitations of In-Place Pod Resizing

It is important to note the following limitations with the current implementation of in-place resizing:

- Only CPU and memory resources can be updated in place.
- Changes to Pod QoS classes and certain other attributes are not supported.
- Init containers and ephemeral containers are not eligible for in-place resizing.
- Resource requests and limits, once assigned to a container, cannot be shifted to another container.
- A container's memory limit cannot be reduced below its current usage; if such a request is made, the resize operation will remain in progress until the new memory limit is achievable.
- Windows Pods are not supported by this feature.