# IDE-Like UI/UX Architecture Research
## Open Source Components for Vanilla JavaScript

**Date:** 2025-01-14
**Purpose:** Research suitable open-source projects to create an IDE-like interface for the YAML configuration builder using vanilla JavaScript.

---

## 🎯 Requirements Summary

- **Framework:** Vanilla JavaScript (no React/Vue/Angular)
- **Feel:** IDE-like interface (VS Code, WebStorm style)
- **Use Case:** YAML configuration builder with visual + code editing
- **Must Support:**
  - Three-pane layout (tree navigation | visual editor | code editor)
  - Resizable panels
  - YAML syntax highlighting and editing
  - Tree-based file/validation navigation
  - Bi-directional sync between visual UI and YAML

---

## 🔧 Recommended Component Stack

### 1. Code Editor: **CodeMirror 6**

**Why CodeMirror over Monaco or Ace:**

| Feature | CodeMirror 6 | Monaco Editor | Ace Editor |
|---------|-------------|---------------|------------|
| Bundle Size | ~300KB (modular) | 5-10MB | ~500KB |
| Mobile Support | Excellent ✅ | Poor ❌ | Good ✓ |
| YAML Support | Built-in (@codemirror/lang-yaml) | Plugin required | Built-in |
| Vanilla JS | Native ✅ | Requires AMD/ESM config | Native ✅ |
| Customization | Highly modular | All-or-nothing | Good |
| License | MIT | MIT | BSD |

**Recommendation:** CodeMirror 6 - lightweight, excellent YAML support, mobile-friendly, truly modular.

**Installation:**
```html
<!-- Via CDN -->
<script type="module">
  import {EditorView, basicSetup} from "https://cdn.jsdelivr.net/npm/codemirror@6/dist/index.js"
  import {yaml} from "https://cdn.jsdelivr.net/npm/@codemirror/lang-yaml@6/dist/index.js"

  let editor = new EditorView({
    doc: "validation_job:\n  name: My Job",
    extensions: [basicSetup, yaml()],
    parent: document.getElementById('editor')
  })
</script>
```

**Features:**
- YAML syntax highlighting
- Auto-indentation
- Code folding
- Search/replace
- Customizable themes
- Change tracking for bi-directional sync

**Official Docs:** https://codemirror.net/

---

### 2. Split Panes: **Split.js**

**Why Split.js:**
- Pure vanilla JavaScript (no dependencies)
- Tiny footprint (~2KB gzipped)
- Supports flexbox and CSS Grid layouts
- Smooth drag-to-resize
- Saves pane sizes to localStorage (can persist user preferences)

**Installation:**
```html
<script src="https://cdn.jsdelivr.net/npm/split.js@1.6.5/dist/split.min.js"></script>
```

**Basic Usage:**
```javascript
// Create three-pane IDE layout
Split(['#tree-panel', '#editor-panel', '#yaml-panel'], {
  sizes: [20, 50, 30],        // Initial percentage widths
  minSize: [200, 400, 300],   // Minimum pixel widths
  gutterSize: 8,              // Drag handle size
  cursor: 'col-resize',       // Cursor style
  onDragEnd: function(sizes) {
    // Save user's panel sizes
    localStorage.setItem('panelSizes', JSON.stringify(sizes));
  }
});
```

**HTML Structure:**
```html
<div class="container">
  <div id="tree-panel" class="split"></div>
  <div id="editor-panel" class="split"></div>
  <div id="yaml-panel" class="split"></div>
</div>
```

**CSS:**
```css
.container {
  display: flex;
  height: 100vh;
}

.split {
  overflow: auto;
}

.gutter {
  background-color: #eee;
  background-repeat: no-repeat;
  background-position: 50%;
}

.gutter.gutter-horizontal {
  background-image: url('data:image/png;base64,iVBORw0KGgo...');
  cursor: col-resize;
}
```

**Official Docs:** https://split.js.org/

---

### 3. Tree View: **js-treeview**

**Why js-treeview:**
- Pure vanilla JavaScript (zero dependencies)
- NPM package available
- Event-driven architecture
- Simple API
- MIT licensed

**Alternative Options:**
- **vanillatree** - More features (context menus, drag-drop)
- **TreeJS** - Windows Explorer-style
- **vanilla-tree-viewer** - Minimalist file browser

**Installation:**
```bash
npm install js-treeview
```

**Usage:**
```javascript
const TreeView = require('js-treeview');

const tree = new TreeView([
  {
    name: 'customers.csv',
    expanded: true,
    children: [
      { name: 'Columns', children: [
        { name: 'id', data: { type: 'string' } },
        { name: 'email', data: { type: 'string' } }
      ]},
      { name: 'Validations', children: [
        { name: 'EmptyFileCheck', data: { severity: 'ERROR' } },
        { name: 'MandatoryFieldCheck', data: { fields: ['email'] } }
      ]}
    ]
  },
  {
    name: 'orders.csv',
    children: []
  }
], 'tree-container');

// Handle selection
tree.on('select', function(e) {
  console.log('Selected:', e.data.name);
  // Update editor panel with selected item
  updateEditorPanel(e.data);
});
```

**GitHub:** https://github.com/justinchmura/js-treeview
**Demo:** http://codepen.io/justinchmura/pen/PZzBOP/

---

### 4. Additional UI Components

#### **Golden Layout** (Advanced Alternative)
If you want a more sophisticated IDE layout with:
- Dockable panels
- Tabs
- Drag-and-drop panel reorganization
- Popout windows

**Golden Layout** is a mature library (used by Bloomberg, Trading View):
- Pure JavaScript
- No framework dependencies
- Complex layouts with minimal code
- https://golden-layout.com/

**Trade-off:** More complex (200KB), but provides VS Code-like docking.

---

## 🏗️ Recommended Architecture

### Three-Pane Layout

```
┌────────────────────────────────────────────────────────────┐
│ Top Bar: File name, Save, Validate, Settings              │
├──────────────┬──────────────────────┬──────────────────────┤
│              │                      │                      │
│  Tree View   │   Visual Editor      │   YAML Editor        │
│  (20%)       │   (50%)              │   (30%)              │
│              │                      │                      │
│ Files        │ ┌──────────────────┐ │ ┌──────────────────┐ │
│ ├─ File1     │ │ Form-based UI    │ │ │ CodeMirror       │ │
│ │  ├─ Cols   │ │ for selected     │ │ │ YAML editor      │ │
│ │  └─ Checks │ │ validation       │ │ │                  │ │
│ │     ├─ Chk1│ │                  │ │ │ validation_job:  │ │
│ │     └─ Chk2│ │ • Name           │ │ │   name: ...      │ │
│ └─ File2     │ │ • Type           │ │ │   files:         │ │
│              │ │ • Severity       │ │ │     - name: ...  │ │
│              │ │ • Parameters     │ │ │                  │ │
│              │ └──────────────────┘ │ │ [Edit YAML]      │ │
│              │                      │ └──────────────────┘ │
│              │                      │                      │
└──────────────┴──────────────────────┴──────────────────────┘
```

### Data Flow

```
User Action (Tree Click)
    ↓
Update State (Selected Node)
    ↓
Render Visual Editor ←→ Update YAML Editor
    ↓
User Edits (Forms or YAML)
    ↓
Sync State
    ↓
Update All Views
```

---

## 📦 Implementation Plan

### Phase 1: Core Layout (Week 1)

**Files to Create:**
```
config-builder/
├── index-ide.html          # Main IDE interface
├── js/
│   ├── ide-layout.js       # Split.js initialization
│   ├── tree-view.js        # Tree component
│   ├── yaml-editor.js      # CodeMirror wrapper
│   ├── visual-editor.js    # Form-based editor (existing code)
│   └── state-manager.js    # Central state management
└── css/
    └── ide-theme.css       # VS Code-inspired theme
```

**index-ide.html skeleton:**
```html
<!DOCTYPE html>
<html>
<head>
  <title>Data Validation Config Builder - IDE</title>
  <link rel="stylesheet" href="css/ide-theme.css">
</head>
<body>
  <!-- Top Bar -->
  <header class="topbar">
    <div class="file-info">
      <span id="filename">validation_config.yaml</span>
      <span id="unsaved-indicator" class="hidden">●</span>
    </div>
    <div class="actions">
      <button onclick="newConfig()">New</button>
      <button onclick="openConfig()">Open</button>
      <button onclick="saveConfig()">Save</button>
      <button onclick="validateYAML()">Validate</button>
    </div>
  </header>

  <!-- Three-Pane Layout -->
  <div class="ide-container">
    <div id="tree-panel" class="panel">
      <div class="panel-header">Files</div>
      <div id="tree-view"></div>
    </div>

    <div id="editor-panel" class="panel">
      <div class="panel-header">Visual Editor</div>
      <div id="visual-editor">
        <!-- Form-based editor (your existing code) -->
      </div>
    </div>

    <div id="yaml-panel" class="panel">
      <div class="panel-header">
        YAML
        <button id="toggle-edit-mode">Edit</button>
      </div>
      <div id="yaml-editor"></div>
    </div>
  </div>

  <!-- Libraries -->
  <script src="https://cdn.jsdelivr.net/npm/split.js@1.6.5/dist/split.min.js"></script>
  <script src="js/tree-view.js"></script>
  <script src="js/yaml-editor.js"></script>
  <script src="js/visual-editor.js"></script>
  <script src="js/state-manager.js"></script>
  <script src="js/ide-layout.js"></script>
</body>
</html>
```

**js/ide-layout.js:**
```javascript
// Initialize split panes
const savedSizes = JSON.parse(localStorage.getItem('panelSizes')) || [20, 50, 30];

Split(['#tree-panel', '#editor-panel', '#yaml-panel'], {
  sizes: savedSizes,
  minSize: [200, 400, 300],
  gutterSize: 8,
  cursor: 'col-resize',
  onDragEnd: function(sizes) {
    localStorage.setItem('panelSizes', JSON.stringify(sizes));
  }
});

// Initialize components
const treeView = initTreeView('tree-view');
const yamlEditor = initYAMLEditor('yaml-editor');
const visualEditor = initVisualEditor('visual-editor');

// Wire up event handlers
treeView.on('select', (node) => {
  StateManager.setSelectedNode(node);
  visualEditor.render(node);
  yamlEditor.highlight(node);
});

visualEditor.on('change', (data) => {
  StateManager.updateNode(data);
  yamlEditor.refresh();
  treeView.updateNode(data);
});

yamlEditor.on('change', (yaml) => {
  try {
    const parsed = parseYAML(yaml);
    StateManager.updateFromYAML(parsed);
    visualEditor.refresh();
    treeView.refresh();
  } catch (err) {
    showValidationError(err);
  }
});
```

### Phase 2: YAML Editor Integration (Week 2)

**js/yaml-editor.js:**
```javascript
import {EditorView, basicSetup} from "codemirror"
import {yaml} from "@codemirror/lang-yaml"
import {oneDark} from "@codemirror/theme-one-dark"

class YAMLEditor {
  constructor(elementId) {
    this.element = document.getElementById(elementId);
    this.mode = 'view'; // 'view' or 'edit'

    this.editor = new EditorView({
      doc: "",
      extensions: [
        basicSetup,
        yaml(),
        oneDark,
        EditorView.editable.of(false), // Read-only by default
        EditorView.updateListener.of((update) => {
          if (update.docChanged && this.mode === 'edit') {
            this.emit('change', this.getValue());
          }
        })
      ],
      parent: this.element
    });
  }

  setValue(yaml) {
    this.editor.dispatch({
      changes: {
        from: 0,
        to: this.editor.state.doc.length,
        insert: yaml
      }
    });
  }

  getValue() {
    return this.editor.state.doc.toString();
  }

  setEditMode(enabled) {
    this.mode = enabled ? 'edit' : 'view';
    this.editor.dispatch({
      effects: EditorView.editable.reconfigure(enabled)
    });
  }

  highlight(node) {
    // Scroll to and highlight relevant YAML section
    // Implementation depends on your YAML structure
  }
}
```

### Phase 3: Tree View Integration (Week 3)

**js/tree-view.js:**
```javascript
class ConfigTreeView {
  constructor(elementId) {
    this.element = document.getElementById(elementId);
    this.listeners = {};
    this.data = [];
  }

  setData(config) {
    // Transform config model to tree structure
    this.data = this.transformConfigToTree(config);
    this.render();
  }

  transformConfigToTree(config) {
    return config.files.map(file => ({
      name: file.name,
      icon: '📁',
      expanded: false,
      children: [
        {
          name: 'Columns',
          icon: '📊',
          children: file.columns?.map(col => ({
            name: col,
            icon: '🔤',
            data: { type: 'column', file: file.name, column: col }
          })) || []
        },
        {
          name: 'Validations',
          icon: '✓',
          expanded: true,
          children: file.validations.map(v => ({
            name: v.name || v.type,
            icon: this.getValidationIcon(v.type),
            data: { type: 'validation', file: file.name, validation: v }
          }))
        }
      ]
    }));
  }

  getValidationIcon(type) {
    const icons = {
      'EmptyFileCheck': '📄',
      'MandatoryFieldCheck': '⚠️',
      'UniqueKeyCheck': '🔑',
      'DateFormatCheck': '📅',
      'RangeCheck': '📏'
    };
    return icons[type] || '✓';
  }

  render() {
    // Render tree HTML
    this.element.innerHTML = this.renderNode(this.data);
    this.attachEventListeners();
  }

  renderNode(nodes, level = 0) {
    return nodes.map(node => `
      <div class="tree-node" data-level="${level}" data-id="${node.id}">
        <div class="tree-node-content">
          <span class="tree-toggle">${node.children ? '▶' : ''}</span>
          <span class="tree-icon">${node.icon || ''}</span>
          <span class="tree-label">${node.name}</span>
        </div>
        ${node.children && node.expanded ?
          `<div class="tree-children">${this.renderNode(node.children, level + 1)}</div>` :
          ''}
      </div>
    `).join('');
  }

  on(event, callback) {
    if (!this.listeners[event]) this.listeners[event] = [];
    this.listeners[event].push(callback);
  }

  emit(event, data) {
    if (this.listeners[event]) {
      this.listeners[event].forEach(cb => cb(data));
    }
  }
}
```

### Phase 4: State Management & Sync (Week 4)

**js/state-manager.js:**
```javascript
const StateManager = (function() {
  let state = {
    config: null,
    selectedNode: null,
    yamlText: '',
    unsaved: false
  };

  const listeners = {};

  function getState() {
    return JSON.parse(JSON.stringify(state));
  }

  function setState(updates) {
    state = { ...state, ...updates };
    state.unsaved = true;
    emit('stateChange', state);
  }

  function setSelectedNode(node) {
    state.selectedNode = node;
    emit('selectionChange', node);
  }

  function updateFromYAML(yaml) {
    try {
      const parsed = parseYAML(yaml);
      state.config = parsed;
      state.yamlText = yaml;
      state.unsaved = true;
      emit('configChange', parsed);
    } catch (err) {
      emit('error', { type: 'yaml-parse', error: err });
    }
  }

  function updateFromVisual(nodeData) {
    // Update config model
    updateConfigNode(state.config, nodeData);

    // Regenerate YAML
    state.yamlText = generateYAML(state.config);
    state.unsaved = true;

    emit('configChange', state.config);
  }

  function on(event, callback) {
    if (!listeners[event]) listeners[event] = [];
    listeners[event].push(callback);
  }

  function emit(event, data) {
    if (listeners[event]) {
      listeners[event].forEach(cb => cb(data));
    }
  }

  return {
    getState,
    setState,
    setSelectedNode,
    updateFromYAML,
    updateFromVisual,
    on
  };
})();
```

---

## 🎨 VS Code-Inspired Theme

**css/ide-theme.css:**
```css
:root {
  /* VS Code Dark+ Theme Colors */
  --bg-primary: #1e1e1e;
  --bg-secondary: #252526;
  --bg-tertiary: #2d2d30;
  --border: #3e3e42;
  --text-primary: #cccccc;
  --text-secondary: #969696;
  --accent: #007acc;
  --accent-hover: #1a8ad1;
  --error: #f48771;
  --warning: #cca700;
  --success: #89d185;
}

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: 'Segoe UI', -apple-system, system-ui, sans-serif;
  font-size: 13px;
  background: var(--bg-primary);
  color: var(--text-primary);
  overflow: hidden;
}

/* Top Bar */
.topbar {
  height: 48px;
  background: var(--bg-tertiary);
  border-bottom: 1px solid var(--border);
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 16px;
}

.file-info {
  display: flex;
  align-items: center;
  gap: 8px;
}

#unsaved-indicator {
  color: var(--accent);
  font-size: 20px;
}

.actions button {
  background: transparent;
  border: 1px solid var(--border);
  color: var(--text-primary);
  padding: 6px 12px;
  border-radius: 2px;
  cursor: pointer;
  font-size: 13px;
  margin-left: 8px;
}

.actions button:hover {
  background: var(--bg-secondary);
  border-color: var(--accent);
}

/* IDE Container */
.ide-container {
  display: flex;
  height: calc(100vh - 48px);
}

.panel {
  background: var(--bg-primary);
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

.panel-header {
  height: 35px;
  background: var(--bg-secondary);
  border-bottom: 1px solid var(--border);
  padding: 0 12px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  font-weight: 600;
  text-transform: uppercase;
  font-size: 11px;
  letter-spacing: 0.5px;
  color: var(--text-secondary);
}

/* Tree View */
#tree-view {
  flex: 1;
  overflow-y: auto;
  padding: 8px 0;
}

.tree-node {
  cursor: pointer;
  user-select: none;
}

.tree-node-content {
  display: flex;
  align-items: center;
  padding: 4px 8px;
  padding-left: calc(8px + var(--level, 0) * 16px);
}

.tree-node-content:hover {
  background: var(--bg-secondary);
}

.tree-node-content.selected {
  background: var(--accent);
  color: white;
}

.tree-toggle {
  width: 16px;
  margin-right: 4px;
  font-size: 10px;
  transition: transform 0.2s;
}

.tree-node.expanded > .tree-node-content .tree-toggle {
  transform: rotate(90deg);
}

.tree-icon {
  margin-right: 6px;
  font-size: 14px;
}

.tree-label {
  flex: 1;
  font-size: 13px;
}

/* Split.js Gutters */
.gutter {
  background-color: var(--border);
  background-repeat: no-repeat;
  background-position: 50%;
}

.gutter.gutter-horizontal {
  cursor: col-resize;
  width: 8px;
}

.gutter.gutter-horizontal:hover {
  background-color: var(--accent);
}

/* CodeMirror Theme Override */
.cm-editor {
  height: 100%;
  font-size: 14px;
  font-family: 'Consolas', 'Courier New', monospace;
}

.cm-scroller {
  font-family: 'Consolas', 'Courier New', monospace;
}

/* Scrollbars */
::-webkit-scrollbar {
  width: 14px;
  height: 14px;
}

::-webkit-scrollbar-track {
  background: var(--bg-primary);
}

::-webkit-scrollbar-thumb {
  background: #424242;
  border: 3px solid var(--bg-primary);
  border-radius: 7px;
}

::-webkit-scrollbar-thumb:hover {
  background: #4e4e4e;
}
```

---

## 📚 Inspiration & Reference Projects

### 1. **Google YAML UI Editor**
- GitHub: https://github.com/google/yaml-ui-editor
- Uses JSON Schema to auto-generate forms
- Backend: Spring Boot with JGit
- Frontend: JSON Editor library
- **Key Takeaway:** Schema-driven form generation

### 2. **Monaco YAML**
- GitHub: https://github.com/remcohaszing/monaco-yaml
- Adds YAML language support to Monaco Editor
- JSON Schema-based validation and autocomplete
- **Key Takeaway:** Schema validation in the editor

### 3. **Ace Editor**
- Website: https://ace.c9.io/
- Used in Cloud9 IDE, GitHub, and many others
- 110+ languages, 20+ themes
- **Alternative to CodeMirror** if you prefer it

### 4. **Golden Layout**
- Website: https://golden-layout.com/
- Advanced docking system
- Used in Bloomberg terminals
- **For future enhancement** when you want draggable panels

---

## 🚀 Quick Start: Minimal Proof of Concept

Want to see it in action quickly? Here's a minimal single-file demo:

```html
<!DOCTYPE html>
<html>
<head>
  <title>IDE Proof of Concept</title>
  <style>
    body { margin: 0; font-family: system-ui; }
    .container { display: flex; height: 100vh; }
    .split { overflow: auto; padding: 20px; }
    #tree { background: #f5f5f5; }
    #yaml { background: #1e1e1e; color: #d4d4d4; font-family: monospace; }
  </style>
</head>
<body>
  <div class="container">
    <div id="tree" class="split">Tree View</div>
    <div id="editor" class="split">Visual Editor</div>
    <div id="yaml" class="split">YAML Editor</div>
  </div>

  <script src="https://cdn.jsdelivr.net/npm/split.js@1.6.5/dist/split.min.js"></script>
  <script>
    Split(['#tree', '#editor', '#yaml'], {
      sizes: [20, 50, 30],
      minSize: 200
    });
  </script>
</body>
</html>
```

Save this as `poc.html` and open it. You'll see a three-pane layout with resizable gutters!

---

## 📊 Comparison Matrix

| Component | Library | Size | License | Pros | Cons |
|-----------|---------|------|---------|------|------|
| **Code Editor** | CodeMirror 6 | 300KB | MIT | Modular, YAML support, mobile | Learning curve |
| | Monaco | 5-10MB | MIT | VS Code features | Heavy, complex setup |
| | Ace | 500KB | BSD | Mature, feature-rich | Older architecture |
| **Split Panes** | Split.js | 2KB | MIT | Tiny, simple | Basic features only |
| | Golden Layout | 200KB | MIT | Advanced docking | Complex API |
| **Tree View** | js-treeview | 5KB | MIT | Simple, events | Limited features |
| | vanillatree | 10KB | MIT | Context menus, DnD | More complex |

---

## 🎯 Final Recommendation

### Core Stack (Recommended)
1. **CodeMirror 6** - Code editor with YAML support
2. **Split.js** - Resizable panes
3. **js-treeview** - Tree navigation
4. **Your existing code** - Visual form editor

### Why This Stack?
- ✅ **100% Vanilla JavaScript** - No build process needed
- ✅ **Lightweight** - Total ~350KB (vs 10MB+ for Monaco-based solution)
- ✅ **CDN-ready** - Users can still open HTML file directly
- ✅ **Mobile-friendly** - Works on tablets
- ✅ **MIT Licensed** - No licensing concerns
- ✅ **Modular** - Easy to swap components later

### Total Implementation Effort
- **Phase 1 (Layout):** 1-2 days
- **Phase 2 (YAML Editor):** 2-3 days
- **Phase 3 (Tree View):** 2-3 days
- **Phase 4 (Sync Logic):** 3-4 days
- **Total:** ~2 weeks for full IDE-like interface

---

## 🔗 Quick Links

- **CodeMirror 6:** https://codemirror.net/
- **Split.js:** https://split.js.org/
- **js-treeview:** https://github.com/justinchmura/js-treeview
- **vanillatree:** https://github.com/vincenthyz/vanillatree
- **Monaco Editor:** https://microsoft.github.io/monaco-editor/
- **Ace Editor:** https://ace.c9.io/
- **Golden Layout:** https://golden-layout.com/

---

## 📝 Next Steps

1. **Review this document** - Confirm the approach fits your needs
2. **Create proof of concept** - Test the three-pane layout with Split.js
3. **Integrate CodeMirror** - Add YAML editor to right panel
4. **Build tree view** - Implement file/validation navigation
5. **Wire up sync** - Connect all three panels with StateManager
6. **Polish UI** - Apply VS Code theme and refine UX

Let me know if you'd like me to start implementing any of these phases!
