import zmq
import json

context = zmq.Context()

socket = context.socket(zmq.SUB)
socket.connect("tcp://localhost:5555")
socket.setsockopt(zmq.SUBSCRIBE, b'')

def monitor():
    #HANDLE SOCKET ERRORS
    try:
        while True:
            print(socket.recv_json())
    except socket.error:
        print("There is an error")
    except KeyboardInterrupt:
        print("Monitoring Stopped")

def ShowLastRecord():
    #ASSIGNING THE OUTPUT WE GET TO A DICTIONARY INSIDE FUNCTIONS BECAUSE WE DONT WANT TO DO IT UNLESS USER WANTS TO ACCESS IT
    dict = socket.recv_json()
    last_module=dict['module']
    last_timestamp=dict['timestamp']
    last_state=dict['state']
    last_stream=dict['log-stream']
    last_message=dict['log-message']

    while True:
        print("1)Module")
        print("2)timestamp")
        print("3)State")
        print("4)Log-Stream")
        print("5)Log-Message")
        print("6)Back To Menu")
        choice=int(input("Which record do you want to see?  "))

        if choice==1:
            print(last_module)
        elif choice==2:
            print(last_timestamp)
        elif choice==3:
            print(last_state)
        elif choice==4:
            print(last_stream)
        elif choice==5:
            print(last_message)
        elif choice==6:
            Menu()
        else:
            print("Invalid choice please try again")

#def keepTrack():
#   dict = socket.recv_json()
#    last_module=dict['module']
#    last_timestamp=dict['timestamp']
#    last_state=dict['state']
#    last_stream=dict['log-stream']
#    last_message=dict['log-message']
#    firstAppearence=["x"]
#    lastAppearence=["x"]
#    
#    firstAppearence[0]=last_timestamp 
#    lastAppearence=list(dict.values())
#
#    print("First appearence of modules are " + firstAppearence[0])
#    print("Last appearence of modules are " + lastAppearence[1])


def Menu():
    print("1) Monitor the logs")
    print("2) Check the last value of any record")
    pick=int(input("What do you want to do?  "))

    if pick == 1:
        monitor()

    elif pick == 2:
        ShowLastRecord()

    else:
        print("Invalid Choice")


Menu()

