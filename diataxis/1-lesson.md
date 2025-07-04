<!--
  ~ Copyright (c) 2025 Arista Networks, Inc.
  ~ Use of this source code is governed by the Apache License 2.0
  ~ that can be found in the LICENSE file.
  -->

# Configuring PTP

Arista best practices are used, simplifying the configuration of several global and interface-specific **PTP** settings.

**PTP** can be enabled on various levels of the **AVD** configuration:

- Fabric level
- Per node type
- Per node

Only when explicitly enabled will the following global **PTP** settings take effect:

- **PTP** mode **`boundary`** is used by default.
- One of three different **PTP** profiles can be used:
  - **`AES67`**
  - **`SMPTE2059-2`**
  - **`AES67-R16-2016`** (used by default if no profile is specified)

The profile will apply **PTP** parameters for the following interfaces:

- All routed interfaces
- Individual **PTP-enabled** interfaces for connected endpoints

Defaults used when **PTP** is enabled:

- All interfaces between leaf and spine switches participate in the **Best Master Clock Algorithm (BMCA)**.
- All interfaces used for endpoints with **PTP** specifically enabled use **`ptp role master`**.
- **PTP priority 1** and **priority 2** are automatically set based on the **`node_type`** and **`switch_id`**.
- **PTP Clock Identity** is automatically set based on a prefix (**`00:1C:73`** by default) + **PTP priority 1** and **priority 2**.

## Enabling PTP

**PTP** must be specifically enabled:

- **On the fabric level**, for example `FABRIC.yml`:

    ```;yaml
    ptp_settings:
      enabled: true
    ```

- **Per node type**, for example for all spine nodes in `SPINES.yml`:

    ```;yaml
    spine:
      defaults:
        ptp:
          enabled: true
    ```

- **Per node** for a specific device, for example for a specific leaf in `LEAFS.yml`:

    ```;yaml
    l3leaf:
      node_groups:
        - group: leaf1
          nodes:
            - name: leaf1a
              ptp:
                enabled: true
    ```

**Please note:** If present, you need to remove the legacy **PTP** notation shown below. If this is not removed, the **PTP** profile-specific interface configuration will not be applied.

```;yaml
# Legacy configuration to be removed
spine:
  defaults:
    uplink_ptp:
      enable: true
```

## Fabric-wide PTP Settings

Common **PTP** settings can be specified for the entire topology to greatly simplify the configuration. These settings can also be defined on a more specific `group_vars` level if the network design requires it.

### PTP Profiles

Based on the **PTP** profile selection, the following parameters are applied to all interfaces between spine and leaf switches:

- **`profile: aes67`** is the slow **PTP** profile:
  - `ptp enable`
  - `ptp sync-message interval 0` (1 message/sec)
  - `ptp announce interval 2` (1 message/4 sec)
  - `ptp transport ipv4`
  - `ptp announce timeout 3`
  - `ptp delay-req interval 0` (1 message/sec)
- **`profile: smpte2059-2`** is the fast **PTP** profile:
  - `ptp enable`
  - `ptp sync-message interval -4` (16 messages/sec)
  - `ptp announce interval -2` (4 messages/sec)
  - `ptp transport ipv4`
  - `ptp announce timeout 3`
  - `ptp delay-req interval -4` (16 messages/sec)
- **`profile: aes67-r16-2016`** is the **default** **PTP** profile:
  - `ptp enable`
  - `ptp sync-message interval -3` (8 messages/sec)
  - `ptp announce interval 0` (1 message/sec)
  - `ptp transport ipv4`
  - `ptp announce timeout 3`
  - `ptp delay-req interval -3` (8 messages/sec)

## Group or Device Specific PTP Settings

### PTP Priorities

#### Automatic PTP priorities

By default, **PTP** priorities are automatically generated:

- **Priority 1** is set based on **`node_type`**.
- **Priority 2** is set based on **`node_id`** (modulus 256).

| Node_Type | Priority 1 | Priority 2 |
| :--- | :--- | :--- |
| **`spine`** | 20 | (node_id modulus 256) |
| **`l3leaf`** | 30 | (node_id modulus 256) |
| anything else | 127 | (node_id modulus 256) |

For leaf switches connecting to a **PTP** GrandMaster, we recommend manually setting **PTP priority 1** lower than other leaf switches, for example to “10”.

```;yaml
l3leaf:
  node_groups:
    - group: leaf1
      nodes:
        - name: leaf1a
          ptp:
            enabled: true
            priority1: 10
```

#### Manually setting PTP priorities

The automatic **PTP** priorities can be manually overridden if required:

```;yaml
l3leaf:
  node_groups:
    - group: leaf1
      nodes:
        - name: leaf1a
          ptp:
            enabled: true
            priority1: <0-255>
            priority2: <0-255>
```

### PTP Clock Identity

#### Setting PTP Clock Identity automatically

By default, **PTP** clock identity is generated automatically from:

1. A prefix (**`00:1C:73`** by default)
2. **PTP priority 1** as HEX
3. **`:00:`**
4. **PTP priority 2** as HEX

To use the system MAC address instead, disable `auto_clock_identity`. This can be set at the fabric, node type, or individual node level.

```;yaml
ptp_settings:
  auto_clock_identity: false
```

#### PTP Clock Identity prefix

The default 3-byte prefix **`00:1C:73`** can be overridden if `auto_clock_identity` is `true`.

```;yaml
spine:
  defaults:
    ptp:
      enabled: true
      clock_identity_prefix: "01:02:03"
```

#### Setting PTP Clock Identity manually

The clock identity can be set manually at various levels of the configuration.

```;yaml
spine:
  defaults:
    ptp:
      clock_identity: "01:02:03:04:05:06"
```

## Other PTP Settings

### Enable PTP unicast forwarding

This feature allows unicast **PTP** packets to be hardware forwarded through the data plane.

```;yaml
spine:
  defaults:
    ptp:
      forward_unicast: true
```

### PTP Source IP address

Manually set the source IP for **PTP** packets if required.

```;yaml
spine:
  defaults:
    ptp:
      source_ip: 10.1.2.3
```

### PTP Time-To-Live (TTL)

The default TTL of 1 can be overridden.

```;yaml
spine:
  defaults:
    ptp:
      ttl: 64
```

### PTP Monitor Threshold configuration

**PTP** monitor thresholds are enabled by default with the following configuration. All parameters can be overridden.

```;
ptp monitor threshold offset-from-master 250
ptp monitor threshold mean-path-delay 1500
ptp monitor sequence-id
ptp monitor threshold missing-message announce 3 sequence-ids
ptp monitor threshold missing-message delay-resp 3 sequence-ids
ptp monitor threshold missing-message follow-up 3 sequence-ids
ptp monitor threshold missing-message sync 3 sequence-ids
```

### PTP Settings for connected endpoints

By default, **PTP** is not enabled on interfaces with connected endpoints. It must be manually enabled.

```;yaml
servers:
  - name: <server-name>
    adapters:
    - ptp:
        enabled: true
        endpoint_role: < follower | bmca | default -> follower >
        profile: < aes67 | smpte2059-2 | aes67-r16-2016 | default -> aes67-r16-2016 >
```
