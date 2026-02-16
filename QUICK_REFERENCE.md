# 🚀 Quick Reference Guide

## Start the System

```bash
cd /Users/khirsagarrishitha/Desktop/concert-ai-agent
source venv/bin/activate
python3 src/main.py "Your request here"
```

## Common Commands

### Install Package
```bash
python3 src/main.py "Install MySQL server and start it"
```
**Asks for:** OS type, package name

### Configure Firewall
```bash
python3 src/main.py "Open port 8080 for web traffic"
```
**Asks for:** OS type, port, protocol

### Create User
```bash
python3 src/main.py "Create user john with sudo access"
```
**Asks for:** OS type, username, groups

### Deploy Docker
```bash
python3 src/main.py "Deploy nginx container on port 80"
```
**Asks for:** OS type, container name, image, ports

### Restart Service
```bash
python3 src/main.py "Restart apache2 service"
```
**Asks for:** OS type, service name

## OS Selection

When prompted, select:
- **1** = Ubuntu/Debian
- **2** = RHEL/CentOS
- **3** = Fedora
- **4** = All (multi-OS)

## Inventory Setup

First time only:
```
📝 Would you like to create an inventory file? (Y/n): y
```

Then provide:
1. **OS type** (1-4)
2. **IP address** (e.g., 192.168.1.100)
3. **SSH user** (e.g., ubuntu)
4. **SSH key path** (e.g., ~/.ssh/my-key)
5. **SSH port** (press Enter for 22)
6. **Use sudo?** (Y/n)

## System Behavior

### Automatic Decisions
- ✅ **Reuses existing playbooks** if ≥80% match
- ✅ **Generates new playbook** if <80% match
- ✅ **Chooses template or LLM** automatically
- ✅ **Commits to Git** automatically

### What You Control
- 🎯 **OS type** (always asks)
- 🎯 **Task parameters** (package name, port, etc.)
- 🎯 **Target hosts** (optional)
- 🎯 **Inventory details** (when creating)
- 🎯 **Git push** (asks for credentials)

## File Locations

```
concert-ai-agent/
├── output/              # Generated playbooks
├── inventory/           # Inventory files
├── config/config.yml    # Configuration
└── src/                 # Source code
```

## Quick Checks

### Check Ollama
```bash
curl http://localhost:11434/api/tags
```

### List Playbooks
```bash
ls -lh output/
```

### View Inventory
```bash
cat inventory/inventory.ini
```

### Git Status
```bash
git log --oneline -5
```

## Troubleshooting

### Ollama Not Running
```bash
ollama serve
```

### Check Model
```bash
ollama list
```

### Validate Playbook
```bash
ansible-playbook --syntax-check output/playbook.yml
```

## Tips

1. **Be specific** in your requests
2. **Always review** generated playbooks
3. **Test in staging** first
4. **Keep inventory** up to date
5. **Commit frequently** to Git

## Example Session

```bash
$ python3 src/main.py "Install nginx and start it"

✓ Ollama detected - using local AI (codellama:7b)
INFO: Concert AI Agent initialized

📝 Your request: Install nginx and start it

🔍 Checking for existing playbooks...
  - No matching playbook found
  → Will generate new playbook

📝 Collecting playbook parameters...

🖥️  Target Operating System:
  1. Ubuntu/Debian
  2. RHEL/CentOS
  3. Fedora
  4. All (multi-OS playbook)
Select OS (1-4, default: 4): 1

📋 Task-specific parameters:
  Package name: nginx

✓ Parameters collected

Step 2: Generating playbook...
  → Using template-based generation
✓ Playbook generated
✓ Saved: output/install_package_ubuntu_20260216_130245.yml

Step 3: Validating playbook...
✓ Playbook syntax is valid!

Step 4: Committing to Git...
✓ Playbook committed to local Git

✨ COMPLETE!
📄 Playbook: output/install_package_ubuntu_20260216_130245.yml
```

---

**Quick Start**: `python3 src/main.py "Your request"`  
**Documentation**: See PRODUCTION_GUIDE.md  
**Support**: Check logs and existing playbooks