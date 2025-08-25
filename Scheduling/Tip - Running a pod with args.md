Let's say you wanna run a busybox pod that will do something:
`kubectl run static-busybox --image=busybox --command -- sleep 1000`
anything after the `--` part (after the --command) will be considered args. 
You can also add `--dry-run` to it to make sure it works.