<!--
  ~ Copyright (c) 2025 Arista Networks, Inc.
  ~ Use of this source code is governed by the Apache License 2.0
  ~ that can be found in the LICENSE file.
  -->

## Tutorial: Your First PTP Configuration with AVD

**Goal:** In this tutorial, you'll learn how to implement a basic, stable Precision Time Protocol (PTP) configuration for an entire network fabric using Arista Validated Designs (AVD).

**Scenario:** We have a simple fabric and our goal is to enable PTP everywhere using the default settings, ensuring our spine switches are the preferred clock sources. We also need to provide PTP timing to one connected server.

### Step 1: Enable PTP for the Entire Fabric

First, we need to turn PTP on. The easiest way to ensure PTP is active everywhere is to enable it globally. This single setting provides a consistent baseline for all switches.

In your main fabric inventory file (e.g., `fabric.yml`), add the following:

```yaml
ptp_settings:
  enabled: true
```

That's it! With this one change, AVD will now generate the basic PTP configuration for all spine and leaf switches.

### Step 2: Review the Default PTP Profile

AVD is designed with smart defaults. Now that PTP is enabled, it automatically applies the **`aes67-r16-2016`** profile. For this tutorial, we will stick with this default.

This profile provides a balanced rate of PTP messages (8 sync messages per second), making it suitable for a wide range of applications. You don't need to configure anything in this step; just be aware that AVD has already selected a sensible profile for you.

### Step 3: Understand Automatic Priorities

With PTP enabled, a process called the **Best Master Clock Algorithm (BMCA)** runs to elect the most stable clock source. AVD helps ensure this election has a predictable and stable outcome.

You don't need to add any configuration here, but AVD is already doing the following for you in the background:

- It has given your **spine switches a PTP priority of 20**.
- It has given your **leaf switches a PTP priority of 30**.

Since a lower number wins, the spines will always be preferred as clock sources over the leaves. This creates a stable hierarchy automatically.

### Step 4: Enable PTP for a Connected Server

Now, let's provide PTP to a device connected to one of our leaf switches. By default, PTP is **not** enabled on endpoint-facing ports, so we must enable it manually.

In your inventory file where you define your servers, find the server that needs PTP and add the `ptp` block to its adapter configuration.

```yaml
servers:
  - name: my-media-server
    adapters:
    - switch_ports: [ Ethernet7 ]
      switches: [ leaf1a ]
      # Add this block to enable PTP for the server
      ptp:
        enabled: true
```

This tells AVD to enable PTP specifically on port `Ethernet7` of switch `leaf1a`, allowing `my-media-server` to receive timing information.

### Step 5: Review and Deploy

Let's review the simple but powerful configuration we've built. Your PTP settings in your inventory files should look something like this:

**In `fabric.yml`:**

```yaml
ptp_settings:
  enabled: true
```

**In your server inventory file:**

```yaml
servers:
  - name: my-media-server
    adapters:
    - switch_ports: [ Ethernet7 ]
      switches: [ leaf1a ]
      ptp:
        enabled: true
```

Now, you can run the AVD playbook to deploy your configuration. Once deployed, you can log into a switch and use the command `show ptp` to verify that PTP is active and see the clock's status.

### Congratulations

You've successfully configured a robust, stable PTP setup for your entire fabric and a connected endpoint. You learned how to enable PTP globally and for specific interfaces, and you understood how AVD's smart defaults for profiles and priorities work to your advantage.

From here, you could try experimenting with different **PTP profiles** or **manually setting a priority** for a specific switch to further your understanding.
