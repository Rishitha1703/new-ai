# 📦 Inventory Template System

## Overview

The simplified workflow uses a **template-based inventory system** with placeholders that get filled in during execution.

---

## How It Works

### 1. Template File (One-Time Setup)

**Location:** `inventory/inventory_template.ini`

**Content:**
```ini
[hosts]
server1 ansible_host={{ANSIBLE_HOST}} ansible_user={{ANSIBLE_USER}} ansible_ssh_private_key_file={{ANSIBLE_SSH_KEY}}
```

**Placeholders:**
- `{{ANSIBLE_HOST}}` - IP address or hostname
- `{{ANSIBLE_USER}}` - SSH user (e.g., root, ubuntu)
- `{{ANSIBLE_SSH_KEY}}` - Path to SSH private key

---

### 2. User Input (During Execution)

When you run the simplified workflow, you'll be asked:

```
======================================================================
INVENTORY CONFIGURATION
======================================================================

📋 Enter inventory details:

ansible_host (IP address): 192.168.1.100
ansible_user (default: root): root
ansible_ssh_private_key_file (default: ~/.ssh/ai-agent): ~/.ssh/ai-agent
```

---

### 3. Filled Inventory (Auto-Generated)

**Location:** `inventory/inventory.ini`

**Content:**
```ini
[hosts]
server1 ansible_host=192.168.1.100 ansible_user=root ansible_ssh_private_key_file=~/.ssh/ai-agent
```

This file is:
- ✅ Created automatically from template
- ✅ Copied to `output/` directory
- ✅ Pushed to Git with playbook
- ✅ Ready for Concert execution

---

## Benefits

### ✅ No File Duplication
- Template stays clean with placeholders
- Only one inventory file created per run
- No clutter in inventory directory

### ✅ Easy Customization
- Modify template once
- All future inventories use new format
- Consistent structure across runs

### ✅ Version Control Friendly
- Template can be committed to Git
- Filled inventory is gitignored (optional)
- Clean separation of template vs data

---

## Customizing the Template

### Add More Hosts

Edit `inventory/inventory_template.ini`:

```ini
[hosts]
server1 ansible_host={{ANSIBLE_HOST_1}} ansible_user={{ANSIBLE_USER}} ansible_ssh_private_key_file={{ANSIBLE_SSH_KEY}}
server2 ansible_host={{ANSIBLE_HOST_2}} ansible_user={{ANSIBLE_USER}} ansible_ssh_private_key_file={{ANSIBLE_SSH_KEY}}
server3 ansible_host={{ANSIBLE_HOST_3}} ansible_user={{ANSIBLE_USER}} ansible_ssh_private_key_file={{ANSIBLE_SSH_KEY}}
```

Then update `main_simple.py` to collect multiple hosts.

---

### Add Host Groups

```ini
[webservers]
web1 ansible_host={{WEB_HOST_1}} ansible_user={{ANSIBLE_USER}} ansible_ssh_private_key_file={{ANSIBLE_SSH_KEY}}
web2 ansible_host={{WEB_HOST_2}} ansible_user={{ANSIBLE_USER}} ansible_ssh_private_key_file={{ANSIBLE_SSH_KEY}}

[databases]
db1 ansible_host={{DB_HOST_1}} ansible_user={{ANSIBLE_USER}} ansible_ssh_private_key_file={{ANSIBLE_SSH_KEY}}

[all:children]
webservers
databases
```

---

### Add Variables

```ini
[hosts]
server1 ansible_host={{ANSIBLE_HOST}} ansible_user={{ANSIBLE_USER}} ansible_ssh_private_key_file={{ANSIBLE_SSH_KEY}}

[hosts:vars]
ansible_python_interpreter=/usr/bin/python3
ansible_connection=ssh
ansible_port=22
```

---

## File Locations

```
ai-concert-1/
├── inventory/
│   ├── inventory_template.ini    # Template with placeholders (committed to Git)
│   └── inventory.ini              # Filled inventory (generated each run)
└── output/
    ├── playbook.yml               # Generated playbook
    ├── inventory.ini              # Copy of filled inventory
    └── .git/                      # Git repository
```

---

## Workflow

```
1. Read template
   ↓
2. Collect user input
   ↓
3. Replace placeholders
   ↓
4. Write inventory.ini
   ↓
5. Copy to output/
   ↓
6. Push to Git
```

---

## Example: Complete Flow

### Step 1: Template Exists
```ini
# inventory/inventory_template.ini
[hosts]
server1 ansible_host={{ANSIBLE_HOST}} ansible_user={{ANSIBLE_USER}} ansible_ssh_private_key_file={{ANSIBLE_SSH_KEY}}
```

### Step 2: User Provides Values
```
ansible_host: 192.168.1.100
ansible_user: root
ansible_ssh_private_key_file: ~/.ssh/ai-agent
```

### Step 3: System Fills Template
```python
content = template.replace('{{ANSIBLE_HOST}}', '192.168.1.100')
content = content.replace('{{ANSIBLE_USER}}', 'root')
content = content.replace('{{ANSIBLE_SSH_KEY}}', '~/.ssh/ai-agent')
```

### Step 4: Result
```ini
# inventory/inventory.ini
[hosts]
server1 ansible_host=192.168.1.100 ansible_user=root ansible_ssh_private_key_file=~/.ssh/ai-agent
```

---

## Testing the Inventory

### Test SSH Connection
```bash
ssh -i ~/.ssh/ai-agent root@192.168.1.100
```

### Test with Ansible
```bash
ansible all -i inventory/inventory.ini -m ping
```

### Expected Output
```
server1 | SUCCESS => {
    "changed": false,
    "ping": "pong"
}
```

---

## Troubleshooting

### Issue: Template not found

**Solution:**
```bash
# Create template manually
cat > inventory/inventory_template.ini << 'EOF'
[hosts]
server1 ansible_host={{ANSIBLE_HOST}} ansible_user={{ANSIBLE_USER}} ansible_ssh_private_key_file={{ANSIBLE_SSH_KEY}}
EOF
```

### Issue: Placeholders not replaced

**Check:**
1. Template uses correct placeholder format: `{{PLACEHOLDER}}`
2. Code replaces all placeholders
3. No typos in placeholder names

### Issue: SSH connection fails

**Check:**
1. SSH key exists: `ls -la ~/.ssh/ai-agent`
2. SSH key has correct permissions: `chmod 600 ~/.ssh/ai-agent`
3. Host is reachable: `ping 192.168.1.100`
4. SSH service running on host: `ssh -v root@192.168.1.100`

---

## Advanced: Multiple Templates

You can create multiple templates for different scenarios:

```
inventory/
├── inventory_template.ini           # Default template
├── inventory_template_multi.ini     # Multiple hosts
├── inventory_template_groups.ini    # Host groups
└── inventory_template_vars.ini      # With variables
```

Then modify `main_simple.py` to ask which template to use.

---

## Best Practices

### ✅ DO:
- Keep template simple and clean
- Use descriptive placeholder names
- Document any custom placeholders
- Test inventory before pushing to Git
- Version control the template

### ❌ DON'T:
- Hardcode sensitive data in template
- Use complex placeholder formats
- Create multiple inventory files per run
- Commit filled inventory to Git (optional)

---

## Summary

**Template System = Clean, Reusable, Consistent**

- ✅ One template file with placeholders
- ✅ User provides values during execution
- ✅ System fills placeholders automatically
- ✅ No file duplication
- ✅ Easy to customize

**Ready to use? The template is already created!** 🚀