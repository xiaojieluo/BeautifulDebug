import collections
import inspect
from os.path import expanduser
from sys import modules


class _SkippedAttribute(object):
    pass


skipped_attribute = _SkippedAttribute()

SKIPPED_ATTRIBUTE = [
    '__class__',
    '__delattr__',
    '__dir__',
    '__init__',
    '__init_subclass__',
    '__reduce__',
    '__reduce_ex__',
    '__setattr__',
    '__subclasshook__',
]
default_obj = skipped_attribute  # reuse!

# Basic category.
CLASS = 'class'
DEFAULT_CATEGORY = 'other'
FUNCTION = 'function'
EXCEPTION = 'exception'

# Detailed category.
MODULE_ATTRIBUTE = 'module attribute'
SPECIAL_ATTRIBUTE = 'special attribute'
ABSTRACT_CLASS = 'abstract class'
MAGIC = 'magic method'
ARITHMETIC = 'arithmetic'
ITER = 'iter'
CONTEXT_MANAGER = 'context manager'
OBJECT_CUSTOMIZATION = 'object customization'
RICH_COMPARISON = 'rich comparison'
ATTRIBUTE_ACCESS = 'attribute access'
DESCRIPTOR = 'descriptor'
DESCRIPTOR_CLASS = 'descriptor class'
CLASS_CUSTOMIZATION = 'class customization'
CONTAINER = 'emulating container'
COUROUTINE = 'couroutine'
COPY = 'copy'
PICKLE = 'pickle'

# There are always exceptions, aka attributes cannot be accessed by getattr.
# They are recorded here, along with the type/class of their host objects.
ATTR_EXCEPTION_MAP = {
    # "<type 'spacy.tokens.token.Token'>": {
    #     'has_repvec': skipped_attribute,
    #     'repvec': skipped_attribute,
    # },
    # "<class 'pandas.core.frame.DataFrame'>": {
    #     'columns': None,  # DEFAULT_CATEGORY.
    #     'index': None,
    # },
    # "<type 'type'>": {  # py2
    #     '__abstractmethods__': None,  # ABSTRACT_CLASS.
    # },
    # "<class 'type'>": {  # py3
    #     '__abstractmethods__': None,  # ABSTRACT_CLASS.
    # }
}


def always_true(obj):
    return True


# Second level
ATTR_MAP = {
    '__doc__': SPECIAL_ATTRIBUTE,
    '__qualname__': SPECIAL_ATTRIBUTE,
    '__module__': SPECIAL_ATTRIBUTE,
    '__defaults__': SPECIAL_ATTRIBUTE,
    '__code__': SPECIAL_ATTRIBUTE,
    '__globals__': SPECIAL_ATTRIBUTE,
    '__dict__': SPECIAL_ATTRIBUTE,
    '__closure__': SPECIAL_ATTRIBUTE,
    '__annotations__': SPECIAL_ATTRIBUTE,
    '__kwdefaults__': SPECIAL_ATTRIBUTE,
    '__func__': SPECIAL_ATTRIBUTE,
    '__self__': SPECIAL_ATTRIBUTE,
    '__bases__': SPECIAL_ATTRIBUTE,
    '__class__': SPECIAL_ATTRIBUTE,
    '__objclass__': SPECIAL_ATTRIBUTE,
    '__slots__': SPECIAL_ATTRIBUTE,
    '__weakref__': SPECIAL_ATTRIBUTE,
    '__next__': ITER,
    '__reversed__': [
        (lambda obj: isinstance(obj, collections.Iterator), ITER),
        (always_true, CONTAINER),
    ],
    '__iter__': [
        (lambda obj: isinstance(obj, collections.Iterator), ITER),
        (always_true, CONTAINER),
    ],
    '__enter__': CONTEXT_MANAGER,
    '__exit__': CONTEXT_MANAGER,
    '__name__': [
        (lambda obj: inspect.ismodule(obj), MODULE_ATTRIBUTE),
        (always_true, SPECIAL_ATTRIBUTE)
    ],
    '__loader__': MODULE_ATTRIBUTE,
    '__package__': MODULE_ATTRIBUTE,
    '__spec__': MODULE_ATTRIBUTE,
    '__path__': MODULE_ATTRIBUTE,
    '__file__': MODULE_ATTRIBUTE,
    '__cached__': MODULE_ATTRIBUTE,
    '__abs__': ARITHMETIC,
    '__add__': ARITHMETIC,
    '__and__': ARITHMETIC,
    '__complex__': ARITHMETIC,
    '__divmod__': ARITHMETIC,
    '__float__': ARITHMETIC,
    '__floordiv__': ARITHMETIC,
    '__iadd__': ARITHMETIC,
    '__iand__': ARITHMETIC,
    '__ifloordiv__': ARITHMETIC,
    '__ilshift__': ARITHMETIC,
    '__imatmul__': ARITHMETIC,
    '__imod__': ARITHMETIC,
    '__imul__': ARITHMETIC,
    '__int__': ARITHMETIC,
    '__invert__': ARITHMETIC,
    '__ior__': ARITHMETIC,
    '__ipow__': ARITHMETIC,
    '__irshift__': ARITHMETIC,
    '__isub__': ARITHMETIC,
    '__itruediv__': ARITHMETIC,
    '__ixor__': ARITHMETIC,
    '__lshift__': ARITHMETIC,
    '__matmul__': ARITHMETIC,
    '__mod__': ARITHMETIC,
    '__mul__': ARITHMETIC,
    '__neg__': ARITHMETIC,
    '__or__': ARITHMETIC,
    '__pos__': ARITHMETIC,
    '__pow__': ARITHMETIC,
    '__radd__': ARITHMETIC,
    '__rand__': ARITHMETIC,
    '__rdivmod__': ARITHMETIC,
    '__rfloordiv__': ARITHMETIC,
    '__rlshift__': ARITHMETIC,
    '__rmatmul__': ARITHMETIC,
    '__rmod__': ARITHMETIC,
    '__rmul__': ARITHMETIC,
    '__ror__': ARITHMETIC,
    '__round__': ARITHMETIC,
    '__rpow__': ARITHMETIC,
    '__rrshift__': ARITHMETIC,
    '__rshift__': ARITHMETIC,
    '__rsub__': ARITHMETIC,
    '__rtruediv__': ARITHMETIC,
    '__rxor__': ARITHMETIC,
    '__sub__': ARITHMETIC,
    '__truediv__': ARITHMETIC,
    '__xor__': ARITHMETIC,
    '__ceil__': ARITHMETIC,
    '__floor__': ARITHMETIC,
    '__trunc__': ARITHMETIC,
    '__init__': OBJECT_CUSTOMIZATION,
    '__new__': OBJECT_CUSTOMIZATION,
    '__del__': OBJECT_CUSTOMIZATION,
    '__repr__': OBJECT_CUSTOMIZATION,
    '__str__': OBJECT_CUSTOMIZATION,
    '__bytes__': OBJECT_CUSTOMIZATION,
    '__format__': OBJECT_CUSTOMIZATION,
    '__hash__': OBJECT_CUSTOMIZATION,
    '__bool__': OBJECT_CUSTOMIZATION,
    '__sizeof__': OBJECT_CUSTOMIZATION,
    '__lt__': RICH_COMPARISON,
    '__le__': RICH_COMPARISON,
    '__eq__': RICH_COMPARISON,
    '__ne__': RICH_COMPARISON,
    '__gt__': RICH_COMPARISON,
    '__ge__': RICH_COMPARISON,
    '__getattr__': ATTRIBUTE_ACCESS,
    '__getattribute__': ATTRIBUTE_ACCESS,
    '__setattr__': ATTRIBUTE_ACCESS,
    '__delattr__': ATTRIBUTE_ACCESS,
    '__dir__': ATTRIBUTE_ACCESS,
    '__get__': DESCRIPTOR_CLASS,
    '__set__': DESCRIPTOR_CLASS,
    '__delete__': DESCRIPTOR_CLASS,
    '__set_name__': DESCRIPTOR_CLASS,
    '__init_subclass__': CLASS_CUSTOMIZATION,
    '__prepare__': CLASS_CUSTOMIZATION,
    '__instancecheck__': CLASS_CUSTOMIZATION,
    '__subclasscheck__': CLASS_CUSTOMIZATION,
    '__subclasshook__': ABSTRACT_CLASS,
    '__isabstractmethod__': ABSTRACT_CLASS,
    '__abstractmethods__': ABSTRACT_CLASS,
    '__len__': CONTAINER,
    '__length_hint__': CONTAINER,
    '__getitem__': CONTAINER,
    '__missing__': CONTAINER,
    '__setitem__': CONTAINER,
    '__delitem__': CONTAINER,
    '__contains__': CONTAINER,
    '__await__': COUROUTINE,
    '__aiter__': COUROUTINE,
    '__anext__': COUROUTINE,
    '__aenter__': COUROUTINE,
    '__aexit__': COUROUTINE,
    '__index__': MAGIC,
    '__call__': MAGIC,
    '__copy__': COPY,
    '__deepcopy__': COPY,
    '__getnewargs_ex__': PICKLE,
    '__getnewargs__': PICKLE,
    '__getstate__': PICKLE,
    '__setstate__': PICKLE,
    '__reduce__': PICKLE,
    '__reduce_ex__': PICKLE,
}

# repl
PYTHON = 'python'
IPYTHON = 'ipython'
PTPYTHON = 'ptpython'
BPYTHON = 'bpython'

# descriptor
GETTER = 'getter'
SETTER = 'setter'
DELETER = 'deleter'
method_descriptor = type(list.append)


def _get_repl_type():
    if any('ptpython' in key for key in modules):
        return PTPYTHON
    if any('bpython' in key for key in modules):
        return BPYTHON
    try:
        __IPYTHON__
        return IPYTHON
    except NameError:
        return PYTHON


repl_type = _get_repl_type()

# Color
BLACK = 'black'
BRIGHT_BLACK = 'bright black'
GREY = 'grey'
RED = 'red'
BRIGHT_RED = 'bright red'
GREEN = 'green'
BRIGHT_GREEN = 'bright green'
YELLOW = 'yellow'
BRIGHT_YELLOW = 'bright yellow'
BLUE = 'blue'
BRIGHT_BLUE = 'bright blue'
MAGENTA = 'magenta'
BRIGHT_MAGENTA = 'bright magenta'
CYAN = 'cyan'
BRIGHT_CYAN = 'bright cyan'
WHITE = 'white'
BRIGHT_WHITE = 'bright white'
VALID_COLORS = frozenset({
    BLACK, BRIGHT_BLACK, RED, BRIGHT_RED, GREEN, BRIGHT_GREEN,
    YELLOW, BRIGHT_YELLOW, BLUE, BRIGHT_BLUE, MAGENTA, BRIGHT_MAGENTA,
    CYAN, BRIGHT_CYAN, WHITE, BRIGHT_WHITE})

# User Configuration
DEFAULT_CONFIG_FILE = expanduser('~/.pdir2config')
CONFIG_FILE_ENV = 'PDIR2_CONFIG_FILE'
DEFAULT = 'global'
UNIFORM_COLOR = 'uniform-color'
CATEGORY_COLOR = 'category-color'
ATTRIBUTE_COLOR = 'attribute-color'
COMMA_COLOR = 'comma-color'
DOC_COLOR = 'doc-color'
VALID_CONFIG_KEYS = frozenset({
    UNIFORM_COLOR, CATEGORY_COLOR, ATTRIBUTE_COLOR, COMMA_COLOR, DOC_COLOR})
