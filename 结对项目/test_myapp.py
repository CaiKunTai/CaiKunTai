import unittest
from Myapp import *
from unittest.mock import patch
import tempfile
import os

class TestMyApp(unittest.TestCase):
    # 测试 generate_number 函数是否生成随机整数
    def test_generate_number(self):
        num = generate_number(10)
        self.assertTrue(1 <= num <= 10)

    # 测试 generate_fraction 函数是否生成随机分数
    def test_generate_fraction(self):
        fraction = generate_fraction(10)
        self.assertIsInstance(fraction, Fraction)
        self.assertTrue(0 <= fraction <= 1)
        self.assertTrue(fraction.numerator <= fraction.denominator <= 10)

    # 测试 generate_operator 函数是否生成运算符
    def test_generate_operator(self):
        operator = generate_operator()
        self.assertIn(operator, ['+', '-', '*', '/'])

    # 测试 generate_expression 函数是否返回一个有效的数学表达式
    def test_generate_expression(self):
        for _ in range(100):
            expression = generate_expression(10, allow_negative=True)
            self.assertTrue(is_valid_expression(expression))

    # 测试 format_fraction 函数是否正确格式化分数
    def test_format_fraction(self):
        fraction = Fraction(3, 4)
        formatted = format_fraction(fraction)
        self.assertEqual(formatted, '3/4')

    # 测试 evaluate_expression 函数是否正确评估数学表达式
    def test_evaluate_expression(self):
        expression = '3 + 4'
        result = evaluate_expression(expression)
        self.assertIsInstance(result, Fraction)
        self.assertEqual(result, Fraction(7, 1))

    # 测试 is_valid_expression 函数是否正确检查表达式的有效性
    def test_is_valid_expression(self):
        self.assertTrue(is_valid_expression("2 + 3"))
        self.assertTrue(is_valid_expression("1/2 - 1/3"))
        self.assertTrue(is_valid_expression("1 * 0"))
        self.assertTrue(is_valid_expression("1 * 0 / 6"))
        self.assertFalse(is_valid_expression("1 / 0"))
        self.assertFalse(is_valid_expression("1 * 6 / 0"))
        self.assertFalse(is_valid_expression("1 / 1/0"))

    # 测试 generate_problem 函数是否生成有效的问题
    def test_generate_problem(self):
        generated_problems = set()
        for _ in range(100):
            problem = generate_problem(10, generated_problems)
            self.assertTrue(is_valid_expression(problem))
            generated_problems.add(problem)

    # 测试 generate_problems_and_answers 函数是否生成有效的问题和答案
    def test_generate_problems_and_answers(self):
        generated_problems = set()
        problems, answers = generate_problems_and_answers(10, 10, generated_problems)
        self.assertEqual(len(problems), 10)
        self.assertEqual(len(answers), 10)
        for problem in problems:
            self.assertTrue(is_valid_expression(problem))
        for answer in answers:
            self.assertIsInstance(answer, Fraction)

    # 测试 save_to_file 函数是否正成功生成数学问题与答案文件
    def test_save_to_file(self):
        # 生成一些虚拟的问题和答案
        problems = ["1 + 2", "3 - 1", "4 * 5"]
        answers = ["3", "2", "20"]
        # 创建一个临时目录来保存测试文件
        with tempfile.TemporaryDirectory() as temp_dir:
            problem_file = os.path.join(temp_dir, "test_problems.txt")
            answer_file = os.path.join(temp_dir, "test_answers.txt")
            # 调用被测试的函数
            save_to_file(problems, answers, problem_file, answer_file)
            # 读取生成的文件内容以进行断言
            with open(problem_file, "r") as f:
                saved_problems = f.read().splitlines()
            with open(answer_file, "r") as f:
                saved_answers = f.read().splitlines()
            # 断言生成的文件内容是否与输入一致
            self.assertEqual(saved_problems, ["1. 1 + 2", "2. 3 - 1", "3. 4 * 5"])
            self.assertEqual(saved_answers, ["1. 3", "2. 2", "3. 20"])

    # 测试 validate_and_grade 函数是否正确验证和评分
    def test_validate_and_grade(self):
        problems = ["1 + 2", "3 - 4"]
        answers = [Fraction(3, 1), Fraction(-1, 1)]
        save_to_file(problems, answers, "test_problems.txt", "test_answers.txt")
        validate_and_grade("test_problems.txt", "test_answers.txt")
        with open("Grade.txt", "r") as f:
            grade_result = f.readlines()
        self.assertTrue("Correct: 2 (1, 2)\n" in grade_result)
        self.assertTrue("Wrong: 0 ()\n" in grade_result)

    # 测试 main 函数是否在输入正确参数的情况下成功运行
    @patch('builtins.open', create=True)
    def test_main_generate(self, mock_open):
        args = argparse.Namespace(n=10, r=10, e=None, a=None)
        with patch('argparse.ArgumentParser.parse_args', return_value=args):
            main()
        # 检查是否生成了 Exercises.txt 和 Answers.txt 文件
        mock_open.assert_any_call('Exercises.txt', 'w')
        mock_open.assert_any_call('Answers.txt', 'w')


if __name__ == '__main__':
    unittest.main()
