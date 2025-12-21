---
tags:
  - exam-tips
---

Here’s a tip!

As you might have seen already, creating and editing YAML files is a bit difficult, especially in the CLI. During the exam, you might find it difficult to copy and paste YAML files from the browser to the terminal. Using the `kubectl run` command can help in generating a YAML template. And sometimes, you can even get away with just the `kubectl run` command without having to create a YAML file at all. For example, if you were asked to create a pod or deployment with a specific name and image, you can simply run the `kubectl run` command.

Use the below set of commands and try the previous practice tests again, but this time, try to use the below commands instead of YAML files. Try to use these as much as you can going forward in all exercises.

Reference (Bookmark this page for the exam. It will be very handy):

[https://kubernetes.io/docs/reference/kubectl/conventions/](https://kubernetes.io/docs/reference/kubectl/conventions/)

Create an NGINX Pod

```
kubectl run nginx --image=nginx
```

Generate POD Manifest YAML file (-o yaml). Don’t create it(–dry-run)

```
kubectl run nginx --image=nginx --dry-run=client -o yaml
```

Create a deployment

```
kubectl create deployment --image=nginx nginx
```

Generate Deployment YAML file (-o yaml). Don’t create it(–dry-run)

```
kubectl create deployment --image=nginx nginx --dry-run=client -o yaml
```

Generate Deployment YAML file (-o yaml). Don’t create it(–dry-run) and save it to a file.

```
kubectl create deployment --image=nginx nginx --dry-run=client -o yaml > nginx-deployment.yaml
```

Make necessary changes to the file (for example, adding more replicas) and then create the deployment.

```
kubectl create -f nginx-deployment.yaml
```

OR

In k8s version 1.19+, we can specify the –replicas option to create a deployment with 4 replicas.

```
kubectl create deployment --image=nginx nginx --replicas=4 --dry-run=client -o yaml > nginx-deployment.yaml
```


## 🧭 Option 1: Full YAML Outline (via `--recursive`)

bash

CopyEdit

`kubectl explain deployment --recursive | less`

🔍 Shows the **entire field hierarchy** — from top to bottom — so you can see:

- What goes where
    
- What fields exist (and which ones don’t!)
    
- How to structure your YAML properly
    

---

## 🧠 Option 2: Deep Dive into One Field

bash

CopyEdit

`kubectl explain deployment.spec.template`

🔍 Gives you a **description** of that specific field — usually tells you:

- What it's used for
    
- Whether it's optional or required
    
- Its substructure
    

You can go as deep as:

bash

CopyEdit

`kubectl explain deployment.spec.template.spec.containers`

---

### 🎯 Use case in exam:

You're staring at a YAML question and forget how to nest `volumeMounts`?

Boom:

bash

CopyEdit

`kubectl explain pod.spec.containers.volumeMounts`

You forget whether to use `matchLabels` or `matchExpressions` in a selector?

Boom:

bash

CopyEdit

`kubectl explain deployment.spec.selector`

---

This is _the_ CLI-native way to debug YAML field-by-field — no browser needed.



**Replacing pods:**
- Lets say your scheduler is down, and you wanna manually schedule a pod to a node. You need to delete and recreate the pod with the new pod definition file. you can use **kubectl delete**, or:
	`kubectl replace --force -f pod.yaml `
	this will ensure it will indeed delete and not give some bullshit about can't delete if nodeName prop is set.