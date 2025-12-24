---
tags:
  - ALM
---
- ## Manual Horizontal Scaling

- As a Kubernetes administrator, you might manually scale your application to ensure it has enough resources during traffic spikes. Consider the following deployment configuration:

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
          resources:
            requests: #here is the resources of the pods
              cpu: "250m"
            limits:
              cpu: "500m"
```

- In this configuration, each pod requests 250 millicores (mCPU) and is limited to 500 mCPU. To monitor the resource usage of a pod, you might run:

```
$ kubectl top pod my-app-pod #this montiros the pod resource consumption
```

- The output would be similar to:

```
NAME         CPU(cores)   MEMORY(bytes)
my-app-pod   450m         350Mi
```

- Once you observe the pod’s CPU usage nearing the threshold (for example, at 450 mCPU), you would manually execute a scale command to add more pods:

```
$ kubectl scale deployment my-app --replicas=3
```
- Manual scaling requires continuous monitoring and timely intervention, which may not be ideal during unexpected surges in traffic.
- So this is the manual way to do it: monitor the deployment, see if resources are being maxed out, add more pods (horizontal scaling)
- ## Introducing the Horizontal Pod Autoscaler (HPA)

- To address the shortcomings of manual scaling, Kubernetes offers the Horizontal Pod Autoscaler (HPA). HPA continuously monitors pod metrics—such as CPU, memory, or custom metrics—using the metrics-server. 
- Based on these metrics, HPA automatically adjusts the number of pod replicas in a deployment, stateful set, or replica set. When resource usage exceeds a preset threshold, HPA increases the pod count; when usage declines, it scales down to conserve resources.

![The image is a diagram explaining the functions of a Horizontal Pod Autoscaler (HPA), highlighting its roles in observing metrics, adding pods, balancing thresholds, and tracking multiple metrics.](https://kodekloud.com/kk-media/image/upload/v1752869662/notes-assets/images/CKA-Certification-Course-Certified-Kubernetes-Administrator-Horizontal-Pod-Autoscaler-HPA-2025-Updates/horizontal-pod-autoscaler-diagram.jpg)

- With the deployment spec above, you can use this cmd:
  `kubectl autoscale deployment my-app --cpu-percent=50 --min=1 --max=10
- This command configures the "my-app" deployment to maintain 50% CPU utilization, scaling the number of pods between 1 and 10
- Kubernetes will then create an HPA that monitors the CPU metrics (using the pod's 500 mCPU limit) via the metrics-server. If the average CPU utilization exceeds 50%, HPA adjusts the replica count to meet demand without manual input.

To review the status of your HPA, use:

```
$ kubectl get hpa
```

This command shows the current CPU usage, threshold set, and the number of replicas—ensuring that pod counts remain within the defined limits. When the HPA is no longer needed, you can remove it with:

```
$ kubectl delete hpa my-app
```

- Beyond the imperative approach, you can create an HPA definition file via the declarative approach:
- Here's an example using the `autoscaling/v2` API:

```
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: my-app-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: my-app
  minReplicas: 1
  maxReplicas: 10
  metrics:
    - type: Resource
      resource:
        name: cpu
        target:
          type: Utilization
          averageUtilization: 50
```

- This configuration ensures that the HPA monitors the CPU utilization of the "my-app" deployment, automatically adjusting the replica count as needed. Note that HPA, integrated into Kubernetes since version 1.23, relies on the metrics-server to obtain resource utilization data.
- K8s depends on the internal Metrics Server, but not only. You can use a custom metrics adapter and also an external source, like a Datadog instance. More info in the K8s autoscaler course.
- 