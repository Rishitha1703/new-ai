# 🚀 Concert AI Agent - Enhanced Production System v3.0

## ⚡ Quick Start

```bash
cd /Users/khirsagarrishitha/Desktop/concert-ai-agent
source venv/bin/activate
python3 src/main.py "Install MySQL server, start service, and enable it on boot"
```

## 🎯 What's New in v3.0

The enhanced version now includes:

### ✅ **Playbook Existence Checking**
Before generating a new playbook, the system checks if a similar one already exists and asks if you want to reuse it.

### ✅ **Interactive Credential Collection**
When Git or Concert API credentials are needed, the system asks for them interactively:
- Git remote URL, branch, authentication
- Concert API URL and key
- LLM provider settings

### ✅ **Interactive Inventory Generation**
Creates Ansible inventory in the correct INI format:
```ini
[hosts]
Server1 ansible_host=9.30.44.81 ansible_user=netcool ansible_ssh_private_key_file=~/.ssh/ai-agent ansible_become=yes
```

### ✅ **Interactive Parameter Collection**
If your request is missing parameters, the system asks for them:
- Package names
- Port numbers
- Usernames
- Container details
- Service names

---

## 📋 Usage Examples

### Example 1: First Time Setup

```bash
# Activate virtual environment
source venv/bin/activate

# Run with your request
python3 src/main.py "Install MySQL server, start service, and enable it on boot"
```

**What happens:**
1. ✅ Checks for existing MySQL playbooks
2. ✅ Shows matches and asks if you want to reuse
3. ✅ If creating new, collects any missing parameters
4. ✅ Generates playbook
5. ✅ Validates syntax
6. ✅ Asks for Git credentials if not configured
7. ✅ Commits to Git
8. ✅ Asks for Concert credentials if enabled
9. ✅ Shows comprehensive summary

### Example 2: Interactive Mode

```bash
python3 src/main.py
```

Then use commands:
- `setup` - Configure all credentials
- `inventory` - Create/manage inventory
- `status` - Show system status
- `logs` - View recent logs
- Type your request naturally
- `exit` - Quit

### Example 3: With Existing Playbook

```bash
python3 src/main.py "Install nginx"
```

**Output:**
```
Step 2: Checking for existing playbooks...
📋 Found 3 existing playbook(s):
1. install_package_all_20260216_124857.yml
   Match Score: 100%

What would you like to do?
   1. Use existing playbook
   2. Create new playbook anyway
   3. View playbook content first

Your choice: 1
✓ Using existing playbook
```

---

## 🔧 Configuration Commands

### Setup All Credentials
```bash
python3 src/main.py
# Then type: setup
```

This will guide you through:
1. **Git Configuration**
   - Remote URL: `https://github.com/Rishitha1703/new-ai.git`
   - Branch: `main`
   - Username and token
   - Push mode (immediate/manual/scheduled)

2. **Concert API** (optional)
   - API URL
   - API Key
   - Workflow settings

3. **LLM Provider**
   - Ollama (local, already installed)
   - OpenAI (requires API key)
   - Anthropic (requires API key)

### Create Inventory
```bash
python3 src/main.py
# Then type: inventory
```

Follow the wizard:
```
Host name: Server1
IP address: 9.30.44.81
SSH user: netcool
SSH key path: ~/.ssh/ai-agent
SSH port: (press Enter for 22)
Use sudo? Y
```

**Result:** `inventory/inventory.ini`
```ini
[hosts]
Server1 ansible_host=9.30.44.81 ansible_user=netcool ansible_ssh_private_key_file=~/.ssh/ai-agent ansible_become=yes
```

---

## 📁 File Structure

```
concert-ai-agent/
├── src/
│   ├── main.py                    # Enhanced main application (v3.0)
│   ├── playbook_checker.py        # Check existing playbooks
│   ├── credential_manager.py      # Interactive credential collection
│   ├── inventory_manager.py       # Interactive inventory generation
│   ├── intent_parser.py           # Parse user requests
│   ├── template_generator.py      # Generate from templates
│   ├── llm_generator.py           # Generate with LLM
│   ├── validator.py               # Validate playbooks
│   ├── git_manager.py             # Git operations
│   ├── concert_api.py             # Concert API integration
│   └── logger.py                  # Logging
├── templates/                     # Playbook templates
├── output/                        # Generated playbooks
├── inventory/
│   └── inventory.ini              # Ansible inventory (INI format)
├── config/
│   └── config.yml                 # Configuration file
└── logs/                          # Application logs
```

---

## 🎨 Interactive Features

### 1. Playbook Checking
```
Step 2: Checking for existing playbooks...
📋 Found 5 existing playbook(s):
1. install_package_all_20260216_124857.yml (100% match)
2. install_package_all_20260216_123948.yml (100% match)

What would you like to do?
   1. Use existing playbook (select number)
   2. Create new playbook anyway (press 'n')
   3. View playbook content first (press 'v')

Your choice: _
```

### 2. Credential Collection
```
🔐 GIT CONFIGURATION
Enable Git integration? (Y/n): Y
Enable auto-commit? (Y/n): Y
Enable remote repository? (Y/n): Y
Remote URL: https://github.com/Rishitha1703/new-ai.git
Branch: main
Push mode (1=immediate/2=manual/3=scheduled): 2
Configure credentials? (y/N): y
Username: Rishitha1703
Token: ********
✓ Git configuration saved
```

### 3. Inventory Generation
```
📋 ANSIBLE INVENTORY CREATION
Host name: Server1
IP address: 9.30.44.81
SSH user: netcool
SSH key path: ~/.ssh/ai-agent
SSH port: (default 22)
Use sudo? Y
✓ Host 'Server1' added

Host name: done
✅ INVENTORY CREATED!
```

### 4. Parameter Collection
```
Step 3: Collecting playbook parameters...
⚠️  Some parameters are missing. Let's collect them:
  Package name: mysql-server
  Change target hosts? (current: all) (y/N): n
✓ Parameters collected
```

---

## 🔐 Security

- **Hidden Password Input**: Uses `getpass` for secure credential entry
- **Config File Storage**: Credentials stored in `config/config.yml`
- **SSH Key Authentication**: Supports custom SSH key paths
- **No Hardcoded Secrets**: All sensitive data collected interactively

**Important:** Add `config/config.yml` to `.gitignore` to protect credentials!

---

## 📊 System Status

Check your configuration anytime:
```bash
python3 src/main.py
# Then type: status
```

**Output:**
```
📊 SYSTEM STATUS
======================================================================

📦 Git:
  Enabled: True
  Branch: main
  Commits: 45
  Remote: True
  Remote URL: https://github.com/Rishitha1703/new-ai.git
  Push Mode: manual

🎭 IBM Concert:
  Enabled: False
  Mode: Simulation

🔧 Hybrid Mode:
  Enabled: True
  Templates: 6 available
  LLM Fallback: True

📋 Inventory:
  Count: 2
```

---

## 🎯 Workflow Comparison

### Old Version (v2.0)
```bash
python3 src/main.py "Install MySQL"
# ❌ No playbook checking
# ❌ No credential prompts
# ❌ No inventory wizard
# ❌ Fails if parameters missing
```

### Enhanced Version (v3.0)
```bash
python3 src/main.py "Install MySQL"
# ✅ Checks existing playbooks
# ✅ Asks for credentials if needed
# ✅ Collects missing parameters
# ✅ Guides through inventory creation
# ✅ Production-ready workflow
```

---

## 💡 Tips

1. **First time?** Run `setup` command to configure everything
2. **Need inventory?** Run `inventory` command to create hosts
3. **Check status** Use `status` command to see configuration
4. **View logs** Use `logs` command to see recent activity
5. **Reuse playbooks** System automatically checks for existing ones

---

## 🚦 Common Scenarios

### Scenario 1: Fresh Installation
```bash
source venv/bin/activate
python3 src/main.py

Your request: setup
# Configure Git, Concert, LLM

Your request: inventory
# Create inventory with hosts

Your request: Install MySQL server
# System generates playbook
```

### Scenario 2: Quick Command
```bash
source venv/bin/activate
python3 src/main.py "Install nginx"
# System checks existing, asks for credentials if needed
```

### Scenario 3: Reusing Playbooks
```bash
python3 src/main.py "Install MySQL"
# Found existing playbook
# Choose: 1=use existing, 2=create new, 3=view first
```

---

## 📞 Support

- **Check logs**: Type `logs` in interactive mode
- **View status**: Type `status` in interactive mode
- **Reconfigure**: Type `setup` to reset credentials
- **Documentation**: See `ENHANCED_FEATURES.md` for details

---

## 🎉 Summary

The enhanced v3.0 system is **production-ready** with:
- ✅ Playbook existence checking
- ✅ Interactive credential collection
- ✅ Interactive inventory generation (INI format)
- ✅ Complete parameter collection
- ✅ On-demand configuration
- ✅ User-friendly interface
- ✅ Comprehensive error handling

**No more manual configuration or demo files needed!**

---

## 🚀 Get Started Now

```bash
cd /Users/khirsagarrishitha/Desktop/concert-ai-agent
source venv/bin/activate
python3 src/main.py "Install MySQL server, start service, and enable it on boot"
```

The system will guide you through everything! 🎯