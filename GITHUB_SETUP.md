# GitHub Setup Instructions

## Quick Method: Create Repository via GitHub Website

### Step 1: Create Repository on GitHub

1. Go to https://github.com/new
2. Set repository name: **data-validation-tool**
3. Set visibility: **Public**
4. **Do NOT** initialize with README, .gitignore, or license (we already have these)
5. Click "Create repository"

### Step 2: Push Your Local Repository

After creating the repository, run these commands:

```bash
cd /home/daniel/www/dqa/data-validation-tool

# Add GitHub as remote
git remote add origin https://github.com/danieledge/data-validation-tool.git

# Push to GitHub
git push -u origin main
```

You'll be prompted for GitHub credentials. Use a **Personal Access Token** instead of password.

### Step 3: Create Personal Access Token (if needed)

If you don't have a token:

1. Go to https://github.com/settings/tokens/new
2. Note: "Data Validation Tool - Repository Access"
3. Expiration: Choose your preference (90 days, 1 year, etc.)
4. Scopes: Check **repo** (Full control of private repositories)
5. Click "Generate token"
6. **Copy the token** (you won't see it again!)
7. When prompted for password during git push, paste the token

### Step 4: Verify

Visit https://github.com/danieledge/data-validation-tool to see your repository!

---

## Alternative: Install GitHub CLI

If you prefer command-line workflow:

```bash
# Install GitHub CLI
# On Debian/Ubuntu:
curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | sudo dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | sudo tee /etc/apt/sources.list.d/github-cli.list > /dev/null
sudo apt update
sudo apt install gh

# Authenticate
gh auth login
# Follow prompts: GitHub.com, HTTPS, Authenticate with browser

# Create and push repository
cd /home/daniel/www/dqa/data-validation-tool
gh repo create data-validation-tool --public --source=. --remote=origin --push
```

---

## Repository Details

- **Name**: data-validation-tool
- **Owner**: danieledge
- **Visibility**: Public
- **License**: MIT
- **URL**: https://github.com/danieledge/data-validation-tool

---

## What's Included

Your repository now contains:

✅ Complete Data Validation Framework (v0.1.0)
✅ 13+ built-in validation types
✅ CSV, Excel, Parquet support
✅ Interactive HTML reporting
✅ Full documentation (README, Getting Started)
✅ Example configurations
✅ Custom validation examples
✅ MIT License
✅ Proper .gitignore

---

## Next Steps After Push

1. **Add Repository Description**:
   - Go to repository settings
   - Description: "A robust data validation framework for pre-load data quality checks. Handles 200GB+ datasets with chunked processing, regex validation, and interactive HTML reports."

2. **Add Topics** (tags for discoverability):
   - `data-validation`
   - `data-quality`
   - `data-engineering`
   - `etl`
   - `python`
   - `csv`
   - `parquet`
   - `data-testing`

3. **Enable Issues** (if you want bug reports/feature requests):
   - Settings → Features → Issues (checkbox)

4. **Consider Adding**:
   - GitHub Actions for CI/CD
   - Code of Conduct
   - Contributing guidelines

---

## Sharing Your Repository

Once pushed, share your project:

```markdown
Check out my data validation framework: https://github.com/danieledge/data-validation-tool

A production-grade CLI tool for validating data quality before data loads.
Handles 200GB+ files with chunked processing, regex validation, and
interactive HTML reports.
```

---

## Troubleshooting

### Error: "remote origin already exists"
```bash
git remote remove origin
git remote add origin https://github.com/danieledge/data-validation-tool.git
```

### Error: "failed to push some refs"
```bash
git pull origin main --rebase
git push -u origin main
```

### Authentication Failed
Make sure you're using a Personal Access Token, not your GitHub password.
Passwords are no longer accepted for Git operations.

---

Need help? Open an issue at https://github.com/danieledge/data-validation-tool/issues
