"""
Template Generator: Fills in playbook templates
File: /Users/khirsagarrishitha/Desktop/concert-agent/src/template_generator.py
"""

import os

class TemplateGenerator:
    """Generate playbooks from templates"""
    
    def __init__(self):
        # Path to templates folder
        self.templates_dir = 'templates'
    
    def generate(self, template_name, params):
        """Fill in template with parameters"""
        # Build full path: /Users/khirsagarrishitha/Desktop/concert-agent/templates/install_package.yml
        template_path = os.path.join(self.templates_dir, template_name)
        
        if not os.path.exists(template_path):
            print(f"❌ Template not found: {template_path}")
            return None
        
        # Read template file
        with open(template_path, 'r') as file:
            template_content = file.read()
        
        # Replace placeholders like {{package_name}} with actual values
        result = template_content
        for key, value in params.items():
            placeholder = f'{{{{{key}}}}}'
            result = result.replace(placeholder, str(value))
        
        return result
    
    def save_playbook(self, content, output_path):
        """Save generated playbook to file"""
        # Create output directory if it doesn't exist
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # Write content to file
        with open(output_path, 'w') as file:
            file.write(content)
        
        print(f"✓ Saved: {output_path}")
        return output_path

# Test code
if __name__ == '__main__':
    generator = TemplateGenerator()
    
    # Test parameters
    params = {
        'package_name': 'nginx',
        'target_hosts': 'debian_servers',
        'os_type': 'ubuntu'
    }
    
    # Generate playbook
    playbook = generator.generate('install_package.yml', params)
    if playbook:
        print("\n📄 Generated Playbook (first 500 chars):")
        print(playbook[:500] + "...")
        
        # Save to: /Users/khirsagarrishitha/Desktop/concert-agent/output/test_playbook.yml
        generator.save_playbook(playbook, 'output/test_playbook.yml')