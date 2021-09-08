import socket

# Menginisiasi object socket dengan layer Transport TCP dan pengalamatan ipv4
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Binding. Kenapa butuh binding? karena server itu harus punya alamat IP dan port yang tidak berubah
sock.bind( ("", 9999) )

# Listen 
sock.listen(100)

while True :
    # Terima permintaan koneksi dari client
    conn, address = sock.accept()
    # Baca 256 byte data dari client
    data = conn.recv(256)
    # Decode dari bytes ke string
    data = data.decode("utf-8")
    print("Menerima request dari client : "+data)
    data = "OK "+data
    # Kirim kembali sebagai response ke client
    conn.send(data.encode("utf-8"))