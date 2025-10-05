---
tags:
  - ALM
---
- Let's try to understand rollouts and versioning in a deployment.
- When you first create a deployment, K8s initiates what's called a **rollout**. This rollout creates a new ReplicaSet, which establishes the first **deployment revision** (Revision 1).
- In the future, when the app is updated, a new rollout is triggered, and a new deployment revision named Revision 2 is subsequently created:
  ![[Pasted image 20251005091822.png]]
- This helps us track deployments, and helps us roll back to a previous deployment if necessary.
- To monitor and review these rollouts, you can use the following commands:

- Check the rollout status:

```
kubectl rollout status deployment/myapp-deployment
```

- View the history of rollouts:

```
kubectl rollout history deployment/myapp-deployment
```

- There are 2 types of **Deployment Strategies.**
- For example, say you have 5 replicas of your webapp. You can destroy all of these and create 5 new ones:
  ![[Pasted image 20251005092019.png]]
  - A more seamless approach is the "**rolling update**" strategy. Here, instances are updated one at a time, ensuring continuous application availability throughout the process.

- ![[Pasted image 20251005092046.png]]

- If no strategy is specified when creating a deployment, Kubernetes uses the rolling update strategy by default.
- How do you actually update though? Update can mean many things: a new app version, different tags, changing the amount of replicas, etc.
- Since we alr. have a dep definition file, we can just update that file and run `kubectl apply`. This will trigger a new rollout and revision number.
- Alternatively, you can update the container image directly using the following command:

```
kubectl set image deployment/myapp-deployment nginx-container=nginx:1.9.1
```
- Remember, using `kubectl set image` updates the running deployment but does not modify your deployment definition file. Ensure you update the file as well for future reference.


- To retrieve detailed information about your deployment—including rollout strategy, scaling events, and more—use:

```
kubectl describe deployment myapp-deployment
```

This output shows different details depending on the strategy used:

- **Recreate Strategy:** Events indicate that the old ReplicaSet is scaled down to zero before scaling up the new ReplicaSet.
- **Rolling Update Strategy:** The old ReplicaSet is gradually scaled down while the new ReplicaSet scales up.

For example, a deployment with the recreate strategy might display the following events:

```
Name:                   myapp-deployment
Namespace:              default
CreationTimestamp:      Sat, 03 Mar 2018 17:01:55 +0000
Labels:                 app=myapp
Annotations:            deployment.kubernetes.io/revision=2
                        kubectl.kubernetes.io/change-cause=kubectl apply --filename=deployment-definition.yml
Selector:               5 desired, 1 updated, 5 total, 5 available, 0 unavailable
StrategyType:           Recreate
MinReadySeconds:        0
Pod Template:
  Labels:  app=myapp
           type=front-end
  Containers:
   nginx-container:
    Image:      nginx:1.7.1
    Port:       <none>
Conditions:
  Type           Status  Reason
  ----           ------  ------
  Available      True    MinimumReplicasAvailable
  Progressing    True    NewReplicaSetAvailable
OldReplicaSets:  <none>
NewReplicaSet:   myapp-deployment-54c7d6ccc (5/5 replicas created)
Events:  
  Type    Reason             Age   From                    Message
  -----   ------             ----  ----                    -------
  Normal  ScalingReplicaSet  11m   deployment-controller  Scaled up replica set myapp-deployment-6795844b58 to 5
  Normal  ScalingReplicaSet  11m   deployment-controller  Scaled down replica set myapp-deployment-6795844b58 to 0
  Normal  ScalingReplicaSet  56s   deployment-controller  Scaled up replica set myapp-deployment-54c7d6ccc to 5
```

- In contrast, a rolling update strategy output would reflect gradual scaling changes:

```
kubectl describe deployment myapp-deployment
```

```
Name:                   myapp-deployment
Namespace:              default
CreationTimestamp:      Sat, 03 Mar 2018 17:16:53 +0800
Labels:                 app=myapp
Annotations:            deployment.kubernetes.io/revision=2
                        kubectl.kubernetes.io/change-cause=kubectl apply --filename=deployment-definition.yml
Selector:               6 desired, 5 updated, 6 total, 4 available, 2 unavailable
StrategyType:           RollingUpdate
MinReadySeconds:        0
RollingUpdateStrategy:  25% max unavailable, 25% max surge
Pod Template:
  Labels:  app=myapp
           type=front-end
  Containers:
   nginx-container:
    Image:      nginx
    Port:       <none>
Conditions:
  Type           Status  Reason
  ----           ------  ------
  Available      True    MinimumReplicasAvailable
  Progressing    True    ReplicaSetUpdated
OldReplicaSets:   myapp-deployment-67c749c58c (1/1 replicas created)
NewReplicaSet:    myapp-deployment-75d7bdbd8d (5/5 replicas created)
Events:  
  Type    Reason             Age   From                    Message
  -----   ------             ----  ----                    -------
  Normal  ScalingReplicaSet  1m    deployment-controller   Scaled up replica set myapp-deployment-67c749c58c to 5
  Normal  ScalingReplicaSet  1m    deployment-controller   Scaled down replica set myapp-deployment-75d7bdbd8d to 2
  Normal  ScalingReplicaSet  1m    deployment-controller   Scaled up replica set myapp-deployment-67c749c58c to 4
  Normal  ScalingReplicaSet  1m    deployment-controller   Scaled down replica set myapp-deployment-75d7bdbd8d to 3
  Normal  ScalingReplicaSet  0s    deployment-controller   Scaled down replica set myapp-deployment-75d7bdbd8d to 1
  Normal  ScalingReplicaSet  0s    deployment-controller   Scaled down replica set myapp-deployment-67c749c58c to 0
```


- **Under the hood**, when you trigger a deployment (ex. for 5 replicas), it first creates a ReplicaSet automatically, which in turn creates the # of pods required.
- When you upgrade your app, the K8s deployment object creates a **new** ReplicaSet under the hood, and start deploying the container there, while at the same time taking down the old pods in a rolling update strat:
  ![[Pasted image 20251005092639.png]]
- If you run `kubectl get replicasets`, you will be able to see this in action:

```
NAME                                 DESIRED   CURRENT   READY   AGE
myapp-deployment-67c749c58c          0         0         0       22m
myapp-deployment-7d57dbd8d           5         5         5       20m
```
- If an issue is detected after an upgrade, you can revert to the previous version using the rollback feature. To perform a rollback, run:

```
kubectl rollout undo deployment/myapp-deployment
```
- This command scales down the new ReplicaSet, restoring pods from the older ReplicaSet.

## Summary of Commands

Below is a quick reference table of the key commands discussed in this article:

| Command Description                               | Command                                                                     |
| ------------------------------------------------- | --------------------------------------------------------------------------- |
| Create the deployment                             | `kubectl create -f deployment-definition.yml`                               |
| List existing deployments                         | `kubectl get deployments`                                                   |
| Update deployment from the YAML definition        | `kubectl apply -f deployment-definition.yml`                                |
| Update the container image with kubectl set image | `kubectl set image deployment/myapp-deployment nginx-container=nginx:1.9.1` |
| Check the status of the rollout                   | `kubectl rollout status deployment/myapp-deployment`                        |
| Rollback to a previous deployment revision        | `kubectl rollout undo deployment/myapp-deployment`                          |