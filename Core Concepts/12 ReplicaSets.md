---
tags:
  - yaml
  - object
  - controllers
  - Controlplane
aliases:
  - replicaset
  - ReplicaSet
  - replicationcontroller
  - replicationcontrollers
  - ReplicationControllers
  - ReplicationController
  - ReplicaSets
---
- A replication controller controls replica. If we go back to the first scenario, where we have our application inside a single pod on a node, and it crashes, our users won't be able to access our app.
- We would like to have more than 1 instance of our application at the same time. 
- The ReplicationController helps us run more than a single instance of a single POD in our cluster, thus providing high availability.
- What if I plan to have a single POD? the RC can help by automatically bringing up a new POD when the existing one fails.
- The RC ensures the specified amount of PODs is always running.
- In the simple example from above, we have a single POD serving a set of users. When the load increases, an additional POD is created, and load is being balanced between the two:
	![[Pasted image 20250317190715.png]]
- If the demand further increases, we can deploy an additional **node** with additional PODs, furthering the load balancing in the cluster:
	![[Pasted image 20250317190810.png]]

- The RC spans across multiple nodes. It helps both balancing the load and scale the app when demand increases.
- RC vs ReplicaSet:
		Both have the same purpose.
		RC is the older tech, being replaced by ReplicaSet.
		ReplicaSet is the new reccomended way to set up an app.
		Minor differences in how they work, but the principles stay the same.
- To create a ReplicationController:	```
		apiVersion: v1 #version of K8s API to create the object.
		kind: ReplicationController #object type
		metadata: #metadata of the pod. Note the indentation.
		  name: myapp-rc
		  labels: #dictionary with any KV you want.
			  app: myapp
			  type: front-end 
		#the most crucial part for an RC:
		spec: #specifies what we need for the object
			template: #define a POD template, we can use a POD definition yaml:
				metadata: #metadata of the pod. Note the indentation.
					  name: myapp-pod
					  labels: #dictionary with any KV you want.
						  app: myapp
						  type: front-end 
					
						spec: #specifies what we need for the object
							containers: #list/array
							 - name: nginx-container
							 image: nginx
		replicas: 3
- Basically, it's like any K8s object yaml. We define a POD definition in the `template` section, note the indentation and not passing apiVersion and kind.
- Also, mention replication amount under `replicas`
- `kubectl create -f rc-filename.yaml`
- `kubectl get replicationcontroller`
- PODs created by and RC will automatically have the RC name and a unique guid.
- **What about ReplicaSet?**
- yaml for **ReplicaSet** is the same, except we use `apps/v1` for apiVersion and a different `kind`.
- There is also one important difference, with ReplicaSets we have to specify a **`selector`**.
- This helps the RS understand what PODs fall under it.
- Why do that if we already passed in a POD definition? Because an RS, unlike an RC, can also manage **PODs not created by it.** This is a required field in RS, not in RC.
- ```selector:
		matchLabels:
		  type: front-end
- This selector matches the labels to whatever you want to attach it to.
- `kubectl get replicatset`
- **Why do we label our objects in the first place?**
- Consider we have 3 PODs not created by an RS. The RS can still monitor them and create new ones if some fail, to achieve a desired state. The RS is more like a process that monitors the PODs.
- The RS knows what PODs to monitor via the **labels**. We can provide these labels under the `selector` section.
- Scaling the RS has multiple options:
		- Update the .yaml and run `kubectl replace -f` 
		- `kubectl scale --replicas=6 -f rs.yaml`
		- `kubectl scale --replicas=6 replicaset rs` TYPE param, NAME param 
- **Deleting the RS will also delete all underlying PODs.**
