# Simple file renamer

#### Manual installation

Installation

```bash
pip3 install --upgrade git+https://github.com/tna76874/renamer.git
```

Local:

```bash
git clone https://github.com/tna76874/renamer.git
cd renamer
pip3 install --upgrade .
```

#### Docker

```bash
./build.sh

./run.sh
```

#### Usage

```usage: renamer [-h] [-d DIRECTORY] -p PATTERN [-r RENAME] [-i]
usage: renamer [-h] [-d DIRECTORY] -p PATTERN [-r RENAME]

options:
  -h, --help            show this help message and exit
  -d DIRECTORY, --directory DIRECTORY
                        Path to batch rename dir
  -p PATTERN, --pattern PATTERN
                        Pattern of renaming. E.g. Real_Humans_-
                        _Echte_Menschen_-_Staffel_{season}_({episode}_10).mp4
  -r RENAME, --rename RENAME
                        Rename into pattern. E.g.
                        Real_Humans_S{season}E{episode}.mp4
