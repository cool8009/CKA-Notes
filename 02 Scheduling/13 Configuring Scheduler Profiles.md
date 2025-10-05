---
aliases:
  - profile
  - scheduler profile
tags:
  - scheduling
---
- First, let's recap how the scheduler works.
- When a pod is defined, it enters a scheduling queue along with other pending pods. Consider a pod that requires 10 CPU; it will only be scheduled on nodes with at least 10 available CPUs. Additionally, pods with higher priorities are placed at the beginning of the queue. For instance, the following pod definition uses a high-priority class:

```
apiVersion: v1
kind: Pod
metadata:
  name: simple-webapp-color
spec:
  priorityClassName: high-priority
  containers:
    - name: simple-webapp-color
      image: simple-webapp-color
      resources:
        requests:
          memory: "1Gi"
          cpu: 10
```

- Before using this priority, you must create a priority class with a specific name and a priority value. Assigning a value like 1,000,000, for example, grants a very high priority. This ensures that pods with higher priorities are scheduled ahead of those with lower ones.
- After being queued, pods progress through several phases:

	1. **Filter Phase:** Nodes that cannot meet the pod's resource requirements (e.g., nodes lacking 10 CPUs) are filtered out.
	2. **Scoring Phase:** Remaining nodes are scored based on resource availability after reserving the required CPU. For example, a node with 6 CPUs left scores higher than one with only 2.
	3. **Binding Phase:** The pod is assigned to the node with the highest score.

- There are a few key **scheduling plugins** that help achieve the above:
  - **PrioritySort** sorts pods in the queue according to their priority. This is how pods with a higher priority class get scheduled over pods with a lower one.
  - **NodeResourcesFit** identifies the nodes with the sufficient resources for the pods, and filters out those that don't, in the filtering phase.    
 - **Scoring Plugins:** During the scoring phase, plugins (such as the **Node Resources Fit** and **Image Locality** plugins) assess each node's suitability. They assign scores rather than outright rejecting nodes.
 - **Default Binder Plugin:** Finalizes the scheduling process by binding the pod to the selected node.
 - **Kubernetes emphasizes extensibility**, allowing you to modify the scheduling process via extension points at stages such as queueing, filtering, scoring, and binding. 
 - **Node Unschedulable Plugin:** Excludes nodes marked as unschedulable. For instance, running commands like drain or cordon (which will be discussed later) will set the unschedulable flag. An example node description is:

 	    ```
	    controlplane ~ → kubectl describe node controlplane
	    Name:               controlplane
	    Roles:              control-plane
	    CreationTimestamp:  Thu, 06 Oct 2022 06:19:57 -0400
	    Taints:             node.kubernetes.io/unschedulable:NoSchedule
	    Unschedulable:      true
	    Lease:
	    ```

  - ![[Pasted image 20250922151859.png]]

- Each phase has **extension points**, which are places where functionality can be extended. These are where the aforementioned plugins, are plugged to.
- These are the various extension poins of the scheduler, including processes like the scheduling queue, filtering, scoring, and binding phases:

![The image outlines Kubernetes scheduler extension points: Scheduling Queue, Filtering, Scoring, and Binding, with specific functions like queueSort, preFilter, and bind.](https://kodekloud.com/kk-media/image/upload/v1752869885/notes-assets/images/CKA-Certification-Course-Certified-Kubernetes-Administrator-Configuring-Scheduler-Profiles/frame_380.jpg)

- Taking a step back, in [[12 Multiple Schedulers|multiple schedulers]] we talked about creating custom scheduler objects and binaries.
- Rather than running separate scheduler binaries (like default scheduler, MyScheduler, and MyScheduler2) with distinct configuration files, Kubernetes 1.18 introduced support for multiple **scheduling profiles** within a single scheduler binary.
- This approach minimizes operational overhead and prevents potential race conditions that can arise when multiple processes schedule workloads on the same node.
- Each profile is defined withing the scheduler config file, and behaves like a separate scheduler:
	```
	# my-scheduler-2-config.yaml
	apiVersion: kubescheduler.config.k8s.io/v1
	kind: KubeSchedulerConfiguration
	profiles:
	  - schedulerName: my-scheduler-2
	  - schedulerName: my-scheduler-3
	```

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
- And also, under each scheduler profile, we configure our plugins any way we want, within the yaml even.
- For instance, you could disable specific plugins or enable custom ones. 
- Below is an example where the "my-scheduler-2" profile disables the TaintToleration plugin and enables two custom plugins (MyCustomPluginA and MyCustomPluginB). Additionally, the "my-scheduler-3" profile disables all preScore and score plugins:
```
apiVersion: kubescheduler.config.k8s.io/v1
kind: KubeSchedulerConfiguration
profiles:
  - schedulerName: my-scheduler-2
    plugins:
      score:
        disabled:
          - name: TaintToleration
        enabled:
          - name: MyCustomPluginA
          - name: MyCustomPluginB
  - schedulerName: my-scheduler-3
    plugins:
      preScore:
        disabled:
          - name: '*'
      score:
        disabled:
          - name: '*'
  - schedulerName: my-scheduler-4
```
  - In the plugins section, specify the extension point and then enable or disable plugins by name (or using a wildcard pattern).
  - This flexible configuration allows you to tailor the scheduling behavior to meet your unique workload requirements by selectively enabling or disabling plugins across different profiles.