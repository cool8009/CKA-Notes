Use the `kubectl edit` command for the deployment and specify the `serviceAccountName` field inside the `spec.template.spec`.  

OR  

Make use of the `kubectl set` command. Run the following command to use the newly created service account: - `kubectl set serviceaccount deploy/web-dashboard dashboard-sa`