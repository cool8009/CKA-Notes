# Changelog

## 2026-04-07

### Overview

- Completed the original three-phase repository refresh:
  - Phase 1: repository audit and conventions analysis
  - Phase 2: local image embed migration for Obsidian and GitHub compatibility
  - Phase 3: internal wikilink and knowledge-graph improvement
- Preserved the existing study-note style and kept changes conservative, deterministic, and reviewable.

### Added

- `repo_audit_report.md`
  - audit summary of repo structure, writing conventions, link conventions, image conventions, and migration cautions
- `context_refresh_log.md`
  - detailed execution log and handoff document
- `final_repo_update_report.md`
  - concise final cross-phase summary
- `00 - CKA Notes Map.md`
  - root navigation page linking all major study chapters
- `01 Core Concepts/00 - Core Concepts Map.md`
  - chapter main page for the core concepts chapter
- `02 Scheduling/00 - Scheduling Map.md`
  - chapter main page for the scheduling chapter
- `03 Logging and Monitoring/00 - Logging and Monitoring Map.md`
  - chapter main page for the logging and monitoring chapter
- `04 Application Lifecycle Management/00 - Application Lifecycle Management Map.md`
  - chapter main page for the application lifecycle chapter
- `05 Cluster Maintenance/00 - Cluster Maintenance Map.md`
  - chapter main page for the cluster maintenance chapter
- `06 Security/00 - Security Map.md`
  - chapter main page for the security chapter
- `Exam Tips/00 - Exam Tips Map.md`
  - chapter main page for the exam tips chapter
- `01 Core Concepts/19 Control Plane.md`
  - new bridge note for control-plane references
- `05 Cluster Maintenance/00 kubeadm.md`
  - new bridge note for kubeadm-related operational references
- `06 Security/00 Certificates.md`
  - new bridge note for the certificate/TLS note cluster
- `scripts/migrate_local_image_embeds.py`
  - dry-run/apply migration script for local image embeds
- `scripts/analyze_internal_links.py`
  - internal wikilink analyzer and weak-note detector
- `scripts/build_chapter_maps.py`
  - dry-run/apply generator for the root map and chapter map pages

### Changed

#### Phase 1: Audit And Planning

- Read the repo before changing note content.
- Audited folder structure, naming patterns, frontmatter usage, internal-link conventions, and image usage.
- Identified local Obsidian image embeds as the main GitHub-rendering risk.
- Confirmed that local image embeds resolved cleanly before any migration work.

#### Phase 2: Local Image Migration

- Migrated `101` local Obsidian image embeds across `43` notes.
- Converted local `![[...]]` embeds to standard Markdown image links with correct relative paths.
- Preserved external Markdown images and other unrelated links.
- Limited formatting cleanup to image-adjacent spacing only.

Files updated in Phase 2:

- `01 Core Concepts`: `00 Cluster Architecture.md`, `01 Docker vs Conainerd.md`, `02 ETCD.md`, `04 kube-api.md`, `06 Controller-Manager.md`, `09 kube-proxy.md`, `10 POD.md`, `12 ReplicaSets.md`, `13 Deployments.md`, `14 Services - NodePort.md`, `15 Services - Cluster IP.md`, `16 Services - Load Balancer.md`, `17 Namespaces.md`, `18 Imperative vs Declarative.md`
- `02 Scheduling`: `1 Manual Scheduling.md`, `10 Static Pods.md`, `11 Priority Classes.md`, `12 Multiple Schedulers.md`, `13 Configuring Scheduler Profiles.md`, `14 Admissions Controllers (new 2025).md`, `15 Validating Admission Controllers (new 2025).md`, `2 Labels and Selectors.md`, `3 Taints and Tonerations.md`, `5 Node Affinity.md`, `6 Node Affinity vs Taints and Tolerations.md`, `7 Resource Limits.md`, `8 DaemonSets.md`
- `04 Application Lifecycle Management`: `1 Rolling Updates and Rollbacks.md`, `13 Vertical Pod Autoscaler.md`, `6 Secrets.md`, `9 Multi-Container Pods Design Patterns.md`
- `05 Cluster Maintenance`: `04 Cluster Upgrade Process.md`
- `06 Security`: `1 Security Intro.md`, `11 KubeConfig.md`, `12 API Groups.md`, `13 Authorization.md`, `14 RBAC.md`, `15 Cluster Roles.md`, `16 Service Accounts.md`, `5 TLS Basics.md`, `6 TLS In K8s.md`, `7 TLS in K8s - Generating Certificates.md`, `8 View Certificate Details.md`

#### Phase 3: Internal Link And Mind-Map Improvements

- Added selective concept-driven wikilinks across the main study clusters.
- Resolved prior placeholder-style links such as `[[control plane]]`, `[[kubeadm]]`, and `[[Certificates]]` by giving those concepts stable homes.
- Expanded the existing `nodes` and `worker node` placeholders into useful link targets.
- Improved note-to-note progression between foundational concepts, scheduling topics, security topics, maintenance topics, and autoscaling topics.
- Avoided bulk overlinking, file renames, and broad rewrites.
- Added a root map plus one chapter main page per top-level study chapter to mirror the navigation pattern used in the Hebrew trading vault.

Files updated in Phase 3:

- `01 Core Concepts`: `00 Cluster Architecture.md`, `02 ETCD.md`, `04 kube-api.md`, `05 Controllers.md`, `06 Controller-Manager.md`, `07 kube-scheduler.md`, `08 kubelet.md`, `09 kube-proxy.md`, `11 PODs as YAML.md`, `12 ReplicaSets.md`, `13 Deployments.md`, `14 Services - NodePort.md`, `15 Services - Cluster IP.md`, `16 Services - Load Balancer.md`, `17 Namespaces.md`, `18 Imperative vs Declarative.md`, `20 nodes.md`, `22 worker node.md`
- `02 Scheduling`: `1 Manual Scheduling.md`, `4 Node Selectors.md`, `5 Node Affinity.md`, `6 Node Affinity vs Taints and Tolerations.md`, `8 DaemonSets.md`, `10 Static Pods.md`, `11 Priority Classes.md`, `12 Multiple Schedulers.md`, `13 Configuring Scheduler Profiles.md`, `14 Admissions Controllers (new 2025).md`, `15 Validating Admission Controllers (new 2025).md`
- `03 Logging and Monitoring`: `1 Monitoring Kubernetes Cluster Components.md`
- `04 Application Lifecycle Management`: `1 Rolling Updates and Rollbacks.md`, `8 Multi Container Pods.md`, `9 Multi-Container Pods Design Patterns.md`, `10 Introduction To Autoscaling (2025 Updates).md`, `11 Horizontal Pod Autoscaler.md`, `12 In Place Pod Resizing.md`, `13 Vertical Pod Autoscaler.md`
- `05 Cluster Maintenance`: `01 Intro.md`, `03 K8s Releases.md`, `04 Cluster Upgrade Process.md`
- `06 Security`: `1 Security Intro.md`, `2 K8s Security Primitives.md`, `3 Authentication.md`, `4 TLS Introduction.md`, `6 TLS In K8s.md`, `7 TLS in K8s - Generating Certificates.md`, `10 Certificates API.md`, `11 KubeConfig.md`, `13 Authorization.md`, `14 RBAC.md`, `15 Cluster Roles.md`, `16 Service Accounts.md`
- root helper docs: `context_refresh_log.md`

### Validation

#### Phase 2 Validation

- local Obsidian image embeds resolved before migration: `101 / 101`
- ambiguous matches: `0`
- missing matches: `0`
- dry-run result:
  - notes scanned: `87`
  - notes with local Obsidian image embeds: `43`
  - local embeds processed: `101`
  - resolution failures: `0`
  - validation errors: `0`
- apply result:
  - notes scanned: `87`
  - notes changed by migration: `43`
  - local embeds converted: `101`
  - resolution failures: `0`
  - validation errors after write: `0`
- post-apply re-check:
  - remaining local Obsidian image embeds in scope: `0`
  - broken migrated local Markdown image links: `0`

#### Phase 3 Validation

- command:

```text
python scripts\analyze_internal_links.py --limit 30
```

- result:
  - notes scanned: `89`
  - wikilinks found: `247`
  - resolved wikilinks: `247`
  - unresolved wikilinks: `0`

#### Script Validation

- `python -m py_compile scripts\analyze_internal_links.py`
  - completed successfully

### Scope Boundaries And Intentional Non-Changes

- external Markdown images were left unchanged
- external regular Markdown links were left unchanged
- note filenames and folder names were not renamed
- placeholder notes were not bulk-normalized
- broad grammar cleanup, encoding cleanup, and style normalization were intentionally avoided
- internal note links remained in Obsidian wikilink style
- `04 Application Lifecycle Management/Images/aim routine.md` was intentionally left untouched

### Remaining Manual Review Candidates

- Placeholder or untitled notes:
  - `01 Core Concepts/21 1Untitled.md`
  - `01 Core Concepts/Untitled.md`
  - `01 Core Concepts/Untitled 1.md`
- Weakly connected study notes:
  - `02 Scheduling/9 Editing Pods and Deployments.md`
  - `03 Logging and Monitoring/2 Managing Application Logs.md`
  - `04 Application Lifecycle Management/2 Commands and Arguments in Docker.md`
  - `04 Application Lifecycle Management/3 Commands and Arguments in Kubernetes.md`
  - `04 Application Lifecycle Management/4 Configure Environment Variables in Applications.md`
  - `04 Application Lifecycle Management/7 Encrypting Secret Data at Rest.md`
  - `05 Cluster Maintenance/02 OS Upgrades.md`
  - `06 Security/17 Image Security.md`
  - `06 Security/18 Prerequisite - Security In Docker.md`
  - `06 Security/19 - Security Contexts.md`
  - `06 Security/20 - Network Policies.md`
  - `06 Security/9 View Certificate Lab Solution.md`
- Several `Exam Tips/*` notes remain intentionally isolated from the main concept graph.

### Generated Artifacts

- `scripts/__pycache__/migrate_local_image_embeds.cpython-311.pyc`
  - generated by running the image-migration script
- `scripts/__pycache__/analyze_internal_links.cpython-311.pyc`
  - generated by running the internal-link analyzer
- These are execution artifacts, not core deliverables.

### Related Project Docs

- `repo_audit_report.md`
- `context_refresh_log.md`
- `final_repo_update_report.md`
