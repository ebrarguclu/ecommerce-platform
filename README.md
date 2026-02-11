# Yaklaşım 2: API Entegrasyonlu Changelog

## Özellikler

- ✅ Git commit'lerden veri
- ✅ JIRA API entegrasyonu (opsiyonel)
- ✅ Bitbucket API entegrasyonu (opsiyonel)

## Kurulum
```bash
# Python dependencies
pip3 install -r requirements.txt

# Config dosyasını düzenle
nano config.yml
```

## Kullanım

### Basit (API'siz)
```bash
python3 changelog_generator.py v1.1.0 v1.2.0 output/CHANGELOG_API.md
```

### API'li (JIRA + Bitbucket)

1. `config.yml` dosyasında `enabled: true` yap
2. Credential'ları gir
3. Çalıştır

## Çıktı

Zenginleştirilmiş changelog:
- JIRA ticket summary, status, assignee
- Bitbucket PR title, reviewers, state

---
**Demo Date:** 2026-02-11
