# GAPS.md - Kapsam taraması (otomatik: tools/gaps.py)

> Cetvel: `tools/gaps.py` içindeki konu listesi (LPIC-1/RHCSA temeli). Anahtar kelime yalnızca komut kartlarında (cmd/example) aranır; 'yok' = hiçbir modülde geçmiyor.


## Seviye 0
| Konu | Durum | Modüller |
|---|---|---|
| Linux/kernel/dağıtım kavramı | YOK |  |
| Sanal makine kurulumu | var | 5.2, 6.4 |
| Terminal/shell/prompt | YOK |  |

## Seviye 1
| Konu | Durum | Modüller |
|---|---|---|
| pwd/ls/cd | var | 0.3, 1.1, 1.4, 2.1, 2.2 |
| whoami/id/uname | var | 0.1, 1.2 |
| man/--help/apropos | var | 0.3, 1.3 |
| Çıkış kodu $?, &&, || | var | 1.4, 3.6, 3.9, 5.6, 6.5 |
| Ortam değişkeni PATH/export | var | 1.5, 2.7 |
| alias | var | 1.3, 1.5 |
| history | var | 0.3, 1.3, 1.5 |
| which/type | var | 1.3, 1.5 |
| date/uptime/hostname | var | 0.3, 1.2, 1.4, 2.1, 2.2, 2.5… |
| Shell tamamlama (Tab) | var | 1.1, 1.5, 2.11, 6.4, 6.7 |

## Seviye 2
| Konu | Durum | Modüller |
|---|---|---|
| Dizin ağacı FHS | var | 0.1, 1.1, 1.2, 2.1, 2.2, 2.5… |
| mkdir/touch/rm/rmdir | var | 2.3 |
| cp/mv | var | 2.4 |
| Mutlak/göreli yol | YOK |  |
| ln (sembolik/sert bağ) | var | 2.2, 2.5 |
| stat/file | var | 2.2, 2.5, 4.4, 4.5, 5.2, 6.8 |
| cat/less/head/tail/wc | var | 1.3, 2.6, 3.2, 5.2, 5.4, 5.6 |
| nano/vim temel | var | 2.7 |
| df/du/free | var | 1.2, 2.8, 5.2 |
| mount/umount | var | 2.9, 6.4 |
| fdisk/lsblk/mkfs | var | 2.9, 6.4 |
| ssh/scp/rsync | var | 2.10, 5.2 |
| ping/curl/wget | var | 6.1, 6.8 |
| cron/crontab/at | var | 2.11, 6.7 |
| fstab | var | 6.4 |
| inode | YOK |  |

## Seviye 3
| Konu | Durum | Modüller |
|---|---|---|
| stdin/stdout/stderr | YOK |  |
| Yönlendirme > >> 2> | var | 1.4, 3.1, 3.2, 3.9, 4.5, 5.4 |
| Pipe |/tee | var | 3.2, 3.9 |
| Joker karakter glob | var | 3.9 |
| Tırnaklama | YOK |  |
| grep (-i -r -v -E) | var | 3.4, 5.6, 6.3 |
| find (-name -type -exec) | var | 1.3, 2.1, 3.4, 3.9, 4.5 |
| sort/uniq/cut/tr | var | 3.2, 3.5, 3.7, 3.9, 6.1, 6.3 |
| sed | var | 3.6 |
| awk | var | 3.6 |
| diff/cmp/comm/patch | var | 3.7 |
| tar/gzip/bzip2/xz/zip | var | 3.8 |
| xargs | var | 3.9 |
| Düzenli ifade (regex) | var | 3.6 |
| Komut yerine koyma $(...) | var | 1.2, 1.5, 3.8, 3.9, 6.5, 6.6 |
| here-doc | var | 3.1, 3.9 |
| locate/updatedb | var | 3.4 |

## Seviye 4
| Konu | Durum | Modüller |
|---|---|---|
| who/w/last | var | 4.1 |
| useradd/usermod/userdel | var | 4.2 |
| passwd/chage (parola yaşlandırma) | var | 4.2 |
| /etc/passwd /etc/shadow /etc/group | YOK |  |
| groupadd/gpasswd | var | 4.2 |
| su/sudo/visudo | var | 4.3 |
| chmod sembolik+oktal | var | 3.9, 4.4, 4.5, 6.5, 6.6, 6.7… |
| chown/chgrp | var | 4.4, 4.5, 6.8 |
| umask | var | 4.4, 4.5 |
| SUID/SGID/sticky | YOK |  |
| ACL (getfacl/setfacl) | var | 6.8 |
| chattr/lsattr | YOK |  |
| Ana dizin /etc/skel | YOK |  |

## Seviye 5
| Konu | Durum | Modüller |
|---|---|---|
| ps/top/pstree | var | 5.1 |
| kill/pkill/killall/sinyaller | YOK |  |
| nice/renice | var | 5.3 |
| jobs/bg/fg/nohup | var | 5.4 |
| htop/vmstat/iostat/free | var | 5.2 |
| lsof/fuser | YOK |  |
| apt/dpkg | var | 5.5 |
| dnf/yum/rpm | var | 5.5 |
| Depo yönetimi (sources.list/.repo) | var | 2.2, 2.4, 2.6, 2.10, 3.9, 4.4… |
| systemctl (start/enable/status) | var | 2.11, 5.6, 6.7, 6.8 |
| journalctl | var | 2.11, 5.6, 6.7 |
| /var/log, rsyslog, logrotate | var | 5.6 |
| Hedef/runlevel (systemctl get-default) | var | 6.3 |
| GRUB/önyükleme süreci | YOK |  |
| dmesg | var | 5.6 |

## Seviye 6
| Konu | Durum | Modüller |
|---|---|---|
| ip/ss/DNS/ports | var | 1.3, 2.6, 2.8, 5.6, 6.1, 6.3… |
| /etc/hosts /etc/resolv.conf | var | 6.1 |
| Ağ yapılandırma (nmcli/netplan) | YOK |  |
| SELinux (getenforce/restorecon/setsebool) | var | 6.2, 6.8 |
| firewalld (firewall-cmd) | var | 6.1, 6.3, 6.8 |
| iptables/nftables/ufw | var | 6.1, 6.3, 6.8 |
| LVM (pvcreate/vgcreate/lvextend) | var | 6.4 |
| RAID/mdadm | YOK |  |
| Bash betik: değişken/koşul | var | 6.5 |
| Bash betik: döngü/fonksiyon | var | 3.6, 6.6 |
| systemd timer | var | 5.6, 6.7, 6.8 |
| Betik hata ayıklama (set -e, bash -x) | var | 6.5, 6.6 |
| SSH anahtarı (ssh-keygen) | var | 0.2, 2.10 |
| Güvenlik sertleştirme (fail2ban, ssh config) | var | 2.1, 3.4 |
| Kernel/modül (lsmod/modprobe/sysctl) | YOK |  |
| Disk kotası/swap | YOK |  |

## Özet
Konu: 90 | Bulunan: 73 | Eksik: 17

- Eksik: S0 Linux/kernel/dağıtım kavramı
- Eksik: S0 Terminal/shell/prompt
- Eksik: S2 Mutlak/göreli yol
- Eksik: S2 inode
- Eksik: S3 stdin/stdout/stderr
- Eksik: S3 Tırnaklama
- Eksik: S4 /etc/passwd /etc/shadow /etc/group
- Eksik: S4 SUID/SGID/sticky
- Eksik: S4 chattr/lsattr
- Eksik: S4 Ana dizin /etc/skel
- Eksik: S5 kill/pkill/killall/sinyaller
- Eksik: S5 lsof/fuser
- Eksik: S5 GRUB/önyükleme süreci
- Eksik: S6 Ağ yapılandırma (nmcli/netplan)
- Eksik: S6 RAID/mdadm
- Eksik: S6 Kernel/modül (lsmod/modprobe/sysctl)
- Eksik: S6 Disk kotası/swap