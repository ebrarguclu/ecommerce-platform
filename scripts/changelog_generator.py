#!/usr/bin/env python3
import os, re, sys, argparse, subprocess, requests
from datetime import datetime
from requests.auth import HTTPBasicAuth

class ChangelogGenerator:
    def __init__(self, mode='fast'):
        self.mode = mode
        # --- COMPANY CONFIGURATION ---
        # These variables should be set in Jenkins Credentials or your Terminal
        self.workspace = os.getenv('BITBUCKET_WORKSPACE', 'senagrun-dev')
        self.repo_slug = os.getenv('REPO_SLUG', 'ecommerce-platform')
        # JIRA URL from environment or default value
        self.jira_url = os.getenv('JIRA_URL', 'https://senagrun.atlassian.net').rstrip('/')
        # # JIRA Authentication (Email and API Token)
        self.jira_email = os.getenv('JIRA_EMAIL')
        self.jira_token = os.getenv('JIRA_TOKEN')

        if self.mode == 'detailed':
            print(f"DEBUG: JIRA Bağlantısı Başlatılıyor...")
            print(f"DEBUG: Email: {self.jira_email}")
            print(f"DEBUG: Token Mevcut mu: {'EVET' if self.jira_token else 'HAYIR'}")

    def parse_commit(self, message):
        pr_match = re.search(r'#(\d+)', message)
        jira_match = re.search(r'([A-Z][A-Z0-9]+-\d+)', message)
        prefix_match = re.search(r'\b(fet|bug|test|prf|ref)\b', message.lower())
        
        pr_num = pr_match.group(1) if pr_match else None
        jira_key = jira_match.group(1) if jira_match else None
        prefix = prefix_match.group(1) if prefix_match else None
        
        clean_msg = re.sub(r'^.*?:\s*', '', message)
        clean_msg = re.sub(r'([A-Z][A-Z0-9]+-\d+)', '', clean_msg)
        clean_msg = re.sub(r'\b(fet|bug|test|prf|ref)\b', '', clean_msg, flags=re.I)
        clean_msg = clean_msg.replace(':', '').strip()
        
        return pr_num, jira_key, prefix, clean_msg

    def fetch_jira_details(self, jira_key):
        if self.mode == 'fast' or not jira_key or not self.jira_token:
            return None
        
        api_url = f"{self.jira_url}/rest/api/3/issue/{jira_key}"
        auth = HTTPBasicAuth(self.jira_email, self.jira_token)
        
        try:
           
            response = requests.get(api_url, auth=auth, timeout=5)
            if response.status_code == 200:
                d = response.json()
                return {
                    'summary': d['fields']['summary'], 
                    'status': d['fields']['status']['name'], 
                    'type': d['fields']['issuetype']['name']
                }
            else:
                print(f"⚠️ JIRA Hatası ({jira_key}): Status Code {response.status_code}")
                return None
        except Exception as e:
            print(f"❌ Bağlantı Hatası: {e}")
            return None

    def categorize_commit(self, prefix, jira_data=None):
        if jira_data and 'type' in jira_data:
            j_type = jira_data['type'].lower()
            if any(w in j_type for w in ['bug', 'hata']): return "🐞 Bug Fixes"
            if any(w in j_type for w in ['feature', 'story']): return "✨ Features"
            return "📝 Improvements"
        
        prefix_map = {
            'fet': "✨ Features", 
            'bug': "🐞 Bug Fixes", 
            'test': "🧪 Tests", 
            'prf': "⚡ Performance", 
            'ref': "🛠 Refactors"
        }
        return prefix_map.get(prefix, "📝 Other Changes")
    
    def get_customer_friendly_category(self, prefix):
        """Müşteri dostu kategori isimleri."""
        customer_map = {
            'fet': "🎉 New Features",
            'bug': "🔧 Bug Fixes & Improvements",
            'prf': "⚡ Performance Enhancements",
            'ref': "🔄 System Updates",
            'test': "✅ Quality Improvements"
        }
        return customer_map.get(prefix, "📋 Other Updates")

    def run(self, from_ref, to_ref, output_file):
        print(f"🚀 Mod: {self.mode.upper()} | {from_ref} -> {to_ref}")
        cmd = ["git", "log", f"{from_ref}..{to_ref}", "--pretty=format:%H|%an|%ad|%s", "--date=short"]
        logs = subprocess.run(cmd, capture_output=True, text=True).stdout.strip().split('\n')
        
        categorized = {}
        for line in logs:
            if not line.strip(): continue
            h, author, date, msg = line.split('|', 3)
            pr_num, jira_key, prefix, clean_msg = self.parse_commit(msg)
            jira_data = self.fetch_jira_details(jira_key)
            
            # Kategori belirleme (CUSTOMER modda farklı)
            if self.mode == 'customer':
                cat = self.get_customer_friendly_category(prefix)
            else:
                cat = self.categorize_commit(prefix, jira_data)
            
            if cat not in categorized: categorized[cat] = []
            categorized[cat].append({
                'hash': h[:7], 
                'author': author, 
                'date': date, 
                'pr_num': pr_num, 
                'jira_key': jira_key, 
                'message': clean_msg, 
                'jira_data': jira_data
            })
        
        # Mod'a göre farklı yazma fonksiyonları
        if self.mode == 'customer':
            self._write_customer_markdown(categorized, from_ref, to_ref, output_file)
        else:
            self._write_standard_markdown(categorized, from_ref, to_ref, output_file)
    
    def _write_standard_markdown(self, categorized, from_ref, to_ref, output_file):
        """Fast ve Detailed modlar için standart yazım."""
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(f"# 🚀 Release Notes: {from_ref} → {to_ref}\n")
            f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M')} | **Mode:** {self.mode}\n\n---\n\n")
            
            for cat in sorted(categorized.keys()):
                f.write(f"## {cat}\n\n")
                for c in categorized[cat]:
                    title = c['jira_data']['summary'] if (self.mode == 'detailed' and c['jira_data']) else c['message']
                    
                    if c['jira_key']:
                        if self.mode == 'detailed':
                            link = f"{self.jira_url}/browse/{c['jira_key']}"
                            f.write(f"### [{c['jira_key']}]({link}): {title}\n\n")
                        else:
                            f.write(f"### {c['jira_key']}: {title}\n\n")
                    else:
                        f.write(f"### {title}\n\n")
                    
                    f.write(f"- 👤 **Developer:** {c['author']}\n")
                    f.write(f"- 📅 **Date:** {c['date']}\n")
                    
                    if c['pr_num']:
                        pr_link = f"https://bitbucket.org/{self.workspace}/{self.repo_slug}/pull-requests/{c['pr_num']}"
                        f.write(f"- 🔗 **Pull Request:** [#{c['pr_num']}]({pr_link})\n")
                    
                    if self.mode == 'detailed' and c['jira_data']:
                        s = c['jira_data']['status']
                        icon = "✅" if s.lower() in ['done', 'closed', 'resolved', 'bitti'] else "⏳"
                        f.write(f"- 📊 **Status:** {icon} `{s}`\n")
                    
                    f.write(f"- 💾 **Commit:** `{c['hash']}`\n\n")
    
    def _write_customer_markdown(self, categorized, from_ref, to_ref, output_file):
        """CUSTOMER modu için müşteri dostu yazım."""
        with open(output_file, 'w', encoding='utf-8') as f:
            # Header - Profesyonel ve temiz
            f.write(f"# 📦 Product Release Notes\n\n")
            f.write(f"**Version:** {to_ref}\n")
            f.write(f"**Release Date:** {datetime.now().strftime('%B %d, %Y')}\n\n")
            f.write("---\n\n")
            
            # Summary
            total_changes = sum(len(commits) for commits in categorized.values())
            f.write(f"## 📊 Release Summary\n\n")
            f.write(f"This release includes **{total_changes} improvements** across the following areas:\n\n")
            
            for cat in sorted(categorized.keys()):
                count = len(categorized[cat])
                f.write(f"- {cat}: **{count}** item{'s' if count > 1 else ''}\n")
            
            f.write("\n---\n\n")
            
            # Detailed Changes - Müşteri odaklı
            for cat in sorted(categorized.keys()):
                f.write(f"## {cat}\n\n")
                
                for idx, c in enumerate(categorized[cat], 1):
                    # Sadece mesaj, teknik detay yok
                    f.write(f"{idx}. **{c['message']}**\n")
                    
                    # Müşteri için önemli: ne zaman eklendi
                    f.write(f"   - *Added on {c['date']}*\n")
                    f.write("\n")
            
            # Footer - Profesyonel kapanış
            f.write("---\n\n")
            f.write("## 📞 Support & Feedback\n\n")
            f.write("For questions or feedback regarding this release, please contact our support team.\n\n")
            f.write("**Thank you for using our product!** 🎉\n")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Changelog Generator - Fast, Detailed, or Customer modes'
    )
    parser.add_argument('from_ref', help='Starting version tag')
    parser.add_argument('to_ref', help='Ending version tag')
    parser.add_argument('-o', '--output', required=True, help='Output markdown file')
    parser.add_argument('--detailed', action='store_true', help='Detailed mode (JIRA integration)')
    parser.add_argument('--customer', action='store_true', help='Customer-friendly mode (for external release notes)')
    
    args = parser.parse_args()
    
    # Mod belirleme
    if args.customer:
        mode = 'customer'
    elif args.detailed:
        mode = 'detailed'
    else:
        mode = 'fast'
    
    ChangelogGenerator(mode=mode).run(args.from_ref, args.to_ref, args.output)
