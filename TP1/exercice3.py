import os,sys
for i in range(4) :
    pid = os.fork()
    if pid != 0 :
        print("Ok !")   
    print("Bonjour !")
sys.exit(0)