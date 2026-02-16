# 🚀 Concert AI Agent - Production Guide

## Overview
This is a fully production-ready AI-powered Ansible playbook generation system with intelligent decision-making, interactive parameter collection, and comprehensive automation.

## ✨ Key Features

### 1. **Intelligent Playbook Management**
- **Automatic Playbook Reuse**: System checks existing playbooks before generating new ones
- **Smart Matching**: Uses ≥80% similarity threshold to automatically reuse existing playbooks
- **No User Intervention**: Automatically decides whether to reuse or generate new playbooks

### 2. **Interactive Parameter Collection**
- **OS Type Selection**: Always asks for target operating system
  - Ubuntu/Debian
  - RHEL/CentOS
  - Fedora
  - All (multi-OS playbook)
- **Intent-Specific Parameters**: Collects all required parameters based on task type
- **Target Host Configuration**: Option to specify custom target hosts

### 3. **Production-Ready Inventory Management**
- **INI Format**: Industry-standard Ansible inventory format
- **Complete Host Details**:
  - Hostname
  - Operating System
  - IP Address
  - SSH User
  - SSH Private Key Path
  - SSH Port (optional)
  - Sudo/Become Settings
- **OS Documentation**: Each host entry includes OS information as a comment

### 4. **Hybrid AI Generation**
- **Template-Based**: Fast, guaranteed accurate for common tasks
- **Ollama/LLM-Based**: Flexible, handles custom requirements
- **Automatic Selection**: System chooses the best generation method

### 5. **Git Integration**
- **Automatic Commits**: All playbooks committed to local Git
- **Interactive Push**: Asks for credentials when pushing to remote
- **Version Control**: Full history of all generated playbooks

## 🎯 Usage

### Basic Usage
```bash
cd concert-ai-agent
source venv/bin/activate
python3 src/main.py "Your request here"
```

### Example Requests

#### 1. Install Package
```bash
python3 src/main.py "Install MySQL server, start service, and enable it on boot"
```
**System will ask for:**
- OS type (Ubuntu/RHEL/Fedora/All)
- Package name (if not detected)
- Target hosts (optional)

#### 2. Configure Firewall
```bash
python3 src/main.py "Open port 8080 for web traffic"
```
**System will ask for:**
- OS type
- Port number
- Protocol (tcp/udp)
- Target hosts (optional)

#### 3. Create User
```bash
python3 src/main.py "Create a new user named john with sudo access"
```
**System will ask for:**
- OS type
- Username
- Additional groups (optional)
- Target hosts (optional)

#### 4. Deploy Docker Container
```bash
python3 src/main.py "Deploy nginx container on port 8080"
```
**System will ask for:**
- OS type
- Container name
- Docker image
- Port mapping
- Target hosts (optional)

## 📋 Workflow

### Step 1: Request Analysis
```
✓ Intent: install_package
✓ Source: template
```
System analyzes your request and determines the intent.

### Step 2: Playbook Existence Check
```
🔍 Checking for existing playbooks...
  ✓ Found matching playbook (85% match)
  → Using existing: output/install_package_all_20260216_124857.yml
```
OR
```
🔍 Checking for existing playbooks...
  - No matching playbook found
  → Will generate new playbook
```

### Step 3: Parameter Collection
```
📝 Collecting playbook parameters...

🖥️  Target Operating System:
  1. Ubuntu/Debian
  2. RHEL/CentOS
  3. Fedora
  4. All (multi-OS playbook)
Select OS (1-4, default: 4): 1

📋 Task-specific parameters:
  Package name: mysql-server

✓ Parameters collected
```

### Step 4: Playbook Generation
```
Step 2: Generating playbook...
  → Using template-based generation (fast, guaranteed accurate)
✓ Playbook generated via template
✓ Saved: output/install_package_ubuntu_20260216_130245.yml
```

### Step 5: Validation
```
Step 3: Validating playbook...
✓ Playbook syntax is valid!
```

### Step 6: Git Commit
```
Step 4: Committing to Git...
✓ Playbook committed to local Git
  Commit: a1b2c3d
```

### Step 7: Inventory Check (if needed)
```
📦 Checking inventory...
  - No inventory file found

📝 Would you like to create an inventory file? (Y/n): y

🖥️  Configuring host: Server1

  Operating System:
    1. Ubuntu/Debian
    2. RHEL/CentOS
    3. Fedora
    4. Other
  Select OS (1-4): 1
  ✓ OS: Ubuntu

  IP address or hostname: 192.168.1.100
  SSH user (default: ansible): ubuntu
  
  SSH private key file:
    Examples: ~/.ssh/id_rsa, ~/.ssh/ai-agent, /path/to/key
  SSH key path (default: ~/.ssh/id_rsa): ~/.ssh/my-key
  SSH port (press Enter for default 22): 
  Use sudo/become? (Y/n): y

✓ Inventory created: inventory/inventory.ini
```

## 📁 Generated Files

### Playbook Example
```yaml
---
- name: Install mysql-server on Ubuntu
  hosts: all
  become: yes
  tasks:
    - name: Update apt cache
      apt:
        update_cache: yes
      when: ansible_os_family == "Debian"
    
    - name: Install mysql-server
      apt:
        name: mysql-server
        state: present
      when: ansible_os_family == "Debian"
    
    - name: Start and enable mysql service
      systemd:
        name: mysql
        state: started
        enabled: yes
```

### Inventory Example
```ini
[hosts]
Server1 ansible_host=192.168.1.100 ansible_user=ubuntu ansible_ssh_private_key_file=~/.ssh/my-key ansible_become=yes # OS: Ubuntu
```

## 🔧 Configuration

### config/config.yml
```yaml
ollama:
  enabled: true
  model: "codellama:7b"
  base_url: "http://localhost:11434"

git:
  enabled: true
  auto_commit: true
  auto_push: false  # Set to true for automatic push

concert:
  enabled: false  # Concert API integration disabled
```

## 🎭 Advanced Features

### 1. Multiple Host Inventory
The system supports adding multiple hosts to the inventory:
```
Add another host? (y/N): y
```

### 2. Custom Parameters
For each host, you can add custom Ansible parameters:
```
Add more parameters? (y/N): y
  Parameter: ansible_python_interpreter=/usr/bin/python3
```

### 3. Git Remote Push
When pushing to remote, system will ask for credentials:
```
🔐 Git Credentials Required

  Remote URL: https://github.com/username/repo.git
  Username: your-username
  Password/Token: ********

✓ Pushed to remote: origin/main
```

## 🧪 Testing

### Run All Tests
```bash
./test_system.sh
```

### Test Specific Component
```bash
# Test playbook checker
python3 src/playbook_checker.py

# Test inventory manager
python3 src/inventory_manager.py

# Test LLM generator
python3 src/llm_generator.py
```

## 📊 System Status

### Check Ollama
```bash
curl http://localhost:11434/api/tags
```

### Check Git Status
```bash
cd concert-ai-agent
git status
git log --oneline -5
```

### Check Existing Playbooks
```bash
ls -lh output/
```

## 🔒 Security Best Practices

1. **SSH Keys**: Use dedicated SSH keys for automation
2. **Git Credentials**: Use personal access tokens, not passwords
3. **Inventory Files**: Keep inventory files secure (add to .gitignore if needed)
4. **Sudo Access**: Only enable sudo when necessary

## 🐛 Troubleshooting

### Ollama Not Running
```bash
# Start Ollama
ollama serve

# Verify model is installed
ollama list
```

### Git Push Fails
```bash
# Check remote URL
git remote -v

# Test connection
git fetch origin
```

### Playbook Validation Fails
```bash
# Manually validate
ansible-playbook --syntax-check output/playbook.yml
```

## 📈 Performance

- **Template Generation**: ~1-2 seconds
- **LLM Generation**: ~5-10 seconds (depends on Ollama)
- **Playbook Validation**: <1 second
- **Git Operations**: <1 second

## 🎓 Best Practices

1. **Always specify OS type** for accurate playbook generation
2. **Use descriptive hostnames** in inventory
3. **Test playbooks** in a staging environment first
4. **Keep inventory files** organized by environment
5. **Review generated playbooks** before execution
6. **Commit frequently** to maintain version history

## 📞 Support

For issues or questions:
1. Check existing playbooks in `output/` directory
2. Review logs in terminal output
3. Verify Ollama is running
4. Check Git configuration

## 🚀 Production Deployment

### Prerequisites
- Python 3.8+
- Ollama with codellama:7b model
- Git configured
- SSH access to target hosts

### Setup
```bash
# Clone repository
git clone <your-repo-url>
cd concert-ai-agent

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure
cp config/config.yml.example config/config.yml
# Edit config.yml as needed

# Test
./test_system.sh
```

### Ready to Use!
```bash
python3 src/main.py "Your automation request"
```

---

**Version**: 2.0  
**Last Updated**: 2026-02-16  
**Status**: Production Ready ✅