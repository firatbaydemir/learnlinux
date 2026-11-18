# REPORT (A6)

## Yanlış bilgi
- FACTS.md: sinyal/port/nice/stdio/umask doğru. verify_examples: seçenek hatası 0; 6.5/6.6 yanlış pozitif.
- Belirsiz (toplu doğrulanmadı): oktal ve yol iddiaları -> A7'de örnekleme ile kontrol.
- Gerçek yanlış bilgi bulgusu: yok.

## Tutarlılık (CONSISTENCY.md)
- tr/de/en yapı farkı 0. Hedef/quiz bayrakları (yol, sembol, tuş) yanlış pozitif.
- Gerçek: 1.2 hedef[2] /etc/os-release, 1.4 hedef[2-3] (2>, hata metni), 2.11 hedef[1] crontab, 2.5 hedef[0] file -> hedefte geçen komut görevde yok; görev ekle ya da hedefi düzelt.
- 0.2 yalnızca 8 görev (kapsam): 2-4 görev eklenebilir.
- 2.4 t07 de/en backtick farkı zararsız.

## Kapsam (GAPS.md, metin araması ile doğrulandı)
Gerçek eksik (hiçbir modülde yok): chattr/lsattr, lsof/fuser, mdadm/RAID, lsmod/modprobe/sysctl, swap (swapon/mkswap), disk quota.
Yanlış pozitif (metinde var, komut kartında yok): SUID (4.5), /etc/passwd, /etc/skel (4.2), kill (5.x), GRUB, nmcli (6.1), inode (2.5/2.8/2.9), stdin/stderr (3.1), mutlak yol.
Kavram eksikleri (komut kartı yok ama anlatım var): terminal/shell kavramı, tırnaklama (3.x) -> varlığı kontrol edilmeli.

## A7 kararı
1. Yanlış bilgi: yok (oktal/yol örneklemesi hızlı kontrol).
2. Hedef-görev uyumsuzlukları: 1.2, 1.4, 2.11, 2.5 düzelt (tr sonra de/en).
3. Eksik konu: yeni modül açmadan mevcutlara ekle: swap -> 2.9 veya 6.4; lsmod/modprobe/sysctl -> 6.8; lsof/fuser -> 5.x; chattr -> 4.5; RAID/quota yalnızca not (RHCSA dışı/ileri).
4. Tırnaklama: 3.x'te yoksa 3.9'a ekle.
