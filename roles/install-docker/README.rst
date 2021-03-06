An ansible role to install docker and configure it to use mirrors if available.

**Role Variables**

.. zuul:rolevar:: mirror_fqdn
   :default: {{ zuul_site_mirror_fqdn }}

   The base host for mirror servers.

.. zuul:rolevar:: docker_mirror

   URL to override the generated docker hub mirror url based on
   :zuul:rolevar:`install-docker.mirror_fqdn`.

.. zuul:rolevar:: use_upstream_docker
   :default: True

   By default this role adds repositories to install docker from upstream
   docker. Set this to False to use the docker that comes with the distro.

.. zuul:rolevar:: docker_update_channel
   :default: stable

   Which update channel to use for upstream docker. The two choices are
   ``stable``, which is the default and updates quarterly, and ``edge``
   which updates monthly.

.. zuul:rolevar:: docker_insecure_registries
   :default: undefined

   Declare this with a list of insecure registries to define the
   registries which are allowed to communicate with HTTP only or
   HTTPS with no valid certificate.

.. zuul:rolevar:: docker_gpg_key
   :default: string

   The raw content of the upstream docker gpg key, as found here
   https://download.docker.com/linux/fedora/gpg

.. zuul:rolevar:: docker_distro_packages
   :default: list

   List of packages to be installed when `use_upstream_docker` is set to
   **false**. The package set is defined by default using distro specific
   variables. If the package set needs to be changed this option can be
   overridden as needed.

.. zuul:rolevar:: docker_upstream_distro_required_packages
   :default: list

   List of packages to be installed when `use_upstream_docker` is set to
   **true**. The package set is defined by default using distro specific
   variables and contains a list of supporting packages required to be
   installed prior to installing docker-ce. If the package set needs to
   be changed this option can be overridden as needed.

.. zuul:rolevar:: docker_upstream_distro_packages
   :default: list

   List of packages to be installed when `use_upstream_docker` is set to
   **true**. The package set is defined by default using distro specific
   variables. If the package set needs to be changed this option can be
   overridden as needed.

.. zuul:rolevar:: docker_download_fqdn
   :default: download.docker.com

   Add default option to set the docker download fqdn.

.. zuul:rolevar:: docker_mirror_base_url
   :default: https://{{ docker_download_fqdn }}/linux/{ubuntu,centos,fedora}

   By default this option sets the repository base url. This variable is
   based on :zuul:rolevar:`install-docker.docker_download_fqdn`. When this
   option is unset, the role will use distro specific variables which are
   loaded at the time of execution.
