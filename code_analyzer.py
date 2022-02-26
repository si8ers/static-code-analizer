# write your code here
import re
import os
import sys
import ast


class CodeAnalyzer:

    def __init__(self, file_name=None):
        self.lines = []
        self.length = 0
        self.file_name = sys.argv[0]
        self.tree = None

        if file_name:
            self.file_name = file_name
            file = open(self.file_name, 'r')
            self.lines = file.readlines()
            file.close()
            self.length = len(self.lines)
            self.tree = ast.parse(''.join(self.lines))

    def test_001(self, index):
        max_len = 79
        if len(self.lines[index]) > max_len:
            print('{}: Line {}: S001 Too long'.format(self.file_name, index + 1))
            return False
        return True

    def test_002(self, index):
        spaces = re.findall(r'^(\s*)\S', self.lines[index])
        if len(spaces) > 0 and len(spaces[0]) % 4 > 0:
            print('{}: Line {}: S002 Indentation is not a multiple of four'.format(self.file_name, index + 1))
            return False
        return True

    def test_003(self, index):
        line = self.lines[index].split('#')[0]
        semicolon = re.findall(r';\s*$', line)
        if len(semicolon) > 0:
            print('{}: Line {}: S003 Unnecessary semicolon'.format(self.file_name, index + 1))
            return False
        return True

    def test_004(self, index):
        spaces = re.findall(r'\S(\s*)#', self.lines[index])
        if len(spaces) > 0 and len(spaces[0]) != 2:
            print('{}: Line {}: S004 At least two spaces required before inline comments'.format(self.file_name, index + 1))
            return False
        return True

    def test_005(self, index):
        todo = re.findall(r'#\stodo', self.lines[index], re.IGNORECASE)
        if len(todo) > 0:
            print('{}: Line {}: S005 TODO found'.format(self.file_name, index + 1))
            return False
        return True

    def test_006(self, index):
        if index < 3:
            return None
        no_space = re.findall(r'\S+', self.lines[index])
        if len(no_space) > 0:
            prev_1 = re.findall(r'\S+', self.lines[index - 1])
            prev_2 = re.findall(r'\S+', self.lines[index - 2])
            prev_3 = re.findall(r'\S+', self.lines[index - 3])
            if len(prev_1) == 0 and len(prev_2) == 0 and len(prev_3) == 0:
                print('{}: Line {}: S006 More than two blank lines preceding a code line'.format(self.file_name, index + 1))
                return False
        return True

    def test_007(self, index):
        construction = re.match(r'^\s*(def|class)\s{2,}', self.lines[index])
        if construction:
            print("{}: Line {}: S007 Too many spaces after '{}'".format(self.file_name, index + 1, construction[1]))
            return False
        return True

    def test_008(self, index):
        for node in ast.walk(self.tree):
            if isinstance(node, ast.ClassDef) and node.lineno == index + 1:
                class_name = node.name
                if class_name.find('_') >= 0 or re.match(r'^[^A-Z].*', class_name):
                    print("{}: Line {}: S008 Class name '{}' should use CamelCase".format(self.file_name, index + 1, class_name))
                    return False
        return True

    def test_009(self, index):
        for node in ast.walk(self.tree):
            if isinstance(node, ast.FunctionDef) and node.lineno == index + 1:
                func_name = node.name
                if re.match(r'.*[A-Z]+.*', func_name):
                    print("{}: Line {}: S009 Function name '{}' should use snake_case".format(self.file_name, index + 1, func_name))
                    return False
        return True

    def test_010(self, index):
        for node in ast.walk(self.tree):
            if isinstance(node, ast.FunctionDef) and node.lineno == index + 1:
                for arg in node.args.args:
                    arg_name = arg.arg
                    if re.match(r'.*[A-Z]+.*', arg_name):
                        print("{}: Line {}: S010 Argument name '{}' should be snake_case".format(self.file_name, index + 1, arg_name))
                        return False
        return True

    def test_011(self, index):
        for node in ast.walk(self.tree):
            if isinstance(node, ast.Assign) and node.lineno == index + 1:
                for var in node.targets:
                    var_name = None
                    if isinstance(var, ast.Name):
                        var_name = var.id
                    elif isinstance(var, ast.Attribute):
                        var_name = var.value.id + '.' + var.attr
                    if var_name and re.match(r'.*[A-Z]+.*', var_name):
                        print("{}: Line {}: S011 Variable '{}' in function should be snake_case".format(self.file_name, index + 1, var_name))
                        return False
        return True

    def test_012(self, index):
        for node in ast.walk(self.tree):
            if isinstance(node, ast.FunctionDef) and node.lineno == index + 1:
                for def_val in node.args.defaults:
                    if isinstance(def_val, ast.List) or isinstance(def_val, ast.Dict):
                        print("{}: Line {}: S012 Default argument value is mutable".format(self.file_name, index + 1))
                        return False
        return True

    def test_all(self, file_name=None):
        if file_name:
            self.file_name = file_name
        file = open(self.file_name, 'r')
        self.lines = file.readlines()
        file.close()
        self.length = len(self.lines)
        self.tree = ast.parse(''.join(self.lines))

        for index in range(self.length):
            self.test_001(index)
            self.test_002(index)
            self.test_003(index)
            self.test_004(index)
            self.test_005(index)
            self.test_006(index)
            self.test_007(index)
            self.test_008(index)
            self.test_009(index)
            self.test_010(index)
            self.test_011(index)
            self.test_012(index)


files = []
path = sys.argv[1] if len(sys.argv) > 1 else sys.argv[0]
if re.findall(r'\.py$', path):
    files.append(path)
else:
    for file_path in os.listdir(path):
        if re.findall(r'\.py$', file_path):
            files.append('{}{}{}'.format(path.rstrip(os.sep), os.sep, file_path))
files.sort()
ca = CodeAnalyzer()
for file_path in files:
    ca.test_all(file_path)
