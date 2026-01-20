# Pushing to GitHub

## Prerequisites

1. **Install Git** (if not already installed):
   - Download from: https://git-scm.com/download/win
   - Run the installer and follow the setup wizard
   - Restart PowerShell after installation

2. **Create a GitHub account** (if you don't have one):
   - Go to https://github.com/signup

---

## Steps to Push This Project to GitHub

### 1. Create a new repository on GitHub

1. Go to https://github.com/new
2. Repository name: `freelancer-finance-dashboard`
3. Description: `Multi-page React web app for freelance income/expense tracking`
4. Choose **Public** or **Private**
5. **Do NOT** initialize with README, .gitignore, or license (we already have these)
6. Click **Create repository**

You'll see instructions like:
```
git remote add origin https://github.com/YOUR-USERNAME/freelancer-finance-dashboard.git
git branch -M main
git push -u origin main
```

### 2. Initialize & Commit Locally

```powershell
cd "C:\Users\mseth\Documents\.github\freelancer-finance-dashboard"

# Initialize git
git init

# Configure your git identity (first time only)
git config user.email "your-email@example.com"
git config user.name "Your Name"

# Stage all files
git add .

# Create initial commit
git commit -m "Initial commit: Freelancer Finance Dashboard with grey/shimmer theme"
```

### 3. Connect to GitHub & Push

Replace `YOUR-USERNAME` with your actual GitHub username:

```powershell
git remote add origin https://github.com/YOUR-USERNAME/freelancer-finance-dashboard.git
git branch -M main
git push -u origin main
```

You'll be prompted for authentication. Use one of:
- **GitHub Personal Access Token** (PAT) - recommended
  - Generate at: https://github.com/settings/tokens
  - Use token as password
- **GitHub CLI** - easiest option
  - Install from: https://cli.github.com
  - Run: `gh auth login`

### 4. Verify

Visit `https://github.com/YOUR-USERNAME/freelancer-finance-dashboard` to see your repo online.

---

## Future Updates

After the first push, updates are simple:

```powershell
cd "C:\Users\mseth\Documents\.github\freelancer-finance-dashboard"
git add .
git commit -m "Description of changes"
git push
```

---

## What Gets Pushed

✅ **Included:**
- All source files (`src/`)
- Config files (`package.json`, `vite.config.js`, etc.)
- Documentation (`README.md`, `DESIGN_UPDATES.md`)
- `.gitignore`

❌ **Excluded (by .gitignore):**
- `node_modules/` (can be reinstalled with `npm install`)
- `.env` files (keep secrets private)
- Build output (`dist/`)
- IDE files (`.vscode/`, `.idea/`)

---

## Need Help?

If you run into issues with authentication or git, check:
- Git is installed: `git --version`
- User configured: `git config --global user.name` and `git config --global user.email`
- Remote is set: `git remote -v`

Feel free to reach out if you hit any snags!
