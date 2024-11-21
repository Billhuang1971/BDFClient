import binascii
import time
from datetime import datetime

import select
import socket
import threading
import pickle
import struct
import time

from concurrent.futures import as_completed
from concurrent.futures import ThreadPoolExecutor

class socketClient:
    def __init__(self):

        self.sock=None
        self.inputs = None
        self.executor= None
        self.hdpack = None

    def appMain(self, serverAddr, REQmsg):
        pass
    def sockOpenConn(self, s_ip, s_port):
        self.ip = s_ip
        self.port = s_port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # 生成socket
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # 不经过WAIT_TIME，直接关闭
        # self.sock.setblocking(False)  # 设置非阻塞编程

        self.inputs = [self.sock, ]
        self.executor = ThreadPoolExecutor(max_workers=1)  # 设置线程池最大数量
        print('client start!!!')
        try:
            self.sock.connect((self.ip, self.port))
        except Exception as e:
            print(f"socketClient.sockOpenConn:{e}")

    def sockClose(self):
        self.inputs.clear()
        self.sock.close()
        self.sock = None

    def handle_received_data(self, data):
        print("接收服务端信息:", data)
        self.appMain("", data)

    def receive_service_data(self):
       while True:
            try:
                r_list, _, _ = select.select(self.inputs, [], [])
                for event in r_list:
                    data, data_len = self.recv_msg(event)
                    if data:
                        try:
                            self.executor.submit(self.handle_received_data, data)
                        except Exception as e:
                            pass
                    else:
                        if event in self.inputs:
                            self.inputs.remove(event)
                            self.sock.close()
                            self.sock = None

            except Exception as e:
                print(f"receive_service_data：exit：{e}")
                exit()

    def send_client_data(self, sendData,  size=1):
        if len(sendData)>2:
            self.hdpack=[sendData[0],sendData[1],sendData[2]]
        else:
            self.hdpack =None
        print(f"客户端发送数据1：{sendData}")
        executors = []
        for i in range(size):
            exe = self.executor.submit(self.send_msg, self.sock, sendData)
            executors.append(exe)
        for feature in as_completed(executors):
            try:
                data, data_len = feature.result()
            except Exception as e:
                print(f"send_client_data.Exception：{e}")
                return False
            else:
                print(f"客户端发送数据：{data}, len:{data_len}")
                return True

    def checksum(self, data):
        chksum = 0
        for byt in bin(data)[2:]:
            chksum += int(byt)
        return chksum & 0xffffffff

    def send_msg(self, conn, data):
        time.sleep(1)
        msg = pickle.dumps(data)
        chknum = self.checksum(len(msg))
        msg0 = struct.pack('>Ii', len(msg), chknum) + msg
        conn.sendall(msg0)
        return data, len(msg0)

    def recv_from(self, conn, n):
        data = b''
        handle_len = 0
        stStime=None
        while handle_len < n:
            try:
                packet = conn.recv(n - handle_len)
                if not packet or packet == b'':
                    if n <= 8:
                        return None
                    print(f'网络掉包(' + str(handle_len) + "<" + str(n) + '), 纠验重置.')
                    if stStime is None:
                        stStime = datetime.datetime.now()
                    else:
                        now = datetime.datetime.now()
                        if int((now - stStime).total_seconds()) > 10:
                            return None
                    continue
                    # return None
                handle_len += len(packet)
                data += packet
                stStime = None
            except Exception as e:
                if n <= 8:
                    return None
                #return None
                if stStime is None:
                    stStime= datetime.now()
                else:
                    now=datetime.now()
                    if int((now - stStime).total_seconds())>10:
                        return None
                if handle_len < n:
                    print(f'异常包(' + str(handle_len) + "<" + str(n) + '),纠验当前操作.')
        return data

    def recv_msg(self, conn):
        hd = self.recv_from(conn, 8)
        if not hd:
            return None, 0
        dd = struct.unpack('>Ii', hd)
        chknum = self.checksum(dd[0])
        if dd[1] != chknum:
            return None, 0
        msg_len = dd[0]
        msg = self.recv_from(conn, msg_len)
        if msg is None:
            if self.hdpack is None or len(self.hdpack)<2:
               return None, 0
            else:
               data=[self.hdpack[0],self.hdpack[1],self.hdpack[2],['0','1','网络异常，接收数据不完整。']]
               return data,4
        msg = pickle.loads(msg)
        return msg, msg_len

