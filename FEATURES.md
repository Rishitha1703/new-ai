# Concert AI Agent - Enhanced Features Documentation

## 🚀 Version 3.0 - Production-Ready Enhanced System

This enhanced version includes all the production-ready features you requested:

### ✨ New Features

#### 1. **Playbook Existence Checking**
- **Before generating a new playbook**, the system checks if a similar one already exists
- Shows matching playbooks with:
  - Creation/modification dates
  - Match score (how well it matches your request)
  - File path
- **Interactive options**:
  - Use existing playbook
  - View playbook content before deciding
  - Create new playbook anyway

#### 2. **Interactive Credential Management**
- **Git Credentials**:
  - Remote repository URL
  - Branch name
  - Authentication (username/token)
  - Push mode (immediate/manual/scheduled)
  - Commit message templates
  
- **IBM Concert API**:
  - API URL
  - API Key (securely hidden input)
  - Workflow name
  - Simulation mode toggle
  
- **LLM Provider**:
  - Ollama (local, free)
  - OpenAI (requires API key)
  - Anthropic (requires API key)
  - Model selection
  - Temperature and token settings

#### 3. **Interactive Inventory Generation**
- **Complete inventory creation wizard** (INI format):
  - Host configuration with all required details
  - IP address/hostname
  - SSH user
  - SSH private key file path
  - SSH port (optional)
  - Sudo/become settings
  - Additional parameters support
  
- **Inventory format**:
  ```ini
  [hosts]
  Server1 ansible_host=9.30.44.81 ansible_user=netcool ansible_ssh_private_key_file=~/.ssh/ai-agent ansible_become=yes
  ```
  
- **Inventory management**:
  - List all inventories
  - View inventory contents
  - Use existing or create new

#### 4. **Interactive Parameter Collection**
- If parameters are missing from your request, the system asks for them
- Collects all required details for each playbook type:
  - Package names
  - Port numbers and protocols
  - Usernames and groups
  - Container names and images
  - Service names
  - Target hosts

#### 5. **Enhanced Git Integration**
- Checks if Git is configured before committing
- Offers to set up Git credentials on-the-fly
- Supports multiple push modes:
  - **Immediate**: Push after each commit
  - **Manual**: Push only when you trigger it
  - **Scheduled**: Push at regular intervals
- Secure credential storage in config

#### 6. **Production-Ready Workflow**
1. Parse user request
2. Check for existing playbooks
3. Collect missing parameters interactively
4. Generate playbook (template or LLM)
5. Validate playbook syntax
6. Commit to Git (with credential check)
7. Trigger Concert workflow (with credential check)
8. Display comprehensive summary

---

## 📋 Usage Guide

### Quick Start

#### Option 1: Interactive Mode (Recommended)
```bash
./run_enhanced.sh
```

This starts the interactive CLI where you can:
- Type natural language requests
- Use commands like `setup`, `inventory`, `status`, `logs`
- Get guided through all configurations

#### Option 2: Command Line Mode
```bash
./run_enhanced.sh "Install MySQL server, start service, and enable it on boot"
```

### First-Time Setup

When you run the enhanced version for the first time:

1. **Configure Credentials** (type `setup` in interactive mode):
   ```
   Your request: setup
   ```
   
   This will guide you through:
   - Git configuration (local + remote)
   - IBM Concert API setup
   - LLM provider selection

2. **Create Inventory** (type `inventory` in interactive mode):
   ```
   Your request: inventory
   ```
   
   Then select option 1 to create a new inventory with all host details.

### Example Workflow

```bash
# Start the enhanced agent
./run_enhanced.sh

# First time? Set up credentials
Your request: setup

# Create inventory
Your request: inventory

# Now make your request
Your request: Install MySQL server, start service, and enable it on boot

# The system will:
# 1. Check if similar playbook exists
# 2. Ask if you want to use existing or create new
# 3. Collect any missing parameters
# 4. Generate/validate playbook
# 5. Commit to Git (asks for credentials if needed)
# 6. Trigger Concert workflow (asks for credentials if needed)
```

---

## 🎯 Available Commands

### In Interactive Mode:

| Command | Description |
|---------|-------------|
| `setup` | Configure all credentials (Git, Concert, LLM) |
| `inventory` | Manage Ansible inventories |
| `status` | Show system status and configuration |
| `logs` | Display recent logs |
| `exit` | Quit the application |

### Natural Language Requests:

Just type what you want to do:
- "Install MySQL server, start service, and enable it on boot"
- "Open port 8080 on RHEL"
- "Create user john with sudo access"
- "Deploy nginx container on port 80"
- "Restart apache service"

---

## 🔧 Configuration Files

### Main Config: `config/config.yml`
All credentials and settings are stored here:
- Git configuration (remote URL, branch, push mode)
- Concert API settings
- LLM provider settings
- Hybrid mode settings

### Inventory: `inventory/hosts.yml`
Your Ansible inventory with all host details:
- Groups and hosts
- Connection settings
- Authentication details
- Custom variables

---

## 📦 New Modules

### 1. `playbook_checker.py`
- Finds similar existing playbooks
- Calculates match scores
- Displays options to user
- Handles playbook reuse

### 2. `credential_manager.py`
- Interactive credential collection
- Secure password/token input
- Configuration file management
- Supports Git, Concert, and LLM providers

### 3. `inventory_manager.py`
- Interactive inventory creation
- Group and host management
- Connection configuration
- Variable collection

### 4. `main_enhanced.py`
- Enhanced main application
- Integrates all new features
- Production-ready workflow
- Comprehensive error handling

---

## 🔐 Security Features

1. **Hidden Password Input**: Uses `getpass` for secure credential entry
2. **Config File Storage**: Credentials stored in YAML (add to .gitignore)
3. **Git URL Encoding**: Credentials embedded in Git URLs for authentication
4. **No Hardcoded Secrets**: All sensitive data collected interactively

---

## 🎨 User Experience Improvements

1. **Clear Progress Indicators**: Step-by-step progress display
2. **Interactive Prompts**: Guided questions for all inputs
3. **Smart Defaults**: Sensible defaults for most settings
4. **Validation**: Input validation at each step
5. **Error Recovery**: Graceful error handling with recovery options
6. **Comprehensive Summaries**: Detailed results after each operation

---

## 🚦 Comparison: Old vs Enhanced

| Feature | Old Version | Enhanced Version |
|---------|-------------|------------------|
| Playbook Check | ❌ No | ✅ Yes, with reuse option |
| Credential Setup | ❌ Manual config file | ✅ Interactive wizard |
| Inventory | ❌ Manual creation | ✅ Interactive generator |
| Parameter Collection | ❌ Must be in request | ✅ Asks if missing |
| Git Setup | ❌ Pre-configured only | ✅ On-demand setup |
| Concert Setup | ❌ Pre-configured only | ✅ On-demand setup |
| Error Handling | ⚠️ Basic | ✅ Comprehensive |
| User Guidance | ⚠️ Minimal | ✅ Step-by-step |

---

## 📝 Example Sessions

### Session 1: First-Time User
```
./run_enhanced.sh

Your request: setup
[Guided through Git, Concert, LLM setup]

Your request: inventory
[Creates inventory with host details]

Your request: Install nginx
[Checks existing playbooks, generates new one, commits to Git]
```

### Session 2: Experienced User
```
./run_enhanced.sh "Deploy redis container"

Step 1: Analyzing request...
✓ Intent: deploy_docker
✓ Source: template

Step 2: Checking for existing playbooks...
📋 Found 1 existing playbook(s):
1. deploy_docker_all_20260215_143022.yml
   Match Score: 80%

What would you like to do?
   1. Use existing playbook
   2. Create new playbook anyway
   
Your choice: 1
✓ Using existing playbook
```

---

## 🛠️ Troubleshooting

### Issue: "Import could not be resolved"
**Solution**: The new modules are in the `src/` directory. Python will find them at runtime.

### Issue: Git push fails
**Solution**: 
1. Run `setup` command
2. Configure Git with valid credentials
3. Use Personal Access Token for GitHub (not password)

### Issue: No inventory found
**Solution**:
1. Type `inventory` in interactive mode
2. Select option 1 to create new inventory
3. Follow the wizard to add hosts

### Issue: Ollama not found
**Solution**: 
- Install Ollama: `brew install ollama` (macOS)
- Pull model: `ollama pull codellama:7b`
- Or use OpenAI/Anthropic instead

---

## 🎯 Best Practices

1. **Always run `setup` first** to configure credentials
2. **Create inventory before execution** to have hosts ready
3. **Use existing playbooks** when possible to save time
4. **Review playbooks** before execution in production
5. **Keep credentials secure** - add config.yml to .gitignore
6. **Use SSH keys** instead of passwords for better security
7. **Test in simulation mode** before production Concert runs

---

## 📞 Support

For issues or questions:
1. Check the logs: Type `logs` in interactive mode
2. Review configuration: Type `status` in interactive mode
3. Reconfigure: Type `setup` to reset credentials

---

## 🎉 Summary

The enhanced version is **production-ready** with:
- ✅ Playbook existence checking
- ✅ Interactive credential collection
- ✅ Interactive inventory generation
- ✅ Complete parameter collection
- ✅ On-demand configuration
- ✅ Comprehensive error handling
- ✅ User-friendly interface
- ✅ Secure credential management

**No more demo files or manual configuration needed!**