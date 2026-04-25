#!/usr/bin/env python3
"""
Deploy Pokémon Card Investment Matrix to GitHub and Vercel
Run this script to push all files to GitHub and complete the deployment
"""

import os
import base64
import json
import subprocess
import sys
from pathlib import Path

def run_command(cmd, cwd=None):
    """Run a shell command"""
    try:
        result = subprocess.run(cmd, shell=True, cwd=cwd, capture_output=True, text=True)
        return result.returncode == 0, result.stdout + result.stderr
    except Exception as e:
        return False, str(e)

def main():
    print("=" * 60)
    print("🚀 Pokémon Card Investment Matrix - GitHub Deployment")
    print("=" * 60)
    print()

    # Configuration
    # Use current directory (script is in the project folder)
    project_dir = os.getcwd()
    token = "ghp_5K9ZHm1q92g64TNbJ6qG1PIf17Kf0hOPtLjb"

    print(f"📁 Project directory: {project_dir}")
    print()

    # Check if directory exists
    if not os.path.exists(project_dir):
        print(f"❌ Project directory not found: {project_dir}")
        sys.exit(1)

    # Change to project directory
    os.chdir(project_dir)

    # Initialize git repository
    print("📝 Initializing git repository...")
    success, output = run_command("git init")
    if success:
        print("✓ Git initialized")
    else:
        print("⚠ Git init message:", output[:100])

    # Configure git
    print("⚙️  Configuring git user...")
    run_command('git config user.name "Chin"')
    run_command('git config user.email "patipat.arc@gmail.com"')
    print("✓ Git configured")

    # Add all files
    print("📦 Adding all files...")
    success, output = run_command("git add .")
    if success:
        print("✓ Files staged")

    # Commit
    print("💾 Creating initial commit...")
    success, output = run_command('git commit -m "Initial commit: Pokémon Card Investment Matrix + Vercel config"')
    if success:
        print("✓ Commit created")
    else:
        print("⚠ Commit message:", output[:100])

    # Rename branch to main
    print("🔀 Setting up main branch...")
    run_command("git branch -M main")
    print("✓ Branch set to main")

    # Add remote
    print("🌐 Adding GitHub remote...")
    success, output = run_command("git remote add origin https://github.com/stoyreo/psa-collectr-matrix.git")
    print("✓ Remote added")

    # Try to push
    print()
    print("=" * 60)
    print("🚀 PUSHING CODE TO GITHUB")
    print("=" * 60)
    print()
    print("Attempting git push with token authentication...")
    print()

    # Try HTTPS with token
    remote_url = f"https://oauth2:{token}@github.com/stoyreo/psa-collectr-matrix.git"
    success, output = run_command(f'git push -u "{remote_url}" main')

    if success:
        print("✅ SUCCESS! Code pushed to GitHub!")
        print()
        print("=" * 60)
        print("📊 NEXT STEPS:")
        print("=" * 60)
        print()
        print("1. Go to: https://vercel.com/new")
        print("2. Click: 'Continue with GitHub'")
        print("3. Select: 'psa-collectr-matrix'")
        print("4. Click: 'Deploy'")
        print()
        print("✨ Your live dashboard will be ready in ~2 minutes!")
        print()
        print("Share this URL with your team:")
        print("https://psa-collectr-matrix-xxx.vercel.app")
        print()
        return 0
    else:
        print("⚠ Push attempt output:")
        print(output)
        print()
        print("=" * 60)
        print("⚠️  ALTERNATIVE: Manual GitHub Upload")
        print("=" * 60)
        print()
        print("If git push fails, use GitHub Desktop (fastest method):")
        print()
        print("1. Download: https://desktop.github.com/")
        print("2. Clone: stoyreo/psa-collectr-matrix")
        print("3. Copy files from this directory into cloned folder:")
        print("   - api/")
        print("   - public/")
        print("   - scripts/")
        print("   - vercel.json")
        print("   - requirements.txt")
        print("   - My Collection CSV - 19.csv")
        print("4. Commit and Push in GitHub Desktop")
        print("5. Then import to Vercel as above")
        print()
        return 1

if __name__ == "__main__":
    exit_code = main()
    print()
    input("Press Enter to exit...")
    sys.exit(exit_code)
