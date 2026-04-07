---
tags:
  - service
  - services
  - yaml
aliases:
  - load balancer
  - LB
  - Load Balancer
---
- Supported on major cloud providers, and leverages the native LB of said providers.
- Does nothing if it's not as part of deployment on cloud.
- In general, after configuring a NodePort, now we can access our app via the same port on each of the nodes IP addresses. Problem here is, if we have 2 nodes with app A, and 2 nodes with app B, each app with a different port, **we can still access app B on nodes A and vise versa, due to how the NodePort works. It spans over all the nodes in the cluster:**
- ![16 Services Load Balancer image 1](Images/Pasted%20image%2020250319203029.png)
- This is what the LB does. 