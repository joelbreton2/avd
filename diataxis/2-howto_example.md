<!--
  ~ Copyright (c) 2025 Arista Networks, Inc.
  ~ Use of this source code is governed by the Apache License 2.0
  ~ that can be found in the LICENSE file.
  -->

## How-To Guide: Configuring PTP with AVD

This guide provides step-by-step instructions for configuring Precision Time Protocol (PTP) in your Arista Validated Designs (AVD) environment.

### Step 1: Enable PTP in Your Fabric

You must first enable PTP. Choose one of the following methods based on how broadly you want to apply the configuration. The most specific configuration always wins.

#### Method A: Enable PTP for the Entire Fabric

This is the most common method. Add the following to your main fabric YAML file (e.g., `FABRIC.yml`):

```yaml
ptp_settings:
  enabled: true
```

#### Method B: Enable PTP for a Specific Switch Type

To enable PTP only for a group of switches, like all spines, add this to the relevant group file (e.g., `SPINES.yml`):

```yaml
spine:
  defaults:
    ptp:
      enabled: true
```

#### Method C: Enable PTP for a Single Device

To enable PTP on just one switch, add the configuration directly under the node's definition:

```yaml
l3leaf:
  node_groups:
    - group: leaf1
      nodes:
        - name: leaf1a
          ptp:
            enabled: true
```

> **Important**: Ensure any legacy `uplink_ptp:` configuration is removed, as it will conflict with modern PTP profile settings.

### Step 2: Select a PTP Profile (Optional)

AVD uses the `aes67-r16-2016` profile by default. If your application requires a different PTP timing profile, you can specify it. This setting is typically applied fabric-wide.

- **`aes67`**: Slower profile (1 sync message/sec).
- **`smpte2059-2`**: Faster profile (16 sync messages/sec).
- **`aes67-r16-2016`**: Default profile (8 sync messages/sec).

To set a profile, add it to your `ptp_settings`:

```yaml
ptp_settings:
  enabled: true
  profile: smpte2059-2
```

### Step 3: Customize PTP Priorities (Optional)

By default, AVD automatically assigns PTP priorities to create a stable clock hierarchy (Spines get priority `20`, Leaves get `30`). If you need to force a specific leaf switch to have a higher priority (e.g., because it's connected to a Grandmaster clock), you can override the default.

*Remember: A lower number means higher priority.*

```yaml
l3leaf:
  node_groups:
    - group: leaf1
      nodes:
        - name: leaf1a
          ptp:
            enabled: true
            # Manually set a higher priority
            priority1: 10
```

### Step 4: Customize PTP Clock Identity (Optional)

AVD automatically generates a unique PTP Clock Identity. If you prefer to use the switch's system MAC address (the default behavior in EOS), you can disable the automatic generation.

#### Method A: Disable Automatic Clock Identity

```yaml
ptp_settings:
  auto_clock_identity: false
```

#### Method B: Manually Set the Clock Identity

If you need a specific, non-system MAC identity, you can set it directly:

```yaml
spine:
  defaults:
    ptp:
      # Use double-quotes
      clock_identity: "01:02:03:04:05:06"
```

### Step 5: Configure PTP for Connected Endpoints

PTP is **not** enabled by default on ports connected to servers or other endpoints. You must enable it manually on a per-adapter basis.

```yaml
servers:
  - name: Blue-Grandmaster
    adapters:
    - type: server
      endpoint_ports: [ eth1 ]
      switch_ports: [ Ethernet5 ]
      switches: [ blue-spine1 ]
      ptp:
        enabled: true
        # 'bmca' lets the interface participate in the election.
        # 'follower' is the default.
        endpoint_role: bmca
```

### Step 6: Configure PTP-Only Links

For dedicated links that should only carry PTP traffic and not participate in underlay routing, you can define them under `p2p_links`.

```yaml
core_interfaces:
  p2p_links:
    - id: 1
      nodes: [ blue-leaf1, blue-leaf2 ]
      interfaces: [ Ethernet10, Ethernet10 ]
      ptp:
        enabled: true
      # This prevents the link from being used for regular data traffic
      include_in_underlay_protocol: false
```

This will configure the interfaces as routed ports with PTP enabled but without an IP address, effectively isolating them for PTP communication.
