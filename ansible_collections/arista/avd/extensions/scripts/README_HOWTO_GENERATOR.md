# How-To Guide Molecule Infrastructure Generator

This script automates the creation of molecule testing infrastructure for AVD how-to guides, making it easy to generate validated configuration examples for documentation.

## Overview

The `generate_howto_molecule.py` script generates all necessary files for creating validated configurations in AVD how-to guides, including:

- Inventory structure (hosts.yml updates)
- L3 leaf switch configurations
- Port profiles
- Network ports or connected endpoints configurations
- Network services (VLANs/VRFs)
- Artifact extraction rules

## Prerequisites

- Python 3.10+
- PyYAML library (`pip install pyyaml`)
- AVD repository cloned locally
- PyAVD installed (matching AVD version)

## Usage

### Basic Usage

```bash
cd ansible_collections/arista/avd/extensions/scripts

python3 generate_howto_molecule.py --config examples/howto_network_ports_example.yml
```

### With Custom Base Path

```bash
python3 generate_howto_molecule.py \
  --config my_howto_config.yml \
  --base-path /path/to/avd/ansible_collections/arista/avd/extensions/molecule/howto
```

### Verbose Mode

```bash
python3 generate_howto_molecule.py --config my_config.yml --verbose
```

## Configuration File Format

The configuration file is a YAML file that defines all aspects of the how-to guide infrastructure.

### Required Sections

#### 1. Guide Information
```yaml
guide:
  name: "Network Ports"  # Human-readable guide name
  prefix: "HTNP"  # Prefix for inventory groups
  docs_path: "../../../../../../docs/howto/network_ports"  # Path to docs
```

#### 2. Switches
```yaml
switches:
  - name: htnp-leaf1a
    mgmt_ip: 172.16.1.201/24
  - name: htnp-leaf1b
    mgmt_ip: 172.16.1.202/24
```

#### 3. Network Services
```yaml
network_services:
  - name: TENANT_HTNP
    vrfs:
      - name: VRF_WEB
        svis:
          - id: 100
            name: WebServers
            enabled: true
            ip_address_virtual: 10.100.100.1/24
```

### Optional Sections

#### Port Profiles (for network_ports or connected_endpoints)
```yaml
port_profiles:
  - profile: PP-WebServer
    mode: access
    vlans: "100"
    spanning_tree_portfast: edge
```

#### Network Ports (interface-centric approach)
```yaml
network_ports:
  - switches:
      - htnp-leaf1a
    switch_ports:
      - Ethernet10-15
    profile: PP-WebServer
    description: "Web Server Ports"
```

#### Connected Endpoints (device-centric approach)
```yaml
connected_endpoints:
  - name: WEB-SERVER-01
    adapters:
      - endpoint_ports: [eth0]
        switch_ports: [Ethernet10]
        switches: [htnp-leaf1a]
        profile: PP-SERVER
```

#### Artifacts (configuration extraction rules)
```yaml
artifacts:
  - file: inventory/intended/configs/htnp-leaf1a.cfg
    sections:
      - header: "interface Ethernet10"
      - header: "interface Ethernet11"
    artifact: "htnp-leaf1a-webserver-ports.cfg"
    output_dir: "../../../../../../docs/howto/network_ports/artifacts/"
```

#### BGP AS and L3 Leaf Defaults
```yaml
bgp_as: 65102  # Optional, default: 65102

l3leaf_defaults:  # Optional, uses standard defaults if not specified
  platform: vEOS-lab
  spanning_tree_mode: mstp
```

## Examples

### Example 1: Network Ports How-To Guide

See `examples/howto_network_ports_example.yml` for a complete example demonstrating:
- Port profiles for web servers, VOIP phones, and trunk uplinks
- Network ports applying profiles to interface ranges
- Multiple VRFs and VLANs
- Artifact extraction for documentation

### Example 2: Connected Endpoints How-To Guide

See `examples/howto_connected_endpoints_example.yml` for a complete example demonstrating:
- Port profiles for servers and storage
- Connected endpoints with port-channels
- Device-centric configuration approach
- Artifact extraction for specific endpoints

## Workflow

### 1. Create Configuration File

Create a YAML configuration file defining your how-to guide requirements:

```bash
cp examples/howto_network_ports_example.yml my_howto_guide.yml
# Edit my_howto_guide.yml with your specifications
```

### 2. Generate Infrastructure

Run the generator script:

```bash
python3 generate_howto_molecule.py --config my_howto_guide.yml
```

### 3. Run Molecule Tests

Generate structured and CLI configurations:

```bash
cd ../molecule/howto
ANSIBLE_COLLECTIONS_PATH=/path/to/avd ansible-playbook converge.yml -i inventory/hosts.yml
```

### 4. Extract Artifacts

Run the side_effect playbook to extract configuration artifacts:

```bash
ANSIBLE_COLLECTIONS_PATH=/path/to/avd ansible-playbook side_effect.yml -i inventory/hosts.yml
```

### 5. Update Documentation

Reference the generated artifacts in your how-to guide markdown:

````markdown
```cli title="Web Server Ports Configuration"
--8<--
avd/docs/howto/network_ports/artifacts/htnp-leaf1a-webserver-ports.cfg
--8<--
```
````

### 6. Commit Changes

```bash
git add .
git commit -m "Feat: Add <guide-name> how-to guide molecule infrastructure"
```

## Output Files

The script generates the following files:

```
molecule/howto/
├── inventory/
│   ├── hosts.yml (updated)
│   └── group_vars/
│       ├── <PREFIX>/
│       │   ├── port_profiles.yml
│       │   ├── network_ports.yml (or connected_endpoints.yml)
│       │   └── network_services.yml
│       └── <PREFIX>_L3_LEAFS/
│           └── l3_leafs.yml
└── artifacts.yml (updated)

docs/howto/<guide-name>/
└── artifacts/
    └── (generated by molecule side_effect)
```

## Tips and Best Practices

1. **Naming Convention**: Use descriptive prefixes (e.g., HTNP for "How-To Network Ports")
2. **IP Addressing**: Use non-overlapping IP ranges for different guides
3. **BGP AS**: Use unique AS numbers for each guide (65102, 65103, etc.)
4. **Artifacts**: Extract only relevant configuration sections for documentation
5. **Testing**: Always run molecule tests to validate generated configurations
6. **Documentation**: Update the how-to guide markdown with artifact references

## Troubleshooting

### PyAVD Version Mismatch

If you encounter PyAVD version errors:

```bash
# Install PyAVD in editable mode from source
cd /path/to/avd/python-avd
uv pip install -e .
```

### Ansible Collection Not Found

Set the ANSIBLE_COLLECTIONS_PATH environment variable:

```bash
export ANSIBLE_COLLECTIONS_PATH=/path/to/avd
```

### YAML Syntax Errors

Validate your configuration file:

```bash
python3 -c "import yaml; yaml.safe_load(open('my_config.yml'))"
```

## References

- [AVD Documentation](https://avd.arista.com/)
- [Molecule Testing Framework](https://molecule.readthedocs.io/)
- [PR #6367 - Connected Endpoints How-To](https://github.com/aristanetworks/avd/pull/6367)

