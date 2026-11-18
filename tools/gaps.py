import json,re
inv=json.load(open('INVENTORY.json',encoding='utf-8'))
# seviye -> (konu, [anahtar kelimeler: biri yeterli])
C={
0:[("Linux/kernel/dağıtım kavramı",["kernel"]),("Sanal makine kurulumu",["virtualbox","vm"]),("Terminal/shell/prompt",["prompt"])],
1:[("pwd/ls/cd",["pwd"]),("whoami/id/uname",["uname"]),("man/--help/apropos",["apropos","man "]),("Çıkış kodu $?, &&, ||",["&&"]),("Ortam değişkeni PATH/export",["export"]),("alias",["alias"]),("history",["history"]),("which/type",["which"]),("date/uptime/hostname",["hostname"]),("Shell tamamlama (Tab)",["tab"])],
2:[("Dizin ağacı FHS",["/etc","/var"]),("mkdir/touch/rm/rmdir",["rmdir"]),("cp/mv",["mv "]),("Mutlak/göreli yol",["absolute"]),("ln (sembolik/sert bağ)",["ln -s"]),("stat/file",["stat "]),("cat/less/head/tail/wc",["tail"]),("nano/vim temel",["vim"]),("df/du/free",["df "]),("mount/umount",["mount"]),("fdisk/lsblk/mkfs",["lsblk"]),("ssh/scp/rsync",["scp"]),("ping/curl/wget",["curl"]),("cron/crontab/at",["crontab"]),("fstab",["fstab"]),("inode",["inode"])],
3:[("stdin/stdout/stderr",["stderr"]),("Yönlendirme > >> 2>",["2>"]),("Pipe |/tee",["tee"]),("Joker karakter glob",["glob"]),("Tırnaklama",["quot"]),("grep (-i -r -v -E)",["grep -i","grep -r"]),("find (-name -type -exec)",["find "]),("sort/uniq/cut/tr",["uniq"]),("sed",["sed "]),("awk",["awk "]),("diff/cmp/comm/patch",["patch"]),("tar/gzip/bzip2/xz/zip",["bzip2","xz"]),("xargs",["xargs"]),("Düzenli ifade (regex)",["regex","regular expression"]),("Komut yerine koyma $(...)",["$("]),("here-doc",["<<"]),("locate/updatedb",["locate"])],
4:[("who/w/last",["last "]),("useradd/usermod/userdel",["usermod"]),("passwd/chage (parola yaşlandırma)",["chage"]),("/etc/passwd /etc/shadow /etc/group",["/etc/shadow"]),("groupadd/gpasswd",["groupadd"]),("su/sudo/visudo",["visudo"]),("chmod sembolik+oktal",["chmod"]),("chown/chgrp",["chgrp"]),("umask",["umask"]),("SUID/SGID/sticky",["sticky"]),("ACL (getfacl/setfacl)",["setfacl"]),("chattr/lsattr",["chattr"]),("Ana dizin /etc/skel",["skel"])],
5:[("ps/top/pstree",["pstree"]),("kill/pkill/killall/sinyaller",["killall"]),("nice/renice",["renice"]),("jobs/bg/fg/nohup",["nohup"]),("htop/vmstat/iostat/free",["vmstat"]),("lsof/fuser",["lsof"]),("apt/dpkg",["dpkg"]),("dnf/yum/rpm",["rpm"]),("Depo yönetimi (sources.list/.repo)",["repo"]),("systemctl (start/enable/status)",["systemctl"]),("journalctl",["journalctl"]),("/var/log, rsyslog, logrotate",["logrotate"]),("Hedef/runlevel (systemctl get-default)",["get-default","runlevel"]),("GRUB/önyükleme süreci",["grub"]),("dmesg",["dmesg"])],
6:[("ip/ss/DNS/ports",["ss "]),("/etc/hosts /etc/resolv.conf",["resolv"]),("Ağ yapılandırma (nmcli/netplan)",["nmcli","netplan"]),("SELinux (getenforce/restorecon/setsebool)",["restorecon"]),("firewalld (firewall-cmd)",["firewall-cmd"]),("iptables/nftables/ufw",["iptables","nft","ufw"]),("LVM (pvcreate/vgcreate/lvextend)",["lvextend"]),("RAID/mdadm",["mdadm"]),("Bash betik: değişken/koşul",["if ["]),("Bash betik: döngü/fonksiyon",["for "]),("systemd timer",["timer"]),("Betik hata ayıklama (set -e, bash -x)",["set -e","bash -x"]),("SSH anahtarı (ssh-keygen)",["ssh-keygen"]),("Güvenlik sertleştirme (fail2ban, ssh config)",["sshd_config"]),("Kernel/modül (lsmod/modprobe/sysctl)",["sysctl","modprobe"]),("Disk kotası/swap",["swap"])],
}
out=["# GAPS.md - Kapsam taraması (otomatik: tools/gaps.py)\n","> Cetvel: `tools/gaps.py` içindeki konu listesi (LPIC-1/RHCSA temeli). Anahtar kelime yalnızca komut kartlarında (cmd/example) aranır; 'yok' = hiçbir modülde geçmiyor.\n"]
miss=[];tot=0;found=0
for lv,items in C.items():
    out.append(f"\n## Seviye {lv}\n| Konu | Durum | Modüller |\n|---|---|---|")
    for name,kws in items:
        tot+=1
        mods=[i for i,v in inv.items() if any(k in ' '.join(c[0]+' '+c[1] for c in v['cmds']).lower()+' ' for k in kws)]
        own=[i for i in mods if inv[i]['level']==lv]
        if not mods: st="YOK";miss.append((lv,name))
        else: st="var";found+=1
        out.append(f"| {name} | {st} | {', '.join(mods[:6])}{'…' if len(mods)>6 else ''} |")
out.append(f"\n## Özet\nKonu: {tot} | Bulunan: {found} | Eksik: {len(miss)}\n")
out+= [f"- Eksik: S{l} {n}" for l,n in miss]
open('GAPS.md','w',encoding='utf-8').write('\n'.join(out))
print(tot,found,len(miss)); [print(l,n) for l,n in miss]
