# 🏗️ Concert AI Agent - System Architecture

## 📊 Architecture Flow Diagram

```
User Input (Natural Language)
          │
          │ "Install MySQL server, start service, and enable it on boot"
          │
          ▼
┌─────────────────────────┐
│   Intent Parser         │
│   (NLP Engine)          │
│   - Analyzes request    │
│   - Extracts intent     │
│   - Identifies params   │
└─────────────────────────┘
          │
          │ Intent: install_package
          │ Params: {package: mysql-server, service: mysql}
          │
          ▼
┌─────────────────────────┐
│ Hybrid Decision Engine  │
│ - Template match?       │
│ - LLM required?         │
└─────────────────────────┘
          │
          ├──────────────────────┐
          │                      │
          ▼                      ▼
┌──────────────────┐   ┌──────────────────┐
│ Template         │   │ AI (LLM)         │
│ Generator        │   │ Generator        │
│ - Fast           │   │ - Flexible       │
│ - Accurate       │   │ - Custom tasks   │
│ - 6 templates    │   │ - Ollama/OpenAI  │
└──────────────────┘   └──────────────────┘
          │                      │
          └──────────┬───────────┘
                     │
                     │ Generated Playbook (YAML)
                     │
                     ▼
          ┌─────────────────────────┐
          │ Ansible Validator       │
          │ - Syntax check          │
          │ - Structure validation  │
          │ - Best practices        │
          └─────────────────────────┘
                     │
                     │ ✓ Valid Playbook
                     │
                     ▼
          ┌─────────────────────────┐
          │ Inventory Manager       │
          │ - Check inventory       │
          │ - Create if needed      │
          │ - INI format            │
          └─────────────────────────┘
                     │
                     │ ✓ Inventory Ready
                     │
                     ▼
          ┌─────────────────────────┐
          │ Git Manager             │
          │ - Local commit          │
          │ - Remote push           │
          │ - Version control       │
          └─────────────────────────┘
                     │
                     │ ✓ Committed
                     │
                     ▼
          ┌─────────────────────────┐
          │ Ready for Execution     │
          │ - Playbook validated    │
          │ - Inventory configured  │
          │ - Version controlled    │
          └─────────────────────────┘
```

---

## 🔧 Component Details

### 1. **Intent Parser (NLP Engine)**
**File:** `src/intent_parser.py`

**Purpose:** Analyzes natural language input and extracts structured intent

**Capabilities:**
- Pattern matching for 6 intent types
- OS detection (Ubuntu, RHEL, CentOS, etc.)
- Parameter extraction
- Confidence scoring

**Example:**
```python
Input: "Install MySQL server, start service, and enable it on boot"
Output: {
    'intent': 'install_package',
    'params': {
        'package_name': 'mysql-server',
        'service_name': 'mysql',
        'os_type': 'all'
    },
    'source': 'template'
}
```

---

### 2. **Hybrid Decision Engine**
**File:** `src/main.py` (process_prompt method)

**Purpose:** Decides whether to use template or LLM generation

**Decision Logic:**
```
IF intent matches template:
    → Use Template Generator (fast, accurate)
ELSE IF hybrid_mode enabled:
    → Use LLM Generator (flexible, custom)
ELSE:
    → Error: Cannot generate
```

**Supported Intents:**
1. `install_package` - Install software packages
2. `configure_firewall` - Configure firewall rules
3. `create_user` - Create system users
4. `deploy_docker` - Deploy Docker containers
5. `restart_service` - Restart system services
6. `update_config` - Update configuration files

---

### 3. **Template Generator**
**File:** `src/template_generator.py`

**Purpose:** Fast, guaranteed-accurate playbook generation from templates

**Templates:** `templates/`
- `install_package.yml`
- `configure_firewall.yml`
- `create_user.yml`
- `deploy_docker.yml`
- `restart_service.yml`
- `update_config.yml`

**Process:**
1. Load template file
2. Replace placeholders with parameters
3. Return complete playbook

**Advantages:**
- ⚡ Fast (milliseconds)
- ✅ 100% accurate
- 🎯 Best practices built-in

---

### 4. **AI (LLM) Generator**
**File:** `src/llm_generator.py`

**Purpose:** Flexible playbook generation for custom/complex tasks

**Supported Providers:**
- **Ollama** (local, free) - codellama:7b
- **OpenAI** (cloud) - GPT-4
- **Anthropic** (cloud) - Claude

**Process:**
1. Build prompt with context
2. Call LLM API
3. Parse YAML response
4. Validate structure

**Use Cases:**
- Custom configurations
- Complex multi-step tasks
- Non-standard requirements

---

### 5. **Ansible Validator**
**File:** `src/validator.py`

**Purpose:** Ensures playbook quality before execution

**Validation Checks:**
- ✅ YAML syntax
- ✅ Ansible structure
- ✅ Required fields
- ✅ Best practices

**Process:**
```python
1. Parse YAML
2. Check structure
3. Validate fields
4. Return status + errors
```

---

### 6. **Git Manager**
**File:** `src/git_manager.py`

**Purpose:** Version control for all generated playbooks

**Features:**
- Local Git repository
- Auto-commit on generation
- Remote push (immediate/manual/scheduled)
- Commit history tracking

**Workflow:**
```
1. Add playbook to Git
2. Commit with timestamp
3. Push to remote (if enabled)
4. Track version history
```

---

### 7. **Concert API Trigger**
**File:** `src/concert_api.py`

**Purpose:** Integration with IBM Concert for workflow orchestration

**Features:**
- Workflow submission
- Metadata tracking
- Status monitoring
- Simulation mode

**API Call:**
```python
POST /api/v1/workflows
{
    "playbook": "path/to/playbook.yml",
    "metadata": {
        "intent": "install_package",
        "source": "template",
        "timestamp": "2026-02-16T12:00:00Z"
    }
}
```

---

### 8. **Execution on Infrastructure**
**Via:** Ansible + Inventory

**Inventory Format:** `inventory/inventory.ini`
```ini
[hosts]
Server1 ansible_host=9.30.44.81 ansible_user=netcool ansible_ssh_private_key_file=~/.ssh/ai-agent ansible_become=yes
```

**Execution:**
```bash
ansible-playbook -i inventory/inventory.ini output/playbook.yml
```

---

## 🔄 Complete Flow Example

### Request: "Install MySQL server, start service, and enable it on boot"

```
1. Intent Parser
   ↓ Analyzes: "Install MySQL..."
   ↓ Extracts: intent=install_package, package=mysql-server
   
2. Hybrid Decision Engine
   ↓ Checks: Template exists for install_package?
   ↓ Decision: Use Template Generator
   
3. Template Generator
   ↓ Loads: templates/install_package.yml
   ↓ Fills: {{package_name}} = mysql-server
   ↓ Generates: Complete playbook
   
4. Ansible Validator
   ↓ Validates: YAML syntax ✓
   ↓ Validates: Ansible structure ✓
   ↓ Result: Valid playbook
   
5. Git Manager
   ↓ Commits: install_package_all_20260216_140605.yml
   ↓ Pushes: To remote repository
   ↓ Hash: dd173ee
   
6. Concert API Trigger
   ↓ Submits: Workflow to Concert
   ↓ Metadata: {intent, source, timestamp}
   ↓ Status: Workflow triggered
   
7. Execution on Infrastructure
   ↓ Ansible: Runs playbook
   ↓ Target: Server1 (9.30.44.81)
   ↓ Result: MySQL installed and enabled
```

---

## 🎯 Enhanced Features (v3.0)

### **Playbook Checker**
**File:** `src/playbook_checker.py`

**Purpose:** Check for existing playbooks before generating new ones

**Process:**
```
1. Search output/ directory
2. Match intent and parameters
3. Calculate similarity score
4. Present options to user
5. Reuse or create new
```

### **Credential Manager**
**File:** `src/credential_manager.py`

**Purpose:** Interactive credential collection

**Collects:**
- Git credentials (URL, branch, token)
- Concert API credentials (URL, key)
- LLM provider credentials (API keys)

### **Inventory Manager**
**File:** `src/inventory_manager.py`

**Purpose:** Interactive inventory generation (INI format)

**Collects:**
- Host name
- IP address
- SSH user
- SSH private key path
- Sudo settings

---

## 📊 Data Flow

```
User Input
    ↓
Intent Parser → {intent, params, source}
    ↓
Hybrid Engine → Decision: template or LLM
    ↓
Generator → Playbook (YAML)
    ↓
Validator → Valid: true/false
    ↓
Git Manager → Commit hash
    ↓
Concert API → Workflow ID
    ↓
Ansible → Execution result
```

---

## 🔐 Security Architecture

```
User Input
    ↓
Credential Manager (getpass - hidden input)
    ↓
Config File (config/config.yml - gitignored)
    ↓
Git Manager (credentials in URL)
    ↓
Concert API (API key in headers)
    ↓
Ansible (SSH keys for authentication)
```

---

## 🎯 System Components Summary

| Component | File | Purpose | Input | Output |
|-----------|------|---------|-------|--------|
| Intent Parser | `intent_parser.py` | Parse NL input | User text | Intent + params |
| Hybrid Engine | `main.py` | Route to generator | Intent | Generator choice |
| Template Gen | `template_generator.py` | Fast generation | Template + params | Playbook |
| LLM Gen | `llm_generator.py` | Flexible generation | Prompt | Playbook |
| Validator | `validator.py` | Validate playbook | Playbook | Valid/Invalid |
| Git Manager | `git_manager.py` | Version control | Playbook | Commit hash |
| Concert API | `concert_api.py` | Workflow trigger | Playbook + metadata | Workflow ID |
| Playbook Checker | `playbook_checker.py` | Find existing | Intent + params | Matches |
| Credential Mgr | `credential_manager.py` | Collect creds | User input | Config |
| Inventory Mgr | `inventory_manager.py` | Create inventory | User input | INI file |

---

## 🚀 Production Architecture

The system follows a **modular, pipeline-based architecture** where each component has a single responsibility and can be tested/replaced independently.

**Key Principles:**
- ✅ Separation of concerns
- ✅ Single responsibility per module
- ✅ Pipeline-based processing
- ✅ Error handling at each stage
- ✅ Logging throughout
- ✅ Configuration-driven
- ✅ Extensible design

This architecture ensures **reliability, maintainability, and scalability** for production use.