import sys
import util
import click
import itertools

from pathlib import Path

from loguru import logger


@click.command()
@click.option('-n', '--num-releases',
              help='If multiple versions are available download the latest num; 0 to get all releases',
              default=1)
@click.option('-o', '--output-dir',
              help='Save torrents in dir instead of submitting to deluge',
              type=click.Path(file_okay=False, writable=True, path_type=Path))
@click.option('--skip-deluge',
              help='Skip adding the torrent files via deluge-console',
              is_flag=True)
@click.option('-v', '--verbose',
              count=True,
              default=0)
def main(num_releases, output_dir, skip_deluge, verbose):
    distro_files = []

    util.setup_loguru(verbose)

    for distro in util.get_distros():
        logger.debug("Parsing {}", distro)
        distro_files.append(distro.get_torrents(num_releases=num_releases))

    # Ensure output dir exists if defined
    if output_dir and not output_dir.exists():
        output_dir.mkdir()

    try:
        for (filename, t_file) in itertools.chain(*distro_files):

            # Add via deluge console, skip if requested
            if not skip_deluge:
                util.run_deluge(t_file)

            # Store copies of torrent files in output_dir
            if output_dir:
                output_file = output_dir / filename

                with output_file.open('wb+') as f:
                    util.copy_file(t_file, f)

    except Exception as e:
        logger.exception("Failed to parse torrents {}", e)


if __name__ == '__main__':
    main()
