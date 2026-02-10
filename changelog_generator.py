#!/usr/bin/env python3
import os
import re
import sys
import subprocess
import yaml
from datetime import datetime

class ChangelogGenerator:
    def __init__(self, config_path='config.yml'):
        # Config dosyası kontrolü
        if not os.path.exists(config_path):
            print(f"❌ Hata: {config_path} bulunamadı! Lütfen config dosyasını oluşturun.")
            sys.exit(1)
            
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)
        
        self.bitbucket_config = self.config.get('bitbucket', {})

    def get_commits(self, from_ref, to_ref):
        try:
            # Git loglarını al (hash|author|date|message)
            format_str = "%H|%an|%ad|%s"
            cmd = ["git", "log", f"{from_ref}..{to_ref}", f"--pretty=format:{format_str}", "--date=short"]
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            
            commits = []
            for line in result.stdout.strip().split('\n'):
                if not line: continue
                h, author, date, msg = line.split('|', 3)
                
                # JIRA Key bulma (Örn: ABC-123)
                jira_match = re.search(r'([A-Z]+-\d+)', msg)
                jira_key = jira_match.group(1) if jira_match else None
                
                # PR Numarası bulma (Örn: #42)
                pr_match = re.search(r'#(\d+)', msg)
                pr_num = pr_match.group(1) if pr_match else None

                commits.append({
                    'hash': h,
                    'author_name': author,
                    'date': date,
                    'message': msg,
                    'jira_key': jira_key,
                    'pr_number': pr_num,
                    'jira_details': None, # API entegrasyonu yoksa boş kalır
                    'pr_details': None    # API entegrasyonu yoksa boş kalır
                })
            return commits
        except Exception as e:
            print(f"❌ Git Hatası: {e}")
            sys.exit(1)

    def generate_changelog(self, from_ref, to_ref, output_file):
        commits = self.get_commits(from_ref, to_ref)
        
        # Klasörü oluştur
        output_dir = os.path.dirname(output_file)
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)

        with open(output_file, 'w', encoding='utf-8') as f:
            # Header (Senin istediğin format)
            f.write(f"# NETWORKHSM Changelog: {from_ref} → {to_ref}\n\n")
            f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write("---\n\n")

            # Commits
            f.write("## 📋 Changes\n\n")
            for commit in commits:
                f.write(f"### {commit['message']}\n\n")

                if commit['jira_key']:
                    url = self.config['jira']['url']
                    f.write(f"**📌 JIRA:** [{commit['jira_key']}]({url}/browse/{commit['jira_key']})\n\n")

                if commit['pr_number']:
                    repo_url = self.bitbucket_config.get('repo_url', '')
                    f.write(f"**🔗 Pull Request:** [#{commit['pr_number']}]({repo_url}/pull-requests/{commit['pr_number']})\n\n")

                f.write(f"**👤 Developer:** {commit['author_name']}\n")
                f.write(f"**📅 Date:** {commit['date']}\n")
                f.write(f"**🔑 Hash:** `{commit['hash'][:7]}`\n\n")
                f.write("---\n\n")

            f.write("## 📊 Summary\n\n")
            f.write(f"- **Total Commits:** {len(commits)}\n")
            f.write(f"- **From:** {from_ref}\n")
            f.write(f"- **To:** {to_ref}\n")

if __name__ == '__main__':
    if len(sys.argv) != 4:
        print("Usage: python3 changelog_generator.py <from_ref> <to_ref> <output_file>")
        sys.exit(1)

    gen = ChangelogGenerator()
    gen.generate_changelog(sys.argv[1], sys.argv[2], sys.argv[3])
