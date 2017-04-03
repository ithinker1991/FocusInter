
import sys
import dis
import operator
import six

if six.PY3:
    byteint = lambda b: b
else:
    byteint = ord

class Frame(object):
    def __init__(self, code, global_names, local_names, prev_frame):
        self.code_obj = code
        self.global_names = global_names
        self.local_names = local_names
        self.prev_frame = prev_frame
        self.stack = []  # data stack
        if prev_frame:
            self.builtin_names = prev_frame
        else:
            self.builtin_names = local_names['__builtins__']
            if hasattr(self.builtin_names, '__dict__'):
                self.builtin_names = self.builtin_names.__dict__

        self.last_instruction = 0
        self.block_stack = []


class VirtualMatchine(object):
    def __init__(self):
        self.frames = []
        self.frame = None
        self.return_value = None
        self.last_exception = None

    def run_code(self, code, global_names=None, local_names=None):
        frame = self.make_frame(code, global_names=global_names, local_names=local_names)
        return self.run_frame(frame)

    def make_frame(self,code, callargs={}, global_names=None, local_names=None):
        if global_names is not None and local_names is not None:
            local_names = global_names
        elif self.frames:
            global_names = self.frame.global_names
            local_names = {}
        else:
            global_names = local_names = {
                '__builtins__': __builtins__,
                '__name__': '__main__',
                '__doc__': None,
                '__package__': None
            }
        local_names.update(callargs)
        frame = Frame(code, global_names, local_names, self.frame)
        return frame

    def parse_byte_and_args(self):
        f = self.frame
        opoffset = f.last_instruction
        op_code = ord(f.code_obj.co_code[opoffset])
        f.last_instruction += 1
        op_name = dis.opname[op_code]
        if op_code >= dis.HAVE_ARGUMENT:
            arg = f.code_obj.co_code[f.last_instruction:f.last_instruction+2]
            f.last_instruction += 2
            arg_val = ord(arg[0]) + (ord(arg[1]) << 8)
            # co_code type
            if op_code in dis.hasconst:
                arg = f.code_obj.co_consts[arg_val]
            elif op_code in dis.hasname:
                arg = f.code_obj.co_names[arg_val]
            elif op_code in dis.haslocal:
                arg = f.code_obj.co_varnames[arg_val]
            elif op_code in dis.hasjrel:
                arg = f.last_instruction + arg_val
            else:
                arg = arg_val
            argument = [arg]
        else:
            argument = []

        return op_name, argument

    def dispatch(self, op_name, arguments):
        why = None
        try:
            bytecode_fn = getattr(self, 'byte_%s' % op_name, None)
            if bytecode_fn is None:
                # todo more operation type: binary, slice
                if op_name.startswith('UNARY_'):
                    pass
                if op_name.startswith('BINARY_'):
                    self.binary_op(op_name[len('BINARY_'):])
            else:
                why = bytecode_fn(*arguments)

            # todo raise an excetion
        except:
            self.last_exception = sys.exc_info()[:2] + (None,)
            why = 'exception'
        return why

    BINARY_OPERATORS = {
        'POWER': pow,
        'MULTIPLY': operator.mul,
        'DIVIDE': operator.div,
        'MODULO': operator.mod,
        'ADD': operator.add,
        'SUBTRACT': operator.sub,
        'SUBSCR': operator.getitem,
        'LSHIFT': operator.lshift,
        'RSHIFT': operator.rshift,
        'AND': operator.and_,
        'XOR': operator.xor,
        'OR': operator.or_,
    }

    def binary_op(self, op):
        fn = self.BINARY_OPERATORS[op]
        arg2 = self.pop()
        arg1 = self.pop()
        self.push(fn(arg1, arg2))


    def push_frame(self, frame):
        self.frames.append(frame)
        self.frame = frame

    def pop_frame(self):
        self.frames.pop()

    def run_frame(self, frame):
        self.push_frame(frame)
        while True:
            op_name, arguments = self.parse_byte_and_args()
            why = self.dispatch(op_name=op_name, arguments=arguments)

            # todo deal with any block managemnt

            if why:
                break

        self.pop_frame()

        if why == 'exception':
            exc, val, tb = self.last_exception
            e = exc(val)
            e.__traceback__ = tb
            raise e

        return self.return_value
    # Data stack manipulation
    def top(self):
        return self.frame.stack[-1]

    def pop(self):
        return self.frame.stack.pop()

    def push(self, *vals):
        self.frame.stack.extend(vals)

    def popn(self, n):
        pass

    ## Stack manipulation

    def byte_LOAD_CONST(self, const):
        self.push(const)

    def byte_POP_TOP(self):
        self.pop()


    ## Names
    def byte_LOAD_NAME(self, name):
        frame = self.frame
        if name in frame.local_names:
            val = frame.local_names[name]
        elif name in frame.global_names:
            val = frame.global_names[name]
        elif name in frame.builtin_names:
            val = frame.builtin_names[name]
        else:
            raise NameError("name '%s' is not defined" % name)
        self.push(val)

    def byte_STORE_NAME(self, name):
        frame = self.frame
        frame.local_names[name] = self.pop()



    def byte_LOAD_FAST(self, name):
        self.push(self.frame.local_names[name])

    def byte_STORE_FAST(self, name):
        self.frame.local_names[name] = self.pop()



    def byte_LOAD_GLOBAL(self, name):
        pass


    def byte_RETURN_VALUE(self):
        self.return_value = self.pop()
        return True

    def byte_PRINT_ITEM(self):
        item = self.pop()
        self.print_item(item)

    def print_item(self, item, to=None):
        if to is None:
            to = sys.stdout
        print item, ''

    def print_newline(self, to=None):
        if to is None:
            to = sys.stdout










def test_demo():
    x = 100
    y = 2
    print 2
    return x + 1

if __name__ == '__main__':
    vm = VirtualMatchine()

    test_code1 = 'print 1'
    code = dis.dis(test_demo)

    ret = vm.run_code(test_demo.__code__)

    print 'ret', ret