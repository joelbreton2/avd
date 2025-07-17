<!--
  ~ Copyright (c) 2025 Arista Networks, Inc.
  ~ Use of this source code is governed by the Apache License 2.0
  ~ that can be found in the LICENSE file.
  -->

# Connected Endpoints

This guide will show you how to connect servers, firewalls, and other devices to your fabric using reusable port profiles.

## Step 1: Define Your Port Profiles

First, create a set of reusable **`port_profiles`**. These are templates that define a standard configuration for switch ports, such as VLANs, trunk or access mode, and Spanning Tree settings. Defining profiles first makes your configuration cleaner and more consistent.

Add a `port_profiles` section to your AVD group variables (e.g., in `group_vars/FABRIC.yml`).

**Example:**

```yaml
port_profiles:

  - profile: VM_Servers
    mode: trunk
    vlans: "110-111,120-121,130-131"
    spanning_tree_portfast: edge

  - profile: MGMT
    mode: access
    vlans: "110"

  - profile: DB_Clusters
    mode: trunk
    vlans: "140-141"
```

## Step 2: Define and Connect Your Endpoints

Next, define your endpoints (servers, firewalls, routers) and connect their network adapters to your switches by applying the profiles you created.

### **How to Connect a Single-Homed Endpoint**

This is the simplest connection, where one port on an endpoint connects to one port on a switch.

Under the `servers` key, define the adapter and apply a profile. The lists for `endpoint_ports`, `switch_ports`, and `switches` will each have a single item.

**Example:**

```yaml
servers:
  - name: server01
    adapters:
      # Connects server port E0 to switch DC1-LEAF1A on port Ethernet5
      - endpoint_ports: [ E0 ]
        switch_ports: [ Ethernet5 ]
        switches: [ DC1-LEAF1A ]
        profile: MGMT
```

### **How to Connect an MLAG Dual-Homed Endpoint**

This is a redundant connection where an endpoint is connected to two different switches that are part of a **Multi-Chassis Link Aggregation (MLAG)** pair. The two physical links are bundled into a single logical Port-Channel.

Define the adapter with two items in each list and add a `port_channel` section.

**Example:**

```yaml
servers:
  - name: server03
    adapters:
      # Connects server port E0 to DC1-SVC3A and E1 to DC1-SVC3B
      - endpoint_ports: [ E0, E1 ]
        switch_ports: [ Ethernet10, Ethernet10 ]
        switches: [ DC1-SVC3A, DC1-SVC3B ]
        profile: VM_Servers
        port_channel:
          mode: active # This enables LACP
```

### **How to Connect an EVPN Active/Active Endpoint**

This is an advanced multihoming method where an endpoint connects to two independent switches (not necessarily MLAG peers) using **EVPN-VXLAN**. This requires an **Ethernet Segment Identifier (ESI)** to identify the connection.

AVD simplifies this with the **`short_esi`** key. You can provide a 3-octet value or set it to `auto` for AVD to generate it for you.

**Example:**

```yaml
servers:
  - name: server01
    adapters:
      # Connects to two different switches in an EVPN Active/Active segment
      - endpoint_ports: [ E0, E1 ]
        switch_ports: [ Ethernet10, Ethernet10 ]
        switches: [ DC1-SVC3A, DC1-SVC4A ]
        profile: VM_Servers
        port_channel:
          mode: active
        # Add the ethernet_segment block for EVPN A/A
        ethernet_segment:
          short_esi: 0303:0202:0101
```
