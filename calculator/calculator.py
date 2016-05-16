# encoding=utf8

import sys


class InputError(Exception):
    pass


class StackEmptyError(Exception):
    pass


def is_digit(ch):
    return ch in '0123456789.'


def is_valid(ch):
    return ch in '0123456789.+-*/^() '


def split_expr(expr):
    """
    将四则运算表达式字符串解析为 token 列表
    :param
        expr: '(1 + 2) * （3 + 4)'
    :return:
        ['(', '1', '+', '2', ')', '*', '(', '3', '+', '4', ')']
    """
    elements = []
    i = 0
    j = 1
    if not is_valid(expr[0]):
        raise InputError

    while j < len(expr):
        if not is_valid(expr[j]):
            raise InputError
        elif expr[i] == ' ':
            i += 1
            j = i + 1
        elif is_digit(expr[i]) and is_digit(expr[j]):
            j += 1
        else:
            elements.append(expr[i:j])
            i = j
            j += 1
    if expr[i] != ' ':
        elements.append(expr[i:j])

    return elements


def is_num(s):
    return is_digit(s[0])


def priority(op):
    if op in '+-':
        return 1
    elif op in '*/':
        return 2
    elif op in '^':
        return 3
    elif op in '(':
        return 4


def str2num(s):
    if '.' in s:
        return float(s)
    else:
        return int(s)


class Stack:
    def __init__(self):
        self._arr = []

    def __getattr__(self, attr):
        if attr == 'length':
            return len(self._arr)
        elif attr == 'is_empty':
            return not len(self._arr)

    def pop(self):
        if self.is_empty:
            raise StackEmptyError
        self._arr = self._arr[:-1]

    def top(self):
        if self.is_empty:
            return None
        return self._arr[-1]

    def push(self, value):
        self._arr.append(value)


def infix2postfix(infix):
    postfix = []
    stack = Stack()
    for e in infix:
        if is_num(e):
            postfix.append(e)
        elif e in '(^':
            stack.push(e)
        elif e == ')':
            while stack.top() != '(':
                postfix.append(stack.top())
                try:
                    stack.pop()
                except StackEmptyError:
                    print('FORMAT ERROR')
                    sys.exit(1)
            stack.pop()
        elif e in '+-*/':
            while not stack.is_empty:
                if priority(e) <= priority(stack.top()) and stack.top() != '(':
                    postfix.append(stack.top())
                    stack.pop()
                else:
                    break
            stack.push(e)
        elif stack.is_empty:
            stack.push(e)
    while not stack.is_empty:
        postfix.append(stack.top())
        stack.pop()
    return postfix


def evaluate_postfix(postfix):
    stack = Stack()
    for ele in postfix:
        if is_num(ele):
            stack.push(str2num(ele))
        else:
            operation = {'+': lambda x, y: x + y,
                         '-': lambda x, y: x - y,
                         '*': lambda x, y: x * y,
                         '/': lambda x, y: x / y,
                         '^': lambda x, y: x ** y}
            op1 = stack.top()
            stack.pop()
            op2 = stack.top()
            stack.pop()
            try:
                stack.push(operation[ele](op2, op1))
            except ZeroDivisionError:
                raise ValueError
    if stack.length == 1:
        return stack.top()
    else:
        print('FORMAT ERROR')
        # sys.exit(1)


def evaluate_infix_str(s):
    try:
        infix = split_expr(s)
        postfix = infix2postfix(infix)
        return evaluate_postfix(postfix)
    except InputError:
        print('INPUT ERROR')
        sys.exit(1)
    except StackEmptyError:
        print('FORMAT ERROR')
        sys.exit(1)
    except ValueError:
        print('VALUE ERROR')
        sys.exit(1)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.exit(0)
    expr = ''.join(sys.argv[1:])
    print('{0:.10G}'.format(evaluate_infix_str(expr)))
