---
tags:
  - security
---
- **How do we create a role?** We create a **Role object**.
- To define a role, create a YAML file that sets the API version to `rbac.authorization.k8s.io/v1` and the kind to `Role`. In this example, we create a role named **developer** to grant developers specific permissions. The role includes a list of rules where each rule specifies the API groups, resources, and allowed verbs. For resources in the core API group, provide an empty string (`""`) for the `apiGroups` field.

- For instance, the following YAML definition grants developers permissions on pods (with various actions) and allows them to create ConfigMaps:

```
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: developer
rules:
- apiGroups: [""]
  resources: ["pods"]
  verbs: ["list", "get", "create", "update", "delete"]
- apiGroups: [""]
  resources: ["ConfigMap"]
  verbs: ["create"]
```

- Create the role by running:

```
kubectl create -f developer-role.yaml
```

- **After creating a role, you need to bind it to a user. To do that, you create a RoleBinding object.**
- Below is the combined YAML definition for both creating the role and its corresponding binding:

```
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: developer
rules:
- apiGroups: [""]
  resources: ["pods"]
  verbs: ["list", "get", "create", "update", "delete"]
- apiGroups: [""]
  resources: ["ConfigMap"]
  verbs: ["create"]
---
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: devuser-developer-binding
subjects:
- kind: User
  name: dev-user
  apiGroup: rbac.authorization.k8s.io
roleRef:
  kind: Role
  name: developer
  apiGroup: rbac.authorization.k8s.io
```

- Create the role binding using the command:

```
kubectl create -f devuser-developer-binding.yaml
```  

- **Roles and RBs fall under the scope of namespaces.**
- If you want to limit namespaces, specify the `namespace` field under the `metadata` section in the RB definition file.
- After applying your configurations, it's important to verify that the roles and role bindings have been created correctly.

- To list all roles in the current namespace, execute:

```
kubectl get roles
```

- Example output:

```
NAME        AGE
developer   4s
```

- Next, list all role bindings:

```
kubectl get rolebindings
```

- Example output:

```
NAME                      AGE
devuser-developer-binding 24s
```

- For detailed information about the **developer** role, run:

```
kubectl describe role developer
```

- Sample output:

```
Name:         developer
Labels:       <none>
Annotations:  <none>
PolicyRule:
  Resources           Non-Resource URLs   Resource Names   Verbs
  -----------         ------------------   --------------   ----
  ConfigMap           []                   []               [create]
  pods                []                   []               [get watch list create delete]
```

- To view the specifics of the role binding:

```
kubectl describe rolebinding devuser-developer-binding
```

- Example output:

```
Name:         devuser-developer-binding
Labels:       <none>
Annotations:  <none>
Role:
  Kind:    Role
  Name:    developer
Subjects:
  Kind     Name      Namespace
  ----     ----      ---------
  User     dev-user
```


- **What you wanna see if you have access to something?**
- You can test whether you have the necessary permissions to perform specific actions by using the `kubectl auth can-i` command. For example, to check if you can create deployments, run:

```
kubectl auth can-i create deployments
```

- This command might return:

```
yes
```

- Similarly, to verify if you can delete nodes:

```
kubectl auth can-i delete nodes
```

- Expected output:

```
no
```

- To test permissions for a specific user without switching user contexts, use the `--as` flag. Although the **developer** role does not permit creating deployments, it does allow creating pods:

```
kubectl auth can-i create deployments
# Output: yes
kubectl auth can-i delete nodes
# Output: no
kubectl auth can-i create deployments --as dev-user
# Output: no
kubectl auth can-i create pods --as dev-user
# Output: yes
```

- You can also specify a namespace in your commands to verify permissions scoped to that particular namespace.

- A note on resource names: 
  - You can go one level down from a Role and give access to a specific resource/s:
    ![[Pasted image 20260110203411.png]]
  - In some scenarios, you may want to restrict user access to a select group of resources. For example, if you have multiple pods in a namespace but only intend to provide access to pods named "blue" and "orange," you can utilize the `resourceNames` field in the role rule.

- Start with a basic role definition without any resource-specific restrictions:

```
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: developer
rules:
- apiGroups: [""]
  resources: ["pods"]
  verbs: ["get", "create", "update"]
```

- Then, update the rule to restrict access solely to the "blue" and "orange" pods:

```
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: developer
rules:
- apiGroups: [""]
  resources: ["pods"]
  verbs: ["get", "create", "update"]
  resourceNames: ["blue", "orange"]
```