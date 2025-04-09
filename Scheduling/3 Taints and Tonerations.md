---
tags:
  - scheduling
aliases:
  - taints
  - tolerations
  - taint
  - toleration
---
- An analogy: 
  A bug approaches the person. To prevent the bug from landing on the person, we spray the bug with a repellent spray, **a Taint.**
- The bug is **intolerant** to the person. However, there might be other bugs that **are tolerant.** The taint **doesn't affect them.**
- ![[Pasted image 20250409125255.png]]
  - 2 things decide if a bug can land on a person: the persons taint, and the bugs toleration to that taint.
  - In the analogy, the bug is a POD and the person is a Node.
  - They are used to set restrictions on what pods can be scheduled on what nodes.
  - When no restrictions apply, the scheduler places pods on the nodes evenly.
  - But what if we have dedicated resources on Node 1 for a particular use case or application.
  - First we prevent all PODs from being placed on node 1 by placing a taint on the node.
  - By default pods have **no tolerations**. This means that at this point, no pods will be placed on node 1, as none of them can tolerate the taint.
  - Second, we specify which pods we want to be able to be placed on the tainted node, so we specify a toleration for pod D.
  - ![[Pasted image 20250409125807.png]]
  - **Taints are set on nodes. Tolerations are set on [[10 POD]]**
  - Use:
    `kubectl taint nodes node-name key=value:taint-effect`
  - `taint-effect` is **what happens to pods that do NOT tolerate this taint.**
  - There are 3 taint effects:
    `NoSchedule | PreferNoSchedule | NoExecute`
  - NoExecute is like NoSchedule, but it also means that **existing pods on the tainted node will be evicted if they don't tolerate the taint.**
  - For pods, in the pod definition file:```
	apiVersion: v1 
	kind: Pod
	metadata:
	 name: myapp-pod 
	spec:
	 containers:
		#container spec

	tolerations:
	 `- key: "app"`
	     operator: "Equal"
	     value: "blue"
	     effect: "NoSchedule"
- Use the same values from the taint in the POD yaml.
- **IMPORTANT: Taints and tolerations do not tell the POD to not go to a particular node. It only tells other PODs where not to go. A pod that can tolerate taint X (toleration X) does not guarantee that it will be placed on a node with the taint X. It just means that it CAN be placed there, as opposed to pods without the specific toleration. In other words, it tells the NODE to accept pods with specific tolerations, not the other way around. 
- **If you goal is to restrict pods from nodes, it is achieved via [[node affinity]].
- The master node has an automatic taint from startup. 