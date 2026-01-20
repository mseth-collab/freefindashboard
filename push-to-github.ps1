param(
    [string]$GitHubUsername = "",
    [string]$RepositoryName = "freelancer-finance-dashboard",
    [string]$Email = "",
    [string]$Name = ""
)

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Freelancer Finance Dashboard - GitHub Setup" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Validate inputs
if (-not $GitHubUsername) {
    $GitHubUsername = Read-Host "Enter your GitHub username"
}

if (-not $Email) {
    $Email = Read-Host "Enter your email address"
}

if (-not $Name) {
    $Name = Read-Host "Enter your name (for git commits)"
}

$RepoURL = "https://github.com/$GitHubUsername/$RepositoryName.git"

Write-Host ""
Write-Host "Configuration:" -ForegroundColor Green
Write-Host "  GitHub Username: $GitHubUsername"
Write-Host "  Repository Name: $RepositoryName"
Write-Host "  Repository URL: $RepoURL"
Write-Host "  Email: $Email"
Write-Host "  Name: $Name"
Write-Host ""

# Change to project directory
$ProjectPath = "C:\Users\mseth\Documents\.github\freelancer-finance-dashboard"
Write-Host "Changing to project directory: $ProjectPath" -ForegroundColor Yellow
Set-Location $ProjectPath

# Check if git is available
Write-Host "Checking git installation..." -ForegroundColor Yellow
$gitVersion = git --version
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Git is not installed or not in PATH" -ForegroundColor Red
    Write-Host "Please install Git from https://git-scm.com/download/win" -ForegroundColor Red
    exit 1
}
Write-Host "✓ Git found: $gitVersion" -ForegroundColor Green
Write-Host ""

# Initialize git repo if not already initialized
Write-Host "Initializing git repository..." -ForegroundColor Yellow
if (-not (Test-Path ".git")) {
    git init
    Write-Host "✓ Git repository initialized" -ForegroundColor Green
} else {
    Write-Host "✓ Git repository already exists" -ForegroundColor Green
}
Write-Host ""

# Configure git user (local)
Write-Host "Configuring git user (local repository)..." -ForegroundColor Yellow
git config user.email $Email
git config user.name $Name
Write-Host "✓ Git user configured" -ForegroundColor Green
Write-Host ""

# Stage all files
Write-Host "Staging all files..." -ForegroundColor Yellow
git add .
$stagedFiles = git diff --cached --name-only | Measure-Object -Line
Write-Host "✓ Staged $($stagedFiles.Lines) files" -ForegroundColor Green
Write-Host ""

# Create initial commit
Write-Host "Creating initial commit..." -ForegroundColor Yellow
git commit -m "Initial commit: Freelancer Finance Dashboard with grey/shimmer fintech theme"
if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ Initial commit created" -ForegroundColor Green
} else {
    Write-Host "⚠ Commit may have failed or there were no changes to commit" -ForegroundColor Yellow
}
Write-Host ""

# Check if remote already exists
Write-Host "Checking remote configuration..." -ForegroundColor Yellow
$existingRemote = git remote get-url origin 2>$null
if ($existingRemote) {
    Write-Host "✓ Remote 'origin' already configured: $existingRemote" -ForegroundColor Green
    $changeRemote = Read-Host "Do you want to change the remote URL? (y/n)"
    if ($changeRemote -eq 'y') {
        git remote remove origin
        git remote add origin $RepoURL
        Write-Host "✓ Remote URL updated to: $RepoURL" -ForegroundColor Green
    }
} else {
    Write-Host "Adding remote repository..." -ForegroundColor Yellow
    git remote add origin $RepoURL
    Write-Host "✓ Remote repository added: $RepoURL" -ForegroundColor Green
}
Write-Host ""

# Rename branch to main if needed
Write-Host "Ensuring main branch..." -ForegroundColor Yellow
$currentBranch = git rev-parse --abbrev-ref HEAD
if ($currentBranch -ne "main") {
    git branch -M main
    Write-Host "✓ Branch renamed to 'main'" -ForegroundColor Green
} else {
    Write-Host "✓ Already on 'main' branch" -ForegroundColor Green
}
Write-Host ""

# Push to GitHub
Write-Host "Pushing to GitHub..." -ForegroundColor Yellow
Write-Host "Note: You will be prompted to authenticate with GitHub" -ForegroundColor Cyan
Write-Host ""

git push -u origin main

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "✅ SUCCESS! Project pushed to GitHub!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Your repository is now available at:" -ForegroundColor Green
    Write-Host "  $RepoURL" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Next steps:" -ForegroundColor Green
    Write-Host "  1. Visit the URL above to see your repository" -ForegroundColor White
    Write-Host "  2. Configure GitHub repository settings (Privacy, description, etc.)" -ForegroundColor White
    Write-Host "  3. For future updates, run: git add . && git commit -m 'message' && git push" -ForegroundColor White
    Write-Host ""
} else {
    Write-Host ""
    Write-Host "❌ ERROR: Failed to push to GitHub" -ForegroundColor Red
    Write-Host ""
    Write-Host "Troubleshooting:" -ForegroundColor Yellow
    Write-Host "  1. Verify you created the repository on GitHub: https://github.com/new" -ForegroundColor White
    Write-Host "  2. Repository name should be: $RepositoryName" -ForegroundColor White
    Write-Host "  3. Verify your GitHub username: $GitHubUsername" -ForegroundColor White
    Write-Host "  4. Check authentication (token or SSH key)" -ForegroundColor White
    Write-Host ""
    exit 1
}

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Setup Complete!" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
