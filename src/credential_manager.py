"""
Credential Manager: Interactive credential collection for Git and other services
"""

import os
import getpass
import yaml
from typing import Dict, Optional

class CredentialManager:
    """Manage credentials for Git, Concert API, and other services"""
    
    def __init__(self, config_path: str = 'config/config.yml'):
        self.config_path = config_path
        self.config = self._load_config()
    
    def _load_config(self) -> dict:
        """Load existing configuration"""
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, 'r') as f:
                    return yaml.safe_load(f) or {}
            except Exception:
                return {}
        return {}
    
    def _save_config(self) -> bool:
        """Save configuration to file"""
        try:
            os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
            with open(self.config_path, 'w') as f:
                yaml.dump(self.config, f, default_flow_style=False, sort_keys=False)
            return True
        except Exception as e:
            print(f"❌ Failed to save config: {e}")
            return False
    
    def collect_git_credentials(self, force: bool = False) -> Dict:
        """
        Collect Git credentials interactively
        
        Args:
            force: Force re-collection even if credentials exist
            
        Returns:
            Dictionary with Git configuration
        """
        git_config = self.config.get('git', {})
        
        # Check if already configured
        if not force and git_config.get('remote_url') and git_config.get('enabled'):
            print("\n✓ Git credentials already configured")
            print(f"  Remote URL: {git_config.get('remote_url')}")
            print(f"  Branch: {git_config.get('branch', 'main')}")
            
            reconfigure = input("\nReconfigure Git settings? (y/N): ").strip().lower()
            if reconfigure != 'y':
                return git_config
        
        print("\n" + "="*70)
        print("🔐 GIT CONFIGURATION")
        print("="*70)
        
        # Enable Git
        enable_git = input("\nEnable Git integration? (Y/n): ").strip().lower()
        git_config['enabled'] = enable_git != 'n'
        
        if not git_config['enabled']:
            print("✓ Git integration disabled")
            self.config['git'] = git_config
            self._save_config()
            return git_config
        
        # Auto-commit
        auto_commit = input("Enable auto-commit for playbooks? (Y/n): ").strip().lower()
        git_config['auto_commit'] = auto_commit != 'n'
        
        # Remote configuration
        enable_remote = input("\nEnable remote Git repository? (Y/n): ").strip().lower()
        git_config['remote_enabled'] = enable_remote != 'n'
        
        if git_config['remote_enabled']:
            # Remote URL
            current_url = git_config.get('remote_url', '')
            print(f"\nCurrent remote URL: {current_url if current_url else 'Not set'}")
            remote_url = input("Enter Git remote URL (e.g., https://github.com/user/repo.git): ").strip()
            
            if remote_url:
                git_config['remote_url'] = remote_url
            elif not current_url:
                print("⚠️  No remote URL provided - remote push disabled")
                git_config['remote_enabled'] = False
            
            # Branch
            current_branch = git_config.get('branch', 'main')
            branch = input(f"Enter branch name (default: {current_branch}): ").strip()
            git_config['branch'] = branch if branch else current_branch
            
            # Push mode
            print("\nPush mode options:")
            print("  1. immediate - Push after each commit")
            print("  2. manual - Push only when manually triggered")
            print("  3. scheduled - Push at regular intervals")
            
            push_mode = input("Select push mode (1/2/3, default: 2): ").strip()
            mode_map = {'1': 'immediate', '2': 'manual', '3': 'scheduled'}
            git_config['remote_push_mode'] = mode_map.get(push_mode, 'manual')
            
            if git_config['remote_push_mode'] == 'scheduled':
                interval = input("Push interval in seconds (default: 3600): ").strip()
                try:
                    git_config['push_interval'] = int(interval) if interval else 3600
                except ValueError:
                    git_config['push_interval'] = 3600
            
            # Git credentials (for HTTPS)
            if 'https://' in git_config.get('remote_url', ''):
                print("\n📝 Git Authentication")
                print("Note: For GitHub, use Personal Access Token instead of password")
                
                use_credentials = input("Configure Git credentials? (y/N): ").strip().lower()
                if use_credentials == 'y':
                    username = input("Git username: ").strip()
                    token = getpass.getpass("Git token/password (hidden): ").strip()
                    
                    if username and token:
                        # Store in URL format (will be used by git)
                        url_parts = git_config['remote_url'].split('://')
                        if len(url_parts) == 2:
                            git_config['remote_url'] = f"{url_parts[0]}://{username}:{token}@{url_parts[1]}"
                            print("✓ Credentials configured")
        
        # Commit message template
        current_template = git_config.get('commit_message_template', 'Add playbook: {filename}')
        print(f"\nCurrent commit message template: {current_template}")
        template = input("Enter new template (or press Enter to keep current): ").strip()
        if template:
            git_config['commit_message_template'] = template
        
        # Save configuration
        self.config['git'] = git_config
        if self._save_config():
            print("\n✓ Git configuration saved")
        
        print("="*70)
        return git_config
    
    def collect_concert_credentials(self, force: bool = False) -> Dict:
        """
        Collect IBM Concert API credentials
        
        Args:
            force: Force re-collection even if credentials exist
            
        Returns:
            Dictionary with Concert configuration
        """
        concert_config = self.config.get('concert', {})
        
        # Check if already configured
        if not force and concert_config.get('api_key') and concert_config.get('enabled'):
            print("\n✓ Concert API credentials already configured")
            
            reconfigure = input("\nReconfigure Concert API settings? (y/N): ").strip().lower()
            if reconfigure != 'y':
                return concert_config
        
        print("\n" + "="*70)
        print("🎭 IBM CONCERT API CONFIGURATION")
        print("="*70)
        
        # Enable Concert
        enable_concert = input("\nEnable IBM Concert integration? (y/N): ").strip().lower()
        concert_config['enabled'] = enable_concert == 'y'
        
        if not concert_config['enabled']:
            print("✓ Concert integration disabled")
            self.config['concert'] = concert_config
            self._save_config()
            return concert_config
        
        # API URL
        current_url = concert_config.get('api_url', 'https://concert.ibm.com/api/v1')
        api_url = input(f"Concert API URL (default: {current_url}): ").strip()
        concert_config['api_url'] = api_url if api_url else current_url
        
        # API Key
        api_key = getpass.getpass("Concert API Key (hidden): ").strip()
        if api_key:
            concert_config['api_key'] = api_key
        else:
            print("⚠️  No API key provided - Concert integration may not work")
        
        # Workflow name
        current_workflow = concert_config.get('workflow_name', 'ansible-execution')
        workflow = input(f"Workflow name (default: {current_workflow}): ").strip()
        concert_config['workflow_name'] = workflow if workflow else current_workflow
        
        # Simulation mode
        simulation = input("Enable simulation mode? (Y/n): ").strip().lower()
        concert_config['simulation_mode'] = simulation != 'n'
        
        # Timeout
        timeout = input("API timeout in seconds (default: 60): ").strip()
        try:
            concert_config['timeout'] = int(timeout) if timeout else 60
        except ValueError:
            concert_config['timeout'] = 60
        
        # Save configuration
        self.config['concert'] = concert_config
        if self._save_config():
            print("\n✓ Concert API configuration saved")
        
        print("="*70)
        return concert_config
    
    def collect_llm_credentials(self, force: bool = False) -> Dict:
        """
        Collect LLM API credentials (OpenAI, Ollama, etc.)
        
        Args:
            force: Force re-collection even if credentials exist
            
        Returns:
            Dictionary with LLM configuration
        """
        llm_config = self.config.get('llm', {})
        
        # Check if already configured
        if not force and llm_config.get('provider'):
            print("\n✓ LLM credentials already configured")
            print(f"  Provider: {llm_config.get('provider')}")
            
            reconfigure = input("\nReconfigure LLM settings? (y/N): ").strip().lower()
            if reconfigure != 'y':
                return llm_config
        
        print("\n" + "="*70)
        print("🤖 LLM CONFIGURATION")
        print("="*70)
        
        # Provider selection
        print("\nAvailable LLM providers:")
        print("  1. ollama (local, free)")
        print("  2. openai (cloud, requires API key)")
        print("  3. anthropic (cloud, requires API key)")
        
        provider_choice = input("Select provider (1/2/3, default: 1): ").strip()
        provider_map = {'1': 'ollama', '2': 'openai', '3': 'anthropic'}
        llm_config['provider'] = provider_map.get(provider_choice, 'ollama')
        
        if llm_config['provider'] == 'ollama':
            # Ollama configuration
            model = input("Ollama model (default: codellama:7b): ").strip()
            llm_config['model'] = model if model else 'codellama:7b'
            
            url = input("Ollama URL (default: http://localhost:11434): ").strip()
            llm_config['api_url'] = url if url else 'http://localhost:11434'
            
        elif llm_config['provider'] == 'openai':
            # OpenAI configuration
            api_key = getpass.getpass("OpenAI API Key (hidden): ").strip()
            if api_key:
                llm_config['api_key'] = api_key
            else:
                print("⚠️  No API key provided - OpenAI integration may not work")
            
            model = input("OpenAI model (default: gpt-4): ").strip()
            llm_config['model'] = model if model else 'gpt-4'
        
        elif llm_config['provider'] == 'anthropic':
            # Anthropic configuration
            api_key = getpass.getpass("Anthropic API Key (hidden): ").strip()
            if api_key:
                llm_config['api_key'] = api_key
            else:
                print("⚠️  No API key provided - Anthropic integration may not work")
            
            model = input("Anthropic model (default: claude-3-opus-20240229): ").strip()
            llm_config['model'] = model if model else 'claude-3-opus-20240229'
        
        # Common settings
        temperature = input("Temperature (0.0-1.0, default: 0.3): ").strip()
        try:
            llm_config['temperature'] = float(temperature) if temperature else 0.3
        except ValueError:
            llm_config['temperature'] = 0.3
        
        max_tokens = input("Max tokens (default: 2000): ").strip()
        try:
            llm_config['max_tokens'] = int(max_tokens) if max_tokens else 2000
        except ValueError:
            llm_config['max_tokens'] = 2000
        
        # Save configuration
        self.config['llm'] = llm_config
        if self._save_config():
            print("\n✓ LLM configuration saved")
        
        print("="*70)
        return llm_config
    
    def setup_all_credentials(self) -> None:
        """Interactive setup for all credentials"""
        print("\n" + "="*70)
        print("🚀 CONCERT AI AGENT - CREDENTIAL SETUP")
        print("="*70)
        print("\nThis wizard will help you configure:")
        print("  • Git integration (local & remote)")
        print("  • IBM Concert API")
        print("  • LLM provider (Ollama/OpenAI/Anthropic)")
        print("\nYou can skip any section and configure it later.")
        print("="*70)
        
        # Git credentials
        setup_git = input("\nConfigure Git? (Y/n): ").strip().lower()
        if setup_git != 'n':
            self.collect_git_credentials(force=True)
        
        # Concert credentials
        setup_concert = input("\nConfigure IBM Concert API? (y/N): ").strip().lower()
        if setup_concert == 'y':
            self.collect_concert_credentials(force=True)
        
        # LLM credentials
        setup_llm = input("\nConfigure LLM provider? (Y/n): ").strip().lower()
        if setup_llm != 'n':
            self.collect_llm_credentials(force=True)
        
        print("\n" + "="*70)
        print("✅ SETUP COMPLETE!")
        print("="*70)
        print(f"\nConfiguration saved to: {self.config_path}")
        print("You can now use the Concert AI Agent with your settings.")
        print("\nTo reconfigure later, run:")
        print("  python src/credential_manager.py")
        print("="*70 + "\n")


# CLI interface
if __name__ == '__main__':
    import sys
    
    manager = CredentialManager()
    
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        
        if command == 'git':
            manager.collect_git_credentials(force=True)
        elif command == 'concert':
            manager.collect_concert_credentials(force=True)
        elif command == 'llm':
            manager.collect_llm_credentials(force=True)
        else:
            print(f"Unknown command: {command}")
            print("Usage: python credential_manager.py [git|concert|llm]")
    else:
        manager.setup_all_credentials()

# Made with Bob
