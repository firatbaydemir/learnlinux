# Temel Linux Akademisi 

Linux temellerini tarayıcıda uygulamalı öğrenmek için hazırlanmış, bağımsız ve statik bir eğitim projesi. Sunucu tarafı veya çalışma zamanında internet bağlantısı gerektirmez.

- **47 modül** · **686 simülatör görevi** · **232 VM görevi** · **188 öz test sorusu**
- **Türkçe, Deutsch ve English**
- Harici JavaScript/CSS kitaplığı veya CDN bağımlılığı yok

## Hızlı başlangıç

Python 3 ile proje kökünde yerel bir web sunucusu başlat:

```bash
python3 -m http.server 8000
```

Tarayıcıda <http://localhost:8000/> adresini aç. Tux ikonlu dil seçicisinden Türkçe, Almanca veya İngilizceyi seç. Ana sayfadaki arama modül başlıklarını ve modüllerde özellikle öğretilen komutları bulur.

İlerleme ve tercihler tarayıcının `localStorage` alanında saklanır. Eğitim görevlerini kendi Linux VM'inde/WSL ortamında yapmak önerilir; yerleşik terminal isteğe bağlı bir simülatördür ve gerçek sistem komutlarını çalıştırmaz.

## Proje yapısı

```text
.
├── index.html              # Dil seçici
├── tr/ de/ en/             # Üretilmiş dil sayfaları
├── content/                # Modül kaynakları ve çeviriler
├── shared/                 # Tarayıcı arayüzü ve terminal simülatörü
├── tools/build.py          # Kaynak içerikten sayfa üretimi
├── tools/validate.py       # İçerik, sayfa ve dil doğrulaması
└── tests/test_terminal.js  # Terminal motoru testleri
```

`content/` altındaki JSON dosyaları kaynak içeriktir; `tr/`, `de/` ve `en/` altındaki HTML sayfaları `tools/build.py` ile üretilir. Üretilen sayfalar statik barındırmada doğrudan kullanılabilir.

## Geliştirme ve doğrulama

İçeriği yeniden üretmek ve doğrulamak için Python 3 gerekir:

```bash
python3 tools/build.py
python3 tools/validate.py
```

Terminal motoru testlerini Node.js ile çalıştır:

```bash
node tests/test_terminal.js
```

Alternatif olarak JavaScriptCore kullanabilirsin:

```bash
jsc shared/terminal.js tests/test_terminal.js
```

Doğrulayıcı JSON şemalarını, üç dildeki modül eşleşmelerini, üretilmiş sayfaları ve bağlantıları denetler; kullanılabilir bir JavaScript çalışma zamanı varsa motor öz testini de çalıştırır.

## GitHub Pages'de yayınlama

`index.html` ve dil klasörleri statik barındırmaya hazırdır. Değişiklikleri GitHub'a göndermeden önce üretilen sayfaları ve testleri doğrula:

```bash
python3 tools/build.py
python3 tools/validate.py
node tests/test_terminal.js
```

Depoyu GitHub'a gönderdikten sonra **Settings → Pages → Build and deployment** bölümünde **Deploy from a branch** seç; `main` dalını ve `/(root)` klasörünü yayın kaynağı yap. GitHub Actions doğrulama iş akışı, içerik ve testleri her push/PR'da çalıştırır ve üretilen HTML'in güncel kalmasını denetler.

## Katkıda bulunma

Yeni modül ekleme ve içerik kuralları için [CONTRIBUTING.md](CONTRIBUTING.md) dosyasına bak.

## Lisans

Bu projenin kodu ve eğitim içeriği MIT lisansı altındadır. Ayrıntılar için [LICENSE](LICENSE) dosyasına bak.
