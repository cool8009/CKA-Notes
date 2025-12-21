---
tags:
  - ALM
---
- While storing non-sensitive details like hostnames or usernames in a ConfigMap is acceptable, placing a password in such a resource is not secure. 
- Kubernetes Secrets provide a mechanism to safely store sensitive information by encoding the data (note: this is not encryption by default).
- Like ConfigMaps, you create a secret and then inject it.
- An imperative way and a declarative way exists.
- 
- `kubectl create secret generic app-secret --from-literal=DB_Host=mysql`
- `kubectl create secret generic app-secret --from-file=app_secret.properties`
- And the declarative way:
- 
 ```
apiVersion: v1
kind: Secret
metadata:
  name: app-secret
data:
  DB_Host: bXlzcWw=
  DB_User: cm9vdA==
  DB_Password: cGFzd3Jk
```
- On Linux hosts, you can convert plaintext values to Base64-encoded strings using the `echo -n` command piped to `base64`. For example:

```
echo -n 'mysql' | base64
echo -n 'root' | base64
echo -n 'paswrd' | base64
# Output: cGFzd3Jk
```

## Viewing and Decoding Secrets

After creating a Secret, you can list and inspect it with the following commands:

- **List Secrets:**
    
    ```
    kubectl get secrets
    ```
    
    Expected output:
    
    ```
    NAME          TYPE    DATA   AGE
    app-secret    Opaque    3    10m
    ```
    
- **Describe a Secret (without showing sensitive data):**
    
    ```
    kubectl describe secret app-secret
    ```
    
- **View the encoded data in YAML format:**
    
    ```
    kubectl get secret app-secret -o yaml
    ```
    

If you need to decode an encoded value, use the `base64 --decode` command:

```
echo -n 'bXlzcWw=' | base64 --decode
echo -n 'cm9vdA==' | base64 --decode
echo -n 'cGFzd3Jk' | base64 --decode
# Output: paswrd
```
### Injecting as Environment Variables

Below is an example Pod definition that injects the Secret as environment variables:

```
# pod-definition.yaml
apiVersion: v1
kind: Pod
metadata:
  name: simple-webapp-color
  labels:
    name: simple-webapp-color
spec:
  containers:
  - name: simple-webapp-color
    image: simple-webapp-color
    ports:
    - containerPort: 8080
    envFrom:
    - secretRef:
        name: app-secret
```
![[Pasted image 20251130230434.png]]
### Mounting Secrets as Files

Alternatively, mount the Secret as files within a volume. Each key in the Secret becomes a separate file:

```
volumes:
- name: app-secret-volume
  secret:
    secretName: app-secret
```

After mounting, listing the directory contents should display each key as a file:

```
ls /opt/app-secret-volumes
# Output: DB_Host  DB_Password  DB_User
```

To view the content of a specific file, such as the DB password:

```
cat /opt/app-secret-volumes/DB_Password
# Output: paswrd
```

## Important Considerations When Using Secrets

Warning

Remember that Kubernetes Secrets are only encoded in Base64, not encrypted by default. Anyone with sufficient access can decode the data. Always handle secret definition files with care and avoid storing them in public repositories.

Here are some key considerations:

- Secrets offer only Base64 encoding. For enhanced security, consider enabling encryption at rest for etcd.
- Limit access to Secrets using Role-Based Access Control (RBAC). Restrict permissions to only those who require it.
- Avoid storing sensitive secret definition files in source control systems that are publicly accessible.
- For even greater security, explore third-party secret management solutions such as AWS Secrets Manager, Azure Key Vault, GCP Secret Manager, or Vault.

## External Secret Providers

External secret providers decouple secret management from etcd and offer advanced encryption, granular access control, and comprehensive auditing capabilities. For further details and best practices, consider exploring courses like the [Certified Kubernetes Security Specialist (CKS)](https://learn.kodekloud.com/user/courses/certified-kubernetes-security-specialist-cks).

![The image provides guidelines on handling secrets, emphasizing encryption, access control, and considering third-party providers for secure storage.](https://kodekloud.com/kk-media/image/upload/v1752869672/notes-assets/images/CKA-Certification-Course-Certified-Kubernetes-Administrator-Secrets/frame_470.jpg)