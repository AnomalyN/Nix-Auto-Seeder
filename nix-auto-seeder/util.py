import os
import imp
import inspect

from pathlib import Path

from loguru import logger


def get_distros(dir='distros'):
    path = Path('.') / dir

    for pyfile in path.glob('*.py'):
        found_module = imp.find_module(pyfile.stem, [path.resolve()])
        module = imp.load_module(pyfile.stem, found_module[0], found_module[1], found_module[2])

        for mem_name, obj in inspect.getmembers(module):
            if inspect.isclass(obj) and inspect.getmodule(obj) is module:
                yield obj()


def verify_torrents(filename):
    return filename.endswith('.torrent')


def copy_file(output_dir, filename, t_file):
    out_file = output_dir / filename
    with out_file.open('wb+') as f:
        t_file.seek(0)
        f.write(t_file.read())
