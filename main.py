class Stack:

    def __init__(self):
        self.list = list()

    def is_empty(self):
        return True if len(self.list) == 0 else False

    def push(self, value):
        self.list.append(value)

    def pop(self):
        return self.list.pop()

    def peek(self):
        return self.list[-1]

    def size(self):
        return len(self.list)


if __name__ == '__main__':
    stack = Stack()
    back = {'(': ')', '[': ']', '{': '}'}
    test_values = (
        '(((([{}]))))',
        '[([])((([[[]]])))]{()}',
        '{{[()]}}',
        '}{}',
        '{{[(])]}}',
        '[[{())}]'
    )
    for value in test_values:
        err = False
        for s in value:
            if s in ['(', '{', '[']:
                stack.push(s)
            if s in [')', '}', ']']:
                if stack.is_empty():
                    err = True
                    break
                if s != back[stack.pop()]:
                    err = True
                    break
        if err:
            print(value, 'Несбалансированно')
        else:
            print(value, 'Сбалансированно')
