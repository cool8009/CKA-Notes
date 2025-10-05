---
tags:
  - scheduling
aliases:
  - custom scheduling
  - multiple schedulers
---

- We have seen how the default scheduler works:
	  - Uses and algorithm to distribute nodes evenly.
	  - Takes into account taints and tolerations, node affinity, etc.
- What if this doesn't satisfy my needs, and I need custom checks or something before placing a pod on a node? 
- I decide to create a custom algorithm to place PODs on nodes, so I can add custom conditions and checks.
- K8s is highly extensible - you can write your own custom scheduler and deploy it, and use it either as a default scheduler or in addition to the default one.
- When creating a POD or a dep, you can instruct K8s to schedule pods with a specific scheduler:
  
- ![[Pasted image 20250826083722.png]]
- Different schedulers need different names. The default schedulers name is `default-scheduler` and it's configured in `shceduler-config.yaml`.
- We create a separate config file for our schedulers and set the name like this:
  Below are examples of configuration files for both the default and a custom scheduler. Each YAML file uses a profiles list to define the scheduler's name.

```
# my-scheduler-config.yaml
apiVersion: kubescheduler.config.k8s.io/v1
kind: KubeSchedulerConfiguration
profiles:
  - schedulerName: my-scheduler
```

```
# scheduler-config.yaml
apiVersion: kubescheduler.config.k8s.io/v1
kind: KubeSchedulerConfiguration
profiles:
  - schedulerName: default-scheduler
```

- The simplest way to deploy an additional scheduler, is to get the binary and run it as a service (like the regular setup), and pass it the config file we created:  ```
	wget https://storage.googleapis.com/kubernetes-release/release/v1.12.0/bin/linux/amd64/kube-scheduler

  Create separate service files for each scheduler. For example, consider the following definitions:
	
	```
	# kube-scheduler.service
	ExecStart=/usr/local/bin/kube-scheduler --config=/etc/kubernetes/config/kube-scheduler.yaml
	```
	
	```
	# my-scheduler-2.service
	ExecStart=/usr/local/bin/kube-scheduler --config=/etc/kubernetes/config/my-scheduler-2-config.yaml
	```
	
	### Step 3: Define Scheduler Configuration Files
	
	Reference the scheduler names in the associated configuration files:
	
	```
	# my-scheduler-2-config.yaml
	apiVersion: kubescheduler.config.k8s.io/v1
	kind: KubeSchedulerConfiguration
	profiles:
	  - schedulerName: my-scheduler-2
	```
	
	```
	# my-scheduler-config.yaml
	apiVersion: kubescheduler.config.k8s.io/v1
	kind: KubeSchedulerConfiguration
	profiles:
	  - schedulerName: my-scheduler
	```

- The thing is, 99% of the time this is **not** how you would deploy your scheduler nowadays.
- With kubeadm, all control plane components run as pods. 
- To deploy it as a POD:
	  ### Example Pod Definition
	
	```
	apiVersion: v1
	kind: Pod
	metadata:
	  name: my-custom-scheduler
	  namespace: kube-system
	spec:
	  containers:
	    - name: kube-scheduler
	      image: k8s.gcr.io/kube-scheduler-amd64:v1.11.3
	      command:
	        - kube-scheduler
	        - --address=127.0.0.1
	        - --kubeconfig=/etc/kubernetes/scheduler.conf
	        - --config=/etc/kubernetes/my-scheduler-config.yaml
	```
	
	The corresponding custom scheduler configuration file might look like:
	
	```
	apiVersion: kubescheduler.config.k8s.io/v1
	kind: KubeSchedulerConfiguration
	profiles:
	  - schedulerName: my-scheduler
	leaderElection:
	  leaderElect: true
	  resourceNamespace: kube-system
	  resourceName: lock-object-my-scheduler
	```
	
	Note
	
	Leader election is an important configuration for high-availability (more in another section) environments. It ensures that while multiple scheduler instances are running, only one actively schedules the pods.

- In the K8s docs, there's a section about making a custom scheduler, how to build it, and how to deploy it. 
- In many modern Kubernetes setups—especially those using kubeadm—control plane components run as pods or deployments. Below is an example of deploying a custom scheduler as a Deployment.

- ## Configuring Workloads to Use the Custom Scheduler

	To have specific pods or deployments use your custom scheduler, add the "schedulerName" field in the pod's specification. For example:
	
	```
	apiVersion: v1
	kind: Pod
	metadata:
	  name: nginx
	spec:
	  containers:
	    - name: nginx
	      image: nginx
	  schedulerName: my-custom-scheduler
	```
	
	Deploy this pod with:
	
	```
	kubectl create -f pod-definition.yaml
	```
	
	If the custom scheduler configuration is incorrect, the pod may remain in the Pending state. Conversely, a properly scheduled pod will transition to the Running state.

- ## Verifying Scheduler Operation

	To confirm which scheduler assigned a pod, review the events in your namespace:
	
	```
	kubectl get events -o wide
	```
	
	A sample output might appear as follows:
	
	```
	LAST SEEN   COUNT   NAME        KIND   TYPE    REASON      SOURCE                  MESSAGE
	9s          1       nginx.15    Pod    Normal  Scheduled   my-custom-scheduler     Successfully assigned default/nginx to node01
	8s          1       nginx.15    Pod    Normal  Pulling     kubelet, node01         pulling image "nginx"
	2s          1       nginx.15    Pod    Normal  Pulled      kubelet, node01         Successfully pulled image "nginx"
	2s          1       nginx.15    Pod    Normal  Created     kubelet, node01         Created container
	2s          1       nginx.15    Pod    Normal  Started     kubelet, node01         Started container
	```
	
	Notice that the event source is "my-custom-scheduler," confirming that the pod was scheduled by your custom scheduler.
	
	If you encounter issues, view the scheduler logs with:
	
	```
	kubectl logs my-custom-scheduler --namespace=kube-system
	```
	
	A sample log output might include messages like:
	
	```
	I0204 09:42:25.819338   1 server.go:126] Version: v1.11.3
	W0204 09:42:25.822720   1 authorization.go:47] Authorization is disabled
	W0204 09:42:25.822745   1 authentication.go:55] Authentication is disabled
	I0204 09:42:25.822801   1 insecure_serving.go:47] Serving healthz insecurely on 127.0.0.1:10251
	I0204 09:45:14.725407   1 controller_utils.go:1025] Waiting for caches to sync for scheduler controller
	I0204 09:45:14.825634   1 controller_utils.go:1032] Caches are synced for scheduler controller
	I0204 09:45:14.825814   1 leaderelection.go:185] attempting to acquire leader lease kube-system/my-custom-scheduler...
	I0204 09:45:14.834953   1 leaderelection.go:194] successfully acquired lease kube-system/my-custom-scheduler
	```
	
	This confirms that the custom scheduler is up and functioning as expected.

# Creating a custom scheduler: Most of the following is stuff we haven't talked about yet, like RBAC, ConfigMaps, etc. Just ignore it for now and keep it here cause it will be useful eventually.
### Step 1: Build and Push a Custom Scheduler Image

Create a Dockerfile for your custom scheduler:

```
FROM busybox
ADD ./.output/local/bin/linux/amd64/kube-scheduler /usr/local/bin/kube-scheduler
```

Build and push the Docker image:

```
docker build -t gcr.io/my-gcp-project/my-kube-scheduler:1.0 .
gcloud docker -- push gcr.io/my-gcp-project/my-kube-scheduler:1.0
```

### Step 2: Create ServiceAccount and RBAC Configurations

Prepare the following YAML to create a service account and set appropriate RBAC permissions:

```
apiVersion: v1
kind: ServiceAccount
metadata:
  name: my-scheduler
  namespace: kube-system
---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: my-scheduler-as-kube-scheduler
subjects:
  - kind: ServiceAccount
    name: my-scheduler
    namespace: kube-system
roleRef:
  kind: ClusterRole
  name: system:kube-scheduler
  apiGroup: rbac.authorization.k8s.io
---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: my-scheduler-as-volume-scheduler
subjects:
  - kind: ServiceAccount
    name: my-scheduler
    namespace: kube-system
roleRef:
  kind: ClusterRole
  name: system:volume-scheduler
  apiGroup: rbac.authorization.k8s.io
```

### Step 3: Create a ConfigMap for Scheduler Configuration

Define a ConfigMap that includes your custom scheduler configuration:

```
apiVersion: v1
kind: ConfigMap
metadata:
  name: my-scheduler-config
  namespace: kube-system
data:
  my-scheduler-config.yaml: |
    apiVersion: kubescheduler.config.k8s.io/v1beta2
    kind: KubeSchedulerConfiguration
    profiles:
      - schedulerName: my-scheduler
        leaderElection:
          leaderElect: false
```

### Step 4: Define the Deployment

Deploy the custom scheduler as a Deployment with the following YAML:

```
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-scheduler
  namespace: kube-system
  labels:
    component: scheduler
    tier: control-plane
spec:
  replicas: 1
  selector:
    matchLabels:
      component: scheduler
      tier: control-plane
  template:
    metadata:
      labels:
        component: scheduler
        tier: control-plane
        version: second
    spec:
      serviceAccountName: my-scheduler
      containers:
        - name: kube-second-scheduler
          image: gcr.io/my-gcp-project/my-kube-scheduler:1.0
          command:
            - /usr/local/bin/kube-scheduler
            - --config=/etc/kubernetes/my-scheduler/my-scheduler-config.yaml
          livenessProbe:
            httpGet:
              path: /healthz
              port: 10259
              scheme: HTTPS
            initialDelaySeconds: 15
          readinessProbe:
            httpGet:
              path: /healthz
              port: 10259
              scheme: HTTPS
          volumeMounts:
            - name: config-volume
              mountPath: /etc/kubernetes/my-scheduler
      volumes:
        - name: config-volume
          configMap:
            name: my-scheduler-config
```

Also, ensure a proper ClusterRole exists for the scheduler. For example:

```
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: system:kube-scheduler
  annotations:
    rbac.authorization.kubernetes.io/autoupdate: "true"
  labels:
    kubernetes.io/bootstrapping: rbac-defaults
rules:
  - apiGroups:
      - coordination.k8s.io
    resources:
      - leases
    verbs:
      - create
  - apiGroups:
      - coordination.k8s.io
    resourceNames:
      - kube-scheduler
      - my-scheduler
    resources:
      - leases
    verbs:
      - get
      - list
      - watch
```