import sys
import util
import inspect
import click

from loguru import logger


@click.command()
@click.option('-o', '--output-dir',
              help='Save torrents in dir instead of submitting to deluge',
              type=click.Path(file_okay=False, writable=True))
def main(output_dir):

    for distro in util.get_distros():
        print(distro)
        distro.get_torrents()

if __name__ == '__main__':
    main()
