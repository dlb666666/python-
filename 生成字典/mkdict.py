from threading import Thread, Lock
import exrex
import re
import argparse


lock = Lock()
default_random = "0"
chars = "!@#$%^&*()_+"
threads = []
dic_file = "dict.txt"
pass_file = "pass.txt"
thread_content = 10

options = {
    "1":"{d}{w}[{c}]{{{n}}}",
    "2":"{d}[{c}]{{{n}}}{w}",
    "3":"{w}{d}[{c}]{{{n}}}",
    "4":"{w}[{c}]{{{n}}}{d}",
    "*":"{d}{w}[{c}]{{{n}}}|{d}[{c}]{{{n}}}{w}|{w}{d}[{c}]{{{n}}}|{w}[{c}]{{{n}}}{d}"
}


parser = argparse.ArgumentParser(prog='mkdict.py')
group = parser.add_mutually_exclusive_group()
parser.add_argument("-n", "--number", default=default_random, help="Add characters randomly")
parser.add_argument("-c",  "--chars", default=chars, help="Replace characters")
parser.add_argument("-w", "--passwd", default=pass_file, help="password absolute path")
parser.add_argument("-p", "--position", default="2", help="chars postion, options 1,2,3,4,*")
parser.add_argument("-r", "--rule", help="d dict c chars w passwd ==> dcw")
group.add_argument("-d", "--dict", default=dic_file, help="dict absolute path")
group.add_argument("-l", "--list", nargs="*", help="password list, split by space")
cmd = parser.parse_args()


dics = open(cmd.dict,"r")
pwds = open(cmd.passwd, "r")
if cmd.list:
    dics = cmd.list

kw1 = {"n":cmd.number, "c":cmd.chars}

def make_dict(dics, pwds):
    for dic in dics:
        lock.acquire()
        kw2 = {"d":dic.strip()}
        for pwd in pwds:
            if '*' in pwd or '?' in pwd:
                pwd = pwd.replace("*","\\*")
                pwd = pwd.replace("?","\\?")
            kw2 = {"d":r''+ dic.strip()}
            kw3 = {"w":r''+ pwd.strip()}
            kw = dict(kw1, **kw2, **kw3)
            rule = options[cmd.position].format(**kw)
            if cmd.rule:
                rule = cmd.rule.replace("d","{d}").replace("w","{w}").replace("c","[{c}]{{{n}}}")
                rule = rule.format(**kw)
            new_dict = list(exrex.generate(rule))
            for _ in new_dict:
                with open("password.txt","a") as f:
                    f.write(_ + "\r")
        try:
            pwds.seek(0)
        except:
            pass
        lock.release()

for th in range(thread_content):
    threads.append(Thread(target=make_dict, args=(dics,pwds)))

for th in threads:
    th.start()

for th in threads:
    th.join()
