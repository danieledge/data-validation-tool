# DataGuard Studio - Brand Guidelines

**Official Name:** DataGuard Studio
**Tagline:** *Your IDE for data quality*
**Version:** 1.0.0
**Created:** January 2025

---

## 📝 Brand Identity

### Name
**DataGuard Studio**

- Always use "DataGuard" as one word (not "Data Guard")
- Always capitalize both words: "DataGuard Studio"
- Short form: "DataGuard" or "DGS"
- Never: "data guard studio", "DataguardStudio", "Data Guard"

### Tagline Options

**Primary:** *Your IDE for data quality*

**Alternatives:**
- *Professional data validation made simple*
- *Guard your data pipelines with confidence*
- *The IDE for data quality engineers*
- *Build bulletproof validation rules*

---

## 🎨 Visual Identity

### Logo Concept

```
╔═══════════════════════════════════════╗
║                                       ║
║    ╔═╗  ┌─┐  ┌─┐                    ║
║    ║ ║  │ │  └─┐                     ║
║    ║ ║  │ │  ┌─┘                     ║
║    ╚═╝  └─┘  └─┘                     ║
║                                       ║
║    D A T A G U A R D                  ║
║    ─────────────────                  ║
║    S T U D I O                        ║
║                                       ║
╚═══════════════════════════════════════╝
```

### Shield Icon

```
        ╱╲
       ╱  ╲
      ╱ ✓  ╲
     ╱  DG  ╲
    ╱────────╲
   ╱          ╲
  ╱____________╲

  Shield with checkmark
  "DG" or "✓" in center
```

### Simplified Icon (Favicon/Small Sizes)

```
┌─────┐
│ 🛡️  │  Shield emoji
└─────┘

OR

┌─────┐
│ ✓D  │  Checkmark + D
└─────┘
```

---

## 🎨 Color Palette

### Primary Colors

**DataGuard Dark** (Main background)
```css
--dgs-dark: #0F172A;
RGB: 15, 23, 42
```

**DataGuard Blue** (Primary accent)
```css
--dgs-blue: #60A5FA;
RGB: 96, 165, 250
```

**DataGuard Green** (Success/Shield accent)
```css
--dgs-green: #34D399;
RGB: 52, 211, 153
```

### Secondary Colors

**Surface Dark**
```css
--dgs-surface: #1E293B;
RGB: 30, 41, 59
```

**Border**
```css
--dgs-border: #3E3E42;
RGB: 62, 62, 66
```

**Text Primary**
```css
--dgs-text: #F8FAFC;
RGB: 248, 250, 252
```

**Text Secondary**
```css
--dgs-text-muted: #94A3B8;
RGB: 148, 163, 184
```

### Status Colors

**Error**
```css
--dgs-error: #F48771;
RGB: 244, 135, 113
```

**Warning**
```css
--dgs-warning: #FBBF24;
RGB: 251, 191, 36
```

**Success**
```css
--dgs-success: #34D399;
RGB: 52, 211, 153
```

**Info**
```css
--dgs-info: #60A5FA;
RGB: 96, 165, 250
```

---

## 🎨 Color Usage Examples

### Gradient Combinations

**Primary Gradient** (Headers, CTAs)
```css
background: linear-gradient(135deg, #60A5FA 0%, #34D399 100%);
```

**Dark Gradient** (Panels)
```css
background: linear-gradient(180deg, #1E293B 0%, #0F172A 100%);
```

**Subtle Accent** (Hover states)
```css
background: linear-gradient(135deg, rgba(96, 165, 250, 0.1) 0%, rgba(52, 211, 153, 0.1) 100%);
```

---

## 📐 Typography

### Font Stack

**Sans-Serif (UI)**
```css
font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, system-ui, sans-serif;
```

**Monospace (Code/YAML)**
```css
font-family: 'Consolas', 'SF Mono', 'Monaco', 'Courier New', monospace;
```

### Font Sizes

| Element | Size | Weight | Use Case |
|---------|------|--------|----------|
| Page Title | 28px | 600 | Main headings |
| Section Header | 22px | 600 | Panel headers |
| Subsection | 18px | 600 | Card titles |
| Body Text | 14px | 400 | Main content |
| Small Text | 13px | 400 | Descriptions |
| Tiny Text | 11px | 500 | Labels, tags |
| Code | 14px | 400 | YAML, code blocks |

### Letter Spacing

- Headers: `-0.02em` (tighter)
- Labels: `0.05em` (wider, uppercase)
- Body: `0` (normal)
- Code: `0` (normal)

---

## 🎯 Brand Voice

### Tone

**Professional** - Enterprise-ready, trustworthy
**Clear** - No jargon, straightforward
**Confident** - "Guard your data" not "Try to guard"
**Helpful** - Guides users, doesn't lecture

### Writing Style

**Do:**
- Use active voice: "DataGuard validates your data"
- Be direct: "Add validation" not "Would you like to add?"
- Use "your" and "you": "Guard your pipelines"
- Technical but accessible

**Don't:**
- Use passive voice: "Data is validated by..."
- Be vague: "Maybe check your data"
- Use corporate speak: "Leverage synergies"
- Over-explain: Keep it concise

### Example Messages

**Good:**
✅ "DataGuard found 3 validation errors"
✅ "Your configuration is ready to download"
✅ "Add a validation check to protect your data"

**Avoid:**
❌ "The system has detected validation issues"
❌ "It appears that your configuration may be ready"
❌ "Consider adding validation to improve quality"

---

## 🖼️ UI Elements

### Buttons

**Primary Button** (Main actions: Save, Add, Download)
```css
background: linear-gradient(135deg, #60A5FA 0%, #3B82F6 100%);
color: #FFFFFF;
border: none;
border-radius: 6px;
padding: 10px 20px;
font-weight: 600;
box-shadow: 0 4px 12px rgba(96, 165, 250, 0.3);
```

**Secondary Button** (Cancel, Close)
```css
background: transparent;
color: #94A3B8;
border: 2px solid #3E3E42;
border-radius: 6px;
padding: 8px 18px;
font-weight: 500;
```

**Danger Button** (Delete)
```css
background: #F48771;
color: #FFFFFF;
border: none;
border-radius: 6px;
padding: 10px 20px;
font-weight: 600;
```

### Cards/Panels

```css
background: #1E293B;
border: 1px solid #3E3E42;
border-radius: 8px;
padding: 20px;
box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
```

### Input Fields

```css
background: #0F172A;
color: #F8FAFC;
border: 2px solid #3E3E42;
border-radius: 6px;
padding: 10px 14px;
font-size: 14px;

/* Focus state */
border-color: #60A5FA;
box-shadow: 0 0 0 3px rgba(96, 165, 250, 0.1);
```

---

## 🏷️ Validation Type Icons

Standard icon set for validation types:

```
📄 EmptyFileCheck
📊 RowCountRangeCheck
📝 MandatoryFieldCheck
🔑 UniqueKeyCheck
📅 DateFormatCheck
📏 RangeCheck
🔗 ForeignKeyCheck
🎯 AcceptedValuesCheck
📧 EmailFormatCheck
🔢 NumericRangeCheck
✅ BooleanCheck
📱 PhoneFormatCheck
🌐 URLFormatCheck
🔤 RegexPatternCheck
🎨 SchemaValidation
📍 GeoCoordinateCheck
💰 CurrencyFormatCheck
⏰ TimestampCheck
🆔 UUIDCheck
📦 JSONSchemaCheck
🔐 HashCheck
```

---

## 📄 File Naming Conventions

### HTML Files
- `index.html` - Main landing/home
- `ide.html` - IDE interface (when built)
- `index-clarity.html` - Current enhanced version

### CSS Files
- `dataguard-theme.css` - Main theme
- `ide-layout.css` - IDE-specific styles
- `components.css` - Reusable components

### JavaScript Files
- `dataguard.js` - Main app
- `dataguard-ide.js` - IDE version
- `validation-types.js` - Validation definitions
- `yaml-parser.js` - YAML handling

---

## 🌐 Web Presence

### Domain Options

**Primary:** `dataguard.studio`
**Alternatives:**
- `dataguardstudio.com`
- `dataguard.dev`
- `dgs.dev`

### Social Media Handles

- GitHub: `/dataguard-studio`
- Twitter: `@DataGuardStudio`
- LinkedIn: `/company/dataguard-studio`

### Email

- General: `hello@dataguard.studio`
- Support: `support@dataguard.studio`
- Security: `security@dataguard.studio`

---

## 📦 Product Variants

### Free/Open Source
**DataGuard Studio** (Community Edition)
- Full-featured config builder
- Local use only
- MIT License

### Future Editions (Potential)

**DataGuard Studio Pro**
- Cloud sync
- Team collaboration
- Advanced templates

**DataGuard Studio Enterprise**
- SSO integration
- Audit logs
- Custom validation types

---

## 📋 Tagline for Different Contexts

**Website Header:**
> DataGuard Studio - Your IDE for data quality

**GitHub Description:**
> Professional IDE for building YAML data validation configurations. Guard your data pipelines with confidence.

**Meta Description (SEO):**
> DataGuard Studio is a free, open-source IDE for creating data validation configurations. Build, test, and deploy YAML validation rules with an intuitive visual interface.

**One-Liner (Elevator Pitch):**
> DataGuard Studio is like VS Code for data quality - a professional IDE that makes building validation rules as easy as writing code.

---

## 🎯 Brand Positioning

### What DataGuard Studio Is:
- ✅ Professional IDE for data validation
- ✅ Visual YAML configuration builder
- ✅ Data quality engineering tool
- ✅ Developer-friendly validation designer

### What DataGuard Studio Is Not:
- ❌ A database management tool
- ❌ A data pipeline orchestrator
- ❌ A data visualization platform
- ❌ Only for non-technical users

### Target Audience:
1. **Data Engineers** - Build validation rules for pipelines
2. **Data Analysts** - Define quality checks visually
3. **QA Engineers** - Validate data quality
4. **Platform Engineers** - Standardize validation configs

---

## 🚀 Launch Messaging

### Announcement Template

**Title:**
Introducing DataGuard Studio - Your IDE for Data Quality

**Body:**
We're excited to announce DataGuard Studio, a professional IDE for building data validation configurations.

Just like VS Code revolutionized code editing, DataGuard Studio brings the same IDE experience to data quality engineering. Build validation rules visually or in YAML, sync changes instantly, and guard your data pipelines with confidence.

**Key Features:**
- 🎨 Visual validation builder
- 💻 YAML code editor with IntelliSense
- 🌳 Hierarchical file navigation
- 🔄 Bi-directional sync
- 📦 21+ built-in validation types
- 🎯 Template library
- 💾 Auto-save to localStorage
- 📱 Mobile-friendly

Try it now: [link]

---

## 📐 ASCII Art Logo

### Full Logo (for terminals, docs)

```
╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║     ██████╗  █████╗ ████████╗ █████╗  ██████╗ ██╗   ██╗ █████╗ ██████╗ ██████╗
║     ██╔══██╗██╔══██╗╚══██╔══╝██╔══██╗██╔════╝ ██║   ██║██╔══██╗██╔══██╗██╔══██╗
║     ██║  ██║███████║   ██║   ███████║██║  ███╗██║   ██║███████║██████╔╝██║  ██║
║     ██║  ██║██╔══██║   ██║   ██╔══██║██║   ██║██║   ██║██╔══██║██╔══██╗██║  ██║
║     ██████╔╝██║  ██║   ██║   ██║  ██║╚██████╔╝╚██████╔╝██║  ██║██║  ██║██████╔╝
║     ╚═════╝ ╚═╝  ╚═╝   ╚═╝   ╚═╝  ╚═╝ ╚═════╝  ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═════╝
║                                                               ║
║     ███████╗████████╗██╗   ██╗██████╗ ██╗ ██████╗            ║
║     ██╔════╝╚══██╔══╝██║   ██║██╔══██╗██║██╔═══██╗           ║
║     ███████╗   ██║   ██║   ██║██║  ██║██║██║   ██║           ║
║     ╚════██║   ██║   ██║   ██║██║  ██║██║██║   ██║           ║
║     ███████║   ██║   ╚██████╔╝██████╔╝██║╚██████╔╝           ║
║     ╚══════╝   ╚═╝    ╚═════╝ ╚═════╝ ╚═╝ ╚═════╝            ║
║                                                               ║
║                  Your IDE for data quality                    ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝
```

### Compact Logo (for headers)

```
╔╦╗╔═╗╔╦╗╔═╗╔═╗╦ ╦╔═╗╦═╗╔╦╗  ╔═╗╔╦╗╦ ╦╔╦╗╦╔═╗
 ║║╠═╣ ║ ╠═╣║ ╦║ ║╠═╣╠╦╝ ║║  ╚═╗ ║ ║ ║ ║║║║ ║
═╩╝╩ ╩ ╩ ╩ ╩╚═╝╚═╝╩ ╩╩╚══╩╝  ╚═╝ ╩ ╚═╝═╩╝╩╚═╝
```

### Minimal (for CLI)

```
[DGS] DataGuard Studio
```

---

## 📜 License & Copyright

**Copyright:** © 2025 DataGuard Studio Contributors
**License:** MIT License
**Repository:** https://github.com/danieledge/data-validation-tool

---

## 🔄 Version History

- **v1.0.0** (January 2025) - Initial branding
  - Chosen name: DataGuard Studio
  - Established color palette
  - Created brand guidelines
  - Defined visual identity

---

*This brand guide is a living document and will evolve as DataGuard Studio grows.*
