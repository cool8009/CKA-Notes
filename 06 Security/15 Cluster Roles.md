---
tags:
  - security
---
- **Roles and RoleBindings are namespaced.**
- This is the cluster-scoped counterpart to [[14 RBAC]].
- They control access within the namespace you mentioned alone. 
- But what about if you want to group non-namespaced resources like nodes? 
- Resources are categorized as namespaced, or **cluster scoped**.
- ![15 Cluster Roles image 1](Images/Pasted%20image%2020260117164549.jpg)
- For the cluster scoped resources, you don't specify a namespace upon creation.
- `kubectl api-resources --namespaced=true/false` to view a full list of resources.
- The API-group side of that resource model is easier to inspect once you know [[12 API Groups]].
- How do we auth users to cluster wide resources? 
- To authorize cluster-scoped resources, such as nodes and persistent volumes, you need to create cluster roles and cluster role bindings. Cluster roles function similarly to roles, but they are tailored for actions that span the entire cluster.

- For example, you can define a cluster administrator role that grants the ability to list, retrieve, create, and delete nodes. Alternatively, you might establish a storage administrator role to manage persistent volumes and persistent volume claims.

- Below is an example of a cluster role definition file named `cluster-admin-role.yaml`. This YAML file defines a ClusterRole that grants administrative permissions on nodes:

```
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: cluster-administrator
rules:
- apiGroups: [""]
  resources: ["nodes"]
  verbs: ["list", "get", "create", "delete"]
```

- Once the ClusterRole is created, you bind it to a user through a ClusterRoleBinding object. The following example binds the `cluster-administrator` ClusterRole to a user named `cluster-admin`:

```
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: cluster-admin-role-binding
subjects:
- kind: User
  name: cluster-admin
  apiGroup: rbac.authorization.k8s.io
roleRef:
  kind: ClusterRole
  name: cluster-administrator
  apiGroup: rbac.authorization.k8s.io
```

- Apply these configurations using the `kubectl create` command.
- Kubernetes provides several default cluster roles when the cluster is initially set up. Be sure to review these defaults to understand the baseline permissions before creating custom roles.
- **It's important to note that while cluster roles and role bindings are primarily used for cluster-scoped resources, they can also manage access to namespace-scoped resources. When you bind a cluster role that grants permissions on pods, for instance, the user will have access to pods in every namespace—unlike a namespaced role which restricts access to a single namespace.**

- The following image further distinguishes how cluster roles work for both namespaced and cluster-scoped resources:

![The image illustrates Kubernetes cluster roles, distinguishing between namespaced and cluster-scoped resources, including pods, services, nodes, and cluster roles.](https://kodekloud.com/kk-media/image/upload/v1752869934/notes-assets/images/CKA-Certification-Course-Certified-Kubernetes-Administrator-Cluster-Roles/frame_240.jpg)

- **ClusterRoles** defines roles on a cluster level, either for cluster scoped resources, or for non-cluster scoped resources that need to be accessed cluster-wide (i.e. giving a ClusterRole access to pods for user `dev` means dev can view all pods in the cluster.)
- 
