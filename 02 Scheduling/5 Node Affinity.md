---
tags:
  - scheduling
aliases:
  - Affinity
  - affinity
  - Node Affinity
---
- Node Affinity is more advanced scheduling solution that goes a step further than [[4 Node Selectors]].
- Node affinity enables advanced ways to limit or enable pod placement on specific nodes.
- **With great power comes great complexity. Consider these 2 examples:
- For node selector:```
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
- For node affinity:```
```
	apiVersion: v1
	kind: Pod
	metadata:
	  name: myapp-pod
	spec:
	  containers:
	    - name: data-processor
	      image: data-processor
	  affinity:
	    nodeAffinity:
	      requiredDuringSchedulingIgnoredDuringExecution:
	        nodeSelectorTerms:
	          - matchExpressions:
	              - key: size
	                operator: In
	                values:
	                  - Large
```

- Both of these examples **do exactly the same thing.**
- Let's understand the configuration of the node affinity yaml:
	• The `affinity` key under `spec` introduces the `nodeAffinity` configuration.  
	• The field `requiredDuringSchedulingIgnoredDuringExecution` indicates that the scheduler must place the pod on a node meeting the criteria. Once the pod is running, any changes to node labels are ignored.  
	• The `nodeSelectorTerms` array contains one or more `matchExpressions`. Each expression specifies a label key, an operator, and a list of values. Here, the `In` operator ensures that the pod is scheduled only on nodes where the label `size` includes ‘Large’.
- Like using `In` as the operator, you can also use `NotIn` which will exclude nodes with the labels specified. For example, to avoid nodes labeled as small:

```
  affinity:
    nodeAffinity:
      requiredDuringSchedulingIgnoredDuringExecution:
        nodeSelectorTerms:
          - matchExpressions:
              - key: size
                operator: NotIn
                values:
                  - Small
```

- For cases where you only want to verify **if a label exists, and not the value** use the `Exists` operator:
```
  affinity:
    nodeAffinity:
      requiredDuringSchedulingIgnoredDuringExecution:
        nodeSelectorTerms:
        - matchExpressions:
          - key: size
            operator: Exists
``````

- **Once a pod is scheduled using node affinity rules, these rules are only evaluated during scheduling. Changes to node labels after scheduling will not affect a running pod due to the "ignored during execution" behavior.**



---

- ![[Pasted image 20250504231323.png]]
- There are two primary scheduling behaviors for node affinity:

1. **Required During Scheduling, Ignored During Execution**
    
    - The pod is scheduled only on nodes that fully satisfy the affinity rules.
    - Once running, changes to node labels do not impact the pod.
2. **Preferred During Scheduling, Ignored During Execution**
    
    - The scheduler prefers nodes that meet the affinity rules but will place the pod on another node if no matching nodes are available.

**There are also 2 new types expected in the future that introduce a difference in the DuringExecution phase. In this model, if a node's labels change after a pod is running and no longer meet the affinity criteria, the pod would be evicted.**
![[Pasted image 20250504231418.jpg]]

**Summary**

Node affinity empowers you to define sophisticated scheduling rules for pod placement based on node labels. Key takeaways include:

- Using `nodeSelectorTerms` with `matchExpressions` to specify rules.
- Leveraging operators such as `In`, `NotIn`, and `Exists` for flexible matching.
- Understanding the scheduling phases: during scheduling and after deployment (execution), and how they interact.