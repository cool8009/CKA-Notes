---
tags:
  - security
---
- The core security features in K8s.
## Securing Cluster Hosts

- The security of your Kubernetes cluster begins with the hosts themselves. Protect your underlying infrastructure by following these practices:

- Disable root access.
- Turn off password-based authentication.
- Enforce SSH key-based authentication.
- Implement additional measures to secure your physical or virtual systems.

- A compromised host can expose your entire cluster, so securing these systems is a critical first step.

![The image illustrates "Secure Hosts" with three outlined devices and notes on disabling password authentication and using SSH key-based authentication.](https://kodekloud.com/kk-media/image/upload/v1752869937/notes-assets/images/CKA-Certification-Course-Certified-Kubernetes-Administrator-Kubernetes-Security-Primitives/frame_40.jpg)

- Our focus though, is more on the cluster itself.
- The API server is the first line of defense, as it is the heart of the system.
- **Who can access the cluster and what can they do?** Are the questions we should ask ourselves.

  ### Authentication

- Authentication verifies the identity of a user or service before granting access to the API server. Kubernetes offers various authentication mechanisms to suit different security needs:

	- Static user IDs and passwords
	- Tokens
	- Client certificates
	- Integration with external authentication providers (e.g., LDAP)

- Additionally, service accounts support non-human processes. Detailed guidance on these methods is available in dedicated sections of our documentation.

![The image outlines authentication methods, including usernames, passwords, tokens, certificates, LDAP, and service accounts, under the question "Who can access?"](https://kodekloud.com/kk-media/image/upload/v1752869939/notes-assets/images/CKA-Certification-Course-Certified-Kubernetes-Administrator-Kubernetes-Security-Primitives/frame_120.jpg)

### Authorization

- After authentication, authorization determines what actions a user or service is allowed to perform. The default mechanism, Role-Based Access Control (RBAC), associates identities with specific permissions. Kubernetes also supports:

	- Attribute-Based Access Control (ABAC)
	- RBAC
	- Node Authorization
	- Webhook-based authorization

- These mechanisms enforce granular access control policies, ensuring that authenticated entities can perform only the operations they are permitted to execute.

![The image lists types of authorization: RBAC, ABAC, Node Authorization, and Webhook Mode, under the heading "Authorization: What can they do?"](https://kodekloud.com/kk-media/image/upload/v1752869939/notes-assets/images/CKA-Certification-Course-Certified-Kubernetes-Administrator-Kubernetes-Security-Primitives/frame_140.jpg)

- All the comms in cluster work via TLS certs.
- More on it later.
- What about stuff in the cluster? by default all pods in the cluster can talk to eachother. You can restrict access inside the cluster as well.
- These policies allow you to:

- Control traffic flow between specific pods
- Enforce security rules at the network level