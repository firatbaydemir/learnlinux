# Katkıda bulunma

V3, modül kaynaklarının JSON olarak tutulduğu ve HTML sayfalarının üretildiği bağımsız bir projedir. Yeni modül eklerken HTML dosyalarını elle düzenleme; `tools/build.py` üretir.

## Modül dosyaları

Yeni bir modül için `content/m<id>/` altında dört dosya oluştur:

```text
module.json
tr.json
de.json
en.json
```

`<id>` değeri `content/_modules.json` içinde bulunmalıdır. `module.json` dilden bağımsız görevleri, VM kontrollerini ve quiz cevaplarını; dil dosyaları ise kullanıcıya gösterilen metinleri içerir.

## İçerik kuralları

1. **Önce kendi VM'in:** Öğrencinin gerçek komutları kendi Linux VM'inde veya WSL ortamında çalıştırmasını hedefle. Yerleşik terminal yalnızca isteğe bağlı bir simülatördür.
2. **Tanımlayıcıları İngilizce ASCII tut:** Kullanıcı, grup, dosya, dizin, host ve proje adları bütün dillerde aynı olmalı. Örnekler: `student`, `alice`, `documents`, `notes.txt`, `linux-lab`.
3. **Güvenliği açıkça anlat:** Yıkıcı komutları simülatör dışındaki bir ortamda çalıştırmayı önermemelisin. VM yönergelerinde riskli adımlardan önce uyarı ve yedek/snapshot hatırlatması ver.
4. **Üç dilin yapısını eşleştir:** Bölüm kimlikleri, komut sayıları, görev ve quiz kimlikleri ile seçenek sayıları `tr.json`, `de.json` ve `en.json` dosyalarında tutarlı olmalı.
5. **HTML yerine kaynak JSON'u düzenle:** Oluşturulan sayfalar `tr/`, `de/` ve `en/` dizinlerinde bulunur; doğrudan düzenlenmemelidir.

### `module.json`

- Simülatör görev kimlikleri sıralı `t01..tNN` biçiminde olmalı. Her görevde kontrol (`check`) ve çözüm (`solution`) bulunmalı.
- Görev türleri: `warmup`, `guided`, `predict`, `debug`, `mini`, `challenge`, `ticket`. Zorluk `diff` değeri 1–3 olmalı.
- Mümkün olduğunda görevi yalnızca komut metniyle değil, oluşan dosya/durum gibi sonuçlarla doğrula.
- VM görevi kimlikleri sıralı `v01..vNN` biçiminde olmalı. `expect: null`, yalnızca öğrencinin görevi tamamladığını onayladığı adımlar içindir.
- Quiz cevapları sıfır tabanlıdır (`answer: 0..3`).

### Dil dosyaları

Her dil dosyası modül başlığı ve hedeflerinin yanı sıra bölümleri, simülatör/VM görev metinlerini, quiz sorularını, özeti ve terimleri içermelidir. Modül başına en az beş simülatör görevi gerekir; yedi görev türünün tamamı önerilir.

Satır içi biçimlendirmede yalnızca `` `kod` `` ve `**kalın**` kullan. HTML ekleme. Kod örneklerindeki dosya ve kullanıcı adları İngilizce ASCII olmalı.

## Yerel doğrulama

Komutları proje kökünden çalıştır:

```bash
python3 tools/build.py
python3 tools/validate.py
node tests/test_terminal.js
```

Node.js yerine JavaScriptCore varsa motor testini şu şekilde çalıştırabilirsin:

```bash
jsc shared/terminal.js tests/test_terminal.js
```

Terminal motorunda bir komut değişikliği gerekiyorsa `shared/terminal.js` ile birlikte `tests/test_terminal.js` içine de odaklı bir test ekle.
