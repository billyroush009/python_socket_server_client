# echo-client.py

import socket
import datetime, time

while True:
    HOST = "127.0.0.1"  # The server's hostname or IP address
    PORT = 4000  # The port used by the server

    #time_start = datetime.datetime.now()
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        #testing one connection w/ repeating requests (still ~4 sec)
        while True:
            time_start = datetime.datetime.now()
            #s.sendall(b"Hello, world")
            #s.sendall(b"{cmd: r, tag: <full_tag_name>}")
            s.sendall(b'{"cmd": "r", "tag": "Program:HM1450_VS14.VPC1.O.LoadProgram"}')
            data = s.recv(1024)

            time_1_end = datetime.datetime.now()
            time_diff = (time_1_end - time_start)
            execution_time = time_diff.total_seconds() * 1000
            print(f'({PORT}) Read took : {execution_time} ms\n')
            print(f"\n({PORT}) Received {data!r}\n")
            time.sleep(1)

    HOST = "127.0.0.1"  # The server's hostname or IP address
    PORT = 4001  # The port used by the server
    time_2_start = datetime.datetime.now()
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.sendall(b"Hello, world")
        data = s.recv(1024)

    time_2_end = datetime.datetime.now()
    time_diff = (time_2_end - time_2_start)
    execution_time = time_diff.total_seconds() * 1000
    print(f'({PORT}) Read took : {execution_time} ms\n')
    print(f"\n({PORT}) Received {data!r}\n")

    time_diff = (time_2_end - time_start)
    execution_time = time_diff.total_seconds() * 1000
    print(f'Both Reads Took : {execution_time} ms\n')
    time.sleep(1)
