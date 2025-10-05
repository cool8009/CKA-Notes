---
tags:
  - LoggingMonitoring
---
- How do you monitor resource consumption? What do you actually monitor?
- I'd like to know node metrics, such as nodes in the cluster, their health, and performance metrics, like CPU, memory, disk, network, etc.
- I'd also like to monitor pod-level metrics.
- As of now, K8s doesn't come with a full featured monitoring solution.
- You must implement an external tool.
- Popular open-source monitoring solutions include Metrics Server, Prometheus, and Elastic Stack. In addition, proprietary options like Datadog and Dynatrace are available for more advanced use cases.
- **Heapster** was the original solution, but it's deprecated. It's now replaced by **Metrics Server**. 
- You can have one Metrics Server instance per K8s cluster. 
- Metrics Server is designed to be deployed once per Kubernetes cluster. 
- It collects metrics from nodes and pods, aggregates the data, and retains it in memory. 
- Keep in mind that because Metrics Server stores data only in memory, it does not support historical performance data. For long-term metrics, consider integrating more advanced monitoring solutions.
- How are the metrics collected?
- The kubelet has a subcomponent called **cAdvisor**. It's responsible for retrieving performance metrics from the pods and exposing them via the kubelet api, to make the metrics available to the Metrics Server.
- If you are experimenting locally with Minikube, you can enable the Metrics Server add-on using the following command:

```
minikube addons enable metrics-server
```

- For other environments, deploy Metrics Server by cloning the GitHub repository and applying its deployment files:

```
git clone https://github.com/kubernetes-incubator/metrics-server.git
kubectl create -f deploy/1.8+/
```

- After executing these commands, you should see confirmation that various Kubernetes objects (such as ClusterRoleBinding, RoleBinding, APIService, ServiceAccount, Deployment, Service, and ClusterRole) have been created successfully. 
- Allow the Metrics Server a few moments to begin collecting data from the nodes.

- After running the Metrics Server, to view the metrics, run:
  `kubectl top node`
- This will display the CPU and memory usage for each node, for example showing that 8% of the CPU on your master node (approximately 166 milli cores) is in use.
- To check performance metrics for pods, run:

```
kubectl top pod
```

- An example output may look like the following:

```
NAME         CPU(cores)   CPU%   MEMORY(bytes)   MEMORY%
kubemaster   166m         8%     1337Mi          70%
kubeno 1     36m          1%     1046Mi          55%
kubeno 2     39m          1%     1048Mi          55%


NAME   CPU(cores)   CPU%   MEMORY(bytes)   MEMORY%
nginx  166m         8%     1337Mi          70%
redis  36m          1%     1046Mi          55%
```