"""
Concert AI Agent: Production-Ready Enhanced System v3.0
With playbook checking, interactive credentials, and inventory management
"""

import os
import sys
import yaml
from datetime import datetime
from intent_parser import IntentParser
from template_generator import TemplateGenerator
from validator import PlaybookValidator
from git_manager import GitManager
from concert_api import ConcertAPI
from llm_generator import LLMGenerator
from logger import AgentLogger
from playbook_checker import PlaybookChecker
from credential_manager import CredentialManager
from inventory_manager import InventoryManager

class ConcertAgentEnhanced:
    """Production-ready AI Agent with enhanced interactive features"""
    
    def __init__(self, config_path: str = 'config/config.yml'):
        self.config = self._load_config(config_path)
        
        # Initialize all components
        self.parser = IntentParser()
        self.template_generator = TemplateGenerator()
        self.llm_generator = LLMGenerator(self.config)
        self.validator = PlaybookValidator()
        self.git_manager = GitManager(config=self.config)
        self.concert_api = ConcertAPI(self.config)
        self.logger = AgentLogger(self.config)
        self.playbook_checker = PlaybookChecker()
        self.credential_manager = CredentialManager(config_path)
        self.inventory_manager = InventoryManager()
        
        self.output_dir = self.config.get('output_dir', 'output')
        self.hybrid_enabled = self.config.get('hybrid_mode', {}).get('enabled', True)
        
        os.makedirs(self.output_dir, exist_ok=True)
        self.logger.info("Concert AI Agent Enhanced initialized")
    
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
    
    def process_prompt(self, user_prompt: str, skip_check: bool = False):
        """Process user request with enhanced features"""
        
        print("\n" + "="*70)
        print("🤖 CONCERT AI AGENT - Production Enhanced System v3.0")
        print("="*70)
        print(f"\n📝 Your request: {user_prompt}\n")
        
        self.logger.info(f"Processing request: {user_prompt}")
        
        # Step 1: Parse intent
        print("Step 1: Analyzing request...")
        intent_result = self.parser.parse(user_prompt)
        
        intent = intent_result['intent']
        source = intent_result['source']
        params = intent_result['params']
        
        print(f"✓ Intent: {intent}")
        print(f"✓ Source: {source}")
        
        # Step 2: Check for existing playbooks (automatic decision)
        if not skip_check:
            print("\nStep 2: Checking for existing playbooks...")
            matches = self.playbook_checker.find_similar_playbooks(intent, params)
            
            if matches and matches[0]['match_score'] >= 0.8:
                # High match found - use existing automatically
                existing_playbook = matches[0]['filepath']
                print(f"✓ Found high-match playbook ({matches[0]['match_score']*100:.0f}% match)")
                print(f"✓ Using existing: {matches[0]['filename']}")
                self._handle_existing_playbook(existing_playbook, intent_result)
                return
            elif matches:
                print(f"⊘ Found similar playbooks but match score too low (<80%)")
                print(f"→ Will generate new playbook")
        else:
            print("\nStep 2: Skipping playbook check (as requested)")
        
        # Step 3: Collect additional parameters if needed
        print("\nStep 3: Collecting playbook parameters...")
        params = self._collect_playbook_parameters(intent, params)
        
        # Step 4: Generate playbook (Hybrid approach)
        print("\nStep 4: Generating playbook...")
        
        if source == 'template':
            print("  → Using template-based generation (fast, guaranteed accurate)")
            playbook = self.template_generator.generate(
                intent_result['template'],
                params
            )
            generation_source = 'template'
            
        elif source == 'llm_required' and self.hybrid_enabled:
            print("  → No template match found")
            print("  → Using LLM-based generation (flexible, handles custom requests)")
            playbook = self.llm_generator.generate(
                user_prompt,
                params
            )
            generation_source = 'llm'
            
        else:
            print("❌ Could not generate playbook")
            print("💡 Try a different request or enable hybrid mode")
            self.logger.error(f"Failed to generate playbook for: {user_prompt}")
            return
        
        if not playbook:
            print("❌ Playbook generation failed")
            return
        
        print(f"✓ Playbook generated via {generation_source}")
        
        # Step 5: Save playbook
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        os_type = params.get('os_type', 'all')
        filename = f"{intent}_{os_type}_{timestamp}.yml"
        filepath = os.path.join(self.output_dir, filename)
        
        self.template_generator.save_playbook(playbook, filepath)
        
        # Step 6: Validate
        print("\nStep 5: Validating playbook...")
        validation = self.validator.validate(filepath)
        
        if validation['valid']:
            print(validation['message'])
        else:
            print(f"❌ {validation['message']}")
            if 'error' in validation:
                print(f"   Error: {validation['error']}")
            self.logger.error(f"Validation failed: {filepath}")
            return
        
        # Step 7: Check/Create Inventory
        print("\nStep 6: Checking inventory...")
        inventory_result = self._handle_inventory()
        
        # Step 7: Git commit
        print("\nStep 7: Committing to Git...")
        git_result = self._handle_git_commit(filepath)
        
        # Step 8: Git push (ask user)
        if git_result.get('success'):
            push_to_remote = input("\n📤 Push playbook to Git remote? (y/N): ").strip().lower()
            if push_to_remote == 'y':
                push_result = self.git_manager.push_with_credentials()
                if push_result.get('success'):
                    print(f"✓ {push_result['message']}")
                    git_result['pushed'] = True
                    git_result['remote_url'] = push_result.get('remote_url')
                else:
                    print(f"⚠️  {push_result['message']}")
                    if 'error' in push_result:
                        print(f"   Error: {push_result['error']}")
        
        # Log the operation
        self.logger.log_playbook_generation(
            intent=intent,
            source=generation_source,
            playbook_path=filepath,
            validation_status=validation['valid']
        )
        
        # Summary
        self._display_summary(filepath, generation_source, params, validation, git_result, inventory_result)
    
    def _collect_playbook_parameters(self, intent: str, params: dict) -> dict:
        """Collect additional parameters interactively"""
        
        print("📝 Collecting playbook parameters...")
        
        # Always ask for OS type
        print("\n🖥️  Target Operating System:")
        print("  1. Ubuntu/Debian")
        print("  2. RHEL/CentOS")
        print("  3. Fedora")
        print("  4. All (multi-OS playbook)")
        
        os_choice = input("Select OS (1-4, default: 4): ").strip()
        os_map = {
            '1': 'ubuntu',
            '2': 'rhel',
            '3': 'fedora',
            '4': 'all'
        }
        params['os_type'] = os_map.get(os_choice, 'all')
        print(f"✓ OS selected: {params['os_type']}")
        
        # Collect intent-specific parameters
        print("\n📋 Task-specific parameters:")
        
        if intent == 'install_package':
            if not params.get('package_name'):
                params['package_name'] = input("  Package name: ").strip()
        
        elif intent == 'configure_firewall':
            if not params.get('port'):
                params['port'] = input("  Port number: ").strip()
            if not params.get('protocol'):
                protocol = input("  Protocol (tcp/udp, default: tcp): ").strip()
                params['protocol'] = protocol if protocol else 'tcp'
        
        elif intent == 'create_user':
            if not params.get('username'):
                params['username'] = input("  Username: ").strip()
            if not params.get('groups'):
                groups = input("  Additional groups (comma-separated, optional): ").strip()
                if groups:
                    params['groups'] = groups
        
        elif intent == 'deploy_docker':
            if not params.get('container_name'):
                params['container_name'] = input("  Container name: ").strip()
            if not params.get('image_name'):
                params['image_name'] = input("  Docker image: ").strip()
            if not params.get('port'):
                params['port'] = input("  Port mapping (e.g., 8080:80): ").strip()
        
        elif intent == 'restart_service':
            if not params.get('service_name'):
                params['service_name'] = input("  Service name: ").strip()
        
        # Ask about target hosts
        change_target = input("\n  Change target hosts? (current: all) (y/N): ").strip().lower()
        if change_target == 'y':
            target = input("  Target hosts/group: ").strip()
            if target:
                params['target_hosts'] = target
        
        print("✓ Parameters collected")
        return params
    
    def _handle_existing_playbook(self, filepath: str, intent_result: dict):
        """Handle using an existing playbook"""
        
        # Validate the existing playbook
        print("\nValidating existing playbook...")
        validation = self.validator.validate(filepath)
        
        if not validation['valid']:
            print(f"❌ Existing playbook validation failed: {validation['message']}")
            recreate = input("Create new playbook instead? (Y/n): ").strip().lower()
            if recreate != 'n':
                self.process_prompt(intent_result.get('user_prompt', ''), skip_check=True)
            return
        
        print(validation['message'])
        
        # Ask if user wants to execute it
        execute = input("\nExecute this playbook now? (y/N): ").strip().lower()
        if execute == 'y':
            self._execute_playbook(filepath)
        
        print("\n" + "="*70)
        print("✨ USING EXISTING PLAYBOOK!")
        print("="*70)
        print(f"📄 Playbook: {filepath}")
        print(f"✅ Status: REUSED")
        print("="*70 + "\n")
    
    def _handle_git_commit(self, filepath: str) -> dict:
        """Handle Git commit with credential checking"""
        
        git_config = self.config.get('git', {})
        
        # Check if Git is configured
        if not git_config.get('enabled'):
            setup_git = input("Git not configured. Set up now? (y/N): ").strip().lower()
            if setup_git == 'y':
                self.credential_manager.collect_git_credentials(force=True)
                # Reload config
                self.config = self._load_config('config/config.yml')
                self.git_manager = GitManager(config=self.config)
        
        git_result = self.git_manager.commit_playbook(filepath)
        
        if git_result.get('success'):
            print(f"✓ {git_result['message']}")
            if 'commit_hash' in git_result:
                print(f"  Commit: {git_result['commit_hash']}")
        elif git_result.get('skipped'):
            print(f"⊘ {git_result['message']}")
        else:
            print(f"⚠️  {git_result['message']}")
        
        return git_result
    
    def _handle_inventory(self) -> dict:
        """Handle inventory checking and creation"""
        
        # Check if inventory exists
        inventories = self.inventory_manager.list_inventories()
        
        if not inventories:
            print("⚠️  No inventory found")
            create_inv = input("Create inventory now? (Y/n): ").strip().lower()
            if create_inv != 'n':
                inv_path = self.inventory_manager.create_inventory_interactive()
                if inv_path:
                    # Commit inventory to Git
                    print("\n📦 Committing inventory to Git...")
                    git_result = self.git_manager.commit_playbook(inv_path,
                                                                  message=f"Add inventory: {os.path.basename(inv_path)}")
                    
                    if git_result.get('success'):
                        print(f"✓ {git_result['message']}")
                        
                        # Ask to push to remote
                        push_inv = input("\n📤 Push inventory to Git remote? (y/N): ").strip().lower()
                        if push_inv == 'y':
                            push_result = self.git_manager.push_with_credentials()
                            if push_result.get('success'):
                                print(f"✓ {push_result['message']}")
                            else:
                                print(f"⚠️  {push_result['message']}")
                    
                    return {
                        'success': True,
                        'message': 'Inventory created',
                        'path': inv_path
                    }
                else:
                    return {
                        'success': False,
                        'message': 'Inventory creation failed'
                    }
            else:
                return {
                    'success': False,
                    'message': 'Inventory creation skipped',
                    'skipped': True
                }
        else:
            print(f"✓ Using inventory: {inventories[0]}")
            return {
                'success': True,
                'message': 'Inventory exists',
                'path': inventories[0]
            }
    
    def _execute_playbook(self, filepath: str):
        """Execute playbook with ansible-playbook"""
        print("\n📋 Checking inventory...")
        
        # Check if inventory exists
        inventories = self.inventory_manager.list_inventories()
        
        if not inventories:
            print("⚠️  No inventory found")
            create_inv = input("Create inventory now? (Y/n): ").strip().lower()
            if create_inv != 'n':
                self.inventory_manager.create_inventory_interactive()
                inventories = self.inventory_manager.list_inventories()
        
        if inventories:
            print(f"✓ Using inventory: {inventories[0]}")
            
            # Ask for execution confirmation
            print(f"\n🚀 Ready to execute: {filepath}")
            confirm = input("Proceed with execution? (y/N): ").strip().lower()
            
            if confirm == 'y':
                import subprocess
                try:
                    cmd = ['ansible-playbook', '-i', inventories[0], filepath]
                    print(f"\nExecuting: {' '.join(cmd)}\n")
                    subprocess.run(cmd)
                except Exception as e:
                    print(f"❌ Execution failed: {e}")
        else:
            print("❌ Cannot execute without inventory")
    
    def _display_summary(self, filepath: str, generation_source: str, params: dict,
                        validation: dict, git_result: dict, inventory_result: dict):
        """Display operation summary"""
        print("\n" + "="*70)
        print("✨ COMPLETE!")
        print("="*70)
        print(f"📄 Playbook: {filepath}")
        print(f"✅ Status: SUCCESS")
        print(f"🔧 Generation: {generation_source.upper()}")
        print(f"🖥️  Target: {params.get('target_hosts', 'all')}")
        print(f"📊 Validated: {validation['valid']}")
        print(f"📦 Git: {git_result.get('success', False)}")
        print(f"📋 Inventory: {inventory_result.get('success', False)}")
        if inventory_result.get('path'):
            print(f"   Path: {inventory_result['path']}")
        print("="*70 + "\n")
    
    def interactive_mode(self):
        """Run agent in interactive CLI mode"""
        print("\n" + "="*70)
        print("🤖 CONCERT AI AGENT - Production Enhanced System v3.0")
        print("="*70)
        print("\n🎯 Features:")
        print("  • Playbook existence checking")
        print("  • Interactive credential management")
        print("  • Interactive inventory generation")
        print("  • Template-based generation (6 templates)")
        print("  • LLM fallback for custom requests")
        print("  • Multi-OS support")
        print("  • Auto Git commits with remote push")
        print("  • IBM Concert integration")
        print("  • Full logging")
        print("\n📝 Commands:")
        print("  • Type your request (e.g., 'Install nginx on Ubuntu')")
        print("  • 'setup' - Configure credentials")
        print("  • 'inventory' - Manage inventory")
        print("  • 'status' - Show system status")
        print("  • 'logs' - Show recent logs")
        print("  • 'exit' - Quit")
        print("\n💡 Examples:")
        print("  • Install MySQL server, start service, and enable it on boot")
        print("  • Open port 8080 on RHEL")
        print("  • Create user john on CentOS")
        print("  • Deploy redis container")
        print("="*70 + "\n")
        
        while True:
            try:
                prompt = input("Your request: ").strip()
                
                if prompt.lower() in ['exit', 'quit', 'q']:
                    print("\n👋 Goodbye!\n")
                    self.logger.info("Agent stopped by user")
                    break
                
                if prompt.lower() == 'setup':
                    self.credential_manager.setup_all_credentials()
                    # Reload config
                    self.config = self._load_config('config/config.yml')
                    continue
                
                if prompt.lower() == 'inventory':
                    self._inventory_menu()
                    continue
                
                if prompt.lower() == 'status':
                    self._show_status()
                    continue
                
                if prompt.lower() == 'logs':
                    self._show_logs()
                    continue
                
                if prompt:
                    self.process_prompt(prompt)
            
            except KeyboardInterrupt:
                print("\n\n👋 Goodbye!\n")
                self.logger.info("Agent stopped by user (Ctrl+C)")
                break
            except Exception as e:
                print(f"\n❌ Error: {e}\n")
                self.logger.error(f"Unexpected error: {e}")
    
    def _inventory_menu(self):
        """Inventory management menu"""
        print("\n" + "="*70)
        print("📋 INVENTORY MANAGEMENT")
        print("="*70)
        print("\n1. Create new inventory")
        print("2. List inventories")
        print("3. Show inventory")
        print("4. Back to main menu")
        
        choice = input("\nSelect option (1-4): ").strip()
        
        if choice == '1':
            self.inventory_manager.create_inventory_interactive()
        elif choice == '2':
            inventories = self.inventory_manager.list_inventories()
            print("\n📋 Available inventories:")
            for inv in inventories:
                print(f"  • {inv}")
            print()
        elif choice == '3':
            self.inventory_manager.display_inventory()
        
        print("="*70 + "\n")
    
    def _show_status(self):
        """Show system status"""
        print("\n" + "="*70)
        print("📊 SYSTEM STATUS")
        print("="*70)
        
        git_status = self.git_manager.get_status()
        print(f"\n📦 Git:")
        print(f"  Enabled: {git_status.get('enabled', False)}")
        if git_status.get('enabled'):
            print(f"  Branch: {git_status.get('branch', 'N/A')}")
            print(f"  Commits: {git_status.get('commit_count', 'N/A')}")
            print(f"  Remote: {git_status.get('remote_enabled', False)}")
            if git_status.get('remote_enabled'):
                print(f"  Remote URL: {git_status.get('remote_url', 'N/A')}")
                print(f"  Push Mode: {git_status.get('push_mode', 'N/A')}")
        
        print(f"\n🎭 IBM Concert:")
        print(f"  Enabled: {self.concert_api.enabled}")
        print(f"  Mode: {'Simulation' if self.concert_api.simulation_mode else 'Production'}")
        
        print(f"\n🔧 Hybrid Mode:")
        print(f"  Enabled: {self.hybrid_enabled}")
        print(f"  Templates: 6 available")
        print(f"  LLM Fallback: {self.config.get('hybrid_mode', {}).get('llm_fallback', True)}")
        
        print(f"\n📋 Inventory:")
        inventories = self.inventory_manager.list_inventories()
        print(f"  Count: {len(inventories)}")
        
        print("="*70 + "\n")
    
    def _show_logs(self):
        """Show recent logs"""
        print("\n" + "="*70)
        print("📋 RECENT LOGS (Last 20 entries)")
        print("="*70 + "\n")
        
        logs = self.logger.get_recent_logs(20)
        for log in logs:
            print(log.strip())
        
        print("\n" + "="*70 + "\n")


if __name__ == '__main__':
    agent = ConcertAgentEnhanced()
    
    if len(sys.argv) > 1:
        prompt = ' '.join(sys.argv[1:])
        agent.process_prompt(prompt)
    else:
        agent.interactive_mode()

# Made with Bob
