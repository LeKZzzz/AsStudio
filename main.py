# -*- coding: UTF-8 -*- 
# Creator：LeK
# Date：2022/10/13


from core import statusupdate, bilidynamic
import threading
import asyncio

if __name__ == '__main__':
    threads = []    # 子线程列表
    lock = threading.Lock()  # 线程锁
    loop = asyncio.new_event_loop()  # 创建事件循环传入模块
    asyncio.set_event_loop(loop)

    # 直播间状态更新线程
    statusupdate = threading.Thread(target=statusupdate.run, name='statusupdate', args=(loop, lock))
    threads.append(statusupdate)

    # b站开播动态线程
    bilidynamic = threading.Thread(target=bilidynamic.run, name='bilidynamic', args=(loop, lock))
    threads.append(bilidynamic)

    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
