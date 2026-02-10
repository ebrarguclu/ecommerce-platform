# Yaklaşım 1: git-changelog-command-line (Basit)

## Kullanım
```bash
java -jar git-changelog.jar \
  -r .. \
  -t PROJ_TEMPLATE.hbs \
  -of CHANGELOG_v1.1.0_to_v1.2.0.md \
  -fr v1.1.0 \
  -tr v1.2.0
```

## Özellikler

- ✅ Git commit'lerden veri
- ❌ JIRA API yok
- ❌ Bitbucket API yok

## Çıktı

Basit changelog, sadece commit mesajlarından bilgi.
