# echo-server.py

import socket

HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
PORT = 65432  # Port to listen on (non-privileged ports are > 1023)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print("listenning ....")
    conn, addr = s.accept()
    with conn:
        print(f"Connected by {addr}")
        while True:
            s.close()
            break
            data = conn.recv(1024)
            print(data)
            if str(data, "utf-8") == "close":
                conn.sendall(b"close done!")
                s.close()
                break
            conn.sendall(data)
            # conn.close()
            # s.close()
            # break
        print("done")
    
        