---
tags:
  - maintenance
---
`kubectl get nodes` shows the node version.
- The version number follows a SemVer structure:
- Kubernetes release versions follow a three-part semantic versioning scheme: major, minor, and patch.

- **Major versions** indicate significant changes.
- **Minor versions** are released every few months and introduce new features and functionalities.
- **Patch versions** are released more frequently to address critical bug fixes.

![The image illustrates semantic versioning, showing version "v1.11.3" with labels for major, minor, and patch updates.](https://kodekloud.com/kk-media/image/upload/v1752869695/notes-assets/images/CKA-Certification-Course-Certified-Kubernetes-Administrator-Kubernetes-Software-Versions/frame_50.jpg)

- ## The Evolution of Kubernetes

The first major release, version 1.0, was introduced in July 2015. At the time of recording, the latest stable version is 1.13.0. Kubernetes releases follow a lifecycle that includes alpha, beta, and stable phases:

- **Alpha releases:** Features are disabled by default and may be unstable.
- **Beta releases:** Features are enabled by default and undergo thorough testing.
- **Stable releases:** Fully tested and ready for production use.

![The image is a timeline showing software version releases from March 2015 to December 2018, including versions v0.12, v1.0, v1.2.0, and v1.13.0.](https://kodekloud.com/kk-media/image/upload/v1752869696/notes-assets/images/CKA-Certification-Course-Certified-Kubernetes-Administrator-Kubernetes-Software-Versions/frame_90.jpg)

Important

Always review the release notes before upgrading to ensure compatibility with your existing Kubernetes environment.

## Accessing Release Artifacts

You can find all Kubernetes releases on the [Kubernetes GitHub releases page](https://github.com/kubernetes/kubernetes/releases). After downloading the kubernetes.tar.gz file and extracting it, you will see executables for all Kubernetes components. Note that while the control plane components share the same version, additional components like the ETCD cluster and CoreDNS servers may have their own version numbers because they are maintained as separate projects. Each release's notes detail the supported versions of these external dependencies.

![The image shows a GitHub release page for Kubernetes version 1.13.4, including download links and SHA512 checksum information.](https://kodekloud.com/kk-media/image/upload/v1752869697/notes-assets/images/CKA-Certification-Course-Certified-Kubernetes-Administrator-Kubernetes-Software-Versions/frame_130.jpg)
  