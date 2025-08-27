<!--
  ~ Copyright (c) 2025 Arista Networks, Inc.
  ~ Use of this source code is governed by the Apache License 2.0
  ~ that can be found in the LICENSE file.
  -->

## Arista AVD Quickstart Guide

This guide provides a rapid introduction to Arista Validated Designs (AVD), focusing on the essential steps to get you up and running with generating network configurations using Ansible. AVD leverages Ansible to automate the design, deployment, and operation of Arista EOS networks.

### 1. Prerequisites

Before you begin, ensure you have the following installed on your control machine (the machine from which you will run Ansible):

- **Python 3.8+**: AVD is built on Python.
- **Ansible 2.14+**: The automation engine.
- **Git**: For cloning repositories.

You can verify your Python and Ansible versions with:

```bash
python3 --version
ansible --version
```

### 2. Install the `arista.avd` Ansible Collection

The core of AVD is distributed as an Ansible Collection.

```bash
pip install "pyavd[ansible]==5.5.1"
ansible-galaxy collection install arista.avd:==5.5.1
```

This command installs version 5.5.1 of the `arista.avd` collection. You can omit :`==5.5.1` to install the latest stable version, but specifying it ensures consistency with the documentation you linked.

### 3. Create Your AVD Project Directory

Create a new directory for your AVD project and navigate into it:

```bash
mkdir my-avd-project
cd my-avd-project
```

### 4. Set Up Your Inventory

Ansible uses an inventory file to define the devices it will manage. For AVD, this is typically a YAML file.

Create an `inventory.yml` file:

```yaml
# my-avd-project/inventory.yml
all:
  children:
    DC1_FABRIC:
      hosts:
        leaf1:
        leaf2:
        spine1:
```

This simple inventory defines a group `DC1_FABRIC` with three devices: `leaf1`, `leaf2`, and `spine1`.

### 5. Define Group Variables

AVD uses group variables to define the network design and device-specific parameters. These variables are consumed by AVD roles to generate configurations.

Create a `group_vars` directory and an all.yml file within it:

```bash
mkdir group_vars
touch group_vars/all.yml
```

Edit `group_vars/all.yml` to include some basic AVD variables. This example sets the fabric name and a default loopback interface prefix.

```yaml
# my-avd-project/group_vars/all.yml
---
# AVD Fabric-wide settings
fabric_name: "DC1"
loopback_ipv4_pool: "192.168.0.0/24"
```

Now, let's add some device-specific variables. Create a `host_vars` directory and a file for `leaf1`:

```bash
mkdir host_vars
touch host_vars/leaf1.yml
```

Edit `host_vars/leaf1.yml`.

```yaml
# my-avd-project/host_vars/leaf1.yml
---
# Device-specific settings for leaf1
is_deployed: true
type: leaf
id: 1
```

Repeat for `leaf2.yml` (change `id: 2`) and `spine1.yml` (change type: `spine`, `id: 1`).

```yaml
# my-avd-project/host_vars/leaf2.yml
---
is_deployed: true
type: leaf
id: 2
```yaml
# my-avd-project/host_vars/spine1.yml
---
is_deployed: true
type: spine
id: 1
```

### 6. Create Your Playbook

Create a `playbook.yml` file in your project root.

```yaml
# my-avd-project/playbook.yml
---
- name: Generate Arista EOS configurations using AVD
  hosts: DC1_FABRIC
  connection: local
  gather_facts: false

  tasks:
    - name: Generate device configurations
      ansible.builtin.import_role:
        name: arista.avd.eos_cli_config_gen

    - name: Generate device documentation
      ansible.builtin.import_role:
        name: arista.avd.eos_designs
```

This playbook uses two key AVD roles:

- `arista.avd.eos_designs`: Processes your inventory and variables to build the structured data model for your network.
- `arista.avd.eos_cli_config_gen`: Takes the structured data from `eos_designs` and generates the final EOS CLI configurations.

### 7. Run the Playbook

Execute the playbook from your `my-avd-project` directory:

```bash
ansible-playbook -i inventory.yml playbook.yml
```

Ansible will run, processing your inventory and variables through the AVD roles. You will see output indicating the tasks being performed.

### 8. Verify Generated Configurations

After the playbook completes, you will find the generated configurations and documentation in the `intended/` directory within your project:

```bash
ls -l intended/configs/
ls -l intended/documentation/
```

You can then view the generated configuration for `leaf1` (for example):

```bash
cat intended/configs/leaf1.cfg
```

You will see a full EOS configuration generated based on the AVD variables and roles.

## Next Steps

This quickstart provides a very basic example. To explore more advanced AVD features:

- **Explore AVD Documentation**: Refer to the official AVD documentation at https://avd.arista.com/5.5/index.html for detailed explanations of roles, variables, and design patterns.
- **Review AVD Examples**: The `arista.avd` collection includes comprehensive examples that demonstrate various network topologies and features. You can find them in the collection's directory (e.g., `~/.ansible/collections/ansible_collections/arista/avd/examples/`).
- **Integrate with CloudVision**: Learn how to deploy these generated configurations with Arista CloudVision.
