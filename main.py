import os
import click

import NAS_settings
import NAS_ubuntu
import NAS_helper
import NAS_raspbian
import NAS_arch
import NAS_debian
import NAS_centos


@click.command()
@click.option('-o', '--output-dir',
              help='Save torrents in dir instead of submitting to deluge',
              type=click.Path(file_okay=False, writable=True))
def main(output_dir):
    settings = NAS_settings.create_settings()

    # Configure output dir
    if output_dir:
        os.mkdir(output_dir, 0o750)
        settings = settings._replace(working_path_NAS=output_dir)
        settings = settings._replace(output_dir_set=True)

    NAS_ubuntu.seed_ubuntu(settings)
    NAS_raspbian.seed_raspbian(settings)
    NAS_arch.seed_arch(settings)
    NAS_debian.seed_debian(settings)
    NAS_centos.seed_centos(settings)


if __name__ == '__main__':
    main()
