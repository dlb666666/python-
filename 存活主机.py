from threading import Thread
from subprocess import PIPE,Popen
from queue import Queue

network = input('请输入网段如127.0.0.0/24\t\n')

def ping_check(ip):
    check = Popen(['ping', ip], stdin=PIPE, stdout=PIPE, stderr=PIPE, shell=True)
    data = check.stdout.read().decode('gbk')
    if 'TTL' in data:
        print(ip + '  is UP !!!')
        ip_list.append(ip)
    else:
        print(ip + '  is DOWN')

thread_list = []
ip_list = []

class check_threading(Thread):
    def __init__(self, ip, host):
        super(check_threading, self).__init__()
        self.ip = ip
        self.host = host
    
    def run(self):
        ip = self.ip + self.host
        ping_check(ip)

if __name__ == "__main__":
    try:
        network=network.split('/')
        net = network[1]
        ip_net = network[0].split('.')
        s = int(net)//8
        ip_net = '.'.join(ip_net[:s]) + '.'
        # 只实现了24子网的划分，其他子网多加循环 应该就可以了
        # 如果ping不通 会有超时等待 所以会先把存活的主机打印出来
        if s == 3:
            for host in range(1, 256):
                thread_list.append(check_threading(ip_net, str(host)))
            for thread in thread_list:
                thread.start()
            for thread in thread_list:
                thread.join()
    except IndexError:
        print('格式错误')

print("存活主机", ip_list)
# 格式感觉很丑 可以优化