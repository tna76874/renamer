#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
rename script
"""
import argparse
import os
import glob
from parse import parse
from functools import reduce
from slugify import slugify


class renamer:
    def __init__(self, **kwargs):
        self.args = {}
        self.args.update(kwargs)

        # 🔍 Dateien und Ordner suchen (rekursiv nur bei --recursive)
        if self.args.get("recursive", False):
            search_path = os.path.join(os.path.abspath(self.args["directory"]), "**", "*")
            self.paths = glob.glob(search_path, recursive=True)
        else:
            search_path = os.path.join(os.path.abspath(self.args["directory"]), "*")
            self.paths = glob.glob(search_path, recursive=False)

        # 🔄 Sortierung: tiefste Pfade zuerst, damit Unterordner vor Eltern verarbeitet werden
        self.paths.sort(key=lambda p: p.count(os.sep), reverse=True)

        # 🧩 Modus wählen: slugify oder patternbasiertes Rename
        if self.args.get("slugify", False):
            self.slugify_items()
        else:
            self.rename_items()

    def slugify_items(self):
        """Slugify all files and folders (recursive optional)."""
        for path in self.paths:
            dirname = os.path.dirname(path)
            basename = os.path.basename(path)

            if not basename:  # skip root directory
                continue

            name, ext = os.path.splitext(basename)
            # Unterscheide Datei oder Ordner: Ordner haben keine Erweiterung
            if os.path.isdir(path):
                new_name = slugify(basename, separator=self.args.get("slug_sep", "_"))
            else:
                new_name = slugify(name, separator=self.args.get("slug_sep", "_")) + ext

            new_path = os.path.join(dirname, new_name)

            if new_path != path:
                if not self.args["no_action"]:
                    os.rename(path, new_path)
                print(f"Slugified: {basename} --> {new_name}")

    def rename_items(self):
        """Rename files and folders according to parse/format pattern."""
        for path in self.paths:
            dirname = os.path.dirname(path)
            basename = os.path.basename(path)

            if not basename:
                continue

            r = parse(self.args["pattern"], basename)

            if r is not None:
                if self.args["rename"] is None:
                    self.args["rename"] = self.args["pattern"]

                parsed = r.named

                # Maximalanzahl der Ziffern bestimmen
                if self.args["max_digits"] is None:
                    max_digits = max(
                        reduce(
                            lambda d, kv: {
                                **d,
                                kv[0]: max(
                                    len(str(kv[1])) if str(kv[1]).isdigit() else 0,
                                    d.get(kv[0], 0),
                                )
                            },
                            parsed.items(),
                            {},
                        ).values(),
                        default=0,
                    )
                else:
                    max_digits = int(self.args["max_digits"])

                parsed = {
                    k: f"{{:0{max_digits}d}}".format(int(v)) if str(v).isdigit() else v
                    for k, v in parsed.items()
                }

                basename_new = self.args["rename"].format(**parsed)
                new_path = os.path.join(dirname, basename_new)

                if new_path != path:
                    if not self.args["no_action"]:
                        os.rename(path, new_path)
                    print(f"Renamed: {basename} --> {basename_new}")


def main(headless=True):
    def dir_file(path):
        if os.path.exists(path):
            return path
        else:
            raise argparse.ArgumentTypeError(f"readable_dir:{path} is not a valid file")

    parser = argparse.ArgumentParser(description="Batch rename or slugify files and folders in a directory.")
    parser.add_argument(
        "-d",
        "--directory",
        type=dir_file,
        help="Path to batch rename dir",
        default=os.path.join(os.getcwd()),
    )
    parser.add_argument("-p", "--pattern", help="Pattern for renaming", type=str)
    parser.add_argument("-r", "--rename", help="Rename into pattern", type=str, default=None)
    parser.add_argument("-i", "--no-integer", help="deprecated - no longer useful", action="store_false")
    parser.add_argument("-n", "--no-action", help="Just print what would be renamed", action="store_true")
    parser.add_argument("-m", "--max-digits", help="Set max digits", type=int, default=None)

    # 🆕 slugify mode
    parser.add_argument("--slugify", help="Slugify filenames/folders instead of using pattern", action="store_true")
    parser.add_argument("--slug-sep", help="Separator for slugify mode (default '_')", default="_")

    # 🆕 Rekursive Suche
    parser.add_argument("--recursive", help="Search files/folders recursively in subdirectories", action="store_true")

    args = parser.parse_args()

    if headless:
        _ = renamer(**vars(args))
    else:
        return renamer(**vars(args))


if __name__ == "__main__":
    self = main(headless=False)
