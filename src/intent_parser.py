"""
Intent Parser: Understands user requests (UPGRADED for 6 templates)
"""

import re
from typing import Dict, Optional

class IntentParser:
    """Parse natural language prompts with OS detection"""
    
    OS_KEYWORDS = {
        'ubuntu': 'all',
        'debian': 'all',
        'rhel': 'all',
        'centos': 'all',
        'rocky': 'all',
        'alma': 'all',
        'almalinux': 'all',
        'fedora': 'all',
        'amazon linux': 'all',
    }
    
    INTENT_PATTERNS = {
        'install_package': [
            r'install\s+(\w+)',
            r'setup\s+(\w+)',
            r'add\s+(\w+)\s+package',
        ],
        'configure_firewall': [
            r'open\s+port\s+(\d+)',
            r'allow\s+port\s+(\d+)',
            r'configure\s+firewall.*port\s+(\d+)',
            r'enable\s+port\s+(\d+)',
        ],
        'create_user': [
            r'create\s+user\s+(\w+)',
            r'add\s+user\s+(\w+)',
            r'setup\s+account\s+for\s+(\w+)',
            r'new\s+user\s+(\w+)',
        ],
        'deploy_docker': [
            r'deploy\s+(\w+)\s+container',
            r'run\s+(\w+)\s+in\s+docker',
            r'start\s+(\w+)\s+docker',
            r'launch\s+(\w+)\s+container',
        ],
        'restart_service': [
            r'restart\s+(\w+)',
            r'reload\s+(\w+)',
            r'bounce\s+(\w+)\s+service',
            r'reboot\s+(\w+)\s+service',
        ],
        'update_config': [
            r'update\s+config(?:uration)?\s+(.+)',
            r'modify\s+(.+)\s+config',
            r'change\s+(.+)\s+setting',
        ],
    }
    
    def parse(self, user_prompt: str) -> Dict:
        """Parse user prompt and extract intent + OS info"""
        prompt_lower = user_prompt.lower().strip()
        
        os_type = self._detect_os(prompt_lower)
        target_hosts = self._get_target_hosts(os_type)
        
        for intent, patterns in self.INTENT_PATTERNS.items():
            for pattern in patterns:
                match = re.search(pattern, prompt_lower)
                if match:
                    params = self._extract_parameters(
                        user_prompt, intent, match, os_type, target_hosts
                    )
                    return {
                        'intent': intent,
                        'template': f'{intent}.yml',
                        'params': params,
                        'confidence': 'high',
                        'source': 'template'
                    }
        
        return {
            'intent': 'unknown',
            'template': None,
            'params': {'os_type': os_type, 'target_hosts': target_hosts},
            'confidence': 'none',
            'source': 'llm_required'
        }
    
    def _detect_os(self, prompt: str) -> str:
        """Detect OS type from prompt"""
        for os_keyword in self.OS_KEYWORDS.keys():
            if os_keyword in prompt:
                return os_keyword
        return 'all'
    
    def _get_target_hosts(self, os_type: str) -> str:
        """Get target hosts based on OS - always returns 'all' for Concert compatibility"""
        # Always return 'all' - Ansible's built-in group that includes all inventory hosts
        # This matches the working setup where playbooks use 'hosts: all'
        return 'all'
    
    def _extract_parameters(self, prompt: str, intent: str, match: re.Match, 
                           os_type: str, target_hosts: str) -> Dict:
        """Extract specific parameters based on intent"""
        params = {'os_type': os_type, 'target_hosts': target_hosts}
        
        if intent == 'install_package':
            params['package_name'] = match.group(1)
            
        elif intent == 'configure_firewall':
            params['port'] = match.group(1)
            
        elif intent == 'create_user':
            params['username'] = match.group(1)
            
        elif intent == 'deploy_docker':
            container_name = match.group(1)
            params['container_name'] = container_name
            params['image_name'] = self._guess_image_name(container_name)
            params['port'] = self._guess_port(container_name)
            
        elif intent == 'restart_service':
            params['service_name'] = match.group(1)
            params['port'] = self._guess_service_port(match.group(1))
            
        elif intent == 'update_config':
            params['config_file'] = match.group(1)
            params['search_pattern'] = ''
            params['replace_line'] = ''
        
        return params
    
    def _guess_image_name(self, container_name: str) -> str:
        """Guess Docker image name"""
        common_images = {
            'nginx': 'nginx:latest',
            'apache': 'httpd:latest',
            'mysql': 'mysql:latest',
            'postgres': 'postgres:latest',
            'redis': 'redis:latest',
            'mongodb': 'mongo:latest',
        }
        return common_images.get(container_name, f'{container_name}:latest')
    
    def _guess_port(self, container_name: str) -> str:
        """Guess port from container name"""
        common_ports = {
            'nginx': '80',
            'apache': '80',
            'mysql': '3306',
            'postgres': '5432',
            'redis': '6379',
            'mongodb': '27017',
        }
        return common_ports.get(container_name, '8080')
    
    def _guess_service_port(self, service_name: str) -> Optional[str]:
        """Guess service port"""
        common_ports = {
            'nginx': '80',
            'apache': '80',
            'apache2': '80',
            'mysql': '3306',
            'postgresql': '5432',
            'redis': '6379',
            'ssh': '22',
        }
        return common_ports.get(service_name)

if __name__ == '__main__':
    parser = IntentParser()
    
    test_prompts = [
        "Install nginx on Ubuntu",
        "Open port 8080 on RHEL",
        "Create user john on CentOS",
        "Deploy redis container on Fedora",
        "Restart apache service",
        "Setup HAProxy load balancer",
    ]
    
    print("Testing Upgraded Intent Parser:\n")
    for prompt in test_prompts:
        result = parser.parse(prompt)
        print(f"Prompt: {prompt}")
        print(f"  Intent: {result['intent']}")
        print(f"  Source: {result['source']}")
        print()