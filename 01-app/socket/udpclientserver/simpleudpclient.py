import socket

# Inisiasi socket udo
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('', 9157))
# Pengiriman pesan ke server dengan port 6428
data = "Selamat pagi"
serverAddr = ("127.0.0.1", 6428)
sock.sendto(data.encode("utf-8"), serverAddr)
# Terima balasan dari server
data, serverAddress = sock.recvfrom(1024)
data = data.decode("utf-8")
print("Menerima balasan dari server : ",serverAddress, " pesan ", data )