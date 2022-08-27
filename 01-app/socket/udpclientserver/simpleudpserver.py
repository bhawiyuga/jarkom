import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('', 6428) )

while True:
    # Terima data dari client beserta alamatnya
    data, clientAddress = sock.recvfrom(1024)
    # Cetak informasi
    print("Menerima data ", str(data), " dari ", clientAddress)
    # Kirimkan balasan ke client
    data = data.decode("utf-8")
    data = "OK "+data
    sock.sendto(data.encode("utf-8"), clientAddress)

