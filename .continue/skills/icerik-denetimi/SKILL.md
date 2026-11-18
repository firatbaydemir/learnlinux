---
name: icerik-denetimi
description: Linux eğitim içeriği için "önce ölçüt, sonra tarama, sonra düzeltme" denetim planı. Yeni sohbette kaldığı yerden devam etmek için kullan.
---

# İçerik denetimi (devam eden iş)

Başlangıç: AGENTS.md ve plan.md oku. Bu skill, plan.md'deki eski A4/A5 sırasının yerine geçen yeni plandır.

## Neden
Eski plan yalnızca biçimi ölçüyordu (kelime, quiz sayısı). Doğruluk ve kapsam ölçülmemişti. Yeni sıra: ölçüt -> kapsam taraması -> doğruluk taraması -> tutarlılık -> düzeltme. Eski A4 (quiz 8) ve A5 (sık hatalar kutusu) en sona kalır.

## Ortam
- WSL: yüklü dağıtım yok. Docker yok. Node yok (`winget` var, v1.29).
- Gerçek bash: `C:\Program Files\Git\usr\bin\bash.exe` (Git Bash, GNU araçları var).
- Python: `$env:LOCALAPPDATA\Programs\Python\Python312\python.exe`, `$env:PYTHONIOENCODING="utf-8"`.
- PowerShell'de `python -c "..."` içinde çift tırnak/ters bölü sorunlu. Betiği dosyaya yaz veya multi_edit kullan.

## Yapılanlar
- A3 bitti: 5.3, 5.4, 5.5 modüllerinde 7 -> 13 görev (tr/de/en). `tools/_a3.py`. build+validate 0 hata.
- Aşama 0: hedef kitle varsayımı LPIC-1 / RHCSA temeli. Cetvel `tools/gaps.py` içinde (6 seviye, 90 konu). Ayrı `CURRICULUM.md` yazılmadı.
- Aşama 1 bitti: `tools/inventory.py` -> `INVENTORY.json` (47 modül, 719 komut kartı, 948 çözüm). `tools/gaps.py` -> `GAPS.md`. Sonuç: 90 konudan 73 bulundu, 17 eksik/şüpheli (anahtar kelime yalnızca komut kartlarında aranır, bu yüzden bazıları yanlış pozitif olabilir).
- Aşama 2 başladı:
  - `tools/facts_extract.py` -> `facts_raw.json` (sinyal, port, nice aralığı, chmod/umask, yol iddiaları). Elle doğrulanmadı, `FACTS.md` henüz yok.
  - `tools/verify_examples.py`: örnek ve çözümlerde `bash -n` sözdizimi + GNU araçlarında `--help` ile seçenek kontrolü. Son çalıştırma (girinti hatası düzeltildikten sonra) çıktı vermedi; tekrar çalıştırıp çıktıyı doğrula. Önceki ilk çalıştırma: 2 sözdizimi bulgusu (6.5 `NAME="${1:-guest}"`, 6.6 `done < ~/lab/servers.txt`); ikisi de parça komut, büyük olasılıkla yanlış pozitif.

## Gap taramasında şüpheli (GAPS.md)
S0 Linux/kernel kavramı, terminal/prompt; S2 mutlak/göreli yol, inode; S3 stdin/stdout/stderr, tırnaklama; S4 /etc/passwd|shadow|group, SUID/SGID/sticky, chattr/lsattr, /etc/skel; S5 kill/pkill/killall, lsof/fuser, GRUB; S6 nmcli/netplan, RAID/mdadm, lsmod/modprobe/sysctl, swap/kota.
Metinde geçip kartı olmayanlar yanlış pozitif olabilir. Kesin yok olanlar: chattr/lsattr, lsof/fuser, GRUB, RAID/mdadm, kernel modül/sysctl.

## Sıradaki adımlar
1. `verify_examples.py` çıktısını al, yanlış pozitifleri ayıkla.
2. `facts_raw.json` içindeki iddiaları doğrula (SIGKILL=9, SIGTERM=15, nice -20..19, port numaraları, chmod/umask anlamları, yollar). Sonuç `FACTS.md`: doğru / yanlış / belirsiz. Man sayfası veya Git Bash çıktısı kullan.
3. Aşama 3: hedef -> görev -> quiz eşleşmesi, quiz cevabı metinde var mı, tr/de/en sayı ve komut farkları.
4. Kullanıcıya genel rapor sun (kapsam boşlukları, yanlış bilgiler, tutarlılık). Hangi değişiklik nerede yapılacak kararını birlikte ver.
5. Düzeltme sırası: yanlış bilgi, eksik konu, sıra/tutarlılık, biçim (quiz 8, sık hatalar kutusu). Sonra node kur (A8) ve `node tests/test_terminal.js` çalıştır.

## Kurallar
- Önce tr, sonra de/en aynı yapıda. Dosyalar CRLF. HTML üretilir, elle düzenleme.
- Doğrulama: `python tools/build.py; python tools/validate.py`.
- Bitince plan.md'ye 2-3 satır oturum notu ekle (O34).
- Geçici dosyalar (`INVENTORY.json`, `facts_raw.json`, `tools/_a3.py`) commit öncesi gözden geçir.
