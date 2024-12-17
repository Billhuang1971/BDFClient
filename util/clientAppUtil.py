import ast
import os
import time, shutil
import hashlib
import uuid
import json
import re


class clientAppUtil():
    def __init__(self):
        self.root_path = os.path.join(os.path.dirname(__file__))[:-16]
        self.model_path = self.root_path + 'client_root\\upload\\model\\'
        self.path = os.path.dirname(__file__)

    def get_now_datetime(self):
        """
        @Description: 返回当前时间，格式为：年月日时分秒
        """
        return time.strftime('%Y-%m-%d-%H_%M_%S', time.localtime(time.time()))

    def get_now_time(self):
        """
        @Description: 返回当前时间，格式为：时分秒
        """
        return time.strftime('%H-%M-%S', time.localtime(time.time()))

    def get_now_date(self):
        """
        @Description: 返回当前时间，格式为：年月日
        """
        return time.strftime('%Y-%m-%d', time.localtime(time.time()))

    def GetSocketIpFile(self):
        f = open(os.path.join(self.path, 'server.txt'))
        d = f.readline()
        f.close()
        sysd = eval(d)
        s_ip = sysd['server_ip']
        s_port = sysd['server_port']
        return s_ip, s_port

    def md5_string(self, in_str):
        md5 = hashlib.md5()
        md5.update(in_str.encode("utf8"))
        result = md5.hexdigest()
        return result

    def getMacAddress(self):
        mac = uuid.UUID(int=uuid.getnode()).hex[-12:]
        return ':'.join([mac[e:e + 2] for e in range(0, 11, 2)])


    # 按字节读取文件
    # 读取某文件目录固定块的脑电文件数据
    def readFile(self, file_path, block_size, block_id):
        try:
            with open(file_path, 'rb') as f:
                received_size = (block_id - 1) * block_size
                f.seek(received_size)
                data = f.read(block_size)
                if not data:
                    return
                else:
                    print(data[:100], "\n")
        except Exception as e:
            print('readEEG', e)
        return data

    # 按字节读取文件
    def readByte(self, file_path, block_size, block_id):
        try:
            print(f'readFile file_path: {file_path}, block_size:{block_size}, block_id: {block_id}')
            with open(file_path, 'rb') as f:
                received_size = (block_id - 1) * block_size
                f.seek(received_size)
                data = f.read(block_size)
                if not data:
                    return
        except Exception as e:
            print('readFile', e)
        return data

    # 写文件功能
    def writeByte(self, savePath, data):
        try:
            with open(savePath, 'ab') as f:
                f.write(data)
        except Exception as e:
            print('writeByte', e)

    # 清空指定路径，指定文件名开头文件
    # 1.仅传入filepath，清空文件夹文件
    # 2.传入filepath与filename，删除指定文件
    # 3.传入filepath与fullname，删除指定文件名开头文件（同时删除脑电文件及txt文件）
    def empty(self, filepath, filename='', fullname=''):
        # 获取文件夹下所有文件
        fileslist = os.listdir(filepath)
        # 删除所有文件
        if filename == '' and fullname == '':
            for file in fileslist:
                file_path = os.path.join(filepath, file)  # 获取文件的完整路径
                os.remove(file_path)  # 删除文件
        # 删除某一文件名文件
        elif filename == '' and fullname != '':
            for file in fileslist:
                if file == fullname:
                    file_path = os.path.join(filepath, file)  # 获取文件的完整路径
                    os.remove(file_path)
        # 删除指定文件名开头文件
        else:
            # 遍历文件夹中的文件
            for file in fileslist:
                if file.startswith(filename):  # 判断文件名是否以指定的文件名开头
                    file_path = os.path.join(filepath, file)  # 获取文件的完整路径
                    os.remove(file_path)  # 删除文件

    def isNull(self, filepath):
        if not os.path.exists(filepath):  # 判断路径是否存在
            return False
        if os.path.isdir(filepath):  # 如果是文件夹
            return not os.listdir(filepath)  # 文件夹为空返回True
        if os.path.isfile(filepath):  # 如果是文件
            # 如果是json文件
            if filepath.endswith('.json'):
                try:
                    # 加载 JSON 文件内容
                    with open(filepath, 'r', encoding='utf-8') as file:
                        data = json.load(file)
                        # 判断 "task" 是否存在且非空
                        return not data.get("task") or not isinstance(data["task"], list) or not any(data["task"])
                except (json.JSONDecodeError, KeyError):  # 捕获 JSON 格式错误或 KeyError
                    return True  # 如果解析失败，认为文件无效/为空
                return False  # 其他情况，默认返回 False
            else:
                return os.path.getsize(filepath) == 0  # 文件大小为0返回True

    # 写文件功能
    def writeEEG(self, savePath, data):
        try:
            with open(savePath, 'ab') as f:
                f.write(data)
        except Exception as e:
            print('writeEEG', e)

    def bdfMontage(self,channels):
        ch0s = ['Fp1', 'Fp2', 'F7', 'F3', 'Fz', 'F4', 'F8', 'T3', 'C3', 'Cz', 'C4', 'T4', 'T5', 'P3', 'Pz', 'P4', 'P6',
                'O1', 'O2']

        dgroup = {}

        chlen=len(channels)
        if chlen<=0:
            return dgroup
        i=0
        while i < chlen:
            cha=channels[i]
            if cha.upper() in ch0s:
                return {}
            bg = []
            i+=1
            try:
               n=int(cha[-1])
            except ValueError:
                continue
            if n!=1 :
                continue
            bkey= cha[:-1]
            bg.append(cha)
            while i < chlen:
                n+=1
                cha=channels[i]
                if cha.upper() in ch0s:
                    return {}
                if cha==f'{bkey}{n}':
                    bg.append(cha)
                    i+=1
                else:
                    if n>1:
                        dgroup.setdefault(bkey,bg)
                    break
            if i >= chlen and n>1:
                        dgroup.setdefault(bkey,bg)
        print(dgroup)
        return dgroup

    def makeTxt(self, file_path):
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write('')

    # 写Txt功能
    def writeTxt(self, file_path, content):
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(content)
        return True

    def readTxt(self, file_path):
        pattern = r'.*?\.npz\s*, \s*.*?\.npz\s*, \s*block_id=\d+\s*, \s*blockN=\d+'
        with open(file_path, 'r') as file:
            content = file.read()
            print(content)

        if not os.path.exists(file_path) or not bool(re.match(pattern, content)):
            # if os.path.exists(file_path):
            #     os.remove(file_path)
            return False, '文件已损坏'
        else:
            return True, content


if __name__ == '__main__':
    a = clientAppUtil()
    print(a.root_path)
