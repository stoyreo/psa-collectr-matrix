#!/usr/bin/env python3
"""
Phase C.4-C.6 Deployment Automation
Automates: Git, GitHub, Vercel deployment, and monitoring
"""

import os
import subprocess
import sys
import json
from pathlib import Path
from datetime import datetime, timedelta

class DeploymentAutomation:
    def __init__(self):
        self.project_root = Path.cwd()
        self.web_dir = self.project_root / "web"
        self.ngrok_url = "https://automated-crummiest-puritan.ngrok-free.dev"
        self.api_key = "dev-secret-key-change-in-prod"
        
    def run_command(self, cmd, cwd=None):
        """Run shell command and return output"""
        try:
            result = subprocess.run(
                cmd, 
                shell=True, 
                cwd=cwd,
                capture_output=True,
                text=True,
                timeout=30
            )
            return result.returncode, result.stdout, result.stderr
        except subprocess.TimeoutExpired:
            return 1, "", "Command timed out"
    
    def phase_c4_git_setup(self):
        """Phase C.4: Initialize Git repository"""
        print("\n" + "="*70)
        print("🚀 PHASE C.4: Git Setup and GitHub Preparation")
        print("="*70)
        
        # Clean up old git
        print("\n📦 Cleaning up old git artifacts...")
        self.run_command("rm -rf .git", cwd=str(self.project_root))
        
        # Initialize git
        print("🔧 Initializing git repository...")
        self.run_command("git init", cwd=str(self.project_root))
        self.run_command('git config user.name "TechCraftLab"', cwd=str(self.project_root))
        self.run_command('git config user.email "techcraftlab.bkk@gmail.com"', cwd=str(self.project_root))
        
        # Create .gitignore
        print("🔒 Creating .gitignore...")
        gitignore_content = """# Next.js
node_modules/
.next/
.vercel/
dist/
build/
*.tsbuildinfo

# Environment
.env.local
.env.*.local

# IDE
.vscode/
.idea/
*.swp

# OS
.DS_Store
Thumbs.db
"""
        with open(self.project_root / ".gitignore", "w") as f:
            f.write(gitignore_content)
        
        # Stage and commit
        print("📝 Committing code...")
        self.run_command("git add .", cwd=str(self.project_root))
        code, stdout, stderr = self.run_command(
            'git commit -m "Phase C.3-C.4: Next.js portfolio frontend - ready for Vercel"',
            cwd=str(self.project_root)
        )
        
        if code == 0:
            print("✅ Git repository ready for GitHub")
            return True
        else:
            print(f"⚠️  Git commit error: {stderr}")
            return False
    
    def phase_c4_github_instructions(self):
        """Phase C.4: GitHub setup instructions"""
        print("\n" + "="*70)
        print("📋 GitHub Setup Instructions")
        print("="*70)
        print("""
1. CREATE REPOSITORY:
   → Go to: https://github.com/new
   → Repository name: PSA-x-Collectr-Tracer
   → Description: Portfolio Intelligence Platform for PSA Pokemon Cards
   → Visibility: Public (recommended for Vercel integration)
   → Click "Create repository"

2. PUSH CODE:
   → Copy HTTPS URL from GitHub repository
   → Run in project root directory:
   
      git remote add origin <paste-github-url>
      git branch -M main
      git push -u origin main
      
3. After pushing, continue with Vercel deployment...
""")
        input("Press Enter once you've pushed code to GitHub: ")
    
    def phase_c4_vercel_instructions(self):
        """Phase C.4: Vercel deployment instructions"""
        print("\n" + "="*70)
        print("🚀 Vercel Deployment Instructions")
        print("="*70)
        print(f"""
1. CONNECT TO VERCEL:
   → Go to: https://vercel.com/new
   → Click "Import Git Repository"
   → Select "PSA-x-Collectr-Tracer"
   
2. CONFIGURE PROJECT:
   → Project name: psa-collectr-tracer
   → Framework: Next.js
   → Root directory: ./web
   
3. SET ENVIRONMENT VARIABLES:
   → NEXT_PUBLIC_API_BASE: {self.ngrok_url}
   → TRACER_API_KEY: {self.api_key}
   
4. DEPLOY:
   → Click "Deploy"
   → Wait 2-3 minutes for build and deployment
   → Save your Vercel URL (e.g., https://psa-collectr-tracer.vercel.app)
""")
        vercel_url = input("Enter your Vercel deployment URL: ").strip()
        return vercel_url
    
    def phase_c5_lighthouse_audit(self, vercel_url):
        """Phase C.5: Lighthouse audit instructions"""
        print("\n" + "="*70)
        print("📊 PHASE C.5: Lighthouse Audit")
        print("="*70)
        print(f"""
1. OPEN LIGHTHOUSE:
   → Navigate to: {vercel_url}
   → Press F12 to open Chrome DevTools
   → Click "Lighthouse" tab
   
2. RUN AUDITS ON ALL PAGES:
   Pages to test:
   • Dashboard: {vercel_url}/
   • Portfolio: {vercel_url}/portfolio
   • Add Card: {vercel_url}/add-card
   • P&L: {vercel_url}/pnl
   
   For each page:
   → Select "Mobile" profile
   → Click "Analyze page load"
   → Wait for report (1-2 minutes)
   
3. TARGET SCORES:
   ✓ Performance: ≥ 90
   ✓ Accessibility: ≥ 95
   ✓ Best Practices: ≥ 95
   ✓ SEO: ≥ 90
   
4. IF SCORES BELOW TARGET:
   → Common optimizations needed:
     - Image optimization
     - Code splitting
     - Remove unused CSS
     - Lazy load below-fold content
""")
        input("Press Enter once Lighthouse audit is complete: ")
    
    def phase_c6_grace_period(self):
        """Phase C.6: 7-day grace period monitoring"""
        print("\n" + "="*70)
        print("⏰ PHASE C.6: 7-Day Grace Period Monitoring")
        print("="*70)
        
        start_date = datetime.now()
        end_date = start_date + timedelta(days=7)
        cutover_date = end_date + timedelta(days=1)
        
        print(f"""
GRACE PERIOD: {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}

SYSTEMS RUNNING IN PARALLEL:
  • Vercel: Production Next.js frontend
  • Flask: localhost:5000 (local backend)
  • ngrok: Tunnel to Flask (https://automated-crummiest-puritan.ngrok-free.dev)
  • Both tunnels must remain active

DAILY CHECKLIST (Days 1-7):
  ☐ Vercel deployment accessible
  ☐ Dashboard loads with portfolio data
  ☐ No errors in browser console
  ☐ API responses return 200 status
  ☐ Flask backend running on localhost:5000
  ☐ ngrok tunnel active

CUTOVER DATE: {cutover_date.strftime('%Y-%m-%d')} (Day 8)
  ☐ Verify all systems working
  ☐ Enable analytics on Vercel
  ☐ Keep ngrok as permanent HTTPS bridge
  ☐ Decommission old tunnel (if applicable)

MONITORING LOG:
""")
        
        # Create monitoring log file
        log_file = self.project_root / "GRACE_PERIOD_LOG.md"
        with open(log_file, "w") as f:
            f.write(f"# Grace Period Monitoring Log\n\n")
            f.write(f"**Start Date:** {start_date.strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"**End Date:** {end_date.strftime('%Y-%m-%d')}\n")
            f.write(f"**Cutover Date:** {cutover_date.strftime('%Y-%m-%d')}\n\n")
            f.write("## Daily Status\n\n")
            for day in range(1, 8):
                date = (start_date + timedelta(days=day-1)).strftime('%Y-%m-%d')
                f.write(f"### Day {day} ({date})\n")
                f.write("- [ ] Vercel accessible\n")
                f.write("- [ ] Portfolio data loads\n")
                f.write("- [ ] No console errors\n")
                f.write("- [ ] API healthy\n")
                f.write("- [ ] Notes: \n\n")
        
        print(f"✅ Grace period log created: GRACE_PERIOD_LOG.md")
        return log_file
    
    def run_all_phases(self):
        """Execute all phases C.4-C.6"""
        print("\n🎯 STARTING PHASE C.4-C.6 AUTOMATION\n")
        
        # Phase C.4: Git setup
        if not self.phase_c4_git_setup():
            print("❌ Git setup failed")
            return False
        
        self.phase_c4_github_instructions()
        vercel_url = self.phase_c4_vercel_instructions()
        
        # Phase C.5: Lighthouse
        self.phase_c5_lighthouse_audit(vercel_url)
        
        # Phase C.6: Grace period
        log_file = self.phase_c6_grace_period()
        
        print("\n" + "="*70)
        print("✅ PHASES C.4-C.6 SETUP COMPLETE")
        print("="*70)
        print(f"""
DEPLOYMENT SUMMARY:
  ✓ Git repository initialized
  ✓ Code ready for GitHub push
  ✓ Vercel deployment instructions provided
  ✓ Lighthouse audit guidelines prepared
  ✓ Grace period monitoring log created
  
NEXT ACTIONS:
  1. Push code to GitHub (follow instructions above)
  2. Deploy to Vercel from GitHub
  3. Run Lighthouse audits on all pages
  4. Monitor for 7 days using {log_file}
  5. On day 8: Review and optimize
  
PHASE D & E (Coming Next):
  → Tab Repairs (20 min)
  → 12 Skill Suite Creation (60 min)
""")
        return True

if __name__ == "__main__":
    automation = DeploymentAutomation()
    success = automation.run_all_phases()
    sys.exit(0 if success else 1)
