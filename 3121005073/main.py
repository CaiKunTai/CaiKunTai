import sys

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
