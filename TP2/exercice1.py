import os,sys


pid = os.fork()
if pid == 0 :
    try:
        os.execlp("python3", "python3", "programme1.py")
    except:
        print("erreur")
else:
    try:
        os.execlp("python3", "python3", "programme2.py")
    except:
        print("erreur")


