<!--
  ~ Copyright (c) 2025 Arista Networks, Inc.
  ~ Use of this source code is governed by the Apache License 2.0
  ~ that can be found in the LICENSE file.
  -->

# Diataxis Framework

Start applying the [diataxis](https://diataxis.fr/) framework to the AVD documentation site

1. Understanding the framework
2. Applying the framework

![Diátaxis framework documentation map](https://diataxis.fr/_images/diataxis.png)

## Definitions

- **Learning**: The process of acquiring new knowledge, skills, values, or behaviors through study, experience, or being taught. It's about gaining competence.

- **Goals**: The specific aim or desired result of an effort or ambition. Goals provide a target to direct actions and measure success.

- **Information**: Raw facts, data, statistics, or details about a subject. It's the "what" of a topic, without interpretation or context.

- **Understanding**: The ability to comprehend or grasp the meaning, significance, and nature of something. It involves interpreting information to see connections and context.

- **Acquisition**: The act of gaining or acquiring something. In this context, it refers to the process of obtaining knowledge, skills, or information.

- **Application**: The act of putting something to a practical use. It involves applying acquired knowledge or tools to solve a real-world problem.

- **Action**: The process of doing something. It refers to the practical steps and activities involved in performing a task or achieving a goal.

- **Cognition**: The mental process of acquiring knowledge and understanding through thought, experience, and the senses. It involves thinking, reasoning, and remembering.

| If the content… | …and serves the user's… | …then it must belong to… |
| :--- | :--- | :--- |
| informs action | acquisition of skill | a tutorial |
| informs action | application of skill | a how-to guide |
| informs cognition | application of skill | reference |
| informs cognition | acquisition of skill | explanation |

| | Tutorials | How-to guides | Reference | Explanation |
| :--- | :--- | :--- | :--- | :--- |
| **what they do** | introduce, educate, lead | guide | state, describe, inform | explain, clarify, discuss |
| **answers the question** | “Can you teach me to…?” | “How do I…?” | “What is…?” | “Why…?” |
| **oriented to** | learning | goals | information | understanding |
| **purpose** | to provide a learning experience | to help achieve a particular goal | to describe the machinery | to illuminate a topic |
| **form** | a lesson | a series of steps | dry description | discursive explanation |
| **analogy** | teaching a child how to cook | a recipe in a cookery book | information on the back of a food packet | an article on culinary social history |

### Compass

| | Tutorials | How-to guides | Reference | Explanation |
| :--- | :--- | :--- | :--- | :--- |
| **Analogy** | Teaching a child how to cook | A recipe in a cookery book | A dictionary | An article on culinary social history |
| **Form** | A lesson, that builds understanding | A series of steps to follow | A description of the machinery | Discursive, like an article |
| **Purpose** | To provide a learning experience | To help the user achieve a goal | To state, describe and specify | To explain, clarify and discuss |
| **User's goal** | Learning | A particular goal | Information | Understanding |
| **Path** | Prescribed and linear | The user’s own | The user’s own | The user’s own |

## Examples

- [Ubuntu](https://documentation.ubuntu.com/server/) **- Bad**
- [Ansible](https://docs.ansible.com/ansible/latest/index.html) **- Bad**
- [Kubernetes](https://kubernetes.io/docs/home/) **- Good**
- [Cloudflare](https://developers.cloudflare.com/products/)
- [Container Lab](https://containerlab.dev/) **- Excellent**

### Structure

| Ubuntu | Ansible | Kubernetes | Cloudflare |
| :--- | :--- | :--- | :--- |
| Tutorial | Getting Started | Concepts | Concepts |
| How-to guides |  Using Ansible | Tasks | *Function Specific* |
| Reference | Reference & Appendices | Reference | Reference |
| Explanation |  |  | Troubleshooting |

### Pros and Cons

| Product | Pros | Cons |
| - | - | - |
| Ubuntu | Simple follows the framework to the letter  |  |
| Ansible | Great reference structure, easy to follow between different projects | Hard to follow documentation structure |

## Proposed Framework

![image](framework.png)

## Organisation/Structure

Key design principals

- easy to navigate
- clear navigation headers

Move Navigation headers horizontally
Use container labs has a reference model
Use some components from diataxis and containerlab

- collapse tutorials and how-to guides **[Tutorials]**
- collapse reference and explanation **[User Manual]**

## Navigation Menu

### Current

```yaml
Home
Getting Started
Examples
Installation
Ansible Collection Roles
Ansible Collection plugins
Contributing to avd
Release Notes
Porting Guide
PyAVD
Versioning
AVD Dev Containers
Support
```

### Proposed

```yaml
Home
Quick Start
Installation
Tutorials [How-to Guides]
User Manual
Release Notes
Contribute
Support
```

### Quick Start

A quick start is a condensed set of instructions designed to help a user begin using a product or service as quickly as possible, focusing only on the most essential steps.
Its primary goal is to get a user to a basic, functional state immediately, bypassing comprehensive details and advanced features. A quick start guide prioritizes speed and immediate results over thorough understanding.

- **Minimalist**: It includes only the critical information needed to get started.
- **Action-Oriented**: It focuses on a sequence of actions rather than explaining concepts.
- **Fast**: It's designed to be completed in a very short amount of time.
- **Not Comprehensive**: It intentionally omits advanced options, detailed explanations, and troubleshooting for edge cases.

```yaml
Installation
Inventory
Inputs [Maybe]
Build
Deploy
Outputs [Maybe]
```

### Tutorials [How-to Guides]

A tutorial is a step-by-step learning experience designed for a beginner. It guides the user through a series of practical steps to complete a specific task from start to finish. The goal is to build foundational skills and understanding.

- **Goal**: To teach a user how to do something.
- **Structure**: Linear and sequential (Step 1, Step 2, Step 3...).
- **Analogy**: A cooking class or a guided project.
- **Use Case**: You're new to a photo editing app and follow a tutorial to learn how to remove a background from an image.

How do we structure the how-to guides ?

- roles
- technology
- topology

```yaml
Node Types
  Definition
  Defaults
Roles
  eos_designs
  eos_cli_config_gen
  cv_deploy
  anta_runner


```

### User Manual

A `user manual` is a comprehensive reference guide that describes a product's features and functions in detail. It's not meant to be read from start to finish. Instead, users consult it when they have a specific question or need to understand a particular feature.

- **Goal**: To inform and provide technical details.
- **Structure**: Topical and organized for quick look-ups (like a dictionary or encyclopedia).
- **Analogy**: A car's owner manual or a technical encyclopedia.
- **Use Case**: You already know how to use the photo editing app, but you look up the "Magic Wand Tool" in the manual to see its specific tolerance settings.

```yaml
Concepts
  Build
  Deploy
  Validate
Roles
  eos_designs
  cli_config_gen
  cvp_configlet_upload
  eos_config_deploy_cvp
  eos_config_deploy_eapi
  eos_validate_state
  eos_snapshot
  dhcp_provisioner
  build_output_folders
  cv_deploy
  anta_runner
Node Types
Network Services
Connected Endpoints
Input Variables
PyAVD
Versioning
```
