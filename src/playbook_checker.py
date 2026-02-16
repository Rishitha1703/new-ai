"""
Playbook Checker: Check if similar playbooks already exist
"""

import os
import yaml
import re
from typing import Dict, List, Optional
from datetime import datetime

class PlaybookChecker:
    """Check for existing playbooks before generating new ones"""
    
    def __init__(self, output_dir: str = 'output'):
        self.output_dir = output_dir
    
    def find_similar_playbooks(self, intent: str, params: Dict) -> List[Dict]:
        """
        Find existing playbooks that match the intent and parameters
        
        Args:
            intent: The intent type (e.g., 'install_package')
            params: Parameters like package_name, port, etc.
            
        Returns:
            List of matching playbooks with metadata
        """
        if not os.path.exists(self.output_dir):
            return []
        
        matching_playbooks = []
        
        # Get all YAML files in output directory
        for filename in os.listdir(self.output_dir):
            if not filename.endswith('.yml') and not filename.endswith('.yaml'):
                continue
            
            filepath = os.path.join(self.output_dir, filename)
            
            # Check if filename matches intent pattern
            if not filename.startswith(intent):
                continue
            
            try:
                # Read and parse the playbook
                with open(filepath, 'r') as f:
                    playbook_content = f.read()
                    playbook_data = yaml.safe_load(playbook_content)
                
                # Check if parameters match
                if self._matches_parameters(playbook_data, params):
                    # Get file metadata
                    stat = os.stat(filepath)
                    matching_playbooks.append({
                        'filename': filename,
                        'filepath': filepath,
                        'created': datetime.fromtimestamp(stat.st_ctime),
                        'modified': datetime.fromtimestamp(stat.st_mtime),
                        'size': stat.st_size,
                        'content': playbook_content,
                        'match_score': self._calculate_match_score(playbook_data, params)
                    })
            except Exception as e:
                # Skip files that can't be parsed
                continue
        
        # Sort by match score (highest first) and then by modification time (newest first)
        matching_playbooks.sort(key=lambda x: (x['match_score'], x['modified']), reverse=True)
        
        return matching_playbooks
    
    def _matches_parameters(self, playbook_data: any, params: Dict) -> bool:
        """Check if playbook matches the given parameters"""
        if not playbook_data or not isinstance(playbook_data, list):
            return False
        
        playbook_str = str(playbook_data).lower()
        
        # Check for key parameters
        for key, value in params.items():
            if key in ['os_type', 'target_hosts']:
                continue  # Skip meta parameters
            
            if value and str(value).lower() not in playbook_str:
                return False
        
        return True
    
    def _calculate_match_score(self, playbook_data: any, params: Dict) -> float:
        """Calculate how well the playbook matches the parameters (0-1)"""
        if not playbook_data:
            return 0.0
        
        playbook_str = str(playbook_data).lower()
        matches = 0
        total = 0
        
        for key, value in params.items():
            if key in ['os_type', 'target_hosts']:
                continue
            
            total += 1
            if value and str(value).lower() in playbook_str:
                matches += 1
        
        return matches / total if total > 0 else 0.0
    
    def display_matches(self, matches: List[Dict]) -> None:
        """Display matching playbooks to the user"""
        if not matches:
            print("\n✓ No existing playbooks found - will create new one")
            return
        
        print(f"\n📋 Found {len(matches)} existing playbook(s):")
        print("="*70)
        
        for i, match in enumerate(matches, 1):
            print(f"\n{i}. {match['filename']}")
            print(f"   Created: {match['created'].strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"   Modified: {match['modified'].strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"   Match Score: {match['match_score']*100:.0f}%")
            print(f"   Path: {match['filepath']}")
        
        print("\n" + "="*70)
    
    def prompt_user_choice(self, matches: List[Dict]) -> Optional[str]:
        """
        Ask user if they want to use an existing playbook or create new one
        
        Returns:
            Path to selected playbook or None to create new
        """
        if not matches:
            return None
        
        print("\n🤔 What would you like to do?")
        print("   1. Use existing playbook (select number)")
        print("   2. Create new playbook anyway (press 'n')")
        print("   3. View playbook content first (press 'v')")
        
        while True:
            choice = input("\nYour choice: ").strip().lower()
            
            if choice == 'n':
                return None
            
            if choice == 'v':
                self._view_playbooks(matches)
                continue
            
            try:
                index = int(choice) - 1
                if 0 <= index < len(matches):
                    selected = matches[index]
                    print(f"\n✓ Using existing playbook: {selected['filename']}")
                    return selected['filepath']
                else:
                    print(f"❌ Invalid choice. Please enter 1-{len(matches)}, 'v', or 'n'")
            except ValueError:
                print(f"❌ Invalid input. Please enter a number (1-{len(matches)}), 'v', or 'n'")
    
    def _view_playbooks(self, matches: List[Dict]) -> None:
        """Display content of playbooks for user review"""
        print("\n" + "="*70)
        print("📄 PLAYBOOK CONTENTS")
        print("="*70)
        
        for i, match in enumerate(matches, 1):
            print(f"\n{i}. {match['filename']}")
            print("-"*70)
            print(match['content'])
            print("-"*70)
        
        print("\n" + "="*70)


# Test
if __name__ == '__main__':
    checker = PlaybookChecker()
    
    # Test finding install_package playbooks
    test_params = {
        'package_name': 'mysql',
        'target_hosts': 'all',
        'os_type': 'all'
    }
    
    print("Testing Playbook Checker...")
    matches = checker.find_similar_playbooks('install_package', test_params)
    checker.display_matches(matches)
    
    if matches:
        choice = checker.prompt_user_choice(matches)
        if choice:
            print(f"\n✓ Selected: {choice}")
        else:
            print("\n✓ Will create new playbook")

# Made with Bob
