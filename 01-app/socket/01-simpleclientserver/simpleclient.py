import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sock.connect( ("192.168.55.4", 9999) )

request = "Selamat pagi"
sock.send(request.encode("utf-8"))

data = sock.recv(256)
data = data.decode("utf-8")

print("Menerima response dari server : "+data)