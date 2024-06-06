import os, sys
if (os.fork() != 0) :
    if (os.fork() == 0) :
        os.fork()
        print("1")
    else :
        print("2")
else :
    print("3")
print("4")
sys.exit(0)