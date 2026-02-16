"""
Inventory Manager: Interactive inventory generation and management
Generates INI format inventory files
"""

import os
from typing import Dict, List, Optional
from datetime import datetime

class InventoryManager:
    """Manage Ansible inventory files with interactive host configuration"""
    
    def __init__(self, inventory_dir: str = 'inventory'):
        self.inventory_dir = inventory_dir
        os.makedirs(self.inventory_dir, exist_ok=True)
        self.default_inventory = os.path.join(inventory_dir, 'inventory.ini')
    
    def create_inventory_interactive(self) -> str:
        """
        Create inventory file interactively in INI format
        
        Returns:
            Path to created inventory file
        """
        print("\n" + "="*70)
        print("📋 ANSIBLE INVENTORY CREATION")
        print("="*70)
        print("\nThis wizard will help you create an Ansible inventory file.")
        print("Format: [hosts]")
        print("        hostname ansible_host=IP ansible_user=user ...")
        print("="*70)
        
        # Ask if user wants to use existing inventory
        if os.path.exists(self.default_inventory):
            print(f"\n✓ Found existing inventory: {self.default_inventory}")
            use_existing = input("Use existing inventory? (Y/n): ").strip().lower()
            if use_existing != 'n':
                return self.default_inventory
        
        # Collect hosts
        hosts = []
        
        print("\n" + "-"*70)
        print("Add hosts to inventory:")
        print("-"*70)
        
        while True:
            print("\n" + "~"*70)
            host_name = input("\nHost name (or 'done' to finish): ").strip()
            
            if host_name.lower() == 'done':
                break
            
            if not host_name:
                print("❌ Host name cannot be empty")
                continue
            
            # Create host configuration
            host_config = self._create_host_interactive_ini(host_name)
            if host_config:
                hosts.append(host_config)
                print(f"✓ Host '{host_name}' added")
        
        # Check if any hosts were added
        if not hosts:
            print("\n⚠️  No hosts added. Creating default host...")
            default_host = self._create_host_interactive_ini("Server1")
            if default_host:
                hosts.append(default_host)
        
        # Save inventory in INI format
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"inventory_{timestamp}.ini"
        filepath = os.path.join(self.inventory_dir, filename)
        
        try:
            # Write INI format
            with open(filepath, 'w') as f:
                f.write("[hosts]\n")
                for host in hosts:
                    f.write(host + "\n")
            
            # Also save as default inventory.ini
            with open(self.default_inventory, 'w') as f:
                f.write("[hosts]\n")
                for host in hosts:
                    f.write(host + "\n")
            
            print("\n" + "="*70)
            print("✅ INVENTORY CREATED!")
            print("="*70)
            print(f"📄 Saved to: {filepath}")
            print(f"📄 Default: {self.default_inventory}")
            print("\n📋 Inventory content:")
            print("-"*70)
            print("[hosts]")
            for host in hosts:
                print(host)
            print("="*70 + "\n")
            
            return filepath
            
        except Exception as e:
            print(f"\n❌ Failed to save inventory: {e}")
            return ""
    
    def _create_host_interactive_ini(self, host_name: str) -> str:
        """
        Create a host configuration line in INI format
        
        Returns:
            String in format: hostname ansible_host=IP ansible_user=user ...
        """
        print(f"\n🖥️  Configuring host: {host_name}")
        
        # Operating System
        print("\n  Operating System:")
        print("    1. Ubuntu/Debian")
        print("    2. RHEL/CentOS")
        print("    3. Fedora")
        print("    4. Other")
        os_choice = input("  Select OS (1-4): ").strip()
        os_map = {
            '1': 'Ubuntu',
            '2': 'RHEL',
            '3': 'Fedora',
            '4': 'Linux'
        }
        host_os = os_map.get(os_choice, 'Linux')
        print(f"  ✓ OS: {host_os}")
        
        # Ansible host (IP or hostname)
        ansible_host = input("\n  IP address or hostname: ").strip()
        if not ansible_host:
            print("  ⚠️  No host address provided - using hostname")
            ansible_host = host_name
        
        # User
        ansible_user = input("  SSH user (default: ansible): ").strip()
        if not ansible_user:
            ansible_user = "ansible"
        
        # SSH key file
        print("\n  SSH private key file:")
        print("    Examples: ~/.ssh/id_rsa, ~/.ssh/ai-agent, /path/to/key")
        ssh_key = input("  SSH key path (default: ~/.ssh/id_rsa): ").strip()
        if not ssh_key:
            ssh_key = "~/.ssh/id_rsa"
        
        # Port (optional)
        port = input("  SSH port (press Enter for default 22): ").strip()
        
        # Become (sudo)
        use_become = input("  Use sudo/become? (Y/n): ").strip().lower()
        ansible_become = "yes" if use_become != 'n' else "no"
        
        # Build the INI line with OS comment
        host_line = f"{host_name} ansible_host={ansible_host} ansible_user={ansible_user} ansible_ssh_private_key_file={ssh_key}"
        
        if port:
            host_line += f" ansible_port={port}"
        
        host_line += f" ansible_become={ansible_become}"
        
        # Add OS as a comment for reference
        host_line += f" # OS: {host_os}"
        
        # Additional parameters
        add_more = input("  Add more parameters? (y/N): ").strip().lower()
        if add_more == 'y':
            print("  Enter additional parameters (key=value format, one per line)")
            print("  Examples: ansible_python_interpreter=/usr/bin/python3")
            print("  Type 'done' when finished")
            
            while True:
                param = input("  Parameter: ").strip()
                if param.lower() == 'done' or not param:
                    break
                if '=' in param:
                    host_line += f" {param}"
                else:
                    print("    ❌ Invalid format. Use: key=value")
        
        return host_line
    
    def load_inventory(self, filepath: Optional[str] = None) -> List[str]:
        """Load inventory from INI file"""
        if filepath is None:
            filepath = self.default_inventory
        
        if not os.path.exists(filepath):
            return []
        
        try:
            with open(filepath, 'r') as f:
                lines = f.readlines()
            
            # Extract host lines (skip [hosts] header and empty lines)
            hosts = []
            in_hosts_section = False
            for line in lines:
                line = line.strip()
                if line == '[hosts]':
                    in_hosts_section = True
                    continue
                if line.startswith('[') and line.endswith(']'):
                    in_hosts_section = False
                    continue
                if in_hosts_section and line and not line.startswith('#'):
                    hosts.append(line)
            
            return hosts
        except Exception as e:
            print(f"❌ Failed to load inventory: {e}")
            return []
    
    def list_inventories(self) -> List[str]:
        """List all inventory files"""
        if not os.path.exists(self.inventory_dir):
            return []
        
        inventories = []
        for filename in os.listdir(self.inventory_dir):
            if filename.endswith('.ini'):
                inventories.append(os.path.join(self.inventory_dir, filename))
        
        return sorted(inventories, key=os.path.getmtime, reverse=True)
    
    def display_inventory(self, filepath: Optional[str] = None) -> None:
        """Display inventory contents"""
        if filepath is None:
            filepath = self.default_inventory
        
        if not os.path.exists(filepath):
            print(f"\n❌ No inventory found at: {filepath}")
            return
        
        try:
            with open(filepath, 'r') as f:
                content = f.read()
            
            print("\n" + "="*70)
            print(f"📋 INVENTORY: {os.path.basename(filepath)}")
            print("="*70)
            print(content)
            print("="*70 + "\n")
        except Exception as e:
            print(f"❌ Failed to read inventory: {e}")
    
    def create_quick_inventory(self, hosts: List[Dict]) -> str:
        """
        Create a quick inventory from a list of host dictionaries
        
        Args:
            hosts: List of dicts with 'name', 'host', 'user', 'key_file', etc.
            
        Returns:
            Path to created inventory file
        """
        host_lines = []
        
        for host_info in hosts:
            host_name = host_info.get('name', f"Server{len(host_lines) + 1}")
            ansible_host = host_info.get('host', host_name)
            ansible_user = host_info.get('user', 'ansible')
            ssh_key = host_info.get('key_file', '~/.ssh/id_rsa')
            ansible_become = host_info.get('become', 'yes')
            
            host_line = f"{host_name} ansible_host={ansible_host} ansible_user={ansible_user} ansible_ssh_private_key_file={ssh_key} ansible_become={ansible_become}"
            
            if 'port' in host_info:
                host_line += f" ansible_port={host_info['port']}"
            
            host_lines.append(host_line)
        
        # Save inventory
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"inventory_{timestamp}.ini"
        filepath = os.path.join(self.inventory_dir, filename)
        
        try:
            with open(filepath, 'w') as f:
                f.write("[hosts]\n")
                for host_line in host_lines:
                    f.write(host_line + "\n")
            return filepath
        except Exception as e:
            print(f"❌ Failed to save inventory: {e}")
            return ""


# CLI interface
if __name__ == '__main__':
    import sys
    
    manager = InventoryManager()
    
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        
        if command == 'create':
            manager.create_inventory_interactive()
        elif command == 'list':
            inventories = manager.list_inventories()
            print("\n📋 Available inventories:")
            for inv in inventories:
                print(f"  • {inv}")
            print()
        elif command == 'show':
            filepath = sys.argv[2] if len(sys.argv) > 2 else None
            manager.display_inventory(filepath)
        else:
            print(f"Unknown command: {command}")
            print("Usage: python inventory_manager.py [create|list|show]")
    else:
        # Interactive mode
        manager.create_inventory_interactive()

# Made with Bob
