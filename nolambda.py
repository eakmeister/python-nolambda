from collections import namedtuple
import ctypes
import inspect

bool_trackers = []

class Tracker(str):
    @classmethod
    def create(cls, op_list):
        tracker = cls()
        tracker.op_list = op_list
        return tracker

    def __add__(self, other):
        def op(x, first):
            if isinstance(other, Tracker):
                var = other(first)
            else:
                var = other

            return x + var

        return Tracker.create(self.op_list + [op])

    def __mul__(self, other):
        def op(x, first):
            if isinstance(other, Tracker):
                var = other(first)
            else:
                var = other

            return x * var

        return Tracker.create(self.op_list + [op])
    

    def __str__(self):
        return Tracker.create(self.op_list + [lambda x, first: str(x)])

    def __repr__(self):
        return object.__repr__(self)

    def __contains__(self, item):
        def op(x, first):
            if isinstance(item, Tracker):
                var = item(first)
            else:
                var = item

            return item in x

        bool_trackers.append(Tracker.create(self.op_list + [op]))
        return True

    def __call__(self, item):
        first = item
        for operation in self.op_list:
            item = operation(item, first)

        return item

current_frame = inspect.currentframe()
caller = inspect.getouterframes(current_frame)[1]
caller[0].f_globals['_'] = Tracker.create([])

# Make bool callable.
callfunc = ctypes.CFUNCTYPE(ctypes.py_object, ctypes.py_object, ctypes.py_object, ctypes.c_void_p)

class PyTypeObject(ctypes.Structure):
    pass

PyTypeObject._fields_ = (
        ("ob_refcnt", ctypes.c_int),
        ("ob_type", ctypes.c_void_p),
        ("ob_size", ctypes.c_int),
        ("tp_name", ctypes.c_char_p),
        ("tp_basicsize", ctypes.c_ssize_t),
        ("tp_itemsize", ctypes.c_ssize_t),
        ("tp_dealloc", ctypes.c_void_p),
        ("tp_print", ctypes.c_void_p),
        ("tp_getattr", ctypes.c_void_p),
        ("tp_setattr", ctypes.c_void_p),
        ("tp_reserved", ctypes.c_void_p),
        ("tp_repr", ctypes.c_void_p),
        ("tp_as_number", ctypes.c_void_p),
        ("tp_as_sequence", ctypes.c_void_p),
        ("tp_as_wrapping", ctypes.c_void_p),
        ("tp_hash", ctypes.c_void_p),
        ("tp_call", callfunc),
    )

class PyObject(ctypes.Structure):
    _fields_ = [
        ('ob_refcnt', ctypes.c_ssize_t),
        ('ob_type', ctypes.POINTER(PyTypeObject)),
    ]

@callfunc
def call(self, args, kwargs):
    if len(args) >= 2:
        return bool_trackers[args[1]](args[0])
    else:
        return bool_trackers[0](args[0])

bool_ptr = PyObject.from_address(id(True))
bool_type_ptr = bool_ptr.ob_type.contents
bool_type_ptr.tp_call = call
