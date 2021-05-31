import sys
import util
import click
import itertools

from pathlib import Path

from loguru import logger


@click.command()
@click.option('-n', '--major',
              help='How many major versions will be downloaded; 0 to get all releases',
              default=1)
@click.option('-m', '--minor',
              help='How many minor versions will be downloaded for every major version; 0 to get all releases',
              default=1)
@click.option('-o', '--output-dir',
              help='Save torrents in dir instead of submitting to deluge',
              type=click.Path(file_okay=False, writable=True, path_type=Path))
@click.option('--skip-deluge',
              help='Skip adding the torrent files via deluge-console',
              is_flag=True)
@click.option('-a', '--arch',
              multiple=True,
              help='Limit downloading torrent for specific architectures')
@click.option('-l', '--limit',
              multiple=True,
              help='Limit downloading torrent for specific distros')
@click.option('-v', '--verbose',
              count=True,
              default=0)
def main(major, minor, output_dir, skip_deluge, arch, limit, verbose):
    distro_files = []

    util.setup_loguru(verbose)

    for distro in util.get_distros():

        # If limit is given, only parse distros who are equal to argument given
        if limit:
            if not any(limit_distro == distro for limit_distro in limit):
                continue

        logger.debug("Parsing {}", distro)
        distro_files += distro.gather(major=major, minor=minor, arch=arch)

    # Ensure output dir exists if defined
    if output_dir and not output_dir.exists():
        output_dir.mkdir()

    try:
        for torrent_file in distro_files:

            # Add via deluge console, skip if requested
            if not skip_deluge:
                util.run_deluge(torrent_file)

            # Store copies of torrent files in output_dir
            if output_dir:
                output_file = output_dir / torrent_file.filename

                with output_file.open('wb+') as f:
                    torrent_file.copy_content_to(f)

    except Exception as e:
        logger.exception("Failed to parse torrents {}", e)


if __name__ == '__main__':
    main()
