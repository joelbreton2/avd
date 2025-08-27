<!--
  ~ Copyright (c) 2025 Arista Networks, Inc.
  ~ Use of this source code is governed by the Apache License 2.0
  ~ that can be found in the LICENSE file.
  -->

## Meeting Notes

## July 17

### Attendance

- Petr, Julio, Carl, Joel

### Topics

- Navigation
- Implementation
  - Date (5.6, 6.0, ...)
  - Workflow (branch)
- Formatting/Styles
- AI utilisation
- Review
  - Quick Start
  - How-to
  - Reference
- Table of Contents
  - i.e. Release Notes
  - Short Title

### Discussion

#### Navigation

Nest PyAVD under User Manual

```yaml
User Manual
 - Ansible Collection
 - Input Variables
 - PyAVD
```

- ~~Reverse How-to Guide and User Manual for now until we grow how-to guides~~

#### Implementation

- Sooner (when navigation pr is ready)
- Work off devel when creating content

#### Input Variables

- **reason** it is one file to easily search with ctrl + f
- split in smaller docs

#### Strategy/Priority

1. Navigation (almost complete)
2. How-to guides (create content)
3. User Manual (rework)

#### Release Notes

Show only H2 headings in table of content

## July 10

### Attendance

- Petr, Julio, Carl, Joel

### Main Navigation

Rename

- Tutorials -> How-to Guides
- Topology Examples -> Examples
- Release Notes -> Versioning & Releases

Repeat topics in different sections

- Connected Endpoint to exist in How-to Guides and User Manual

[Connected Endpoints](https://avd.arista.com/5.5/ansible_collections/arista/avd/roles/eos_designs/docs/input-variables.html#endpoint-connectivity)

- How-to Guide -> Examples with profiles
- User Manual -> Tables

Video

- Video link at the end of the tutorials or Manuals
- Videos somewhere in the github library

[Recording Sessions](https://docs.google.com/document/d/1_a2-5dKp6UzZOwjR_xZnZ4u-7HBsW2TE65PtW_Qvyqo/edit?tab=t.v141dbxts83q#heading=h.8vuolx6korue)

Versioning & Releases

``` yaml
Versioning [landing page]
Release Notes
Porting Guide
```

emphasize `stay on the latest release`

Structure order

- Reference: Alphabetical
- User Manual: Alphabetical

### Quick start

quickly onboarding a user
people fail to copy and paste

Option

- one touch button container labs
- unpack examples
example

### Next Steps

start with Connected Endpoints

- tutorials
- user manual

Create how-to guide docs in contribute
