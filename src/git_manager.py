"""
Git Manager: Production-Ready Hybrid Git Strategy
Handles both local commits and remote pushes
"""

import os
import subprocess
import time
from datetime import datetime
from typing import Dict, Optional
from threading import Thread, Lock

class GitManager:
    """Production Git Manager with Hybrid Strategy"""
    
    def __init__(self, repo_path: str = 'output', config: dict = None):
        self.repo_path = repo_path
        self.config = config or {}
        self.git_config = self.config.get('git', {})
        
        # Local Git settings
        self.enabled = self.git_config.get('enabled', True)
        self.auto_commit = self.git_config.get('auto_commit', True)
        
        # Remote Git settings
        self.remote_enabled = self.git_config.get('remote_enabled', False)
        self.remote_push_mode = self.git_config.get('remote_push_mode', 'manual')
        self.remote_url = self.git_config.get('remote_url', '')
        self.remote_branch = self.git_config.get('branch', 'main')
        self.push_interval = self.git_config.get('push_interval', 3600)
        
        # State
        self.pending_pushes = []
        self.last_push_time = 0
        self.push_lock = Lock()
        
        if self.enabled:
            self._ensure_git_repo()
            if self.remote_enabled and self.remote_url:
                self._setup_remote()
            if self.remote_push_mode == 'scheduled':
                self._start_push_scheduler()
    
    def _ensure_git_repo(self):
        """Initialize Git repo if it doesn't exist"""
        git_dir = os.path.join(self.repo_path, '.git')
        if not os.path.exists(git_dir):
            try:
                os.makedirs(self.repo_path, exist_ok=True)
                subprocess.run(
                    ['git', 'init'], 
                    cwd=self.repo_path, 
                    check=True,
                    capture_output=True
                )
                
                # Configure Git user (if not set globally)
                self._configure_git_user()
                
                # Create .gitignore
                gitignore_path = os.path.join(self.repo_path, '.gitignore')
                with open(gitignore_path, 'w') as f:
                    f.write("# Ignore temporary files\n*.tmp\n*.swp\n.DS_Store\n")
                
                print(f"✓ Initialized Git repository: {self.repo_path}")
            except Exception as e:
                print(f"⚠️  Could not initialize Git: {e}")
                self.enabled = False
    
    def _configure_git_user(self):
        """Configure Git user if not set"""
        try:
            # Check if user is configured
            result = subprocess.run(
                ['git', 'config', 'user.name'],
                cwd=self.repo_path,
                capture_output=True,
                text=True
            )
            
            if result.returncode != 0:
                # Set default user
                subprocess.run(
                    ['git', 'config', 'user.name', 'Concert AI Agent'],
                    cwd=self.repo_path,
                    check=True
                )
                subprocess.run(
                    ['git', 'config', 'user.email', 'concert-agent@ibm.com'],
                    cwd=self.repo_path,
                    check=True
                )
                print("✓ Configured Git user")
        except Exception:
            pass
    
    def _setup_remote(self):
        """Setup remote repository"""
        try:
            # Check if remote exists
            result = subprocess.run(
                ['git', 'remote', 'get-url', 'origin'],
                cwd=self.repo_path,
                capture_output=True,
                text=True
            )
            
            if result.returncode != 0:
                # Add remote
                subprocess.run(
                    ['git', 'remote', 'add', 'origin', self.remote_url],
                    cwd=self.repo_path,
                    check=True,
                    capture_output=True
                )
                print(f"✓ Added remote: {self.remote_url}")
            else:
                # Update remote URL if different
                current_url = result.stdout.strip()
                if current_url != self.remote_url:
                    subprocess.run(
                        ['git', 'remote', 'set-url', 'origin', self.remote_url],
                        cwd=self.repo_path,
                        check=True
                    )
                    print(f"✓ Updated remote: {self.remote_url}")
        except Exception as e:
            print(f"⚠️  Could not setup remote: {e}")
            self.remote_enabled = False
    
    def commit_playbook(self, playbook_path: str, message: Optional[str] = None) -> Dict:
        """
        Commit playbook to local Git
        
        Args:
            playbook_path: Path to playbook file
            message: Commit message (auto-generated if None)
            
        Returns:
            Dictionary with commit result
        """
        if not self.enabled or not self.auto_commit:
            return {
                'success': False,
                'message': 'Git auto-commit is disabled',
                'skipped': True
            }
        
        try:
            # Get relative path
            rel_path = os.path.relpath(playbook_path, self.repo_path)
            
            # Add file
            subprocess.run(
                ['git', 'add', rel_path],
                cwd=self.repo_path,
                check=True,
                capture_output=True
            )
            
            # Generate commit message
            if message is None:
                timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                filename = os.path.basename(playbook_path)
                template = self.git_config.get('commit_message_template', 
                                              'Add playbook: {filename} - {timestamp}')
                message = template.format(filename=filename, timestamp=timestamp)
            
            # Commit
            result = subprocess.run(
                ['git', 'commit', '-m', message],
                cwd=self.repo_path,
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                # Get commit hash
                hash_result = subprocess.run(
                    ['git', 'rev-parse', '--short', 'HEAD'],
                    cwd=self.repo_path,
                    capture_output=True,
                    text=True
                )
                commit_hash = hash_result.stdout.strip()
                
                # Add to pending pushes
                if self.remote_enabled:
                    with self.push_lock:
                        self.pending_pushes.append(commit_hash)
                    
                    # Push immediately if mode is "immediate"
                    if self.remote_push_mode == 'immediate':
                        self._push_to_remote()
                
                return {
                    'success': True,
                    'message': 'Playbook committed to local Git',
                    'commit_message': message,
                    'commit_hash': commit_hash,
                    'pending_push': self.remote_enabled
                }
            else:
                return {
                    'success': False,
                    'error': result.stderr,
                    'message': 'Git commit failed'
                }
                
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'message': 'Git operation failed'
            }
    
    def _push_to_remote(self) -> Dict:
        """Push commits to remote repository"""
        if not self.remote_enabled or not self.remote_url:
            return {'success': False, 'message': 'Remote push not configured'}
        
        try:
            with self.push_lock:
                if not self.pending_pushes:
                    return {'success': True, 'message': 'No pending commits to push'}
                
                # Push to remote
                result = subprocess.run(
                    ['git', 'push', 'origin', self.remote_branch],
                    cwd=self.repo_path,
                    capture_output=True,
                    text=True,
                    timeout=30
                )
                
                if result.returncode == 0:
                    pushed_count = len(self.pending_pushes)
                    self.pending_pushes = []
                    self.last_push_time = time.time()
                    
                    return {
                        'success': True,
                        'message': f'Pushed {pushed_count} commits to remote',
                        'pushed_count': pushed_count
                    }
                else:
                    return {
                        'success': False,
                        'error': result.stderr,
                        'message': 'Remote push failed'
                    }
        except subprocess.TimeoutExpired:
            return {
                'success': False,
                'error': 'Push timeout',
                'message': 'Remote push timed out'
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'message': 'Remote push failed'
            }
    
    def _start_push_scheduler(self):
        """Start background thread for scheduled pushes"""
        def push_scheduler():
            while True:
                time.sleep(self.push_interval)
                if self.pending_pushes:
                    print("\n⏰ Scheduled push to remote...")
                    result = self._push_to_remote()
                    if result['success']:
                        print(f"✓ {result['message']}")
                    else:
                        print(f"⚠️  {result['message']}")
        
        thread = Thread(target=push_scheduler, daemon=True)
        thread.start()
    
    def manual_push(self) -> Dict:
        """Manually trigger push to remote"""
        print("\n📤 Manually pushing to remote...")
        return self._push_to_remote()
    
    def push_with_credentials(self, remote_url: str = None, username: str = None, token: str = None) -> Dict:
        """
        Push to remote with credentials
        
        Args:
            remote_url: Git remote URL (if None, asks user)
            username: Git username (if None, asks user)
            token: Git token/password (if None, asks user)
            
        Returns:
            Dictionary with push result
        """
        print("\n📤 Pushing to Git remote...")
        
        # Ask for credentials if not provided
        if not remote_url:
            print("\n🔐 Git Remote Configuration")
            remote_url = input("  Remote URL (e.g., https://github.com/user/repo.git): ").strip()
            if not remote_url:
                return {'success': False, 'message': 'No remote URL provided'}
        
        if not username:
            username = input("  Username: ").strip()
            if not username:
                return {'success': False, 'message': 'No username provided'}
        
        if not token:
            import getpass
            token = getpass.getpass("  Password/Token: ").strip()
            if not token:
                return {'success': False, 'message': 'No password/token provided'}
        
        try:
            # Setup remote if not exists
            result = subprocess.run(
                ['git', 'remote', 'get-url', 'origin'],
                cwd=self.repo_path,
                capture_output=True,
                text=True
            )
            
            if result.returncode != 0:
                # Add remote
                subprocess.run(
                    ['git', 'remote', 'add', 'origin', remote_url],
                    cwd=self.repo_path,
                    check=True,
                    capture_output=True
                )
                print(f"  ✓ Added remote: {remote_url}")
            else:
                # Update remote URL
                subprocess.run(
                    ['git', 'remote', 'set-url', 'origin', remote_url],
                    cwd=self.repo_path,
                    check=True,
                    capture_output=True
                )
                print(f"  ✓ Updated remote: {remote_url}")
            
            # Create authenticated URL
            if remote_url.startswith('https://'):
                # Extract domain and path
                url_parts = remote_url.replace('https://', '').split('/', 1)
                if len(url_parts) == 2:
                    domain, path = url_parts
                    auth_url = f"https://{username}:{token}@{domain}/{path}"
                else:
                    auth_url = remote_url
            else:
                auth_url = remote_url
            
            # Push to remote with credentials
            result = subprocess.run(
                ['git', 'push', auth_url, self.remote_branch],
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                timeout=60
            )
            
            if result.returncode == 0:
                print(f"✓ Pushed to remote: {remote_url}")
                return {
                    'success': True,
                    'message': f'Successfully pushed to {remote_url}',
                    'remote_url': remote_url
                }
            else:
                error_msg = result.stderr.strip()
                # Hide credentials in error message
                if token in error_msg:
                    error_msg = error_msg.replace(token, '***')
                return {
                    'success': False,
                    'error': error_msg,
                    'message': 'Push failed - check credentials and permissions'
                }
                
        except subprocess.TimeoutExpired:
            return {
                'success': False,
                'error': 'Push timeout',
                'message': 'Push timed out - check network connection'
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'message': 'Push failed'
            }
    
    def get_commit_history(self, limit: int = 10) -> list:
        """Get recent commit history"""
        if not self.enabled:
            return []
        
        try:
            result = subprocess.run(
                ['git', 'log', f'-{limit}', '--oneline'],
                cwd=self.repo_path,
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                commits = result.stdout.strip().split('\n')
                return [c for c in commits if c]
            return []
            
        except Exception:
            return []
    
    def get_status(self) -> Dict:
        """Get comprehensive Git status"""
        if not self.enabled:
            return {'enabled': False}
        
        try:
            # Get branch name
            branch_result = subprocess.run(
                ['git', 'rev-parse', '--abbrev-ref', 'HEAD'],
                cwd=self.repo_path,
                capture_output=True,
                text=True
            )
            branch = branch_result.stdout.strip()
            
            # Get commit count
            count_result = subprocess.run(
                ['git', 'rev-list', '--count', 'HEAD'],
                cwd=self.repo_path,
                capture_output=True,
                text=True
            )
            commit_count = count_result.stdout.strip()
            
            status = {
                'enabled': True,
                'branch': branch,
                'commit_count': commit_count,
                'repo_path': self.repo_path,
                'remote_enabled': self.remote_enabled,
                'remote_url': self.remote_url if self.remote_enabled else 'N/A',
                'push_mode': self.remote_push_mode if self.remote_enabled else 'N/A',
                'pending_pushes': len(self.pending_pushes) if self.remote_enabled else 0
            }
            
            return status
        except Exception as e:
            return {
                'enabled': True,
                'error': str(e)
            }
    
    def shutdown(self):
        """Cleanup on shutdown"""
        if self.git_config.get('push_on_shutdown', True) and self.pending_pushes:
            print("\n📤 Pushing pending commits before shutdown...")
            result = self._push_to_remote()
            if result['success']:
                print(f"✓ {result['message']}")

# Test
if __name__ == '__main__':
    # Test with local-only config
    config = {
        'git': {
            'enabled': True,
            'auto_commit': True,
            'remote_enabled': False
        }
    }
    
    git_mgr = GitManager(config=config)
    
    print("\n📊 Git Manager Status:")
    status = git_mgr.get_status()
    for key, value in status.items():
        print(f"  {key}: {value}")
    
    print("\n📜 Recent commits:")
    history = git_mgr.get_commit_history(5)
    for commit in history:
        print(f"  {commit}")