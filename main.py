# -*- coding: UTF-8 -*- 
# Creator：LeK
# Date：2022/10/13


from core import statusupdate, bilidynamic
import threading

if __name__ == '__main__':
    threads = []
    # 直播间状态更新线程
    statusupdate = threading.Thread(target=statusupdate.run, name='statusupdate')
    threads.append(statusupdate)
    # b站开播动态线程
    bilidynamic = threading.Thread(target=bilidynamic.run, name='bilidynamic')
    threads.append(bilidynamic)

    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
