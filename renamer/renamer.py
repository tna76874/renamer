#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
rename script
"""
import argparse
import os
import glob2
from parse import parse
from functools import reduce


class renamer:
    def __init__(self, **kwargs):
        self.args = {
                    }
        self.args.update(kwargs)
        
        self.files = glob2.glob('{:}/**/*'.format(os.path.abspath(self.args['directory'])))        
        
        self.rename()

    def rename(self):
        for i in self.files:
            dirname = os.path.dirname(i)
            basename = os.path.basename(i)
            r = parse(self.args['pattern'], basename)
            if not isinstance(r,type(None)):
                if isinstance(self.args['rename'],type(None)): self.args['rename'] = self.args['pattern']
                parsed = r.named
                
                if isinstance(self.args['max_digits'],type(None)):
                    max_digits = max(reduce(lambda d, kv: {**d, kv[0]: max(len(str(kv[1])) if str(kv[1]).isdigit() else 0, d.get(kv[0], 0))}, parsed.items(), {}).values(), default=0)
                else:
                    max_digits = int(self.args['max_digits'])
                    
                parsed = {k: f"{{:0{max_digits}d}}".format(int(v)) if str(v).isdigit() else v for k, v in parsed.items()}

                basename_new = self.args['rename'].format(**parsed)
                new_file_path = os.path.join(dirname,basename_new)
                if not self.args['no_action']: os.rename(i,new_file_path)
                print("Renamed: {old} --> {new}".format(old=basename,new=basename_new))


def main(headless=True):
    def dir_file(path):
        if os.path.exists(path):
            return path
        else:
            raise argparse.ArgumentTypeError(f"readable_dir:{path} is not a valid file")
            
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--directory", type=dir_file, help="Path to batch rename dir", default=os.path.join(os.getcwd()))
    parser.add_argument("-p", "--pattern", help='Pattern of renaming. E.g. Real_Humans_-_Echte_Menschen_-_Staffel_{season:2d}_({episode:2d}_10).mp4', type=str, required=True)
    parser.add_argument("-r", "--rename", help='Rename into pattern. E.g. S{season}E{episode}_Real_Humans.mp4', type=str, default=None)
    parser.add_argument("-i", "--no-integer", help="depreciated - no longer useful", action="store_false")
    parser.add_argument("-n", "--no-action", help="just print what would be renamed", action="store_true")
    parser.add_argument("-m", "--max-digits", help='set max digits', type=int, default=None)

    args = vars(parser.parse_args())

    args = parser.parse_args()
  
    # init object
    if headless: _ = renamer(**vars(args))
    else: return renamer(**vars(args))

if __name__ == "__main__":   
    self = main(headless=False)
