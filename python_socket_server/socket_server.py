# echo-server.py

import socket
#from pycomm3 import LogixDriver
#from pycomm3.cip.data_types import DINT, UINT
import json
import threading
import sys

#HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
#PORT = 4000  # Port to listen on (non-privileged ports are > 1023)

kill_threads = False

def start_server(host, port):
    global kill_threads

    while True:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((host, port))
            print(f'({host}):({port}) Alive and listening!\n')
            #print(f'({host}):({port}) Connecting to PLC...\n')
            #with LogixDriver('120.57.42.114') as plc:
            #print(f'({host}):({port}) Connected to PLC!\n')
            try:
                while True:
                    if(kill_threads):
                        print(f'({host}):({port}) kill_threads True, restarting threads...')
                        break
                    s.listen()
                    conn, addr = s.accept()
                    with conn:
                        print(f"({host}):({port}) Connected by {addr}\n")
                        while True:
                            data = conn.recv(1024)
                            if not data:
                                break
                            request_result = {}
                            data_txt = data.decode("utf-8")
                            #print(data_txt)
                            request_result = json.loads(data_txt)
                            #print(request_result)
                            #print(request_result['cmd'])
                            
                            #cleaning message, data_cmd will be 'r' or 'w', data_tag will be '<full_tag_name>'
                            data_list = []
                            data_list = data_txt.split(',')
                            data_list_cmd = data_list[0].split(' ')
                            data_cmd = data_list_cmd[1]
                            data_list_tag = data_list[1].split(' ')
                            

                            response_string = '{ok' #beginning of response for either read or write request
                            print(data_cmd)

                            if(port == 4000):
                                if(data_cmd == '\"r\"'):
                                    print('READ')
                                    data_tag = data_list_tag[2]
                                    data_tag = data_tag.strip('}')
                                    #plc_value = read_plc_tag(plc, data_tag)
                                    #response_string = response_string + ', ' + plc_value + '}\n'
                                elif(data_cmd == '\"w\"'):
                                    data_tag = data_list_tag[2]
                                    print(data_tag)
                                    #print(data_list[2])
                                    data_tag_value_list = data_list[2].split()
                                    data_tag_value = data_tag_value_list[1]
                                    data_tag_value = data_tag_value.strip('}')
                                    print(data_tag_value)
                                    print('WRITE')
                                else:
                                    print('Invalid Command (should be \'r\' or \'w\')')
                            elif(port == 4001):
                                #plc_result = read_plc_dict('15', plc)
                                #plc_result['1'] = str(data)
                                pass
                            else:
                                print('Invalid Server Port! Should be : 4000 or 4001')
                            #print(data_list)
                            #print(data_cmd)
                            #print(data_tag)
                            test_bool = True
                            conn.sendall(str('{ok, ' + str(test_bool) + '}\n').encode())
                            #plc_result_json = json.dumps(plc_result) + '\n'
                            #print(sys.getsizeof(plc_result_json))
                            #conn.sendall(plc_result_json.encode())
                            #print(f'({host}):({port}) Sent Booleans to {addr}')
                    if(kill_threads):
                        print(f'({host}):({port}) kill_threads True, restarting threads...')
                        break
            except Exception as e:
                print(f'({host}):({port}) Exception : {str(e)}')
                kill_threads = True

def main():
    global kill_threads

    # Thread declaration / initialization
    t1 = threading.Thread(target=start_server, args=["127.0.0.1", 4000])
    t2 = threading.Thread(target=start_server, args=["127.0.0.1", 4001])
    #start_server(HOST, PORT)

    kill_threads = False
    t1.start()
    t2.start()

    t1.join()
    t2.join()
    pass

#implicit 'main()' declaration
if __name__ == '__main__':
    while(True):
        main()
        print('Main Loop Disrupted, restarting servers...')