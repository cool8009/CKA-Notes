When trying to figure out who owns a pod, whether it's a node, a ReplicaSet, a Deployment etc. you can inspect a POD's yaml by running:
`kubectl get pod PodName -o yaml`
and looking for the `ownerReference` section. This property holds information about the owner of the POD.
You can also use filters and advanced kubectl commands, but we haven't learned them yet.