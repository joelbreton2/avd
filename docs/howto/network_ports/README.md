<!--
  ~ Copyright (c) 2025-2026 Arista Networks, Inc.
  ~ Use of this source code is governed by the Apache License 2.0
  ~ that can be found in the LICENSE file.
  -->

# Network Ports

## Introduction

The **network_ports** model is an interface-centric approach used to apply bulk settings to switch ports. It is ideal for scenarios where you need to apply standardized configurations to ranges of interfaces across one or multiple switches without needing to document unique endpoint-specific settings for every connection.

This guide explains how to use the network_ports data model in Arista AVD to manage switch port configurations efficiently.

### When to Use Network Ports

Use `network_ports` when:

- Many ports share identical configurations
- You want to apply the same profile to a range of interfaces
- Endpoint-specific details are not required

Use `connected_endpoints` instead when:

- Each server or device has a unique configuration (specific VLANs, port-channels, descriptions)
- You need to document the endpoint name and connection details
- You want to track which device connects to which switch port

!!! warning
    Both data models share the same underlying implementation and can coexist without conflicts. If a switch port is defined in both "Connected Endpoints" and "Network Ports", the "Connected Endpoints" configuration will take precedence.

## Concepts

Effective use of network_ports relies on the relationship between **Port Profiles** and the **Switch Interface** definition.

### Port Profiles

A **Port Profile** is a reusable template that defines a standard set of switchport configurations. You create a profile once and then apply it to any number of connected endpoints. This ensures consistency and dramatically simplifies configuration. A port profile can refer to another port profile using parent_profile to inherit settings in up to two levels (adapter->profile->parent_profile).

- **Shared Logic**: These profiles are used by both connected_endpoints and network_ports.
- **Standardization**: Changes made to a profile automatically propagate to every interface associated with it.
- **Precedence**: While profiles provide defaults, any key defined directly under a specific adapter will take precedence over the profile setting.

### Parent Profiles

A **Parent Profile** is a mechanism used within port_profiles to create a hierarchical inheritance structure for interface configurations. This feature allows you to define a "base" profile with common settings and then create more specific profiles that inherit those settings while adding or overriding specific parameters.

- **Inheritance**: A child profile inherits all settings defined in its parent profile.
- **Depth Limit**: AVD supports inheritance up to two levels deep (e.g., adapter -> child_profile -> parent_profile).
- **Overriding**: Settings defined in the child profile take precedence over the parent. Similarly, settings defined directly on the adapter (the specific interface mapping) take precedence over both the child and parent profiles.

## Examples

The following workflow demonstrates how to define a bulk configuration for a range of web server ports.

### Define Port Profiles

First, establish the template for your ports.

```yaml title="group_vars/HTNP/port_profiles.yml"
--8<--
ansible_collections/arista/avd/extensions/molecule/howto/inventory/group_vars/HTNP/port_profiles.yml
--8<--
```

1. Profile for web server ports with access mode, portfast, and storm control
2. Profile for VOIP phone ports with access mode, portfast, BPDU guard, and PoE settings
3. Profile for trunk uplink ports with multiple VLANs

### Apply to Network Ports

Apply the profile to a range of interfaces on specific switches.

```yaml title="group_vars/HTNP/network_ports.yml"
--8<--
ansible_collections/arista/avd/extensions/molecule/howto/inventory/group_vars/HTNP/network_ports.yml
--8<--
```

1. Web server ports applied to Ethernet10-15 on both leaf switches
2. VOIP phone ports applied to Ethernet20-24 on htnp-leaf1a
3. Trunk uplink port applied to Ethernet20 on htnp-leaf1b

### Validated Configurations

The following validated configurations demonstrate the network_ports model in action. These configurations were generated using AVD's eos_designs role with the inventory defined above.

#### Web Server Ports (Access Mode)

Web server ports configured with access mode on VLAN 100, portfast, and storm control.

```cli title="htnp-leaf1a Web Server Ports (Ethernet10-15)"
--8<--
docs/howto/network_ports/artifacts/htnp-leaf1a-webserver-ports.cfg
--8<--
```

```cli title="htnp-leaf1b Web Server Ports (Ethernet10-15)"
--8<--
docs/howto/network_ports/artifacts/htnp-leaf1b-webserver-ports.cfg
--8<--
```

#### VOIP Phone Ports (Access Mode with PoE)

VOIP phone ports configured with access mode on VLAN 200, portfast, BPDU guard, and PoE settings.

```cli title="htnp-leaf1a VOIP Phone Ports (Ethernet20-24)"
--8<--
docs/howto/network_ports/artifacts/htnp-leaf1a-voip-ports.cfg
--8<--
```

#### Trunk Uplink Port

Trunk port configured with multiple VLANs for uplink connectivity.

```cli title="htnp-leaf1b Trunk Uplink Port (Ethernet20)"
--8<--
docs/howto/network_ports/artifacts/htnp-leaf1b-trunk-port.cfg
--8<--
```

## Best Practices

1. **Use Port Profiles for Consistency**: Always use profiles to define shared settings like STP and storm control to ensure your fabric remains uniform.
2. **Leverage Interface Ranges**: Use the range syntax (e.g., Ethernet1-48) to keep your YAML files concise and easy to read.
3. **Descriptive Profiles**: Name your profiles based on function (e.g., PP-VOIP-PHONE) rather than technical settings to make the intent clear to other users.
4. **Validate Port Overlap**: Be aware that if a port in a range is also defined in `connected_endpoints`, the latter will override your bulk settings.

## Troubleshooting

### Configuration Not Applied to Certain Ports

**Issue**: Ports within a range are not showing the expected configuration.

**Solution**: Check if those specific ports are also defined under connected_endpoints. The connected_endpoints model takes precedence.

### VLANs Missing from Config

**Issue**: The switchport access vlan is missing.

**Solution**: Ensure the VLAN is defined in the network_services for that specific switch or tenant.

### Range Syntax Errors

**Issue**: Configuration fails to generate for the interface list.

**Solution**: Verify that the switch_ports syntax matches the EOS naming convention (e.g., Ethernet1-24 or Eth1-24).

## Reference

For complete details on all available properties, see:

- [Port Profiles Settings](../../../ansible_collections/arista/avd/roles/eos_designs/docs/data-models.md#port-profiles-settings)
- [Network Ports Settings](../../../ansible_collections/arista/avd/roles/eos_designs/docs/data-models.md#network-ports-settings)

