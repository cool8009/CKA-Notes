---
tags:
  - scheduling
aliases:
  - labels
  - selectors
  - label
  - selector
---
- They are a standard method to group and filter things together based on a single or multiple criteria.
- Labels are KV format, and are added under the `labels` section, under `metadata`.
- To select PODs with labels, use the `kubectl get pods --selector app=App1`
- For example, in a [[ReplicaSet]], we use a label for each of the PODs we want in our RS, and use a Selector in the RS definition, under the `template` section. **Make sure to not confuse this with the labels in the metadata, these are the RS's labels.**
- ```
```
apiVersion: apps/v1
kind: ReplicaSet
metadata:
  name: simple-webapp
  labels:
    app: App1
    function: Front-end
   annotations:
     buildVersion: 1.35
spec:
  replicas: 3
  selector:
    matchLabels:
      app: App1
  template:
    metadata:
      labels:
        app: App1
        function: Front-end
    spec:
      containers:
      - name: simple-webapp
        image: simple-webapp
```
- If you require more granular control for selecting Pods, you can list multiple labels in the `matchLabels` section.
- **Annotations** also exist. While labels and selectors are used for grouping and filtering, annotations are used to record other details for informatory purposes.
- Things like name, version, build version, contact info, whatever else you want. These also go under `metadata`