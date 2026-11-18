# FACTS (Aşama 2, elle gözden geçirildi)
- Sinyal: SIGKILL=9, SIGTERM=15 doğru; 'SIGCHLD 1500' ps çıktısı örneği (iddia değil).
- Port: 22 ssh, 80 http, 443 https, 8080/9090/8888/5432/2222 örnek/özel port; doğru kullanılmış.
- nice: -20..19 doğru; '1..3','1 to 4','0 to 10' bağlam örnekleri (nice değil, elle kontrol gerekirse).
- Stdin/out/err = 0/1/2 doğru; umask varsayılan 0022 doğru; pratikte 'default via' ağ örnekleri.
- verify_examples: 2 sözdizimi bulgusu (6.5, 6.6) parça komut, yanlış pozitif; seçenek hatası 0.
- Belirsiz: oktal (39) ve yol (123) iddiaları toplu doğrulanmadı.
