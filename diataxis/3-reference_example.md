<!--
  ~ Copyright (c) 2025 Arista Networks, Inc.
  ~ Use of this source code is governed by the Apache License 2.0
  ~ that can be found in the LICENSE file.
  -->

# PTP Configuration Reference for AVD

This document provides a reference for all parameters used to configure Precision Time Protocol (PTP) in Arista Validated Designs (AVD).

## Fabric Level Settings (`ptp_settings`)

These parameters are defined at the top level of the fabric configuration (e.g., in `FABRIC.yml`).

| Parameter | Description | Type | Default |
| :--- | :--- | :--- | :--- |
| **`enabled`** | Globally enables or disables PTP for the fabric. | Boolean | `false` |
| **`profile`** | Sets the PTP profile for all devices. | String | `aes67-r16-2016` |
| | **Accepted Values:** `aes67`, `smpte2059-2`, `aes67-r16-2016` | | |
| **`auto_clock_identity`** | Enables or disables automatic generation of the PTP clock identity. If `false`, the system MAC is used. | Boolean | `true` |

## Node and Group Level Settings (`ptp:`)

These parameters can be set under `defaults:` for a node type (e.g., `spine`), under a `node_group`, or under a specific `node`. The most specific setting takes precedence.

| Parameter | Description | Type | Default |
| :--- | :--- | :--- | :--- |
| **`enabled`** | Enables or disables PTP for the specific scope (node, group, etc.). | Boolean | `false` |
| **`profile`** | Overrides the fabric-level PTP profile. | String | Inherited from fabric |
| **`priority1`** | Manually overrides the PTP priority 1 value. Lower is higher priority. | Integer (0-255) | `20` for spines, `30` for leaves, `127` otherwise |
| **`priority2`** | Manually overrides the PTP priority 2 value. | Integer (0-255) | `node_id % 265` |
| **`auto_clock_identity`** | Overrides the fabric-level auto clock identity setting. | Boolean | Inherited from fabric |
| **`clock_identity_prefix`** | Sets a custom 3-byte prefix for the auto-generated clock identity. Must be a quoted string. | String | `"00:1C:73"` |
| **`clock_identity`** | Manually sets the entire 6-byte clock identity. Must be a quoted string. | String | `null` |
| **`forward_unicast`** | Enables hardware forwarding of unicast PTP packets. | Boolean | `false` |
| **`source_ip`** | Manually sets the source IP address for PTP packets. | String (IPv4) | `null` (uses interface IP) |
| **`ttl`** | Manually sets the Time-To-Live for PTP packets. | Integer | `1` |
| **`monitor.enabled`** | Enables or disables the PTP monitor feature. | Boolean | `true` |
| **`monitor.threshold...`** | Sets various thresholds for monitoring PTP state. | Integer | See EOS docs |

## Endpoint Settings

These parameters are configured under a specific adapter for a server connected to a switch.

| Parameter | Description | Type | Default |
| :--- | :--- | :--- | :--- |
| **`ptp.enabled`** | Enables or disables PTP on the switch port connected to the endpoint. | Boolean | `false` |
| **`ptp.endpoint_role`** | Defines the PTP role for the endpoint interface on the switch. `master` is a fixed role, while `bmca` allows the port to participate in the clock election. | String | `follower` |
| | **Accepted Values:** `follower`, `bmca` | | |
| **`ptp.profile`** | Sets a specific PTP profile for this endpoint interface, overriding the global profile. | String | Inherited from fabric |

**Example:**

```yaml
servers:
  - name: PTP-Grandmaster
    adapters:
    - switch_ports: [ Ethernet5 ]
      switches: [ blue-spine1 ]
      ptp:
        enabled: true
        endpoint_role: bmca
```

## P2P Link Settings

These parameters are for dedicated point-to-point links between switches that should only carry PTP traffic.

| Parameter | Description | Type | Default |
| :--- | :--- | :--- | :--- |
| **`ptp.enabled`** | Enables PTP on the point-to-point link. | Boolean | `false` |
| **`include_in_underlay_protocol`** | If `false`, the link will be configured as a routed port without an IP address and will not participate in the routing underlay. | Boolean | `true` |

**Example:**

```yaml
core_interfaces:
  p2p_links:
    - id: 1
      nodes: [ blue-leaf1, blue-leaf2 ]
      interfaces: [ Ethernet10, Ethernet10 ]
      ptp:
        enabled: true
      include_in_underlay_protocol: false
```
