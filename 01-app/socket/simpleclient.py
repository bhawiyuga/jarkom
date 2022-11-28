import socket

# Protokol TCP di layer Transport dan IPv4 di layer Network
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Koneksi ke server dengan IP dan port tertentu
sock.connect(("18.140.224.119", 8000))

data = "Selamat siang"

sock.send(data.encode("utf-8"))

data = sock.recv(100)

data = data.decode("utf-8")

print(data)

sock.close()