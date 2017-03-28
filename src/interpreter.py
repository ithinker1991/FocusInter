# coding: utf-8




class Interpreter(object):

    def __init__(self):
        self.stack = []

    def LOAD_DATA(self, number):
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
        numbers = what_to_execute["numbers"]

        for step in instructions:
            instruction, argment = step
            if instruction == "LOAD_DATA":
                number = numbers[argment]
                self.LOAD_DATA(number)
            elif instruction == "ADD_TWO_VALUES":
                self.ADD_TWO_VALUES()
            elif instruction == "PRINT_ANSWER":
                self.PRINT_ANSWER()


if __name__ == '__main__':
    what_to_execute = {
        "instructions" : [
            ("LOAD_DATA", 0),
            ("LOAD_DATA", 1),
            ("ADD_TWO_VALUES", None),
            ("PRINT_ANSWER", None)
        ],
        "numbers": [100, 4]
    }

    interpreter = Interpreter()
    interpreter.ran_code(what_to_execute)