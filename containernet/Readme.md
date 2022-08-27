# Lab Virtual Praktikum Jaringan Komputer berbasis Containernet
Praktikum Jaringan Komputer di Program Studi Teknik Informatika Universitas Brawijaya memanfaatkan platform containernet.

## Instalasi dan Persiapan Lingkungan Kerja
### Kebutuhan perangkat
Containernet membutuhkan perangkat host, dalam bentuk mesin fisik maupun mesin virtual, dengan sistem operasi Ubuntu 20.04 atau 18.04 dengan arsitektur prosesor x86-64 atau arm64. Perangkat host ini dapat disediakan dengan beberapa cara :
1. Menggunakan mesin virtual lokal (VM) berbasis perangkat lunak hypervisor seperti VirtualBox, VMWare, Parallels Desktop atau KVM. Mesin virtual dapat dibuat secara manual maupun memanfaatkan perangkat provisioning seperti Vagrant (https://app.vagrantup.com/bento/boxes/ubuntu-20.04).
2. Menggunakan mesin virtual cloud berbasis layanan AWS EC2 pada platform AWS Academy. Petunjuk penggunaan AWS Academy bagi mahasiswa UB dapat dilihat pada tautan berikut https://docs.google.com/document/d/1tEuVmvbfvvDccGbqV2BSZTLiB65iz6pNcHYl7Vk7YKA/edit?usp=sharing. Anda dapat memanfaatkan AMI berjenis Cloud9 Ubuntu dengan jenis instance t2-small. Sebagai catatan, setelah selesai digunakan mesin virtual harap dimatikan (Stop) agar kredit tidak cepat habis.
3. Menggunakan mesin fisik yang sudah dilengkapi dengan sistem operasi Ubuntu 20.04 atau 18.04.

### Instalasi Docker pada perangkat host Ubuntu
```bash
curl -fsSL https://test.docker.com -o test-docker.sh; sudo sh test-docker.sh
sudo usermod -aG docker $(whoami)
newgrp docker
```

### Instalasi containernet pada perangkat host Ubuntu

```bash
curl -fsSL https://bit.ly/installcontainernet -o installcontainer.sh; bash installcontainer.sh
```

### Akses mesin virtual host Ubuntu dengan SSH dan xterm
Untuk mengakses mesin virtual menggunakan protokol SSH, anda dapat memanfaatkan aplikasi Terminal (Linux/MacOS), GitBash, PowerShell atau WSL (Windows) dengan menjalankan perintag berikut.  

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
## Menjalankan Containernet
### Menjalankan Topologi Contoh
### Menjalankan Perintah pada Perangkat Virtual
### Membangun Topologi Sendiri
#### Mendefinisikan perangkat host
#### Mendefinisikan perangkat router
#### Mendefinisikan perintah saat startup
