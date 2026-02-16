"""
LLM Generator: Free local AI using Ollama
Supports multiple LLM providers with fallback to mock mode
"""

import requests
import yaml
import os
from typing import Dict, Optional

class LLMGenerator:
    """Generate Ansible playbooks using Ollama (free, local AI)"""
    
    def __init__(self, config: dict = None):
        self.config = config or {}
        
        # Ollama configuration
        self.ollama_url = self.config.get('ollama', {}).get('url', 'http://localhost:11434/api/generate')
        self.ollama_model = self.config.get('ollama', {}).get('model', 'codellama:7b')
        
        # Check if Ollama is running
        self.ollama_available = self._check_ollama()
        
        if self.ollama_available:
            print(f"✓ Ollama detected - using local AI ({self.ollama_model})")
            self.simulation_mode = False
        else:
            print("⚠️  Ollama not running - using mock mode")
            print("   Install: curl -fsSL https://ollama.com/install.sh | sh")
            print("   Start: ollama serve")
            print(f"   Download model: ollama pull {self.ollama_model}")
            self.simulation_mode = True
    
    def _check_ollama(self) -> bool:
        """Check if Ollama is running"""
        try:
            response = requests.get("http://localhost:11434", timeout=2)
            return response.status_code == 200
        except:
            return False
    
    def generate(self, user_prompt: str, params: dict) -> str:
        """Generate playbook using available LLM"""
        if self.simulation_mode:
            return self._mock_generate(user_prompt, params)
        else:
            return self._ollama_generate(user_prompt, params)
    
    def _ollama_generate(self, user_prompt: str, params: dict) -> str:
        """Generate playbook using Ollama (free, local)"""
        print("🤖 Generating playbook with local AI (Ollama)...")
        print(f"   Model: {self.ollama_model}")
        print(f"   This may take 10-30 seconds...")
        
        try:
            # Craft detailed prompt for Ansible generation
            system_context = """You are an expert Ansible playbook generator. Generate valid, production-ready Ansible playbooks in YAML format."""
            
            prompt = f"""{system_context}

Task: {user_prompt}

Generate an Ansible playbook with these requirements:
- Use 'hosts: all' (required for Concert compatibility)
- Include 'become: yes' if sudo/root access needed
- Support multiple OS families: Debian, RedHat, Fedora
- Use 'when: ansible_os_family == "Debian"' for OS-specific tasks
- Use 'when: ansible_os_family == "RedHat"' for RHEL/CentOS
- Use 'when: ansible_os_family == "Fedora"' for Fedora
- Include verification tasks to confirm success
- Add descriptive task names
- Make playbooks idempotent (safe to run multiple times)
- Add a final success message using ansible_distribution variable

Output ONLY the YAML playbook starting with '---', no explanations or markdown:

---
"""
            
            # Call Ollama API
            response = requests.post(self.ollama_url, json={
                "model": self.ollama_model,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0.1,  # Low temperature for consistent code
                    "top_p": 0.9,
                    "top_k": 40,
                    "num_predict": 1500  # Max tokens
                }
            }, timeout=60)
            
            if response.status_code == 200:
                result = response.json()
                playbook_yaml = result.get('response', '').strip()
                
                # Clean up the response
                playbook_yaml = self._clean_yaml_response(playbook_yaml)
                
                # Validate YAML
                try:
                    yaml.safe_load(playbook_yaml)
                    print("✓ Generated playbook is valid YAML")
                except yaml.YAMLError as e:
                    print(f"⚠️  YAML validation warning: {e}")
                    print("→ Attempting to fix...")
                    playbook_yaml = self._fix_yaml(playbook_yaml)
                
                print("✓ Playbook generated successfully by local AI")
                return playbook_yaml
            else:
                print(f"❌ Ollama API error: {response.status_code}")
                print(f"   Response: {response.text[:200]}")
                return self._mock_generate(user_prompt, params)
                
        except requests.exceptions.Timeout:
            print("❌ Ollama request timed out (>60s)")
            print("→ Try a smaller model: ollama pull codellama:7b")
            return self._mock_generate(user_prompt, params)
        except Exception as e:
            print(f"❌ Error calling Ollama: {e}")
            print("→ Make sure Ollama is running: ollama serve")
            return self._mock_generate(user_prompt, params)
    
    def _clean_yaml_response(self, yaml_text: str) -> str:
        """Clean up LLM response to extract valid YAML"""
        # Remove markdown code blocks
        if '```' in yaml_text:
            lines = yaml_text.split('\n')
            yaml_lines = []
            in_code_block = False
            
            for line in lines:
                if line.strip().startswith('```'):
                    in_code_block = not in_code_block
                    continue
                if in_code_block or line.strip().startswith('-') or line.strip().startswith('name:'):
                    yaml_lines.append(line)
            
            yaml_text = '\n'.join(yaml_lines)
        
        # Ensure it starts with ---
        if not yaml_text.strip().startswith('---'):
            yaml_text = '---\n' + yaml_text
        
        return yaml_text.strip()
    
    def _fix_yaml(self, yaml_text: str) -> str:
        """Attempt to fix common YAML issues"""
        try:
            # Try to parse and re-dump to fix formatting
            data = yaml.safe_load(yaml_text)
            return yaml.dump(data, default_flow_style=False, sort_keys=False)
        except:
            # If that fails, return original
            return yaml_text
    
    def _mock_generate(self, user_prompt: str, params: dict) -> str:
        """Mock generation when Ollama not available"""
        print("🤖 Mock mode - Install Ollama for real AI generation")
        print("   1. Install: curl -fsSL https://ollama.com/install.sh | sh")
        print("   2. Start: ollama serve")
        print("   3. Download model: ollama pull codellama:7b")
        
        # Generate a reasonable mock playbook based on the request
        playbook = self._generate_mock_playbook(user_prompt, params)
        
        yaml_content = yaml.dump([playbook], default_flow_style=False, sort_keys=False)
        return f"---\n{yaml_content}"
    
    def _generate_mock_playbook(self, user_prompt: str, params: dict) -> dict:
        """Generate a mock playbook that looks realistic"""
        # Try to infer task type from prompt
        prompt_lower = user_prompt.lower()
        
        tasks = [
            {
                'name': f'Task: {user_prompt}',
                'debug': {
                    'msg': f"This is a mock playbook. Install Ollama for real AI generation."
                }
            }
        ]
        
        # Add some realistic-looking tasks based on keywords
        if 'install' in prompt_lower:
            tasks.append({
                'name': 'Mock: Would install package here',
                'debug': {
                    'msg': "In real mode, this would install the requested package"
                }
            })
        
        if 'firewall' in prompt_lower or 'port' in prompt_lower:
            tasks.append({
                'name': 'Mock: Would configure firewall here',
                'debug': {
                    'msg': "In real mode, this would configure firewall rules"
                }
            })
        
        if 'disable' in prompt_lower or 'stop' in prompt_lower:
            tasks.append({
                'name': 'Mock: Would stop/disable service here',
                'debug': {
                    'msg': "In real mode, this would stop or disable the service"
                }
            })
        
        tasks.append({
            'name': 'Success message',
            'debug': {
                'msg': "✓ Mock task completed on {{ ansible_distribution }}"
            }
        })
        
        playbook = {
            'name': f"Mock playbook: {user_prompt}",
            'hosts': params.get('target_hosts', 'all'),
            'become': True,
            'gather_facts': True,
            'tasks': tasks
        }
        
        return playbook

# Made with Bob
