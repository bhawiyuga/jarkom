## Install docker
```bash
curl -fsSL https://test.docker.com -o test-docker.sh; sudo sh test-docker.sh
sudo usermod -aG docker $(whoami)
newgrp docker
```

## One line script to install containernet

```bash
curl -fsSL https://bit.ly/installcontainernet -o installcontainer.sh; bash installcontainer.sh
```

## Akses mesin virtual (VM) Mininet dengan SSH dan xterm

```bash
ssh -Y user@alamat-ip-vm
```

Untuk pengguna MacOS nyalakan XQuartz dan untuk pengguna Windows nyalakan Xmingw

### Troubleshooting
- X11 connection rejected because of wrong authentication
1. Akses VM dengan ssh -Y
2. Jalankan perintah berikut untuk memastikan bahwa user root juga punya cookie akses
```bash
sudo xauth add $(xauth list $DISPLAY)
```
