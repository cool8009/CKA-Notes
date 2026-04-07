---
tags:
  - security
---
- 2 types of accs in K8s - **service account and user accounts.**
- Service accounts are the non-human identity side of [[3 Authentication]].
- ![16 Service Accounts image 1](Images/Pasted%20image%2020260117165747.jpg)
- Consider an example: "my Kubernetes dashboard," a basic dashboard application built with Python. 
- This application retrieves a list of Pods from a Kubernetes cluster by sending API requests and subsequently displays the results on a web page. To authenticate its API requests, the application uses a dedicated service account.

![The image shows a Kubernetes dashboard interface connected to a Kubernetes cluster with three nodes via the kube-api.](https://kodekloud.com/kk-media/image/upload/v1752869951/notes-assets/images/CKA-Certification-Course-Certified-Kubernetes-Administrator-Service-Accounts/frame_110.jpg)

- To create a service account named `dashboard-sa`, run:

```
kubectl create serviceaccount dashboard-sa
```

- To view all service accounts, use:

```
kubectl get serviceaccount
```

- The output will appear similar to:

```
NAME           SECRETS   AGE
default        1         218d
dashboard-sa   1         4d
```

- Upon creation, Kubernetes automatically generates a service account token stored as a Secret and links it to the account. To inspect the details of your service account and its token, execute:

```
kubectl describe serviceaccount dashboard-sa
```

- Expected output:

```
Name:                dashboard-sa
Namespace:           default
Labels:              <none>
Annotations:         <none>
Image pull secrets:  <none>
Mountable secrets:   dashboard-sa-token-kbbdm
Tokens:              dashboard-sa-token-kbbdm
Events:              <none>
```

- To examine the token itself, view the corresponding Secret:

```
kubectl describe secret dashboard-sa-token-kbbdm
```

- Sample output:

```
Name:                dashboard-sa-token-kbbdm
Namespace:           default
Labels:              <none>
Type:                kubernetes.io/service-account-token
Data
  token: eyJhbGciOiJSUzI1NiIsImtpZCI6Ij...  (truncated for privacy)
```

- This token serves as the authentication bearer token for accessing the Kubernetes API. For example, using curl:

```
curl https://192.168.56.70:6443/api -k \
--header "Authorization: Bearer eyJhbgG…"
```


- By default, K8s creates an SA called `default`.
- When a pod is created, the default SA is automatically attached to it:
  ![16 Service Accounts image 2](Images/Pasted%20image%2020260117170112.png)
- The SA gets mounted as a **projected volume**, like a dynamic dir created inside the pod by K8s.
- This token is typically available at the path: `/var/run/secrets/kubernetes.io/serviceaccount`.
- You must create a custom SA if you don't want the default one, like desc. Above.
- Upon creation, Kubernetes automatically generates a service account token stored as a Secret and links it to the account. To inspect the details of your service account and its token, execute:

```
kubectl describe serviceaccount dashboard-sa
```

- Expected output:

```
Name:                dashboard-sa
Namespace:           default
Labels:              <none>
Annotations:         <none>
Image pull secrets:  <none>
Mountable secrets:   dashboard-sa-token-kbbdm
Tokens:              dashboard-sa-token-kbbdm
Events:              <none>
```

- To examine the token itself, view the corresponding Secret:

```
kubectl describe secret dashboard-sa-token-kbbdm
```

- Sample output:

```
Name:                dashboard-sa-token-kbbdm
Namespace:           default
Labels:              <none>
Type:                kubernetes.io/service-account-token
Data
  token: eyJhbGciOiJSUzI1NiIsImtpZCI6Ij...  (truncated for privacy)
```

- This token serves as the authentication bearer token for accessing the Kubernetes API. For example, using curl:

```
curl https://192.168.56.70:6443/api -k \
--header "Authorization: Bearer eyJhbgG…"
```  


- By default, Pods use the `default` service account. To assign a different service account—like the previously created `dashboard-sa`—update your Pod definition to include the `serviceAccountName` field:

```
apiVersion: v1
kind: Pod
metadata:
  name: my-kubernetes-dashboard
spec:
  serviceAccountName: dashboard-sa
  containers:
    - name: my-kubernetes-dashboard
      image: my-kubernetes-dashboard
```


- After deploying the updated manifest, running:

```
kubectl describe pod my-kubernetes-dashboard
```

will show that the new service account is now in effect, with volume mounting information reflecting the token for `dashboard-sa` (e.g., `dashboard-sa-token-kbbdm`).

- If you wish to disable the automatic mounting of the service account token, set `automountServiceAccountToken` to `false` in the Pod specification:

```
apiVersion: v1
kind: Pod
metadata:
  name: my-kubernetes-dashboard
spec:
  automountServiceAccountToken: false
  containers:
  - name: my-kubernetes-dashboard
    image: my-kubernetes-dashboard
```
Or use the same param in the SA definition file to make it SA wide.

- Permissions for these accounts are typically granted with [[14 RBAC]] or [[15 Cluster Roles]].


**What if you want to create a token to be used outside a cluster?**
- In such cases, you can run:
  `kubectl create token my-sa`
- This will print a token, that is not stored anywhere.
- By default, these tokens are valid for 1 hour. To extend the duration use the `--duration=2h` flag.
- You can verify and decode this token using tools like jq or [jwt.io](https://jwt.io/):

```
jq -R 'split(".") | select(length > 0) | .[0] | @base64 | fromjson' <<< <TOKEN>
```

- If necessary (though not recommended), you can still create a non-expiring token by manually creating a Secret. Ensure the service account exists first:

```
apiVersion: v1
kind: Secret
metadata:
  name: mysecretname
  annotations:
    kubernetes.io/service-account.name: dashboard-sa
type: kubernetes.io/service-account-token
```

- It is highly recommended to use the TokenRequest API to generate tokens, as API-generated tokens provide additional security features such as expiry, audience restrictions, and improved manageability.
## Summary

- **Service Accounts vs. User Accounts:** Service accounts are meant for applications (or machines), whereas user accounts are for human users.
- **Token Generation:** Creating a service account automatically generates a token stored in a Secret, which is used for API authentication.
- **Automatic Token Mounting:** Pods can automatically mount the service account token at `/var/run/secrets/kubernetes.io/serviceaccount`, though this behavior can be modified.
- **Enhanced Security:** Since Kubernetes v1.22, tokens are generated using the TokenRequest API, making them audience-bound, time-bound, and more secure.
- **Kubernetes v1.24 Changes:** With v1.24, Kubernetes no longer provisions non-expiring tokens automatically via Secrets; use the `kubectl create token` command to generate tokens as needed.

![16 Service Accounts image 3](Images/Pasted%20image%2020260117171050.png)


****
