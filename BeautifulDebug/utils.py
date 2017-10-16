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

        print(Fore.YELLOW + 'content:')
        if obj is None:
            self.dump_None()
        if isinstance(obj, str):
            self.dump_str(obj, *args, **kw)
        elif isinstance(obj, dict):
            self.dump_dict(obj, *args, **kw)

        # self.check_attribute(type_)

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

    def dump_dict(self, obj, *args, **kw):
        # print('\t{}{}'.format(Fore.CYAN, obj))
        print('\t{')
        for key, value in obj.items():
            print("\t   '{}'".format(key), end='')
            print(" : ", end='')
            format_ = "'{}'"
            if isinstance(value, int):
                format_ = "{}"
            print(format_.format(value))

        print('\t}')

    def dump_module(self):
        ''' 模块'''
        pass

    def dump_str(self, obj, *args, **kw):
        ''' 字符串 '''
        print(Fore.YELLOW+"content:")
        print(Fore.CYAN + '\t{}'.format(obj))

    def check_attribute(self, obj):
        '''显示对象的方法'''
        # arithmetic = {}
        # function = {}
        for key in obj.__dict__.keys():
            # print(getattr(obj, key).__doc__)
            doc = getattr(obj, key).__doc__
            print(Fore.CYAN + key+ ':\t', end='')
            if doc is not None:
                print(Style.DIM + doc)


        # print(Fore.YELLOW + 'arithmetic:')
        # self.show_arthmetic(arithmetic, separator='\t{} ', detail=False)
        # print('\n'+Fore.YELLOW + 'Function:')
        # self.show_arthmetic(function)
                # print('\t'+Fore.YELLOW + key + ':\t', end='')
                # print(Style.DIM + str(value))

    # def show_function(data):

    def show_arthmetic(self, data, separator = '\t{}:\t', detail = True):
        '''显示操作符'''
        for key, value in data.items():
            print(separator.format(Fore.CYAN + key), end='')
            if detail is True:
                print(Style.DIM + str(value))

    arithmetic = [
        '__add__',
        '__mod__',
        '__mul__',
        '__rmod__',
        '__rmul__'
    ]
