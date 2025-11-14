# YAML Configuration Compatibility Guide

This guide ensures your YAML configuration files work correctly on both **Windows** and **Linux** systems.

## ✅ Correct YAML Structure

The Data Validation Tool expects this structure:

```yaml
validation_job:
  name: "Your Validation Job Name"
  files:
    - name: "file1"
      path: "data/file1.csv"
      format: "csv"
      validations:
        - type: "EmptyFileCheck"
          severity: "ERROR"
          params: {}
        - type: "MandatoryFieldCheck"
          severity: "ERROR"
          params:
            fields:
              - "id"
              - "name"
    - name: "file2"
      path: "data/file2.csv"
      format: "csv"
      validations:
        - type: "UniqueKeyCheck"
          severity: "ERROR"
          params:
            key_fields:
              - "id"
  processing:
    chunk_size: 50000
    max_sample_failures: 100
    fail_fast: false
    log_level: INFO
```

### Key Points:
- ✅ `files:` is **nested under** `validation_job:`
- ✅ `processing:` is **nested under** `validation_job:`
- ✅ **No blank lines** within structures
- ✅ **No standalone comment lines** (comments inline only)
- ✅ **2-space indentation** (never tabs)
- ✅ **Consistent indentation** throughout

## ❌ Common Windows Compatibility Issues

### Issue 1: Incorrect Nesting

**WRONG:**
```yaml
validation_job:
  name: "My Job"

settings:          # ❌ At root level
  chunk_size: 5000

files:             # ❌ At root level
  - name: "data"
```

**CORRECT:**
```yaml
validation_job:
  name: "My Job"
  files:           # ✅ Nested
    - name: "data"
  processing:      # ✅ Nested
    chunk_size: 5000
```

### Issue 2: Blank Lines in Structures

**WRONG:**
```yaml
validation_job:
  name: "My Job"

  files:           # ❌ Blank line before
    - name: "data"
      path: "file.csv"

      validations: # ❌ Blank line before
        - type: "EmptyFileCheck"

        - type: "MandatoryFieldCheck"  # ❌ Blank line before
```

**CORRECT:**
```yaml
validation_job:
  name: "My Job"
  files:
    - name: "data"
      path: "file.csv"
      validations:
        - type: "EmptyFileCheck"
          severity: "ERROR"
        - type: "MandatoryFieldCheck"
          severity: "ERROR"
```

### Issue 3: Standalone Comment Lines

**WRONG:**
```yaml
validations:
  - type: "EmptyFileCheck"
    severity: "ERROR"
    # This is a standalone comment  ❌
    # It causes Windows parse errors  ❌

  - type: "MandatoryFieldCheck"
```

**CORRECT:**
```yaml
validations:
  - type: "EmptyFileCheck"  # Inline comments work fine
    severity: "ERROR"
  - type: "MandatoryFieldCheck"
    severity: "ERROR"
```

### Issue 4: Tab Characters

**WRONG:**
```yaml
validation_job:
→ name: "My Job"     # ❌ Tab character (shown as →)
```

**CORRECT:**
```yaml
validation_job:
  name: "My Job"     # ✅ 2 spaces
```

## 🪟 Windows-Specific Considerations

### File Paths

Use **forward slashes** for maximum compatibility:

```yaml
# ✅ RECOMMENDED (works on Windows AND Linux)
files:
  - name: "data"
    path: "C:/Users/YourName/data/file.csv"

  - name: "relative"
    path: "data/subfolder/file.csv"

# ✅ Alternative: Single quotes with backslashes
files:
  - name: "data"
    path: 'C:\Users\YourName\data\file.csv'

# ❌ WRONG: Double quotes need escaping
files:
  - name: "data"
    path: "C:\Users\YourName\data\file.csv"  # Will fail!

# ✅ CORRECT: Double backslashes
files:
  - name: "data"
    path: "C:\\Users\\YourName\\data\\file.csv"
```

### Line Endings

- Windows: CRLF (`\r\n`)
- Linux: LF (`\n`)
- **Both work** in modern YAML parsers, but LF is preferred

### Case Sensitivity

- **Windows:** Paths are case-insensitive (`Data.csv` = `data.csv`)
- **Linux:** Paths are case-sensitive (`Data.csv` ≠ `data.csv`)
- **Recommendation:** Always use lowercase for portability

## 🛠️ Config Builder Generated YAML

The Config Builder tool (`config-builder/index.html`) now generates Windows/Linux compatible YAML automatically:

- ✅ Correct nesting structure
- ✅ No blank lines in structures
- ✅ Inline comments only
- ✅ Consistent 2-space indentation
- ✅ Forward slashes in paths work everywhere

## 📋 Validation Checklist

Before running your YAML on Windows, verify:

- [ ] `files:` is nested under `validation_job:`
- [ ] `processing:` is nested under `validation_job:` (not `settings:`)
- [ ] No blank lines within validation lists
- [ ] No standalone comment lines
- [ ] All indentation uses spaces (not tabs)
- [ ] File paths use forward slashes or properly escaped backslashes
- [ ] No trailing whitespace on blank lines

## 🧪 Testing Your YAML

Test your YAML file before deployment:

```python
import yaml

with open('your_config.yaml', 'r') as f:
    try:
        config = yaml.safe_load(f)
        print("✅ YAML is valid!")

        # Verify structure
        assert 'validation_job' in config
        assert 'files' in config['validation_job']
        assert 'processing' in config['validation_job']
        print("✅ Structure is correct!")

    except yaml.YAMLError as e:
        print(f"❌ Error: {e}")
```

## 📚 Related Documentation

- [Getting Started Guide](GETTING_STARTED.md)
- [User Guide](USER_GUIDE.md)
- [Advanced Guide](ADVANCED_GUIDE.md)
- [Examples](EXAMPLES.md)

## 🆘 Troubleshooting

**Error: "unexpected data scalar" at line X**
- Check for blank lines with trailing whitespace
- Verify indentation is consistent (2 spaces)
- Remove standalone comment lines

**Error: "Configuration must specify at least one file"**
- Ensure `files:` is nested under `validation_job:`
- Not at root level

**Error: "expected <block end>, but found..."**
- Check for tab characters (use spaces)
- Verify closing of all lists/maps

## 📝 Summary

**Golden Rules for Windows/Linux Compatibility:**

1. Nest `files:` and `processing:` under `validation_job:`
2. No blank lines within structures
3. Use 2-space indentation (never tabs)
4. Comments inline only (not standalone)
5. Forward slashes in paths work everywhere
6. Test with `yaml.safe_load()` before deployment

Following these guidelines ensures your YAML configuration files work perfectly on **both Windows and Linux**! 🚀
