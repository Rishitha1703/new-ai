# 🚀 Simplified Workflow Guide

## Overview

This simplified version asks **minimal questions** and follows a **streamlined workflow**:

1. **User Request** → OS Type
2. **Generate Playbook** → Validate
3. **Git Details** → URL, Token, Repo Name, Playbook Name
4. **Inventory Details** → Host, User, SSH Key
5. **Auto Push to Git** → Done!

---

## Quick Start

### Run the Simplified Agent

```bash
cd ai-concert-1
./run_simple.sh
```

Or directly:

```bash
cd ai-concert-1
source venv/bin/activate
python3 src/main_simple.py
```

---

## Workflow Example

### Step 1: Enter Request

```
Enter your request: Install nginx on all servers
```

### Step 2: Select OS Type

```
🖥️  Target Operating System:
  1. Ubuntu/Debian
  2. RHEL/CentOS
  3. Fedora
  4. All (multi-OS playbook)

Select OS (1-4, default: 4): 4
✓ OS selected: all
```

### Step 3: Playbook Generated & Validated

```
Step 2: Generating playbook...
  → Using template (fast & accurate)

Step 3: Validating playbook...
✓ Playbook is valid
```

### Step 4: Git Configuration

```
======================================================================
GIT CONFIGURATION
======================================================================

📋 Enter Git details:

Git URL (e.g., https://github.com/user/repo.git): https://github.com/myuser/myrepo.git
Git username: myuser
Git token/password: ghp_xxxxxxxxxxxxx
Repository name: myrepo
Branch (default: main): main

Use playbook name 'install_package_all_20260216_150330.yml'? (Y/n): y
```

### Step 5: Inventory Configuration

```
======================================================================
INVENTORY CONFIGURATION
======================================================================

📋 Enter inventory details:

ansible_host (IP address): 192.168.1.100
ansible_user (default: root): root
ansible_ssh_private_key_file (default: ~/.ssh/ai-agent): ~/.ssh/ai-agent
```

### Step 6: Auto Push to Git

```
======================================================================
PUSHING TO GIT
======================================================================

✓ Created inventory: inventory/inventory.ini
✓ Initialized Git repository
✓ Configured remote: myrepo

🚀 Pushing to main...
✓ Successfully pushed to myrepo
```

### Step 7: Complete!

```
======================================================================
✨ COMPLETE!
======================================================================
📄 Playbook: install_package_all_20260216_150330.yml
📁 Location: output/install_package_all_20260216_150330.yml
🌐 Git Repo: myrepo
📦 Inventory: inventory/inventory.ini
======================================================================
```

---

## What Gets Asked

### For Playbook Generation:
- ✅ **OS Type** (Ubuntu/RHEL/Fedora/All)
- ✅ **Task-specific params** (package name, port, username, etc.)

### For Git:
- ✅ **Git URL** (e.g., https://github.com/user/repo.git)
- ✅ **Username** (Git username)
- ✅ **Token** (Personal access token or password)
- ✅ **Repo Name** (Repository name)
- ✅ **Branch** (default: main)
- ✅ **Playbook Name** (auto-generated or custom)

### For Inventory:
- ✅ **ansible_host** (IP address)
- ✅ **ansible_user** (default: root)
- ✅ **ansible_ssh_private_key_file** (default: ~/.ssh/ai-agent)

---

## What's Removed

### ❌ No longer asks:
- Existing playbook check
- Change target hosts
- Execute playbook now
- Push to remote (auto-pushes)
- Concert workflow trigger
- Multiple credential prompts

---

## Comparison: Original vs Simplified

| Feature | Original | Simplified |
|---------|----------|------------|
| Playbook check | ✅ Interactive | ❌ Skipped |
| OS selection | ✅ Yes | ✅ Yes |
| Task params | ✅ Yes | ✅ Minimal |
| Target hosts | ✅ Asks | ❌ Always "all" |
| Git setup | ✅ Interactive | ✅ One-time |
| Git push | ✅ Asks | ✅ Auto |
| Inventory | ✅ Interactive | ✅ One-time |
| Concert trigger | ✅ Optional | ❌ Removed |
| Questions | ~10-15 | ~8 |

---

## Use Cases

### Perfect For:
- ✅ Quick playbook generation
- ✅ Demo presentations
- ✅ Batch operations
- ✅ CI/CD pipelines
- ✅ Simple workflows

### Not Ideal For:
- ❌ Complex multi-step tasks
- ❌ Reusing existing playbooks
- ❌ Custom target hosts
- ❌ Interactive debugging

---

## Tips

### 1. Prepare Git Token
```bash
# Generate token at: https://github.com/settings/tokens
# Permissions needed: repo (full control)
```

### 2. Prepare SSH Key
```bash
# Ensure SSH key exists
ls -la ~/.ssh/ai-agent

# If not, create one:
ssh-keygen -t rsa -b 4096 -f ~/.ssh/ai-agent
```

### 3. Test Inventory
```bash
# Test SSH connection
ssh -i ~/.ssh/ai-agent root@192.168.1.100
```

### 4. Use Command Line
```bash
# Pass request as argument
./run_simple.sh "Install nginx on all servers"
```

---

## Troubleshooting

### Issue: Git push fails

**Solution:**
```bash
# Check token permissions
# Ensure token has 'repo' scope

# Verify remote URL
cd output && git remote -v
```

### Issue: SSH key not found

**Solution:**
```bash
# Create SSH key
ssh-keygen -t rsa -b 4096 -f ~/.ssh/ai-agent

# Copy to server
ssh-copy-id -i ~/.ssh/ai-agent root@192.168.1.100
```

### Issue: Ollama not detected

**Solution:**
```bash
# Start Ollama (in another terminal)
ollama serve

# Pull model
ollama pull codellama:7b
```

---

## Files Created

After running, you'll have:

```
ai-concert-1/
├── output/
│   ├── install_package_all_20260216_150330.yml  # Generated playbook
│   ├── inventory.ini                              # Filled inventory file
│   └── .git/                                      # Git repository
├── inventory/
│   ├── inventory_template.ini                     # Template with placeholders
│   └── inventory.ini                              # Filled inventory file
└── logs/
    └── agent.log                                  # Operation logs
```

### Inventory Template System

The system uses a **template-based approach**:

1. **Template file** (`inventory/inventory_template.ini`):
   ```ini
   [hosts]
   server1 ansible_host={{ANSIBLE_HOST}} ansible_user={{ANSIBLE_USER}} ansible_ssh_private_key_file={{ANSIBLE_SSH_KEY}}
   ```

2. **User provides values** during execution

3. **System fills placeholders** and creates `inventory/inventory.ini`:
   ```ini
   [hosts]
   server1 ansible_host=192.168.1.100 ansible_user=root ansible_ssh_private_key_file=~/.ssh/ai-agent
   ```

**Benefits:**
- ✅ No new files created each time
- ✅ Template stays clean with placeholders
- ✅ Easy to modify template structure
- ✅ Consistent inventory format

---

## Next Steps

### After Generation:

1. **Verify Playbook**
   ```bash
   cat output/install_package_all_20260216_150330.yml
   ```

2. **Check Git**
   ```bash
   cd output
   git log
   git remote -v
   ```

3. **Test Inventory**
   ```bash
   ansible all -i inventory/inventory.ini -m ping
   ```

4. **Run in Concert**
   - Go to Concert UI
   - Create workflow
   - Point to Git repo
   - Execute playbook

---

## Switching Between Versions

### Use Original (Full Features):
```bash
./run.sh
# or
python3 src/main.py
```

### Use Simplified (Minimal Questions):
```bash
./run_simple.sh
# or
python3 src/main_simple.py
```

---

## Summary

**Simplified Workflow = Faster, Fewer Questions, Auto-Push**

Perfect for demos, quick tasks, and streamlined operations!

🚀 **Ready to use? Run:** `./run_simple.sh`