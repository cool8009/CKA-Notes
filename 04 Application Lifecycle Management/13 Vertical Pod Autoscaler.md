---
tags:
  - ALM
---
- Vertically scaling a workload manually involves (after using `kubectl top` command and seeing that the resources are exhausted) editing the deployment file, specifically to what container is running, and changing the `resources:` part to add more resources to the pods in the deployment.
- This scales the pods up.
- After saving, Kubernetes will terminate the current pod and create a new one with the updated resource configuration.
- Manually updating pods can be time-consuming and error-prone. Kubernetes provides the Vertical Pod Autoscaler (VPA) to automate this process.
- The VPA Also monitors the metric server, and adjust scaling accordingly.
- The VPA **doesn't come built in**, we need to deploy it.
- Start by applying the VPA definition file from the autoscaler GitHub repository:

```
$ kubectl apply -f https://github.com/kubernetes/autoscaler/releases/latest/download/vertical-pod-autoscaler.yaml
```

- Verify that the VPA components are running in the kube-system namespace:

```
$ kubectl get pods -n kube-system | grep vpa
vpa-admission-controller-xxxx   Running
vpa-recommender-xxxx            Running
vpa-updater-xxxx                Running
```

- The VPA deployment includes three key components:

1. **VPA Recommender:** Continuously monitors resource usage via the Kubernetes metrics API, analyzes historical and live data, and provides optimized recommendations for CPU and memory.
2. **VPA Updater:** Compares current pod resource settings against recommendations and evicts pods running with suboptimal resources. This eviction triggers the creation of new pods with updated configurations.
3. **VPA Admission Controller:** Intercepts pod creation requests and mutates the pod specification based on the recommender's suggestions, ensuring that new pods start with the ideal resource configuration.

- Next, create a VPA resource with a YAML definition. Unlike HPA, the VPA isn’t set up through imperative commands. The example below shows a configuration that monitors the "my-app" deployment, enforces minimum and maximum CPU limits, and uses the "Auto" update mode:

```
apiVersion: autoscaling.k8s.io/v1
kind: VerticalPodAutoscaler
metadata:
  name: my-app-vpa
spec:
  targetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: my-app
  updatePolicy:
    updateMode: "Auto"
  resourcePolicy:
    containerPolicies:
      - containerName: "my-app"
        minAllowed:
          cpu: "250m"
        maxAllowed:
          cpu: "2"
        controlledResources: ["cpu"]
```

- There are 4 `updateMode` modes:
  ![[Pasted image 20251223220506.png]]
- To inspect the resource recommendations provided by VPA for your deployment, run:

```
$ kubectl describe vpa my-app-vpa
```

You might see an output similar to this, which indicates a recommended CPU value of 1.5:

```
Recommendations:
  Target:
    Cpu: 1.5
```

## Comparing Vertical and Horizontal Pod Autoscaling

Understanding when to use VPA versus HPA is crucial for efficient resource management:

|Feature|Vertical Pod Autoscaling (VPA)|Horizontal Pod Autoscaling (HPA)|
|---|---|---|
|Scaling Method|Adjusts CPU and memory settings of individual pods (may restart pods for changes).|Increases or decreases the number of pods to distribute load.|
|Pod Behavior|May cause temporary downtime during pod restarts.|Scales pods seamlessly without interrupting existing ones.|
|Traffic Handling|Less effective for sudden spikes due to restart delays.|Ideal for handling rapid traffic spikes by adding more pods instantly.|
|Cost Optimization|Prevents over-provisioning by matching resource allocation with actual usage.|Reduces operational costs by avoiding underutilized pods.|
|Use Cases|Stateful workloads, databases, JVM-based applications, and AI workloads requiring precise tuning.|Stateless applications, web services, and microservices requiring rapid scaling.|

![The image is a comparison chart highlighting the key differences between Vertical Pod Autoscaling (VPA) and Horizontal Pod Autoscaling (HPA) in Kubernetes, focusing on features like scaling method, pod behavior, traffic handling, cost optimization, and use cases.](https://kodekloud.com/kk-media/image/upload/v1752869688/notes-assets/images/CKA-Certification-Course-Certified-Kubernetes-Administrator-Vertical-Pod-Autoscaling-VPA-2025-Updates/vpa-hpa-comparison-chart-kubernetes.jpg)