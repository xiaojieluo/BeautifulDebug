from .settings import Setting
import time
import traceback
import sys
from colorama import Fore, Back, Style, init

init(autoreset=True)

class Dump(object):
    def __init__(self, setting={}):
        self.setting = Setting()

    def run(self, obj, *args, **kw):
        # 分隔符
        self.separator()

        stack = traceback.format_stack()
        stack.pop(-1)
        for line in stack:
            print(Style.DIM + '>> '+line.strip())

        type_ = type(obj)
        print(Fore.YELLOW + 'type:')
        print(Fore.CYAN + '\t{}'.format(type_))

        if obj is None:
            self.dump_None()

        if isinstance(obj, str):
            self.dump_str(obj, *args, **kw)

    def separator(self):
        '''显示分隔符'''
        if self.setting.separator is not None:
            print(Style.DIM + self.setting.separator)


    def check(self):
        '''检查 obj 类型'''
        pass

    def dump_None(self):
        print("None")
        pass

    def dump_object(self):
        ''' 对象类型'''
        pass

    def dump_module(self):
        ''' 模块'''
        pass

    def dump_str(self, obj, *args, **kw):
        ''' 字符串 '''
        print(Fore.YELLOW+"content:")
        print(Fore.CYAN + '\t{}'.format(obj))
