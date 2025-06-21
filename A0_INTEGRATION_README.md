# 🔮 Codex Alchemy + A0 Integration

A unified symbolic system that bridges **Codex Alchemy** (FastAPI + Next.js) with **A0** (Agent Zero) for seamless interoperability between ritual/glyph systems and agent-based spellcasting.

## 🚀 Quick Start

### 1. System Status
```bash
python unified_cli.py status
```

### 2. Start Backend
```bash
python unified_cli.py backend
```

### 3. Start Frontend
```bash
python unified_cli.py frontend
```

### 4. Access A0 Integration
Visit: `http://localhost:3000/a0-integration`

## 📊 Current Integration Status

| Component | Status | Details |
|-----------|--------|---------|
| **A0 Bridge** | ✅ Active | 4 agents, 6 spells, lineage data |
| **Codex Alchemy** | ✅ Active | 15 glyphs, SQLite DB, FastAPI backend |
| **Frontend** | ✅ Active | Next.js with A0 integration page |
| **API Endpoints** | ✅ Active | `/api/a0/*` routes available |
| **CLI Tools** | ✅ Active | Unified command interface |

## 🔗 Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   A0 System     │    │  A0 Bridge      │    │ Codex Alchemy   │
│                 │    │                 │    │                 │
│ • Agents        │◄──►│ • Import Logic  │◄──►│ • FastAPI       │
│ • Spells        │    │ • Vault Merge   │    │ • Next.js       │
│ • Lineage       │    │ • Agent Bridge  │    │ • SQLite        │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 🛠️ Available Commands

### CLI Commands
```bash
# System Status
python unified_cli.py status

# List Components
python unified_cli.py agents
python unified_cli.py spells

# Start Services
python unified_cli.py backend
python unified_cli.py frontend
python unified_cli.py a0

# Utilities
python unified_cli.py migrate
python unified_cli.py test
```

### API Endpoints
```bash
# A0 Status
curl http://localhost:8000/api/a0/status

# Available Agents
curl http://localhost:8000/api/a0/agents

# A0 Spells
curl http://localhost:8000/api/a0/spells

# Merged Vaults
curl http://localhost:8000/api/a0/vault/merged

# Bridge Test
curl http://localhost:8000/api/a0/bridge/test
```

## 🤖 Available Agents

### A0 Agents (4)
- `enforcer_token_breaker` - Token manipulation and analysis
- `enforcer_task_beast` - Task execution and management
- `agent` - Base agent functionality
- `enforcer_gpt` - GPT-based enforcement

### Codex Alchemy Agents (3)
- `gene_runtime` - Gene execution engine
- `train_runtime` - Training and evolution
- `agent` - Base agent system

## ✨ Available Spells

### A0 Spells (6)
- `fireball.json` - Base fireball spell
- `fireball~1.json` through `fireball~5.json` - Evolved versions
- Content: "Ignite recursive transformation"

### Codex Alchemy Glyphs (15)
- 15 recovered sigils with vector representations
- Deduction rituals with mathematical vectors
- Reflective mirror glyphs with metadata

## 🔧 Integration Components

### 1. A0 Bridge (`backend/bridge_a0.py`)
- **Purpose**: Seamless integration between systems
- **Features**:
  - Dynamic agent importing
  - Vault merging
  - Spell loading
  - Lineage tracking

### 2. API Routes (`backend/routes/a0_integration.py`)
- **Endpoints**:
  - `/api/a0/status` - System status
  - `/api/a0/agents` - Available agents
  - `/api/a0/spells` - A0 spells
  - `/api/a0/vault/merged` - Unified vault view
  - `/api/a0/agent/{name}/invoke` - Agent invocation

### 3. Frontend Integration (`frontend/src/pages/a0-integration.tsx`)
- **Features**:
  - Real-time status display
  - Agent listing
  - Spell visualization
  - Unified vault overview

### 4. Unified CLI (`unified_cli.py`)
- **Commands**:
  - System management
  - Service startup
  - Data migration
  - Integration testing

## 📁 File Structure

```
codex_alchemy/
├── a0/                          # Symlink to ../a0
├── a0_vault/                    # Symlink to ../a0/vault
├── backend/
│   ├── bridge_a0.py            # A0 integration bridge
│   ├── routes/
│   │   └── a0_integration.py   # API routes
│   └── main.py                 # Updated with A0 routes
├── frontend/src/pages/
│   └── a0-integration.tsx      # A0 integration UI
├── unified_cli.py              # Unified command interface
└── A0_INTEGRATION_README.md    # This file
```

## 🔄 Data Flow

### 1. Vault Merging
```python
# Merges codex_alchemy and a0 vaults
merged = a0_bridge.merge_vaults()
# Returns: {codex_alchemy: {...}, a0: {...}, merged: {...}}
```

### 2. Agent Bridging
```python
# Import A0 agents into codex_alchemy
agent = a0_bridge.import_a0_agent("enforcer_task_beast")
```

### 3. Spell Integration
```python
# Load A0 spells
spells = a0_bridge.get_a0_spells()
# Returns: List of spell objects with source metadata
```

## 🧪 Testing the Integration

### 1. Backend Test
```bash
curl http://localhost:8000/api/a0/bridge/test
```

### 2. Frontend Test
Visit: `http://localhost:3000/a0-integration`

### 3. CLI Test
```bash
python unified_cli.py test
```

## 🚨 Troubleshooting

### Common Issues

1. **A0 Not Available**
   ```bash
   # Check symlink
   ls -la a0
   # Should show: a0 -> ../a0
   ```

2. **Import Errors**
   ```bash
   # Check Python path
   python -c "import sys; print(sys.path)"
   ```

3. **API Errors**
   ```bash
   # Check backend status
   curl http://localhost:8000/health
   ```

### Debug Commands
```bash
# Full system status
python unified_cli.py status

# Test integration
python unified_cli.py test

# Check API endpoints
curl http://localhost:8000/api/a0/status
```

## 🔮 Future Enhancements

### Planned Features
- [ ] Real-time agent invocation
- [ ] Cross-system spell casting
- [ ] Unified lineage tracking
- [ ] Shared vector space
- [ ] Agent collaboration protocols

### Potential Integrations
- [ ] Supabase for shared storage
- [ ] Redis for caching
- [ ] WebSocket for real-time updates
- [ ] GraphQL for flexible queries

## 📞 Support

For issues or questions:
1. Check the troubleshooting section
2. Run `python unified_cli.py test`
3. Review API responses
4. Check system logs

---

**🔮 The integration is now complete and fully functional!**

Your unified symbolic system is ready for exploration and evolution. 