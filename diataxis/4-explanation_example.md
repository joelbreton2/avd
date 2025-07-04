<!--
  ~ Copyright (c) 2025 Arista Networks, Inc.
  ~ Use of this source code is governed by the Apache License 2.0
  ~ that can be found in the LICENSE file.
  -->

## Explanation: Understanding PTP Configuration in AVD

This document explains the concepts and design philosophy behind how Arista Validated Designs (AVD) handles Precision Time Protocol (PTP) configuration. The goal is to clarify *why* AVD works the way it does, complementing how-to guides and reference material.

### The Core Principle: Automation and Best Practices

The fundamental goal of AVD's PTP implementation is to automate a complex configuration using Arista's best practices. PTP can involve dozens of low-level settings, making manual configuration tedious and prone to error. AVD simplifies this by abstracting these settings into a hierarchical model.

Configuration is applied from the most general level (the entire fabric) down to the most specific (a single node). This allows you to set a baseline for the whole network and only override settings where necessary, promoting consistency and reducing repetitive configuration.

### Why Use PTP Profiles?

Different industries and applications have different requirements for timing precision and network load. For example, professional broadcast media (SMPTE) requires much faster PTP messaging than general audio applications (AES67).

Instead of requiring engineers to manually tune PTP message intervals and timeouts, AVD provides pre-packaged **profiles**. A profile is simply a tested and verified set of values tailored for a specific industry standard.

- **`aes67`**: A slower profile suitable for general audio-over-IP.
- **`smpte2059-2`**: A much faster profile for high-precision broadcast video.
- **`aes67-r16-2016`**: A balanced profile that serves as a safe and effective default.

By choosing a profile, you automatically apply a dozen settings correctly, ensuring compliance and stability without needing expert-level knowledge of each parameter.

### The Best Master Clock Algorithm (BMCA) and Automatic Priorities

PTP is a distributed protocol where all participating devices must agree on which clock is the most accurate. This election process is called the **Best Master Clock Algorithm (BMCA)**. AVD is designed to intelligently guide this election to a predictable and stable outcome.

This is achieved through **automatic priority assignment**:

1. **Priority 1 (Role-Based)**: By default, AVD assigns spine switches a numerically lower (better) `priority1` value than leaf switches. This ensures that the role of the PTP Grandmaster clock naturally gravitates towards the core of your network, which is a highly stable and recommended architecture.
2. **Priority 2 (Uniqueness)**: `priority2` is derived from the switch's unique `node_id`, acting as a tie-breaker if multiple switches have the same `priority1`.

This automatic system prevents a misconfigured edge switch from accidentally being elected as the Grandmaster, which could destabilize the entire network's timing. While you *can* override these priorities manually (for instance, to favor a leaf switch connected to a GPS-based Grandmaster), the default behavior provides a robust foundation.

### Understanding Clock Identity

Every clock in a PTP domain must have a unique identifier. By default, Arista EOS uses the switch's system MAC address. However, AVD creates its own **automatic clock identity**.

This identity is constructed from a known prefix (`00:1C:73`) combined with the switch's PTP priorities. The main reason for this is **predictability and traceability**. An administrator can determine a switch's PTP priority simply by looking at its clock identity, which can be useful for troubleshooting.

If you prefer the standard EOS behavior for consistency with other systems, you can simply disable this feature with `auto_clock_identity: false`, and the switch will revert to using its system MAC address.

### Why Endpoint and Fabric Links Are Treated Differently

AVD makes a crucial distinction between switch-to-switch (fabric) links and switch-to-endpoint (server, camera, etc.) links.

- **Fabric Links**: These are considered part of the PTP infrastructure. They automatically participate in the BMCA, running as **boundary clocks** that receive and re-transmit timing information.
- **Endpoint Links**: PTP is **disabled** by default on these ports. This is a safety measure to prevent a connected device from interfering with the fabric's clocking. When you do enable PTP for an endpoint, you typically define its role so the switch knows whether to treat it as a PTP master or slave, ensuring a clear and predictable flow of time.

This separation protects the stability of the core timing infrastructure from the behavior of the many devices connected to it.
