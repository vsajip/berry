# python3 main.py -o out in
# coc 

import re
import os
from coc_parser import *
from str_build import *
from block_builder import *
from macro_table import *

class builder:
    Input = 0
    Output = 1
    Config = 2

    def __init__(self, input_folders, output_folder, macro_files):
        self.output = output_folder
        self.input = input_folders
        self.config = macro_files
        self.macro = None
        self.strmap = {}

        self.macro = macro_table()
        for path in self.config:
            self.macro.scan_file(path)                

        for d in self.input:
            self.scandir(d)
        
        sb = str_build(self.strmap)
        sb.build(self.output)
    
    def parse_file(self, filename):
        if re.search(r"\.(c|cc|cpp)$", filename):
            # print(f"> parse {filename}")
            text = ""
            with open(filename) as f:
                text = f.read()
            # print(f"> len(text)={len(text)}")
            parser = coc_parser(text)
            for s in parser.strtab:
                self.strmap[s] = 0
            for obj in parser.objects:
                builder = block_builder(obj, self.macro)
                for s in builder.strtab:
                    self.strmap[s] = 0
                builder.dumpfile(self.output)

    def scandir(self, srcpath):
        for item in os.listdir(srcpath):
            path = os.path.join(srcpath, item)
            if os.path.isfile(path): self.parse_file(path)


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("input_folder", nargs='+', help='folders containing the C/C++ files to be parsed')
    parser.add_argument("-o", help='output folder', required=True)
    parser.add_argument("-c", nargs='+', help='configuration folders for preprocessor')

    args = vars(parser.parse_args())
    # print(args)
    b = builder(args["input_folder"], args["o"], args["c"])
