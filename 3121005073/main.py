import sys
import re
from difflib import SequenceMatcher

def read_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            text = file.read()
        return text
    except FileNotFoundError:
        print(f"文件 '{file_path}' 未找到。")
        sys.exit(1)
    except Exception as e:
        print(f"读取文件 '{file_path}' 时发生错误: {str(e)}")
        sys.exit(1)

def clean_text(text):
    # 去除标点符号和空格，并转换为小写
    text = re.sub(r'[^\w\s]', '', text)
    text = text.lower()
    return text

def calculate_similarity(original_text, copied_text):
    original_text = clean_text(original_text)
    copied_text = clean_text(copied_text)
    # 使用difflib库的SequenceMatcher计算相似度
    similarity = SequenceMatcher(None, original_text, copied_text).ratio()
    return similarity

def main():
    if len(sys.argv) != 4:
        print("Usage: python plagiarism_checker.py <original_file_path> <copied_file_path> <output_file_path>")
        sys.exit(1)
    original_file_path = sys.argv[1]
    copied_file_path = sys.argv[2]
    output_file_path = sys.argv[3]
    original_text = read_file(original_file_path)
    copied_text = read_file(copied_file_path)
    similarity = calculate_similarity(original_text, copied_text)
    with open(output_file_path, 'w', encoding='utf-8') as output_file:
        output_file.write(f"重复率: {similarity * 100:.2f}%\n")

if __name__ == "__main__":
    main()
