import src.main.util.Image as im

from threading import Thread, Lock
# im.readPicture('F:\\abc\\6.png')
# im.appendCsvFileByDirectry("F:\\abc",True)
im.appendCsvFileByFileName("F:\\7.png",False)
xx=['2.png', '3.png', '4.png', '5.png', '6.png']
lock=Lock()
def aa(a):
    global xx
    flag = True
    while flag:
        lock.acquire()
        z=0
        flag = len(xx)>0
        if flag:
            z=xx.pop()
        lock.release()
        print(z)
def b():
    thread1 = Thread(target=aa, args=(dir,))
    thread2 = Thread(target=aa, args=(dir,))
    thread1.start()
    thread2.start()
    thread1.join()
    thread2.join()
# b()