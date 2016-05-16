# encoding=utf8

import unittest
import calculator


class MyTest(unittest.TestCase):
    def test_split_expr(self):
        expr1 = '1+2+3'
        expr2 = ' 1+2+3 '
        expr3 = ' 1 + 2 * 3'
        expr4 = '(3.14 * 3.1 ** 2 + 2) * 3'
        expr5 = 'a + 1'
        answer1 = ['1', '+', '2', '+', '3']
        answer2 = ['1', '+', '2', '+', '3']
        answer3 = ['1', '+', '2', '*', '3']
        answer4 = ['(', '3.14', '*', '3.1', '*', '*', '2', '+', '2', ')', '*', '3']
        self.assertEqual(calculator.split_expr(expr1), answer1)
        self.assertEqual(calculator.split_expr(expr2), answer2)
        self.assertEqual(calculator.split_expr(expr3), answer3)
        self.assertEqual(calculator.split_expr(expr4), answer4)
        self.assertRaises(calculator.InputError, calculator.split_expr, expr5)

    def test_infix2postfix(self):
        infix1 = ['1', '+', '2', '+', '3']
        infix2 = ['1', '*', '2', '+', '3']
        infix3 = ['(', '3.14', '*', '3.1', '^', '2', '+', '2', ')', '*', '3']
        self.assertEqual(calculator.infix2postfix(infix1), ['1', '2', '+', '3', '+'])
        self.assertEqual(calculator.infix2postfix(infix2), ['1', '2', '*', '3', '+'])
        self.assertEqual(calculator.infix2postfix(infix3), ['3.14', '3.1', '2', '^', '*', '2', '+', '3', '*'])

    def test_evaluate_postfix(self):
        postfix1 = ['1', '2', '+', '3', '+']
        postfix2 = ['1', '2', '*', '3', '+']
        postfix3 = ['3.14', '3.1', '2', '^', '*', '2', '+', '3', '*']
        self.assertEqual(calculator.evaluate_postfix(postfix1), 6)
        self.assertEqual(calculator.evaluate_postfix(postfix2), 5)
        self.assertAlmostEqual(calculator.evaluate_postfix(postfix3), 96.5262)

    def test_evaluate_infix_str(self):
        expr1 = '1 + 2'
        expr2 = '1 + 2 - 3 + 4'
        expr3 = '1 + 2 * 3'
        expr4 = '1 - 2 / 4'
        expr5 = '2 ^ 3 ^ 2'
        expr6 = '(2 + 3) * 5'
        expr7 = 'a + 1'
        expr8 = '1 + 2 - 3 + 1 / 3'
        expr9 = '1 ++ 2'
        expr10 = '1 + + 2'
        expr11 = '1 / 0'
        self.assertEqual(calculator.evaluate_infix_str(expr1), 3)
        self.assertEqual(calculator.evaluate_infix_str(expr2), 4)
        self.assertEqual(calculator.evaluate_infix_str(expr3), 7)
        self.assertAlmostEqual(calculator.evaluate_infix_str(expr4), 0.5)
        self.assertEqual(calculator.evaluate_infix_str(expr5), 512)
        self.assertEqual(calculator.evaluate_infix_str(expr6), 25)
        # self.assertEqual(calculator.evaluate_infix_str(expr7), 2)
        self.assertAlmostEqual(calculator.evaluate_infix_str(expr8), 0.3333333)
        # self.assertEqual(calculator.evaluate_infix_str(expr9), 2)
        # self.assertEqual(calculator.evaluate_infix_str(expr10), 2)
        self.assertEqual(calculator.evaluate_infix_str(expr11), 111)


class StackTest(unittest.TestCase):
    def __init__(self):
        unittest.TestCase.__init__(self)
        self.stack = calculator.Stack()

    def test_stack_is_empty(self):
        self.assertTrue(self.stack.is_empty)

    def test_stack_length(self):
        self.assertEqual(self.stack.length, 0)
        self.stack.push(2)
        self.assertEqual(self.stack.length, 1)
        self.stack.pop()
        self.assertEqual(self.stack.length, 0)

    def test_stack_push_top_pop(self):
        self.stack.push(2)
        self.assertEqual(self.stack.top(), 2)
        self.stack.pop()
        self.assertEqual(self.stack.top(), None)
        self.assertRaises(calculator.StackEmptyError, self.stack.pop)

    def test_all(self):
        self.test_stack_is_empty()
        self.test_stack_length()
        self.test_stack_push_top_pop()


if __name__ == '__main__':
    stack_test = StackTest()
    stack_test.test_all()

    test = MyTest()
    test.test_split_expr()
    test.test_infix2postfix()
    test.test_evaluate_postfix()
    test.test_evaluate_infix_str()
