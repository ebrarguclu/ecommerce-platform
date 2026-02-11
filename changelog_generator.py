#!/usr/bin/env python3
"""
Professional Changelog Generator
Supports multiple modes for different use cases.

Usage:
    # Fast mode (CI/CD)
    python3 changelog_generator.py v1.0.0 v1.1.0 -o output.md

    # Detailed mode (Release notes)
    python3 changelog_generator.py v1.0.0 v1.1.0 -o output.md --detailed

    # Debug mode (Troubleshooting)
    python3 changelog_generator.py v1.0.0 v1.1.0 -o output.md --debug --verify-links
"""

import os
import re
import sys
import argparse
import subprocess
import requests
from datetime import datetime
from requests.auth import HTTPBasicAuth

class ChangelogGenerator:
    def __init__(self, mode='fast'):
        """
        mode: 'fast', 'detailed', 'debug'
        """
        self.mode = mode
        self.workspace = os.getenv('BITBUCKET_WORKSPACE', 'senagrun-dev')
        self.repo_slug = os.getenv('REPO_SLUG', 'ecommerce-platform')
        self.jira_url = os.getenv('JIRA_URL')
        self.jira_email = os.getenv('JIRA_EMAIL')
        self.jira_token = os.getenv('JIRA_TOKEN')
        
        # Performans sayaçları
        self.stats = {
            'commits_processed': 0,
            'jira_api_calls': 0,
            'bitbucket_api_calls': 0,
            'cache_hits': 0
        }
    
    def parse_commit(self, message):
        """Parse commit message to extract PR, JIRA key, and description."""
        pr_match = re.search(r'#(\d+)', message)
        jira_match = re.search(r'([A-Z][A-Z0-9]+-\d+)', message)
        
        pr_num = pr_match.group(1) if pr_match else None
        jira_key = jira_match.group(1) if jira_match else None
        
        # Extract clean message
        clean_msg = re.sub(r'^.*?:\s*[A-Z][A-Z0-9]+-\d+\s*', '', message).strip()
        if not clean_msg:
            clean_msg = message.split(':')[-1].strip()
        
        return pr_num, jira_key, clean_msg
    
    def fetch_jira_details(self, jira_key):
        """Fetch JIRA issue details (only in detailed mode)."""
        if self.mode == 'fast' or not jira_key or not self.jira_token:
            return None
        
        api_url = f"{self.jira_url}/rest/api/3/issue/{jira_key}"
        auth = HTTPBasicAuth(self.jira_email, self.jira_token)
        
        try:
            self.stats['jira_api_calls'] += 1
            response = requests.get(api_url, auth=auth, timeout=5)
            if response.status_code == 200:
                data = response.json()
                return {
                    'summary': data['fields']['summary'],
                    'status': data['fields']['status']['name'],
                    'type': data['fields']['issuetype']['name']
                }
        except Exception as e:
            if self.mode == 'debug':
                print(f"⚠️ JIRA API Error for {jira_key}: {e}")
        return None
    
    def verify_pr_link(self, pr_num):
        """Verify PR exists on Bitbucket (only in debug mode)."""
        if self.mode != 'debug' or not pr_num:
            return True
        
        # Simplified check - you can add actual API call here
        return True
    
    def categorize_commit(self, jira_key, message, jira_data=None):
        """Categorize commit based on keywords or JIRA type."""
        if jira_data:
            jira_type = jira_data['type'].lower()
            if 'bug' in jira_type:
                return "🐞 Bug Fixes"
            elif 'feature' in jira_type or 'story' in jira_type:
                return "✨ Features"
            elif 'task' in jira_type:
                return "📝 Tasks"
        
        # Fallback to keyword detection
        msg_lower = message.lower()
        if any(w in msg_lower for w in ['fix', 'bug', 'hata', 'düzelt']):
            return "🐞 Bug Fixes"
        elif any(w in msg_lower for w in ['add', 'new', 'feature', 'ekle', 'yeni']):
            return "✨ Features"
        elif any(w in msg_lower for w in ['update', 'improve', 'güncelle']):
            return "📝 Improvements"
        else:
            return "📄 Other Changes"
    
    def get_git_logs(self, from_ref, to_ref):
        """Get git commit logs between two refs."""
        fmt = "%H|%an|%ae|%ad|%s"
        cmd = ["git", "log", f"{from_ref}..{to_ref}", f"--pretty=format:{fmt}", "--date=short"]
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            return result.stdout.strip().split('\n')
        except subprocess.CalledProcessError as e:
            print(f"❌ Git error: {e}")
            return []
    
    def run(self, from_ref, to_ref, output_file, verify_links=False):
        """Generate changelog."""
        print(f"\n🚀 Changelog Generator - Mode: {self.mode.upper()}")
        print(f"📊 Range: {from_ref} → {to_ref}")
        print(f"📝 Output: {output_file}\n")
        
        start_time = datetime.now()
        
        # Get commits
        logs = self.get_git_logs(from_ref, to_ref)
        if not logs or logs == ['']:
            print("⚠️ No commits found in range.")
            return
        
        print(f"✅ Found {len(logs)} commits")
        
        # Categorize commits
        categorized = {}
        
        for line in logs:
            if not line.strip():
                continue
            
            h, author, email, date, msg = line.split('|', 4)
            self.stats['commits_processed'] += 1
            
            pr_num, jira_key, clean_msg = self.parse_commit(msg)
            
            # Fetch JIRA data (only in detailed mode)
            jira_data = self.fetch_jira_details(jira_key) if self.mode != 'fast' else None
            
            # Verify links (only in debug mode)
            if verify_links:
                self.verify_pr_link(pr_num)
            
            # Categorize
            category = self.categorize_commit(jira_key, clean_msg, jira_data)
            
            if category not in categorized:
                categorized[category] = []
            
            # Build commit entry
            commit_entry = {
                'hash': h[:7],
                'author': author,
                'date': date,
                'pr_num': pr_num,
                'jira_key': jira_key,
                'message': clean_msg,
                'jira_data': jira_data
            }
            
            categorized[category].append(commit_entry)
        
        # Generate markdown
        self._write_markdown(categorized, from_ref, to_ref, output_file)
        
        # Stats
        elapsed = (datetime.now() - start_time).total_seconds()
        print(f"\n📊 Statistics:")
        print(f"   • Commits processed: {self.stats['commits_processed']}")
        print(f"   • JIRA API calls: {self.stats['jira_api_calls']}")
        print(f"   • Time elapsed: {elapsed:.2f}s")
        print(f"\n✅ Changelog created: {output_file}")
    
    def _write_markdown(self, categorized, from_ref, to_ref, output_file):
        """Write categorized commits to markdown file."""
        with open(output_file, 'w', encoding='utf-8') as f:
            # Header
            f.write(f"# 🚀 Release Notes: {from_ref} → {to_ref}\n\n")
            f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
            f.write(f"**Mode:** {self.mode}\n\n")
            f.write("---\n\n")
            
            # Table of Contents
            f.write("## 📋 Table of Contents\n\n")
            for category in categorized.keys():
                anchor = category.lower().replace(' ', '-').replace('🐞', '').replace('✨', '').replace('📝', '').replace('📄', '').strip()
                f.write(f"- [{category}](#{anchor})\n")
            f.write("\n---\n\n")
            
            # Categories
            for category, commits in categorized.items():
                if not commits:
                    continue
                
                f.write(f"## {category}\n\n")
                
                for c in commits:
                    # Title
                    if self.mode == 'detailed' and c['jira_data']:
                        title = c['jira_data']['summary']
                    else:
                        title = c['message']
                    
                    # JIRA link
                    if c['jira_key']:
                        jira_link = f"{self.jira_url}/browse/{c['jira_key']}" if self.jira_url else f"JIRA-{c['jira_key']}"
                        f.write(f"### [{c['jira_key']}]({jira_link}): {title}\n\n")
                    else:
                        f.write(f"### {title}\n\n")
                    
                    # Details
                    f.write(f"- 👤 **Developer:** {c['author']}\n")
                    f.write(f"- 📅 **Date:** {c['date']}\n")
                    
                    if c['pr_num']:

                        pr_link = f"https://bitbucket.org/{self.workspace}/{self.repo_slug}/pull-requests/{c['pr_num']}"
 
                        f.write(f"- 🔗 **Pull Request:** [#{c['pr_num']}]({pr_link})\n")
                    
                    f.write(f"- 💾 **Commit:** `{c['hash']}`\n")
                    
                    # Extra details in detailed mode
                    if self.mode != 'fast' and c['jira_data']:
                        f.write(f"- 📊 **Status:** {c['jira_data']['status']}\n")
                        f.write(f"- 🏷️ **Type:** {c['jira_data']['type']}\n")
                    
                    f.write("\n")
            
            # Summary
            f.write("---\n\n")
            f.write("## 📊 Summary\n\n")
            f.write(f"- **Total Commits:** {sum(len(commits) for commits in categorized.values())}\n")
            for category, commits in categorized.items():
                f.write(f"- **{category}:** {len(commits)}\n")

def main():
    parser = argparse.ArgumentParser(
        description='Professional Changelog Generator',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Fast mode (default)
  python3 changelog_generator.py v1.0.0 v1.1.0 -o CHANGELOG.md
  
  # Detailed mode with JIRA integration
  python3 changelog_generator.py v1.0.0 v1.1.0 -o CHANGELOG.md --detailed
  
  # Debug mode with link verification
  python3 changelog_generator.py v1.0.0 v1.1.0 -o CHANGELOG.md --debug --verify-links
        """
    )
    
    parser.add_argument('from_ref', help='Starting git reference (tag/branch)')
    parser.add_argument('to_ref', help='Ending git reference (tag/branch)')
    parser.add_argument('-o', '--output', required=True, help='Output markdown file')
    parser.add_argument('--mode', choices=['fast', 'detailed', 'debug'], default='fast',
                        help='Generation mode (default: fast)')
    parser.add_argument('--detailed', action='store_const', const='detailed', dest='mode',
                        help='Shortcut for --mode detailed')
    parser.add_argument('--debug', action='store_const', const='debug', dest='mode',
                        help='Shortcut for --mode debug')
    parser.add_argument('--verify-links', action='store_true',
                        help='Verify PR links exist (slow)')
    
    args = parser.parse_args()
    
    # Create generator
    gen = ChangelogGenerator(mode=args.mode)
    
    # Run
    gen.run(args.from_ref, args.to_ref, args.output, args.verify_links)

if __name__ == '__main__':
    main()
