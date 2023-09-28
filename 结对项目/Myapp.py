import argparse
import random
from fractions import Fraction

# generate_number 函数生成一个随机整数，用于创建数学表达式的操作数
def generate_number(range_limit):
    return random.randint(1, range_limit)

# generate_fraction 函数生成一个随机分数，用于创建数学表达式的操作数
def generate_fraction(range_limit):
    numerator = random.randint(1, range_limit)
    denominator = random.randint(numerator, range_limit)
    return Fraction(numerator, denominator)

# generate_operator 函数生成一个运算符，用于创建数学表达式的操作数。
def generate_operator():
    operators = ['+', '-', '*', '/']
    return random.choice(operators)

# generate_expression 函数生成数学表达式，并提供一个参数allow_negative，用于控制是否生成负数
def generate_expression(range_limit, allow_negative=False):
    if random.random() < 0.5:
        return str(generate_number(range_limit))
    else:
        if allow_negative:
            return str(generate_fraction(range_limit))
        else:
            return str(generate_number(range_limit))

# format_fraction 函数将分数格式化为字符串，包括整数、带分数和分数
def format_fraction(fraction):
    if fraction == 0:
        return '0'
    if fraction.numerator < fraction.denominator:
        return f"{fraction.numerator}/{fraction.denominator}"
    else:
        whole_part = fraction.numerator // fraction.denominator
        numerator = fraction.numerator % fraction.denominator
        if numerator == 0:
            return str(whole_part)
        return f"{whole_part}'{numerator}/{fraction.denominator}"

# evaluate_expression 函数使用eval函数来计算数学表达式的结果，处理可能出现的异常情况
def evaluate_expression(expression):
    try:
        result = eval(expression)
        if isinstance(result, Fraction):
            return result
        return Fraction(result).limit_denominator()
    except ZeroDivisionError:
        return None

# is_valid_expression 函数检查数学表达式是否有效，是否可以进行计算
def is_valid_expression(expression):
    return evaluate_expression(expression) is not None

# generate_problem 函数生成一个完整的数学问题，并确保问题是唯一的
def generate_problem(range_limit, generated_problems):
    while True:
        num_operators = random.randint(1, 3)
        problem = generate_expression(range_limit, allow_negative=True)
        for _ in range(num_operators):
            operator = generate_operator()
            operand = generate_expression(range_limit)
            # 如果结果为整数，则将整数形式添加到问题中
            if evaluate_expression(problem).denominator == 1:
                problem += f" {operator} {int(evaluate_expression(operand))}"
            else:
                problem += f" {operator} {operand}"
        # 检查是否已生成过相同的题目，如果是则重新生成
        if problem not in generated_problems:
            generated_problems.add(problem)
            return problem

# generate_problems_and_answers 函数生成一批数学问题和相应的答案，确保它们是有效的且非负的
def generate_problems_and_answers(num_problems, range_limit, generated_problems):
    problems = []
    answers = []
    while len(problems) < num_problems:
        problem = generate_problem(range_limit, generated_problems)
        answer = evaluate_expression(problem)
        if is_valid_expression(problem) and answer is not None and answer >= 0:
            problems.append(problem)
            answers.append(answer)
    return problems, answers

# save_to_file 函数将生成的问题和答案保存到文件中
def save_to_file(problems, answers, problem_file, answer_file):
    with open(problem_file, "w") as f:
        for i, problem in enumerate(problems, start=1):
            f.write(f"{i}. {problem}\n")
    with open(answer_file, "w") as f:
        for i, answer in enumerate(answers, start=1):
            formatted_answer = format_fraction(Fraction(answer))
            f.write(f"{i}. {formatted_answer}\n")

# validate_and_grade 函数用于验证生成的问题和答案是否正确，并生成一个评分报告
def validate_and_grade(exercise_file, answer_file):
    with open(exercise_file, "r") as f:
        problems = [line.strip().split('. ')[1] for line in f if line.strip()]
    with open(answer_file, "r") as f:
        answers = [line.strip().split('. ')[1] for line in f if line.strip()]
    correct = 0
    wrong = 0
    wrong_indices = []
    for i, (problem, answer) in enumerate(zip(problems, answers), start=1):
        formatted_answer = format_fraction(evaluate_expression(problem))
        if formatted_answer == answer:
            correct += 1
        else:
            wrong += 1
            wrong_indices.append(i)
    with open("Grade.txt", "w") as f:
        f.write(f"Correct: {correct} ({', '.join(map(str, range(1, correct + 1)))})\n")
        f.write(f"Wrong: {wrong} ({', '.join(map(str, wrong_indices))})\n")

def main():
    parser = argparse.ArgumentParser(description="Generate and validate elementary math problems.")
    parser.add_argument("-n", type=int, default=None, help="Number of problems to generate")
    parser.add_argument("-r", type=int, default=None, help="Range limit for numbers")
    parser.add_argument("-e", type=str, help="Exercise file for validation")
    parser.add_argument("-a", type=str, help="Answer file for validation")
    args = parser.parse_args()
    if args.e and args.a:
        validate_and_grade(args.e, args.a)
    else:
        if args.n is not None and args.r is not None:
            generated_problems = set()  # 用于存储已生成的题目
            problems, answers = generate_problems_and_answers(args.n, args.r, generated_problems)
            save_to_file(problems, answers, "Exercises.txt", "Answers.txt")
        else:
            print("usage: Myapp.py -n N -r R")
            print("-n and -r are required when generating problems.")
            print("usage: Myapp.py -e E -a A")
            print("-e and -a are required when checking results.")


if __name__ == "__main__":
    main()
