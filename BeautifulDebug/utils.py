from .settings import Setting
import time
import traceback
import sys
from colorama import Fore, Back, Style, init
import types
import inspect
from .defines import ATTR_MAP, ATTR_EXCEPTION_MAP
# from .defines import ATTR_MAP
import pprint
# print(sys.path)
# import define

# SPECIAL_ATTRIBUTE = [
#     '__doc__'
# ]
init(autoreset=True)

class Dump(object):
    def __init__(self, setting={}):
        self.setting = Setting()

    def run(self, obj, *args, **kw):
        self.obj = obj
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
        print(inspect.isclass(obj))
        if obj is None:
            self.dump_None()
        elif inspect.isclass(obj):
            self.dump_class()
        if isinstance(obj, str):
            self.dump_str(*args, **kw)
        elif isinstance(obj, dict):
            self.dump_dict(*args, **kw)
        elif isinstance(obj, list):
            self.dump_list(*args, **kw)
        elif isinstance(obj, types.ModuleType):
            self.dump_module(*args, **kw)


        # self.check_attribute(type_)

    def separator(self):
        '''显示分隔符'''
        if self.setting.separator is not None:
            print(Style.DIM + self.setting.separator)

    def call_stack(self):
        '''显示调用栈'''
        index = 1
        stack = tuple(reversed((inspect.stack())))
        # print(stack)
        update = []
        for i, s in enumerate(stack):
            # print(index)
            # if i < 3:
            #     continue
            tmp = inspect.getframeinfo(s[0])
            update.append({
                'filename': tmp[0],
                'lineno': tmp[1],
                'function': tmp[2],
                'code_context': tmp[3],
            })
        update = update[:-3]
        for index, stack in enumerate(update):
            print(Fore.YELLOW + "\t{}: filename = {}, lineno = {}, function = {}"
                    .format(index, stack['filename'], stack['lineno'], stack['function']))
            for code in stack['code_context']:
                print(Style.DIM + "\t\t{}".format(code))

    def dump_class(self, *args, **kw):
        '''
        dump class
        1. doc
        2.
        '''
        print(Fore.YELLOW+"Description:")
        doc = self.obj.__doc__.split('\n')
        doc = "\t" + "\n\t".join(doc)
        print(Style.DIM + doc)

        function = []
        for name in self.obj.__dict__:
            # 获取 attr 的文档
            if name not in ATTR_MAP:
                doc = inspect.getdoc(getattr(self.obj, name)).split('\n', 1)[0]
                function.append({
                    'name': name,
                    'doc': doc
                })
        print(Fore.YELLOW + "Function:")
        for func in function:
            print(Fore.CYAN + "\t{} : \t".format(func['name']), end="")
            print(Style.DIM + "{}".format(func['doc']))

    def check(self):
        '''检查 obj 类型'''
        pass

    def dump_list(self, *args, **kw):
        print('\t{}'.format(self.obj))

    def dump_None(self):
        print("None")
        pass

    def dump_object(self):
        ''' 对象类型'''
        pass

    def dump_dict(self, *args, **kw):
        # print('\t{}{}'.format(Fore.CYAN, obj))
        print('\t{')
        for key, value in self.obj.items():
            print("\t   '{}'".format(key), end='')
            print(" : ", end='')
            format_ = "'{}'"
            if isinstance(value, int):
                format_ = "{}"
            print(format_.format(value))

        print('\t}')

    def dump_module(self,*args, **kw):
        ''' 模块'''
        print(dir(self.obj))

    def dump_str(self, *args, **kw):
        ''' 字符串 '''
        # try:
        print('s' + self.obj.__str__())
            # except Except
        print(inspect.getsourcefile(self.obj))
        print(Fore.YELLOW+"content:")
        print(Fore.CYAN + '\t{}'.format(self.obj))

    def check_attribute(self):
        '''显示对象的方法'''
        # arithmetic = {}
        # function = {}
        for key in self.obj.__dict__.keys():
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

# Copied from http://stackoverflow.com/a/3681323/2142577.
def get_dict_attr(obj, attr):
    for obj in [obj] + list(obj.__class__.__mro__):
        if attr in obj.__dict__:
            return obj.__dict__[attr]
    raise AttributeError


def is_descriptor(obj):
    return (hasattr(obj, "__get__") or
            hasattr(obj, "__set__") or
            hasattr(obj, "__delete__"))
