# CHOMP64

CHOMP64 is a Python library for converting programs written in v2 Basic to native-accurate .prg files for use with Commodore64 hardware or emulations.

## Installation

Use the Python package manager [pip](https://pip.pypa.io/en/stable/) to install CHOMP64 for library use, or download the chomp64.py file from the repository for use as a CLI. 

```bash
pip intall chomp64
```

## Usage 
```python
from chomp64 import v2BasicChomper

#initializes tokenizer object
var = v2BasicChomper.Tokenizer("path/to/input/file", "path/to/ouput/file")  #optional parameters: verbose: Bool, overwrite: Bool

#generates .prg output file at specified path
var.Tokenize()
```
