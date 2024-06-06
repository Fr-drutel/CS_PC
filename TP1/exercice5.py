import os,sys

pid = os.fork()
if pid == 0 :
    for i in range(1,101):
        print(i,end=" ")
    sys.exit(0)
else:
    os.wait()

print()

pid = os.fork()
if pid == 0 :
    for i in range(101,201):
        print(i,end=" ")
    sys.exit(0)
else:
    os.wait()

sys.exit(0)