# 🚀 Quick Start Guide - Enhanced Version

## Get Started in 3 Steps!

### Step 1: Run the Enhanced Agent
```bash
cd /Users/khirsagarrishitha/Desktop/concert-ai-agent
./run_enhanced.sh
```

### Step 2: Configure (First Time Only)
When you see the prompt, type:
```
Your request: setup
```

Follow the wizard to configure:
1. **Git** (for version control)
   - Enable Git? **Y**
   - Enable auto-commit? **Y**
   - Enable remote repository? **Y**
   - Remote URL: `https://github.com/Rishitha1703/new-ai.git`
   - Branch: `main`
   - Push mode: Select **2** (manual) or **1** (immediate)
   - Configure credentials? **y**
   - Username: `your-github-username`
   - Token: `your-personal-access-token`

2. **IBM Concert API** (optional)
   - Enable Concert? **n** (skip for now)

3. **LLM Provider**
   - Select provider: **1** (Ollama - already installed)
   - Model: `codellama:7b` (press Enter for default)

### Step 3: Create Inventory
Type:
```
Your request: inventory
```

Select option **1** to create new inventory:

**Example Configuration:**
```
Host name: Server1
IP address: 9.30.44.81
SSH user: netcool
SSH key path: ~/.ssh/ai-agent
SSH port: (press Enter for default 22)
Use sudo? Y

Host name: done
```

**Generated inventory.ini:**
```
[hosts]
Server1 ansible_host=9.30.44.81 ansible_user=netcool ansible_ssh_private_key_file=~/.ssh/ai-agent ansible_become=yes
```

---

## 🎯 Now You're Ready!

### Make Your First Request

```
Your request: Install MySQL server, start service, and enable it on boot
```

The system will:
1. ✅ Check if similar playbook exists
2. ✅ Ask if you want to use existing or create new
3. ✅ Collect any missing parameters
4. ✅ Generate the playbook
5. ✅ Validate syntax
6. ✅ Commit to Git
7. ✅ Show summary

---

## 📝 Common Commands

| Command | What It Does |
|---------|--------------|
| `setup` | Configure credentials |
| `inventory` | Manage inventories |
| `status` | Show system status |
| `logs` | View recent logs |
| `exit` | Quit |

---

## 💡 Example Requests

Try these natural language requests:

```
Install nginx on Ubuntu
Open port 8080 on RHEL
Create user john on CentOS
Deploy redis container
Restart apache service
```

---

## 🔑 GitHub Personal Access Token

To push to GitHub, you need a Personal Access Token:

1. Go to: https://github.com/settings/tokens
2. Click "Generate new token (classic)"
3. Select scopes: `repo` (all)
4. Generate and copy the token
5. Use it as password when configuring Git

---

## 🎨 What Makes This Enhanced?

### Before (Old Version):
- ❌ No playbook checking
- ❌ Manual config file editing
- ❌ Manual inventory creation
- ❌ Missing parameters = failure

### After (Enhanced Version):
- ✅ Checks existing playbooks first
- ✅ Interactive credential setup
- ✅ Interactive inventory creation
- ✅ Asks for missing parameters
- ✅ On-demand configuration
- ✅ Production-ready workflow

---

## 🛠️ Troubleshooting

### Can't push to Git?
```
Your request: setup
# Reconfigure Git with correct credentials
```

### No inventory?
```
Your request: inventory
# Create new inventory with hosts
```

### Want to see what's configured?
```
Your request: status
# Shows all settings
```

---

## 🎉 You're All Set!

The enhanced system is now:
- ✅ Checking for existing playbooks
- ✅ Collecting credentials interactively
- ✅ Managing inventory interactively
- ✅ Asking for all required details
- ✅ Production-ready

**No more demo files or manual configuration!**

---

## 📞 Need Help?

Type `status` to see your configuration
Type `logs` to see recent activity
Type `setup` to reconfigure anything

Enjoy your production-ready Concert AI Agent! 🚀