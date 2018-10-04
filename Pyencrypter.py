import shutil
import os
import argparse

class encrypter:
    def __init__(self, file_path):
        if os.path.exists(file_path):
            self.file_path = file_path
        else:
            raise (Exception('{} does not exists!'.format(file_path)))
        self.file_name = os.path.basename(self.file_path)
        self.file_dir = os.path.dirname(self.file_path)
        self.file_base_name, self.file_extension = os.path.splitext(self.file_name)
        if not self.file_extension == '.py':
            raise (Exception('{} is not .py format!'.format(self.file_extension)))
        ## Creating .pvx file
        self.file_pyx_name = self.file_base_name + '.pyx'
        shutil.copy(self.file_path, self.file_pyx_name)
        self.setup_file()
        self.encrypt()

    def setup_file(self):
        with open('setup.py', '+w') as file:
            file.write("from distutils.core import setup\n"
                       "from Cython.Build import cythonize\n\n"
                       "setup(ext_modules=cythonize('{}'))".format(self.file_pyx_name))

    def encrypt(self):
        command = 'python setup.py build_ext --inplace'
        os.system(str(command))

        print("Now you can directly use import {} to use your file and its functions from .pyd file.".format(self.file_base_name))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Convert .py file to .pyd file using Cython')
    parser.add_argument('-f', '--file', type=str, action='store', help='Enter the file_path(if file is in other directory else file name) which you want to convert to .pyd format\n'
                                                                       'Please use "FILE_NAME" for your file name')
    args = parser.parse_args()
    encrypter(args.file)
