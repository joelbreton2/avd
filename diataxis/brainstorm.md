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

### Key design principals

- Easy to navigate
- Clear navigation headers
- Optimize page length for content and performance
- Use container labs has a reference model
- Use some components from diataxis and containerlab
- Remove Roles concept as this is an ansiblism, focus on cloudvision integration model

### Proposed changes

- Move Navigation headers horizontally
- collapse tutorials and how-to guides **[Tutorials]**
- collapse reference and explanation **[User Manual]**

> ***Note:*** The current structure is designed to be flexible. As the project evolves, we can separate the content into more granular sections to maintain clarity and organization
>
## Navigation Menu

### Discussion

#### Changes

- Move the Main Navigation Menu Horizontally to the top of the Page

#### Questions

- Do we remove completely the navigation menu on the left?
- Where do we move Ansible Collection Plugins

### Current Navigation

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

### Proposed Navigation

```yaml
Home
Quick Start
Installation
Tutorials [How-to Guides]
User Manual
Topology Examples
Release Notes
Contribute
Support
```

#### Horizontally

[aclabs](https://aclabs.arista.com/)
![image](navigation_menu.png)

```yaml
Home   Quick Start   Installation   Tutorials   User Manual   Topology Examples   Release Notes   Contribute   Support
```

## Quick Start

### Definition

A quick start is a condensed set of instructions designed to help a user begin using a product or service as quickly as possible, focusing only on the most essential steps.
Its primary goal is to get a user to a basic, functional state immediately, bypassing comprehensive details and advanced features. A quick start guide prioritizes speed and immediate results over thorough understanding.

- **Minimalist**: It includes only the critical information needed to get started.
- **Action-Oriented**: It focuses on a sequence of actions rather than explaining concepts.
- **Fast**: It's designed to be completed in a very short amount of time.
- **Not Comprehensive**: It intentionally omits advanced options, detailed explanations, and troubleshooting for edge cases.

### Questions/Discussion

1. Do we need a separate section for local and cvaas?

### Proposed Structure

```yaml
Table of contents

Installation
Inventory
Inputs (group_vars)
  Fabric (physical)
    Common Settings
    Node Types
      Defaults
      Nodes
      Node Groups
  Network Services (logical)
  Connected Endpoint (clients)
Workflow
  Build (playbook)
  Deploy (playbook)
  Validate (playbook)
Folder Structure (outputs)
  Intended
  Documentation
```

### With Topics

``` yaml
Table of contents

Installation
  pip [topic]
  uv [topic]
Inventory
Inputs
  Fabric (physical)
    Node Types [section]
      spine [topic]
      l3leaf [topic]
      l2leaf [topic]
    Defaults [section]
    Nodes [section]
    Node Groups [section]
    Common Settings [section]
      connectivity [topic]
      fabric_name [topic]
      local_users [topic]
      mgmt_gateway [topic]
      dns_settings [topic]
      ntp_settings [topic]
  Network Services (logical)
  Connected Endpoint (clients)
Build

Deploy
Outputs [Maybe]
```

## Tutorials [How-to Guides]

### Definition

A tutorial is a step-by-step learning experience designed for a beginner. It guides the user through a series of practical steps to complete a specific task from start to finish. The goal is to build foundational skills and understanding.

- **Goal**: To teach a user how to do something.
- **Structure**: Linear and sequential (Step 1, Step 2, Step 3...).
- **Analogy**: A cooking class or a guided project.
- **Use Case**: You're new to a photo editing app and follow a tutorial to learn how to remove a background from an image.

### Question/Discussion

1. Do we use Tutorials or How-to Guides

### Proposed Structure

```yaml
Node Types
  Definition
  Defaults
Connected Endpoints
Network Services

Current How-to's
  Configuring PTP
  Configuring WAN
  Custom Descriptions and Names
  Custom Structured Configuration
  Custom Templates x2
  Generate Cloudvision Tags
```

## User Manual

### Definition

A `user manual` is a comprehensive reference guide that describes a product's features and functions in detail. It's not meant to be read from start to finish. Instead, users consult it when they have a specific question or need to understand a particular feature.

- **Goal**: To inform and provide technical details.
- **Structure**: Topical and organized for quick look-ups (like a dictionary or encyclopedia).
- **Analogy**: A car's owner manual or a technical encyclopedia.
- **Use Case**: You already know how to use the photo editing app, but you look up the "Magic Wand Tool" in the manual to see its specific tolerance settings.

### Question/Discussion

### Current Structure

```yaml
Ansible Collection Roles
  eos_designs
    Input Variables
      Supported designs
      Design Type
      Fabric Topology
      Fabric IP Addressing
      Fabric Numbering
      Node Type Variables
      Node Type Customization
      Type Settings
      Default Node Type Settings
      Node Type Settings
      Default Interface Settings
      L3 Edge and DCI
      Core Interfaces Settings
      Flagging a device as not deployed
      Fabric Settings
      Management Interface Settings
      BFD Settings
      BGP Settings
      ACL Settings
      OSPF Settings
      Overlay Settings
      EVPN Settings
      WAN Settings
      Management Settings
      Monitoring
      QoS
      System Settings
      Cloud Vision
      Endpoint Connectivity
      Network Services
      Platform Settings
      PTP Settings
      Custom Structure
      CloudVision Topology
      Digital Twin
  eos_cli_config_gen
    Input Variables
      Authentication
      ACLs
      Endpoint Security
      Filters and Policies
      Interfaces
      Maintenance Mode
      Management
      Miscellaneous
      Monitoring
      Multicast
      Quality of Service
      Routing
      Security
      Switching
      System Settings
      Metadata

### Proposed Structure
```yaml
Concepts
  Build
  Deploy
  Validate
Node Types
Network Services
Connected Endpoints
Input Variables
  Node Types
    Variables
    Settings
    Customization
    Defaults
  Top Level Keys
    default_interfaces
    l3_edge
    core_interfaces
    is_deployed
  Fabric Settings
  Management Interface Settings
  BFD Settings
  BGP Settings
  ACL Settings
  OSPF Settings
  Overlay Settings
  EVPN Settings
  WAN Settings
  Management Settings
  Monitoring
  QoS
  System Settings
  Cloud Vision
  Endpoint Connectivity
  Network Services
  Platform Settings
  PTP Settings
  Custom Structure
  CloudVision Topology
  Digital Twin
PyAVD
AVD Dev Containers
```

### Change log [Release Notes]

A great category for versioning, porting guides, and release notes would be something that clearly communicates to the user that this section is all about changes, updates, and managing different versions of the software.

Here are a few excellent options, from most to least formal:

1. **Versioning & Releases**
Why it works: This is the most direct and technically accurate category. It uses the exact keywords for the content, making it very clear for developers and technical users. "Versioning" covers the policy, and "Releases" covers the specific artifacts like notes and guides.

2. **Releases & Upgrades**
Why it works: This is a very user-focused option. It highlights the main goal a user has when visiting this section: to learn about new releases and figure out how to upgrade. It's a bit more action-oriented.

3. **Release Information**
Why it works: A simple, all-encompassing, and safe choice. It's slightly more generic but still clearly communicates the purpose of the documents within.

4. **Changelog**
Why it works: In many modern software projects, "Changelog" is used as the top-level category for all release-related information. It's a very common and understood term. You would typically have the release notes directly on the main page and then link to versioning policies and porting guides from there.

```yaml
Porting Guide
Release Notes
Versioning
```
