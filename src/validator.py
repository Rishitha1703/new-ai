"""
Validator: Checks playbook syntax
File: /Users/khirsagarrishitha/Desktop/concert-agent/src/validator.py
"""

import subprocess
import os

class PlaybookValidator:
    """Validate Ansible playbooks"""
    
    def validate(self, playbook_path):
        """
        Validate playbook syntax using ansible-playbook command
        
        Args:
            playbook_path: Path to playbook file
            
        Returns:
            Dictionary with validation result
        """
        # Check if file exists
        if not os.path.exists(playbook_path):
            return {
                'valid': False,
                'error': 'File not found',
                'message': f'Playbook not found: {playbook_path}'
            }
        
        try:
            # Run: ansible-playbook --syntax-check <playbook_path>
            # This checks if the YAML syntax is correct
            result = subprocess.run(
                ['ansible-playbook', '--syntax-check', playbook_path],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            # Check if command succeeded (returncode 0 = success)
            if result.returncode == 0:
                return {
                    'valid': True,
                    'message': '✓ Playbook syntax is valid!'
                }
            else:
                return {
                    'valid': False,
                    'error': result.stderr,
                    'message': '✗ Syntax errors found'
                }
        
        except Exception as e:
            return {
                'valid': False,
                'error': str(e),
                'message': '✗ Validation failed'
            }

# Test code
if __name__ == '__main__':
    validator = PlaybookValidator()
    
    # Test with: /Users/khirsagarrishitha/Desktop/concert-agent/output/test_playbook.yml
    result = validator.validate('output/test_playbook.yml')
    
    print(f"Valid: {result['valid']}")
    print(f"Message: {result['message']}")