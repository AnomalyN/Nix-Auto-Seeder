import imp
import sys
import inspect
import tempfile
import subprocess

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


def copy_file(f_input, f_output):
    f_input.seek(0)  # Ensure input file is read from beginning
    f_output.write(f_input.read())


def run_deluge(t_file):
    try:
        with tempfile.NamedTemporaryFile() as tmp_file:

            # Copy content of torrent file in mem to tmp file
            copy_file(t_file, tmp_file)

            subprocess.run(
                ['deluge-console', 'add', tmp_file.name],
                check=True
            )
    except subprocess.CalledProcessError as cpe:
        logger.error("deluge-console exited with error: {}", cpe)

    except Exception as e:
        logger.error("Failed to run deluge-console: {}", e)


def setup_loguru(verbose):
    # Based on default loguru
    format = str(
        "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
        "<level>{level: <8}</level> | "
        "<level>{message}</level>",
    )

    logger.remove()

    # Set logging level based on verbose level
    if verbose == 0:
        logger.add(sys.stderr, format=format, level="INFO", diagnose=False, backtrace=False, catch=False)
    elif verbose == 1:
        logger.add(sys.stderr, format=format, level="DEBUG", diagnose=False, backtrace=True)
    elif verbose >= 2:
        logger.add(sys.stderr, format=format, level="TRACE", diagnose=True, backtrace=True)
