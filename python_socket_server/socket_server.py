# echo-server.py

'''
Ritesh wants to see the C# implementation in place. 
Since my current PLC api still has a problem reading .O bools I need you to modify your plc server to just read the .O signals from the PLC. 
* Write it as a socket server to listen on 127.0.0.1:4000 for robot 2 requests and 127.0.0.1:4001 for robot 3 read requests. *
I'm using different sockets to keep the communications simple. Request format will be simply a text string "read\n".

When you get a read request, read the signals from the plc for the corresponding robot and put the result into a dictionary. 
Use the same format as in your test program with the last part of the tag name as the key and the result should be a bool (True | False). 
Use json.dumps(<dictionary>) to serialize the dictionary and return the serialized string terminated with "\n".
'''

import socket
#from pycomm3 import LogixDriver
#from pycomm3.cip.data_types import DINT, UINT
import json
import threading
import sys

#HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
#PORT = 4000  # Port to listen on (non-privileged ports are > 1023)

kill_threads = False

# global variable declarations, some are probably unnecessary(?)
'''
arrayOutTags = [
    'LoadProgram',
    'StartProgram',
    'EndProgram',
    'EndScan',
    'AbortProgram',
    'Reset'
    ];
'''

arrayOutTags = [
    'LoadProgram',
    'StartProgram',
    'EndProgram',
    'AbortProgram',
    'Reset',
    'PartType',
    'PartProgram',
    'ScanNumber',
    'PUN{64}',
    'GMPartNumber{8}',
    'Module',
    'PlantCode',
    'Month',
    'Day',
    'Year',
    'Hour',
    'Minute',
    'Second',
    'QualityCheckOP110',
    'QualityCheckOP120',
    'QualityCheckOP130',
    'QualityCheckOP140',
    'QualityCheckOP150',
    'QualityCheckOP310',
    'QualityCheckOP320',
    'QualityCheckOP330',
    'QualityCheckOP340',
    'QualityCheckOP360',
    'QualityCheckOP370',
    'QualityCheckOP380',
    'QualityCheckOP390',
    'QualityCheckScoutPartTracking'
    #'KeyenceFltCode',
    #'PhoenixFltCode'
    ];

tagKeys = []
for tag in arrayOutTags:
    tagKeys.append(tag.split("{")[0]) # delete trailiing { if it exists

#single-shot read of all 'arrayOutTags' off PLC
def read_plc_dict(machine_num, plc):
    #print("read_plc_dict, generating list of read tags")
    readList = []
    for tag in arrayOutTags :
        newTag = 'Program:HM1450_VS' + machine_num + '.VPC1.O.' + tag;
        #print(newTag);
        readList.append(newTag)
        
    resultsList = plc.read(*readList) # tag, value, type, error
    readDict = {}

    #print("returned results")
    #print(resultsList)

    for tag in resultsList:
        key = tag.tag.split(".")[-1]
        #key = tag[0] #prints entire tag name, Program:HM1450_VS' + machine_num + '.VPC1.O.' + tag
        #print(key)
        #print(tag)
        readDict[key] = tag[1]

    #print(readDict)
    return readDict
#END read_plc_dict

def read_plc_tag(plc, tag):
    read_plc = plc.read(tag)
    read_plc_value = str(read_plc[1])
    return read_plc_value

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