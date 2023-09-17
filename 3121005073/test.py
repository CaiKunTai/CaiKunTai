import unittest
import tempfile
import os
from main import read_file, clean_text, calculate_similarity


class MyTestCase(unittest.TestCase):
    def setUp(self):
        # 在每个测试函数执行前创建一个临时测试文件
        self.temp_dir = tempfile.TemporaryDirectory()
        self.original_file_path = os.path.join(self.temp_dir.name, 'original.txt')
        self.copied_file_path = os.path.join(self.temp_dir.name, 'copied.txt')
        with open(self.original_file_path, 'w', encoding='utf-8') as original_file:
            original_file.write('This is a test file.')
        with open(self.copied_file_path, 'w', encoding='utf-8') as copied_file:
            copied_file.write('This is a test file.')

    def test_read_file(self):
        # 测试文件读取功能
        # 测试正常情况
        result = read_file(self.original_file_path)
        self.assertEqual(result, 'This is a test file.')
        # 测试文件不存在的情况
        with self.assertRaises(SystemExit):
            read_file('non_existent_file.txt')
        # 测试文件内容为空的情况
        empty_file_path = os.path.join(self.temp_dir.name, 'empty.txt')
        with open(empty_file_path, 'w', encoding='utf-8') as empty_file:
            pass
        result = read_file(empty_file_path)
        self.assertEqual(result, '')

    def test_clean_text(self):
        # 测试文本清理功能
        text = 'This is a test, with some punctuation and spaces!'
        cleaned_text = clean_text(text)
        self.assertEqual(cleaned_text, 'this is a test with some punctuation and spaces')
        # 测试空文本的情况
        empty_text = ''
        cleaned_empty_text = clean_text(empty_text)
        self.assertEqual(cleaned_empty_text, '')

    def test_calculate_similarity(self):
        # 测试相似性计算功能
        original_text = 'This is a test.'
        copied_text = 'This is a test.'
        similarity = calculate_similarity(original_text, copied_text)
        self.assertEqual(similarity, 1.0)  # 两个完全相同的文本，相似度应为1.0
        original_text = 'This is a test.'
        copied_text = 'This Is A Test.'
        similarity = calculate_similarity(original_text, copied_text)
        self.assertEqual(similarity, 1.0)  # 两个仅大小写不同的文本，相似度应为1.0
        original_text = 'This is a test.'
        copied_text = 'This, is a test.'
        similarity = calculate_similarity(original_text, copied_text)
        self.assertEqual(similarity, 1.0)  # 两个仅标点符号不同的文本，相似度应为1.0
        original_text = 'This is a test.'
        copied_text = 'This is not a test.'
        similarity = calculate_similarity(original_text, copied_text)
        self.assertLess(similarity, 1.0)  # 两个不同的文本，相似度应小于1.0
        # 测试空文本的情况
        empty_text = ''
        similarity = calculate_similarity(empty_text, empty_text)
        self.assertEqual(similarity, 1.0)  # 两个空文本，相似度应为1.0
        # 测试一个文本为空的情况
        original_text = 'This is a test.'
        copied_empty_text = ''
        similarity = calculate_similarity(original_text, copied_empty_text)
        self.assertEqual(similarity, 0.0)  # 一个文本为空，相似度应为0.0


if __name__ == '__main__':
    unittest.main()
