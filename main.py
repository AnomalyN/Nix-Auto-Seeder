import NAS_settings
import NAS_ubuntu
import NAS_helper
import NAS_raspbian
import NAS_arch
import NAS_debian
import NAS_centos

def main():
    settings = NAS_settings.create_settings()
    NAS_ubuntu.seed_ubuntu(settings)
    NAS_raspbian.seed_raspbian(settings)
    NAS_arch.seed_arch(settings)
    NAS_debian.seed_debian(settings)
    NAS_centos.seed_centos(settings)


if __name__ == '__main__':
    main()
