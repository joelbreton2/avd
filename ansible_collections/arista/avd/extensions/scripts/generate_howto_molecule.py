#!/usr/bin/env python3
"""
Generate Molecule Infrastructure for AVD How-To Guides

This script generates the necessary molecule test infrastructure files for creating
validated configuration examples in AVD how-to guides.

Usage:
    python3 generate_howto_molecule.py --config howto_config.yml

The configuration file should define:
- Guide name and prefix
- Switches to create
- Port profiles
- Network ports or connected endpoints
- Network services (VLANs/VRFs)
- Artifact extraction rules
"""

import argparse
import logging
from pathlib import Path
from typing import Any

import yaml

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='[%(levelname)s] %(message)s'
)
logger = logging.getLogger(__name__)


class HowToMoleculeGenerator:
    """Generator for How-To guide molecule infrastructure."""

    def __init__(self, config_file: Path, base_path: Path | None = None):
        """Initialize the generator with configuration."""
        self.config_file = config_file
        self.config = self._load_config()

        # Set base path (molecule/howto directory)
        if base_path:
            self.base_path = base_path
        else:
            # Default to the howto molecule directory
            script_dir = Path(__file__).parent
            self.base_path = script_dir.parent / "molecule" / "howto"

        # Extract configuration
        self.guide_name = self.config['guide']['name']
        self.prefix = self.config['guide']['prefix']
        self.switches = self.config['switches']
        self.port_profiles = self.config.get('port_profiles', [])
        self.network_ports = self.config.get('network_ports', [])
        self.connected_endpoints = self.config.get('connected_endpoints', [])
        self.network_services = self.config['network_services']
        self.artifacts = self.config.get('artifacts', [])

        logger.info(f"Initialized generator for guide: {self.guide_name}")

    def _load_config(self) -> dict[str, Any]:
        """Load configuration from YAML file."""
        logger.info(f"Loading configuration from: {self.config_file}")
        with open(self.config_file, 'r') as f:
            return yaml.safe_load(f)

    def generate_all(self):
        """Generate all molecule infrastructure files."""
        logger.info("Starting generation of molecule infrastructure...")

        # Create directory structure
        self._create_directories()

        # Generate inventory files
        self._generate_hosts_yml()
        self._generate_l3_leafs_yml()

        # Generate data model files
        if self.port_profiles:
            self._generate_port_profiles_yml()
        if self.network_ports:
            self._generate_network_ports_yml()
        if self.connected_endpoints:
            self._generate_connected_endpoints_yml()
        self._generate_network_services_yml()

        # Update artifacts.yml
        if self.artifacts:
            self._update_artifacts_yml()

        logger.info("✅ Generation complete!")
        logger.info(f"Files created in: {self.base_path}")
        logger.info("\nNext steps:")
        logger.info("1. Run: ANSIBLE_COLLECTIONS_PATH=<path_to_avd> ansible-playbook converge.yml -i inventory/hosts.yml")
        logger.info("2. Run: ANSIBLE_COLLECTIONS_PATH=<path_to_avd> ansible-playbook side_effect.yml -i inventory/hosts.yml")
        logger.info("3. Review generated configs and artifacts")
        logger.info("4. Update the how-to guide markdown with artifact references")

    def _create_directories(self):
        """Create necessary directory structure."""
        dirs = [
            self.base_path / "inventory" / "group_vars" / self.prefix,
            self.base_path / "inventory" / "group_vars" / f"{self.prefix}_L3_LEAFS",
            self.base_path / "inventory" / "intended" / "configs",
            self.base_path / "inventory" / "intended" / "structured_configs",
            Path(self.config['guide']['docs_path']) / "artifacts",
        ]

        for dir_path in dirs:
            dir_path.mkdir(parents=True, exist_ok=True)
            logger.debug(f"Created directory: {dir_path}")

    def _generate_hosts_yml(self):
        """Update hosts.yml with new fabric group."""
        hosts_file = self.base_path / "inventory" / "hosts.yml"

        logger.info(f"Updating {hosts_file}")

        # Load existing hosts.yml
        with open(hosts_file, 'r') as f:
            hosts_data = yaml.safe_load(f)

        # Create new fabric group
        fabric_group = {
            self.prefix: {
                'children': {
                    f'{self.prefix}_L3_LEAFS': {
                        'hosts': {}
                    }
                }
            }
        }

        # Add switches to the group
        for switch in self.switches:
            fabric_group[self.prefix]['children'][f'{self.prefix}_L3_LEAFS']['hosts'][switch['name']] = {
                'ansible_host': switch['mgmt_ip'].split('/')[0]
            }

        # Add to FABRIC children
        if 'FABRIC' not in hosts_data['all']['children']:
            hosts_data['all']['children']['FABRIC'] = {'children': {}}

        hosts_data['all']['children']['FABRIC']['children'][self.prefix] = fabric_group[self.prefix]

        # Add to NETWORK_SERVICES if network_ports or connected_endpoints exist
        if self.network_ports or self.connected_endpoints or self.network_services:
            if 'NETWORK_SERVICES' not in hosts_data['all']['children']:
                hosts_data['all']['children']['NETWORK_SERVICES'] = {'children': {}}

            if 'children' not in hosts_data['all']['children']['NETWORK_SERVICES']:
                hosts_data['all']['children']['NETWORK_SERVICES']['children'] = {}

            hosts_data['all']['children']['NETWORK_SERVICES']['children'][f'{self.prefix}_L3_LEAFS'] = None

        # Add to CONNECTED_ENDPOINTS if connected_endpoints exist
        if self.connected_endpoints:
            if 'CONNECTED_ENDPOINTS' not in hosts_data['all']['children']:
                hosts_data['all']['children']['CONNECTED_ENDPOINTS'] = {'children': {}}

            if 'children' not in hosts_data['all']['children']['CONNECTED_ENDPOINTS']:
                hosts_data['all']['children']['CONNECTED_ENDPOINTS']['children'] = {}

            hosts_data['all']['children']['CONNECTED_ENDPOINTS']['children'][f'{self.prefix}_L3_LEAFS'] = None

        # Write back to file
        with open(hosts_file, 'w') as f:
            yaml.dump(hosts_data, f, default_flow_style=False, sort_keys=False)

        logger.info(f"✅ Updated {hosts_file}")

    def _generate_l3_leafs_yml(self):
        """Generate L3 leafs configuration file."""
        output_file = self.base_path / "inventory" / "group_vars" / f"{self.prefix}_L3_LEAFS" / "l3_leafs.yml"

        logger.info(f"Generating {output_file}")

        # Get defaults from config or use standard defaults
        defaults = self.config.get('l3leaf_defaults', {
            'platform': 'vEOS-lab',
            'loopback_ipv4_pool': '10.255.0.0/27',
            'loopback_ipv4_offset': 10,
            'vtep_loopback_ipv4_pool': '10.255.2.0/27',
            'mlag_peer_ipv4_pool': '10.255.2.64/27',
            'mlag_peer_l3_ipv4_pool': '10.255.2.96/27',
            'virtual_router_mac_address': '00:1c:73:00:00:99',
            'spanning_tree_priority': 4096,
            'spanning_tree_mode': 'mstp'
        })

        # Build node groups
        nodes = []
        for idx, switch in enumerate(self.switches, start=1):
            node = {
                'name': switch['name'],
                'id': idx,
                'mgmt_ip': switch['mgmt_ip']
            }
            nodes.append(node)

        node_group = {
            'group': f'{self.prefix}_L3_LEAFS',
            'bgp_as': self.config.get('bgp_as', 65102),
            'nodes': nodes
        }

        l3leaf_config = {
            'type': 'l3leaf',
            'l3leaf': {
                'defaults': defaults,
                'node_groups': [node_group]
            }
        }

        with open(output_file, 'w') as f:
            f.write('---\n')
            yaml.dump(l3leaf_config, f, default_flow_style=False, sort_keys=False)

        logger.info(f"✅ Generated {output_file}")

    def _generate_port_profiles_yml(self):
        """Generate port profiles configuration file."""
        output_file = self.base_path / "inventory" / "group_vars" / self.prefix / "port_profiles.yml"

        logger.info(f"Generating {output_file}")

        port_profiles_config = {
            'port_profiles': self.port_profiles
        }

        with open(output_file, 'w') as f:
            f.write('---\n')
            yaml.dump(port_profiles_config, f, default_flow_style=False, sort_keys=False)

        logger.info(f"✅ Generated {output_file}")

    def _generate_network_ports_yml(self):
        """Generate network ports configuration file."""
        output_file = self.base_path / "inventory" / "group_vars" / self.prefix / "network_ports.yml"

        logger.info(f"Generating {output_file}")

        network_ports_config = {
            'network_ports': self.network_ports
        }

        with open(output_file, 'w') as f:
            f.write('---\n')
            yaml.dump(network_ports_config, f, default_flow_style=False, sort_keys=False)

        logger.info(f"✅ Generated {output_file}")

    def _generate_connected_endpoints_yml(self):
        """Generate connected endpoints configuration file."""
        output_file = self.base_path / "inventory" / "group_vars" / self.prefix / "connected_endpoints.yml"

        logger.info(f"Generating {output_file}")

        connected_endpoints_config = {
            'servers': self.connected_endpoints
        }

        with open(output_file, 'w') as f:
            f.write('---\n')
            yaml.dump(connected_endpoints_config, f, default_flow_style=False, sort_keys=False)

        logger.info(f"✅ Generated {output_file}")

    def _generate_network_services_yml(self):
        """Generate network services configuration file."""
        output_file = self.base_path / "inventory" / "group_vars" / self.prefix / "network_services.yml"

        logger.info(f"Generating {output_file}")

        network_services_config = {
            'tenants': self.network_services
        }

        with open(output_file, 'w') as f:
            f.write('---\n')
            yaml.dump(network_services_config, f, default_flow_style=False, sort_keys=False)

        logger.info(f"✅ Generated {output_file}")

    def _update_artifacts_yml(self):
        """Update artifacts.yml with new artifact extraction rules."""
        artifacts_file = self.base_path / "artifacts.yml"

        logger.info(f"Updating {artifacts_file}")

        # Load existing artifacts.yml
        with open(artifacts_file, 'r') as f:
            existing_artifacts = yaml.safe_load(f) or []

        # Add new artifacts
        for artifact in self.artifacts:
            existing_artifacts.append(artifact)

        # Write back to file
        with open(artifacts_file, 'w') as f:
            yaml.dump(existing_artifacts, f, default_flow_style=False, sort_keys=False)

        logger.info(f"✅ Updated {artifacts_file} with {len(self.artifacts)} new artifact(s)")


def main():
    """Main entry point for the script."""
    parser = argparse.ArgumentParser(
        description='Generate Molecule Infrastructure for AVD How-To Guides',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Example configuration file (howto_network_ports.yml):
---
guide:
  name: "Network Ports"
  prefix: "HTNP"
  docs_path: "../../../../../../docs/howto/network_ports"

switches:
  - name: htnp-leaf1a
    mgmt_ip: 172.16.1.201/24
  - name: htnp-leaf1b
    mgmt_ip: 172.16.1.202/24

bgp_as: 65102

port_profiles:
  - profile: PP-WebServer
    mode: access
    vlans: "100"
    spanning_tree_portfast: edge

network_ports:
  - switches:
      - htnp-leaf1a
      - htnp-leaf1b
    switch_ports:
      - Ethernet10-15
    profile: PP-WebServer
    description: "Web Server Ports"

network_services:
  - name: TENANT_HTNP
    vrfs:
      - name: VRF_WEB
        svis:
          - id: 100
            name: WebServers
            enabled: true
            ip_address_virtual: 10.100.100.1/24

artifacts:
  - file: inventory/intended/configs/htnp-leaf1a.cfg
    sections:
      - header: "interface Ethernet10"
      - header: "interface Ethernet11"
    artifact: "htnp-leaf1a-webserver-ports.cfg"
    output_dir: "../../../../../../docs/howto/network_ports/artifacts/"
        """
    )

    parser.add_argument(
        '--config',
        type=Path,
        required=True,
        help='Path to the YAML configuration file'
    )

    parser.add_argument(
        '--base-path',
        type=Path,
        help='Base path for molecule howto directory (default: auto-detect)'
    )

    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Enable verbose logging'
    )

    args = parser.parse_args()

    if args.verbose:
        logger.setLevel(logging.DEBUG)

    # Validate config file exists
    if not args.config.exists():
        logger.error(f"Configuration file not found: {args.config}")
        return 1

    try:
        # Create generator and run
        generator = HowToMoleculeGenerator(args.config, args.base_path)
        generator.generate_all()
        return 0
    except Exception as e:
        logger.error(f"Error generating molecule infrastructure: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        return 1


if __name__ == '__main__':
    exit(main())
