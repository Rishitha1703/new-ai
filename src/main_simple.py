"""
Concert AI Agent: Simplified Version
Minimal questions, streamlined workflow
"""

import os
import sys
import yaml
from datetime import datetime
from intent_parser import IntentParser
from template_generator import TemplateGenerator
from validator import PlaybookValidator
from git_manager import GitManager
from llm_generator import LLMGenerator
from logger import AgentLogger

class ConcertAgentSimple:
    """Simplified AI Agent with minimal user interaction"""
    
    def __init__(self, config_path: str = 'config/config.yml'):
        self.config = self._load_config(config_path)
        
        # Initialize components
        self.parser = IntentParser()
        self.template_generator = TemplateGenerator()
        self.llm_generator = LLMGenerator(self.config)
        self.validator = PlaybookValidator()
        self.logger = AgentLogger(self.config)
        
        self.output_dir = self.config.get('output_dir', 'output')
        os.makedirs(self.output_dir, exist_ok=True)
        os.makedirs('inventory', exist_ok=True)
        
        self.logger.info("Concert AI Agent Simple initialized")
    
    def _load_config(self, config_path: str) -> dict:
        """Load configuration from YAML file"""
        if os.path.exists(config_path):
            try:
                with open(config_path, 'r') as f:
                    return yaml.safe_load(f) or {}
            except Exception as e:
                print(f"⚠️  Could not load config: {e}")
                return {}
        return {}
    
    def process_request(self, user_prompt: str):
        """Process user request with simplified workflow"""
        
        print("\n" + "="*70)
        print("🤖 CONCERT AI AGENT - Simplified Workflow")
        print("="*70)
        print(f"\n📝 Request: {user_prompt}\n")
        
        # Step 1: Parse intent
        print("Step 1: Analyzing request...")
        intent_result = self.parser.parse(user_prompt)
        intent = intent_result['intent']
        source = intent_result['source']
        params = intent_result['params']
        
        print(f"✓ Intent: {intent}")
        print(f"✓ Source: {source}")
        
        # Step 2: Ask ONLY for OS type
        print("\n" + "="*70)
        print("PLAYBOOK GENERATION")
        print("="*70)
        params = self._ask_os_type(params)
        
        # Collect intent-specific params (minimal)
        params = self._collect_minimal_params(intent, params)
        
        # Step 3: Generate playbook
        print("\nStep 2: Generating playbook...")
        playbook = self._generate_playbook(user_prompt, intent_result, params)
        
        if not playbook:
            print("❌ Playbook generation failed")
            return
        
        # Step 4: Save and validate
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        os_type = params.get('os_type', 'all')
        playbook_name = f"{intent}_{os_type}_{timestamp}.yml"
        filepath = os.path.join(self.output_dir, playbook_name)
        
        self.template_generator.save_playbook(playbook, filepath)
        
        print("\nStep 3: Validating playbook...")
        validation = self.validator.validate(filepath)
        
        if not validation['valid']:
            print(f"❌ {validation['message']}")
            return
        
        print(f"✓ {validation['message']}")
        
        # Step 5: Git configuration
        print("\n" + "="*70)
        print("GIT CONFIGURATION")
        print("="*70)
        git_info = self._collect_git_info(playbook_name)
        
        # Step 6: Inventory configuration
        print("\n" + "="*70)
        print("INVENTORY CONFIGURATION")
        print("="*70)
        inventory_info = self._collect_inventory_info()
        
        # Step 7: Push to Git
        print("\n" + "="*70)
        print("PUSHING TO GIT")
        print("="*70)
        self._push_to_git(filepath, git_info, inventory_info)
        
        # Summary
        print("\n" + "="*70)
        print("✨ COMPLETE!")
        print("="*70)
        print(f"📄 Playbook: {playbook_name}")
        print(f"📁 Location: {filepath}")
        print(f"🌐 Git Repo: {git_info['repo_name']}")
        print(f"📦 Inventory: inventory/inventory.ini")
        print("="*70 + "\n")
        
        self.logger.log_playbook_generation(
            intent=intent,
            source=source,
            playbook_path=filepath,
            validation_status=validation['valid']
        )
    
    def _ask_os_type(self, params: dict) -> dict:
        """Ask only for OS type"""
        print("\n🖥️  Target Operating System:")
        print("  1. Ubuntu/Debian")
        print("  2. RHEL/CentOS")
        print("  3. Fedora")
        print("  4. All (multi-OS playbook)")
        
        os_choice = input("\nSelect OS (1-4, default: 4): ").strip()
        os_map = {
            '1': 'ubuntu',
            '2': 'rhel',
            '3': 'fedora',
            '4': 'all'
        }
        params['os_type'] = os_map.get(os_choice, 'all')
        print(f"✓ OS selected: {params['os_type']}")
        
        return params
    
    def _collect_minimal_params(self, intent: str, params: dict) -> dict:
        """Collect only essential parameters for the intent"""
        
        if intent == 'install_package' and not params.get('package_name'):
            params['package_name'] = input("\n📦 Package name: ").strip()
        
        elif intent == 'configure_firewall':
            if not params.get('port'):
                params['port'] = input("\n🔥 Port number: ").strip()
            if not params.get('protocol'):
                params['protocol'] = input("Protocol (tcp/udp, default: tcp): ").strip() or 'tcp'
        
        elif intent == 'create_user' and not params.get('username'):
            params['username'] = input("\n👤 Username: ").strip()
        
        elif intent == 'deploy_docker':
            if not params.get('container_name'):
                params['container_name'] = input("\n🐳 Container name: ").strip()
            if not params.get('image_name'):
                params['image_name'] = input("Docker image: ").strip()
        
        elif intent == 'restart_service' and not params.get('service_name'):
            params['service_name'] = input("\n⚙️  Service name: ").strip()
        
        return params
    
    def _generate_playbook(self, user_prompt: str, intent_result: dict, params: dict):
        """Generate playbook using template or LLM"""
        
        source = intent_result['source']
        
        if source == 'template':
            print("  → Using template (fast & accurate)")
            return self.template_generator.generate(
                intent_result['template'],
                params
            )
        
        elif source == 'llm_required':
            print("  → Using LLM (flexible)")
            return self.llm_generator.generate(user_prompt, params)
        
        return None
    
    def _collect_git_info(self, playbook_name: str) -> dict:
        """Collect Git information"""
        
        print("\n📋 Enter Git details:\n")
        
        # Git URL
        git_url = input("Git repository URL (e.g., https://github.com/user/repo.git): ").strip()
        
        # Clean URL - remove /tree/branch if present
        if '/tree/' in git_url:
            git_url = git_url.split('/tree/')[0]
        
        # Ensure .git extension
        if not git_url.endswith('.git'):
            git_url += '.git'
        
        print(f"✓ Using URL: {git_url}")
        
        # Credentials
        username = input("\nGit username: ").strip()
        token = input("Git token/password (visible): ").strip()
        
        # Repository details
        repo_name = input("\nRepository name: ").strip()
        branch = input("Branch to push to (default: main): ").strip() or "main"
        
        # File names
        print(f"\n📄 File names:")
        use_playbook_name = input(f"Playbook name (default: {playbook_name}): ").strip()
        if use_playbook_name:
            playbook_name = use_playbook_name
        
        inventory_name = input("Inventory name (default: inventory.ini): ").strip() or "inventory.ini"
        
        return {
            'url': git_url,
            'username': username,
            'token': token,
            'repo_name': repo_name,
            'branch': branch,
            'playbook_name': playbook_name,
            'inventory_name': inventory_name
        }
    
    def _collect_inventory_info(self) -> dict:
        """Collect inventory information"""
        
        print("\n📋 Enter inventory details:\n")
        
        ansible_host = input("ansible_host (IP address): ").strip()
        ansible_user = input("ansible_user (default: root): ").strip() or "root"
        ssh_key = input("ansible_ssh_private_key_file (default: ~/.ssh/ai-agent): ").strip()
        
        if not ssh_key:
            ssh_key = "~/.ssh/ai-agent"
        
        return {
            'ansible_host': ansible_host,
            'ansible_user': ansible_user,
            'ansible_ssh_private_key_file': ssh_key
        }
    
    def _push_to_git(self, filepath: str, git_info: dict, inventory_info: dict):
        """Push playbook and inventory to Git"""
        
        try:
            # Create inventory file with custom name
            inventory_path = f"inventory/{git_info['inventory_name']}"
            self._create_inventory_file(inventory_path, inventory_info)
            print(f"✓ Created inventory: {inventory_path}")
            
            # Initialize Git if needed
            if not os.path.exists(os.path.join(self.output_dir, '.git')):
                os.system(f"cd {self.output_dir} && git init")
                print(f"✓ Initialized Git repository")
            
            # Configure Git
            os.system(f"cd {self.output_dir} && git config user.name '{git_info['username']}'")
            os.system(f"cd {self.output_dir} && git config user.email '{git_info['username']}@example.com'")
            
            # Add remote with credentials embedded
            remote_url = git_info['url'].replace('https://', f"https://{git_info['username']}:{git_info['token']}@")
            os.system(f"cd {self.output_dir} && git remote remove origin 2>/dev/null")
            os.system(f"cd {self.output_dir} && git remote add origin {remote_url}")
            print(f"✓ Configured remote: {git_info['repo_name']}")
            
            # Copy inventory to output directory with custom name
            os.system(f"cp {inventory_path} {self.output_dir}/{git_info['inventory_name']}")
            
            # Rename playbook if custom name provided
            playbook_file = os.path.basename(filepath)
            if git_info['playbook_name'] != playbook_file:
                new_playbook_path = os.path.join(self.output_dir, git_info['playbook_name'])
                os.system(f"cp {filepath} {new_playbook_path}")
                playbook_file = git_info['playbook_name']
            
            # Add, commit, and push
            os.system(f"cd {self.output_dir} && git add {playbook_file} {git_info['inventory_name']}")
            os.system(f"cd {self.output_dir} && git commit -m 'Add {git_info['playbook_name']} and {git_info['inventory_name']}'")
            
            print(f"\n🚀 Pushing to branch '{git_info['branch']}'...")
            result = os.system(f"cd {self.output_dir} && git push -f origin {git_info['branch']}")
            
            if result == 0:
                print(f"✓ Successfully pushed to {git_info['repo_name']}/{git_info['branch']}")
                print(f"  📄 Playbook: {playbook_file}")
                print(f"  📦 Inventory: {git_info['inventory_name']}")
            else:
                print(f"⚠️  Push failed. Check:")
                print(f"  - Git URL is correct: {git_info['url']}")
                print(f"  - Token has push permissions")
                print(f"  - Branch '{git_info['branch']}' exists or can be created")
            
        except Exception as e:
            print(f"❌ Git push failed: {e}")
    
    def _create_inventory_file(self, filepath: str, info: dict):
        """Create Ansible inventory file from template"""
        
        # Read template
        template_path = 'inventory/inventory_template.ini'
        
        if not os.path.exists(template_path):
            # Create template if it doesn't exist
            template_content = "[hosts]\nserver1 ansible_host={{ANSIBLE_HOST}} ansible_user={{ANSIBLE_USER}} ansible_ssh_private_key_file={{ANSIBLE_SSH_KEY}}\n"
            os.makedirs('inventory', exist_ok=True)
            with open(template_path, 'w') as f:
                f.write(template_content)
        
        # Read template
        with open(template_path, 'r') as f:
            content = f.read()
        
        # Replace placeholders
        content = content.replace('{{ANSIBLE_HOST}}', info['ansible_host'])
        content = content.replace('{{ANSIBLE_USER}}', info['ansible_user'])
        content = content.replace('{{ANSIBLE_SSH_KEY}}', info['ansible_ssh_private_key_file'])
        
        # Write filled inventory
        with open(filepath, 'w') as f:
            f.write(content)


def main():
    """Main entry point"""
    
    agent = ConcertAgentSimple()
    
    # Check for command line argument
    if len(sys.argv) > 1:
        user_prompt = ' '.join(sys.argv[1:])
    else:
        print("\n" + "="*70)
        print("🤖 CONCERT AI AGENT - Simplified Workflow")
        print("="*70)
        print("\nExamples:")
        print("  • Install nginx on all servers")
        print("  • Open port 80 and 443 on firewall")
        print("  • Create user admin with sudo access")
        print("  • Deploy docker container")
        print("="*70 + "\n")
        
        user_prompt = input("Enter your request: ").strip()
    
    if not user_prompt:
        print("❌ No request provided")
        return
    
    agent.process_request(user_prompt)


if __name__ == "__main__":
    main()

# Made with Bob
