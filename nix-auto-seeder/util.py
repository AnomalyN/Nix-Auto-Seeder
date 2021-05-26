import os
import imp
import inspect

from pathlib import Path


def get_distros(dir='distros'):
    path = Path('.') / dir

    for pyfile in path.glob('*.py'):
        found_module = imp.find_module(pyfile.stem, [path.resolve()])
        module = imp.load_module(pyfile.stem, found_module[0], found_module[1], found_module[2])

        for mem_name, obj in inspect.getmembers(module):
            if inspect.isclass(obj) and inspect.getmodule(obj) is module:
                yield obj()
