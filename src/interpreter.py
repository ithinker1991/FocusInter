# coding: utf-8


class Interpreter(object):
    def __init__(self):
        self.stack = []
        self.environment = {}

    def LOAD_VALUE(self, number):
        self.stack.append(number)

    def PRINT_ANSWER(self):
        val = self.stack.pop()
        print val

    def ADD_TWO_VALUES(self):
        v1 = self.stack.pop()
        v2 = self.stack.pop()
        ret = v1 + v2
        self.stack.append(ret)

    def ran_code(self, what_to_execute):
        instructions = what_to_execute["instructions"]

        for step in instructions:
            instruction, argment = step
            argment = self.parse_argument(instruction, argment, what_to_execute)
            if instruction == "LOAD_VALUE":
                self.LOAD_VALUE(argment)
            elif instruction == "ADD_TWO_VALUES":
                self.ADD_TWO_VALUES()
            elif instruction == "PRINT_ANSWER":
                self.PRINT_ANSWER()
            elif instruction == "LOAD_NAME":
                self.LOAD_NAME(argment)
            elif instruction == "STORE_NAME":
                self.STORE_NAME(argment)

    def LOAD_NAME(self, name):
        val = self.environment[name]
        self.stack.append(val)

    def STORE_NAME(self, name):
        val = self.stack.pop()
        self.environment[name] = val

    def parse_argument(self, instruction, argument, what_to_execute):
        numbers = ["LOAD_VALUE"]
        names = ["STORE_NAME", "LOAD_NAME"]

        if instruction in numbers:
            argument = what_to_execute["numbers"][argument]
        elif instruction in names:
            argument = what_to_execute["names"][argument]

        return argument


if __name__ == '__main__':
    what_to_execute = {
        "instructions": [
            ("LOAD_VALUE", 0),
            ("LOAD_VALUE", 1),
            ("ADD_TWO_VALUES", None),
            ("PRINT_ANSWER", None)
        ],
        "numbers": [100, 4]
    }

    what_to_execute1 = {
        "instructions": [
            ("LOAD_VALUE", 0),
            ("LOAD_VALUE", 1),
            ("ADD_TWO_VALUES", None),
            ("LOAD_VALUE", 2),
            ("ADD_TWO_VALUES", None),
            ("PRINT_ANSWER", None)
        ],
        "numbers": [100, 4, 3]
    }

    what_to_execute2 = {
        "instructions": [
            ("LOAD_VALUE", 0),
            ("STORE_NAME", 0),
            ("LOAD_VALUE", 1),
            ("STORE_NAME", 1),
            ("LOAD_NAME", 0),
            ("LOAD_NAME", 1),
            ("ADD_TWO_VALUES", None),
            ("PRINT_ANSWER", None)
        ],
        "numbers": [100, 4],
        "names": ['a', 'b']


    }

    interpreter = Interpreter()

    # 100 + 4
    interpreter.ran_code(what_to_execute)

    # 100 + 4 + 3
    interpreter.ran_code(what_to_execute1)

    # a = 100
    # b = 4
    # a + b
    interpreter.ran_code(what_to_execute2)