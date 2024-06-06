import os,sys
N = 1

for i in range(N) :
#__________début des ajouts_________
    os.fork()
    os.fork()
# __________fin des ajouts__________

print("Bonjour")
sys.exit(0)