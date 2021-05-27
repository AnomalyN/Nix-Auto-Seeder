import util
import click
import itertools

from pathlib import Path

from loguru import logger


@click.command()
@click.option('-o', '--output-dir',
              help='Save torrents in dir instead of submitting to deluge',
              type=click.Path(file_okay=False, writable=True, path_type=Path))
def main(output_dir):
    distro_files = []

    for distro in util.get_distros():
        logger.info("Parsing {}", distro)
        distro_files.append(distro.get_torrents())

    # Ensure output dir exists if defined
    if output_dir and not output_dir.exists():
        output_dir.mkdir()

    for (filename, t_file) in itertools.chain(*distro_files):

        # Store copies of torrent files in output_dir
        if output_dir:
            util.copy_file(output_dir, filename, t_file)


if __name__ == '__main__':
    main()
