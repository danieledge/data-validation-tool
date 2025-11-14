# DataGuard Studio

> **Your IDE for Data Quality**

A professional, browser-based IDE for building YAML data validation configurations. Create, edit, and manage validation rules with an intuitive visual interface or direct YAML editing.

![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Status](https://img.shields.io/badge/status-production-success.svg)

---

## 🛡️ What is DataGuard Studio?

DataGuard Studio is a free, open-source IDE that makes building data validation configurations as easy as writing code. Whether you're a data engineer crafting pipeline validations or a data analyst defining quality checks, DataGuard Studio provides the perfect interface.

**Think VS Code for data quality** - that's DataGuard Studio.

---

## ✨ Key Features

### Visual Validation Builder
- 📝 Form-based validation creation
- 🎨 21+ built-in validation types
- 🔍 Smart field selectors
- 📊 Parameter validation and preview

### YAML Editor
- 💻 Syntax highlighting
- ✅ Real-time validation
- 📋 Auto-formatting
- 🔄 Bi-directional sync with visual editor (coming soon)

### IDE-Like Experience
- 🌳 Hierarchical file navigation
- ⚡ Split-pane layout with resizable panels (coming soon)
- 🎯 Quick validation picker
- ⌨️ Keyboard shortcuts

### Smart Features
- 💾 Auto-save to localStorage
- ↩️ Undo/Redo support
- 📦 Template library
- 🔄 Import/Export YAML
- 🎨 Dark theme optimized for long sessions

---

## 🚀 Quick Start

### Option 1: Open Directly (No Installation)

1. Download or clone this repository
2. Open `index-clarity.html` in your browser
3. Start building validations!

```bash
# Clone the repo
git clone https://github.com/danieledge/data-validation-tool.git
cd data-validation-tool/config-builder

# Open in browser (macOS)
open index-clarity.html

# Open in browser (Linux)
xdg-open index-clarity.html

# Open in browser (Windows)
start index-clarity.html
```

### Option 2: Serve Locally

```bash
# Python 3
python3 -m http.server 8000

# Node.js
npx serve .

# PHP
php -S localhost:8000

# Then visit: http://localhost:8000/index-clarity.html
```

---

## 📖 Usage Guide

### Creating Your First Validation

1. **Add a File**
   - Click "➕ Add File" in the Files section
   - Enter file details (name, path, format)
   - Click "Add File"

2. **Add Validations**
   - Select your file in the list
   - Click "➕ Add Validation"
   - Choose a validation type (e.g., "Mandatory Field Check")
   - Configure parameters (select fields, set severity)
   - Click "Add Validation"

3. **Download Configuration**
   - Click "⬇️ Download Configuration" in the Summary section
   - Save the YAML file
   - Use it with your data validation framework

### Validation Types

DataGuard Studio supports 21 validation types across 5 categories:

**File-Level Checks:**
- 📄 Empty File Check
- 📊 Row Count Range Check

**Schema Validation:**
- 🎨 Schema Completeness Check
- 📋 Schema Accuracy Check
- 🔄 Column Order Check
- 📝 Column Name Format Check

**Field-Level Checks:**
- ⚠️ Mandatory Field Check
- 🔑 Unique Key Check
- 🔢 Numeric Range Check
- 📅 Date Format Check
- 📧 Email Format Check
- 📱 Phone Format Check
- 🌐 URL Format Check
- ✅ Boolean Check
- 💰 Currency Format Check
- 🆔 UUID Check
- 🎯 Accepted Values Check
- 🔤 Regex Pattern Check

**Record-Level Checks:**
- 🔐 Hash Check

**Cross-File Checks:**
- 🔗 Foreign Key Check
- 📦 JSON Schema Check

---

## 🎨 Interface Overview

```
┌──────────────────────────────────────────────────────────────┐
│ DataGuard Studio                                    [Save]   │
├────────────────┬─────────────────────────────────────────────┤
│                │                                             │
│ 📁 Files       │  📝 Visual Editor                           │
│ ├─ File 1      │  ┌─────────────────────────────────────┐   │
│ │  └─ Checks   │  │ Mandatory Field Check               │   │
│ │     ├─ Check1│  │ Name: [Customer Required Fields]    │   │
│ │     └─ Check2│  │ Fields: ☑ email  ☑ name             │   │
│ └─ File 2      │  │ Severity: ⚫ ERROR  ○ WARNING       │   │
│                │  │ [Save] [Cancel]                     │   │
│ ⚙️ Settings    │  └─────────────────────────────────────┘   │
│                │                                             │
│ 📊 Summary     │  📋 YAML Preview                            │
│                │  validation_job:                            │
│                │    name: "My Validation"                    │
│                │    files:                                   │
│                │      - name: "customers.csv"                │
└────────────────┴─────────────────────────────────────────────┘
```

---

## 🔧 Configuration

### Job Settings

- **Job Name**: Give your validation job a descriptive name
- **Description**: Add context about what this validates

### Processing Options

- **Chunk Size**: Rows processed at once (default: 10,000)
- **Max Sample Failures**: Stop after N errors (default: 100)
- **Fail Fast**: Stop on first error (default: false)
- **Log Level**: INFO, WARNING, ERROR, DEBUG

---

## 📦 Templates

DataGuard Studio includes pre-built templates:

### Essential File Checks
Basic validations every file should have:
- Empty File Check
- Row Count Range Check

### Data Quality Basics
Common quality checks:
- Mandatory Field Check
- Unique Key Check
- Date Format Check

### E-commerce
Validations for product/customer data:
- Product catalog validations
- Customer record checks
- Order validation rules

### Financial Data
Strict validations for financial records:
- Currency format checks
- Numeric range validations
- Mandatory field requirements

---

## ⌨️ Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Ctrl+S` | Download configuration |
| `Ctrl+Z` | Undo last change |
| `Ctrl+Shift+Z` | Redo |
| `Ctrl+K` | Search (coming soon) |
| `Ctrl+Shift+P` | Add validation (coming soon) |

---

## 🛠️ Advanced Features

### Import Existing YAML

1. Click "📂 Import YAML"
2. Paste your YAML configuration
3. Click "Import"
4. DataGuard Studio will parse and load your config

### Export Options

- **Download YAML**: Get the configuration file
- **Copy to Clipboard**: Copy YAML to paste elsewhere
- **Share URL**: Generate shareable URL (localStorage based)

### Undo/Redo

DataGuard Studio tracks up to 50 changes. Use the undo/redo buttons or keyboard shortcuts to navigate your edit history.

---

## 🎯 Roadmap

### Coming Soon (v1.1)

- [ ] **IDE Mode**: Three-pane layout with tree navigation
- [ ] **YAML Editor**: CodeMirror integration with syntax highlighting
- [ ] **Bi-directional Sync**: Edit YAML directly, sync to visual editor
- [ ] **Quick Picker**: VS Code-style command palette
- [ ] **Validation Testing**: Test validations against sample data

### Future (v2.0)

- [ ] **Cloud Sync**: Save configurations to cloud storage
- [ ] **Team Collaboration**: Share and collaborate on configs
- [ ] **Custom Validations**: Define your own validation types
- [ ] **Validation Library**: Community-shared validation templates
- [ ] **CI/CD Integration**: GitHub Actions, GitLab CI support

---

## 📚 Documentation

- [Brand Guidelines](../BRANDING.md)
- [IDE Architecture Research](IDE_ARCHITECTURE_RESEARCH.md)
- [UI/UX Improvements](UI_IMPROVEMENTS.md)
- [Validation UI Mockups](VALIDATION_UI_MOCKUPS.md)
- [Refactoring Guide](REFACTORING.md)

---

## 🤝 Contributing

DataGuard Studio is open source and welcomes contributions!

### Ways to Contribute

- 🐛 Report bugs
- 💡 Suggest features
- 📖 Improve documentation
- 🎨 Design improvements
- 💻 Code contributions

### Development Setup

```bash
# Clone the repository
git clone https://github.com/danieledge/data-validation-tool.git
cd data-validation-tool/config-builder

# Make your changes
# Test by opening index-clarity.html in your browser

# Commit your changes
git add .
git commit -m "Description of changes"
git push origin main
```

---

## 📄 License

DataGuard Studio is released under the MIT License. See [LICENSE](../LICENSE) for details.

---

## 🙏 Acknowledgments

- Built with vanilla JavaScript (no frameworks!)
- Inspired by VS Code, IntelliJ, and modern IDEs
- Uses Material Design 3 color system
- Font: Google Roboto & Roboto Mono

---

## 📧 Support

- **Issues**: [GitHub Issues](https://github.com/danieledge/data-validation-tool/issues)
- **Discussions**: [GitHub Discussions](https://github.com/danieledge/data-validation-tool/discussions)
- **Email**: hello@dataguard.studio (future)

---

## 🌟 Star Us!

If DataGuard Studio helps you build better data validation, give us a star on GitHub! ⭐

---

<div align="center">

**DataGuard Studio** - *Your IDE for Data Quality*

Made with ❤️ by the DataGuard Studio team

[Website](https://dataguard.studio) • [GitHub](https://github.com/danieledge/data-validation-tool) • [Documentation](../docs)

</div>
