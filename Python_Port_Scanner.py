import socket
import threading
import queue
import time
import sys

server = input("Enter the Host you wish to scan: ")
serverIP = socket.gethostbyname(server)
q = queue.Queue()

print("Please wait scanning Host...", serverIP)

startTime = time.time()

#Storing port numbers in queue
for i in range(1, 1026):
    q.put(i)


def scan():
    while not q.empty():
        port = q.get()
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(0.5)
            try:
                s.connect((serverIP, port))
                print(f"Port {port} is OPEN")

            except KeyboardInterrupt:
                print("CTRL+C has been pressed. Exiting now...")
                sys.exit()

            except socket.gaierror:
                print("Hostname could not be resolved. Exiting scanner.")
                sys.exit()
                
            except:
                pass
        q.task_done()

#Create number of threads we want to use
for i in range(300):
    t = threading.Thread(target=scan, daemon=True)
    t.start()

#All the q.done tasks have to be done before it prints "Scanning completed in: x"
q.join()

print("Scanning completed in:", round(time.time() - startTime, 2), "seconds")
print("Press 'Enter' to exit scanner...")

input()