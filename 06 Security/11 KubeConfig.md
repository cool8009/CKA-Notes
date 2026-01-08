---
tags:
  - security
---
- We've seen how to generate certs for users.
- We can also query the K8s API with curl.
- Previously, we generated a certificate for a user and utilized the certificate along with a key to query the Kubernetes REST API for a list of pods. For instance, if your cluster is named "my kube playground," you can make a curl request to the API server as follows:

```
curl https://my-kube-playground:6443/api/v1/pods \
  --key admin.key \
  --cert admin.crt \
  --cacert ca.crt
```

- The API server then returns a response similar to this:

```
{
  "kind": "PodList",
  "apiVersion": "v1",
  "metadata": {
    "selfLink": "/api/v1/pods"
  },
  "items": []
}
```

- Likewise, when using the kubectl command-line tool, you can supply the same parameters:

```
kubectl get pods \
  --server https://my-kube-playground:6443 \
  --client-key admin.key \
  --client-certificate admin.crt \
  --certificate-authority ca.crt
```

- The response in this case might be:

```
No resources found.
```


- Typing this is a tedious task. We can move this information to a config file, and specify it in a command line option:
  ![[Pasted image 20260106191311.png]]
- By default, `--kubeconfig` looks for a file called `config` in `~/.kube`.
- Once properly set up, you can simply execute:

```
kubectl get pods
```
   and kubectl will automatically use the configurations defined within the file.

- The kubeconfig file is organized into three key sections:

	- **Clusters:** Define the Kubernetes clusters you need access to (e.g., development, production, or clusters hosted by different cloud providers).
	- **Users:** Specify the user accounts and associated credentials (such as admin, dev, or prod users) that have permissions on the clusters.
	- **Contexts:** Link a cluster with a user by specifying which user should access which cluster. A context can also define a default namespace.

- Below is an example of a basic kubeconfig file in YAML format:

```
apiVersion: v1
kind: Config
clusters:
- name: my-kube-playground  # values hidden…
- name: development
- name: production
- name: google
contexts:
- name: my-kube-admin@my-kube-playground
- name: dev-user@google
- name: prod-user@production
users:
- name: my-kube-admin
- name: admin
- name: dev-user
- name: prod-user
```

- In this configuration, the server specification for the "my kube playground" cluster is defined in the clusters section, the admin user’s credentials are listed in the users section, and the context named `my-kube-admin@my-kube-playground` ties them together. Multiple contexts can be created for different clusters and users, and you can set a default context using the `current-context` field.
- **You are not configuring any users. You are just defining what users that already exist can access. **
- ![[Pasted image 20260106191625.png]]
- The `--server my-server:6441` and `--certificate-authority ca.crt` goes into the "Clusters" section.
  The `--client-key admin.key`, `--client-certificate admin.crt`,  go to the "Users" section.
- You then create a "Context" to tie the cluster to the user.
- To view the current kubeconfig settings, run:

```
kubectl config view
```

- This command outputs details about clusters, users, contexts, and the active context. An example output might look like:

```
apiVersion: v1
kind: Config
current-context: kubernetes-admin@kubernetes
clusters:
- cluster:
    certificate-authority-data: REDACTED
    server: https://172.17.0.5:6443
  name: kubernetes
contexts:
- context:
    cluster: kubernetes
    user: kubernetes-admin
  name: kubernetes-admin@kubernetes
users:
- name: kubernetes-admin
  user:
    client-certificate-data: REDACTED
    client-key-data: REDACTED
```

- If you want to view a custom kubeconfig file, use the `--kubeconfig` option:

```
kubectl config view --kubeconfig=my-custom-config
```

- A sample custom configuration may appear as follows:

```
apiVersion: v1
kind: Config
current-context: my-kube-admin@my-kube-playground #default context
clusters:
- name: my-kube-playground
  cluster:
    certificate-authority: ca.rt
    server: https://myserver:6443
    
- name: development
- name: production
contexts: #this links the cluster and the user together
- name: my-kube-admin@my-kube-playground
  context:
    cluster: my-kube-playground
    user: my-kube-admin
- name: prod-user@production
users:
- name: my-kube-admin
  user:
  	client-certificate: admin.cer
  	client-key: admin.key
- name: prod-user
```

- To change the active context—for example, switching from the admin user to the production user—execute:

```
kubectl config use-context prod-user@production
```
## Configuring Default Namespaces

- Namespaces in Kubernetes help segment clusters into multiple virtual clusters. You can configure a context to automatically use a specific namespace. Consider the following kubeconfig snippet without a default namespace:

```
apiVersion: v1
kind: Config
clusters:
- name: production
  cluster:
    certificate-authority: ca.crt
    server: https://172.17.0.51:6443
contexts:
- name: admin@production
  context:
    cluster: production
    user: admin
users:
- name: admin
  user:
    client-certificate: admin.crt
    client-key: admin.key
```

- To specify a default namespace (for example, "finance"), simply add the `namespace` field:

```
apiVersion: v1
kind: Config
clusters:
- name: production
  cluster:
    certificate-authority: ca.crt
    server: https://172.17.0.51:6443
contexts:
- name: admin@production
  context:
    cluster: production
    user: admin
    namespace: finance
users:
- name: admin
  user:
    client-certificate: admin.crt
    client-key: admin.key
```

- When you switch to this context, kubectl will automatically operate within the specified namespace.
- For best practices, use full paths for certificate files in your kubeconfig file. Alternatively, you can embed the certificate data directly using the `certificate-authority-data` field.
- For instance, specifying a full path looks like this:

```
apiVersion: v1
kind: Config
clusters:
- name: production
  cluster:
    certificate-authority: /etc/kubernetes/pki/ca.crt
```

Alternatively, you may embed the certificate data directly:

```
apiVersion: v1
kind: Config
clusters:
- name: production
  cluster:
    certificate-authority: /etc/kubernetes/pki/ca.crt
    certificate-authority-data: LS0tLS1CRUdJTiBD...
```

To decode base64 encoded certificate data, use the following command:

```
echo "LS0...bnJ" | base64 --decode
```

The decoded output will resemble:

```
-----BEGIN CERTIFICATE-----
MIICDCCAuCAQAwE...
-----END CERTIFICATE-----
```

In order to use a custom config, **Add the** `my-kube-config` **file to the** `KUBECONFIG` **environment variable.**

1. **Open your shell configuration file:**

```bash
vi ~/.bashrc
```

2. **Add one of these lines to export the variable:**

```bash
export KUBECONFIG=/root/my-kube-config
# OR
export KUBECONFIG=~/my-kube-config
# OR
export KUBECONFIG=$HOME/my-kube-config
```

3. **Apply the Changes:**
    
    **Reload the shell configuration to apply the changes in the current session:**
    

```bash
source ~/.bashrc
```