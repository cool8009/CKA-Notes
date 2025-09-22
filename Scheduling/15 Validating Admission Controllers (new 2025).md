---
tags:
  - scheduling
aliases:
---
- In this lesson, we take an in-depth look at Admission Controllers in Kubernetes—covering both validating and mutating functions—and learn how to configure custom Admission Controllers.
- Understanding these controllers is essential for ensuring that Kubernetes objects are created and modified correctly.
- We looked at the `NamespaceExists` AC. It helps validate if a namespace alr. exists, and reject the req if it doesn't. This is known as a **validating AC**.
- The `DefaultStorageClass` plugin.
- The default storage class admission controller is enabled by default. When you create a PersistentVolumeClaim (PVC) without specifying a storage class, the request is authenticated, authorized, and then passed through the admission controller. This controller mutates the request by adding the default storage class if none is provided.

- For example, consider the following PVC creation request:

```
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: myclaim
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 500Mi
```

- After the request passes through the admission controller, it is mutated to include the default storage class:

```
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: myclaim
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 500Mi
  storageClassName: default
```

![[Pasted image 20250922170641.png]]

- This is a **Mutating Admission Controllers:** Modify the object (mutate the request) before it is created.
- There is also **Dual-Purpose Controllers:** Some controllers support both mutating and validating functions.
- Generally, mutiating ACs are invoked **first**, before validating ACs. This is so every change the mutating AC has made, can be considered by the validating AC.
- For example, if the namespace auto-provisioning admission controller (mutating) runs before the namespace existence admission controller (validating), the missing namespace is created, preventing potential validation failures:
  ![[Pasted image 20250922170847.png]]

## What if we want our own AC?

- To support external ACs, there are 2 special ACs available:
	  `MutatingAdmissionWebhook`
	  `ValidatingAdmissionWebhook`
- We can configure the webhooks to point to a server, whether external or inside the K8s cluster, and the server will have our own admission webhook service running, with our own code and logic.
- After a req goes through the the default AC chain, it will go through our custom AC.
- It does that by passing a json formatted `AdmissionReview` object, with all the data and details about the req.
- The webhook then sends back the response with an `AdmissionReview` object, with a result of whether the req is allowed or not.
- An example admission review object is as follows:

```
{
  "apiVersion": "admission.k8s.io/v1",
  "kind": "AdmissionReview",
  "request": {
    "uid": "705ab4f5-6393-11e8-b7cc-42010aa80002",
    "kind": {"group": "autoscaling", "version": "v1", "kind": "Scale"},
    "resource": {"group": "apps", "version": "v1", "resource": "deployments"},
    "subResource": "scale",
    "requestKind": {"group": "autoscaling", "version": "v1", "kind": "Scale"},
    "requestResource": {"group": "apps", "version": "v1", "resource": "deployments"}
  }
}
```

- A successful (allowed) response from the webhook might look like:

```
{
  "apiVersion": "admission.k8s.io/v1",
  "kind": "AdmissionReview",
  "response": {
    "uid": "<value_from request.uid>",
    "allowed": true
  }
}
```

- If the "allowed" field is false, the request is rejected.
- ![[Pasted image 20250922171347.png]]An illustration of the process.
- To start using webhooks, deploy your custom webhook server. This server handles your custom logic for mutating and/or validating requests. You can implement the server in any language that supports processing JSON admission review objects.
- Example impl.:
  Below is a sample snippet in Go that demonstrates setting up a webhook server:

```
package main


import (
	"encoding/json"
	"flag"
	"fmt"
	"io/ioutil"
	"net/http"


	admissionv1beta1 "k8s.io/api/admission/v1beta1"
	metav1 "k8s.io/apimachinery/pkg/apis/meta/v1"
	"k8s.io/klog"
)


// toAdmissionResponse creates an AdmissionResponse containing an error message.
func toAdmissionResponse(err error) *admissionv1beta1.AdmissionResponse {
	return &admissionv1beta1.AdmissionResponse{
		Result: &metav1.Status{
			Message: err.Error(),
		},
	}
}


// admitFunc defines the function type for validators and mutators.
type admitFunc func(*admissionv1beta1.AdmissionReview) *admissionv1beta1.AdmissionResponse


// serve handles the HTTP requests and passes them to the admit function.
func serve(w http.ResponseWriter, r *http.Request, admit admitFunc) {
	var body []byte
	if r.Body != nil {
		data, err := ioutil.ReadAll(r.Body)
		if err == nil {
			body = data
		}
	}
	// Further processing of the admission review object would occur here.
}
```

### Example: Python Webhook Server

Below is pseudocode for a simple webhook server using Python and Flask. This example includes both a validating and a mutating webhook endpoint.

```
from flask import Flask, request, jsonify
import base64


app = Flask(__name__)


@app.route("/validate", methods=["POST"])
def validate():
    object_name = request.json["object"]["metadata"]["name"]
    user_name = request.json["request"]["userInfo"]["name"]
    status = True
    message = ""
    if object_name == user_name:
        message = "You can't create objects with your own name"
        status = False
    return jsonify({
        "response": {
            "allowed": status,
            "uid": request.json["request"]["uid"],
            "status": {"message": message},
        }
    })


@app.route("/mutate", methods=["POST"])
def mutate():
    user_name = request.json["request"]["userInfo"]["name"]
    patch = [{"op": "add", "path": "/metadata/labels/users", "value": user_name}]
    encoded_patch = base64.b64encode(bytes(str(patch), 'utf-8')).decode('utf-8')
    return jsonify({
        "response": {
            "allowed": True,
            "uid": request.json["request"]["uid"],
            "patch": encoded_patch,
            "patchType": "JSONPatch",
        }
    })


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=443, ssl_context=('path/to/tls.crt', 'path/to/tls.key'))
```

- As you can see in the python code, the `validate()` method checks if a created object has the same name as the username of the creator. If so, it fails:
```
    object_name = request.json["object"]["metadata"]["name"]
    user_name = request.json["request"]["userInfo"]["name"]
    status = True
    message = ""
    if object_name == user_name:
        message = "You can't create objects with your own name"
        status = False
```
- There's also the `mutate()` method/webhook in the code, which will add the username as a label to any newly created object. If we take a closer look at the `patch` object in that method, it takes a json object with instructions on how to patch the object:
  `patch = [{"op": "add", "path": "/metadata/labels/users", "value": user_name}]
- The critical aspect of setting up webhooks is ensuring that your server processes the admission review objects and responds with a valid JSON object following the mutate and validate APIs.
- In the exam we won't be asked to actually develop this code, just need to know what it does and what the admission webhook server does.

## Configuring the Webhook in Kubernetes

Once your webhook server is deployed, configure Kubernetes to route requests to your service by creating a webhook configuration object. 
This is in case you run your webhook service in a POD in the cluster, and created a service for it so it can be accessed:
![[Pasted image 20250922172232.png]]
For instance, the following example shows a [ValidatingWebhookConfiguration] that validates pod creation:

```
apiVersion: admissionregistration.k8s.io/v1
kind: ValidatingWebhookConfiguration
metadata:
  name: "pod-policy.example.com"
webhooks:
  - name: "pod-policy.example.com"
    clientConfig:
      service:
        namespace: "webhook-namespace"
        name: "webhook-service"
      caBundle: "CiOtLS0tQk......tLS0K"
    rules:
      - apiGroups: [""]
        apiVersions: ["v1"]
        operations: ["CREATE"]
        resources: ["pods"]
        scope: "Namespaced"
```

In this configuration:

- **API Server Invocation:** The API server calls the webhook service when a pod is created:```
  operations: ["CREATE"]
  resources: ["pods"])
- **Security:** TLS is enforced by providing a valid certificate bundle: `caBundle`
- **Rules:** The `rules` section precisely specifies which operations (in this case, pod creation) trigger the webhook.
  