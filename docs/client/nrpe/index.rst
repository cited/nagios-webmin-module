.. This is a comment. Note how any initial comments are moved by
   transforms to after the document title, subtitle, and docinfo.

.. demo.rst from: http://docutils.sourceforge.net/docs/user/rst/demo.txt

.. |EXAMPLE| image:: static/yi_jing_01_chien.jpg
   :width: 1em

**********************
Nrpe Agent
**********************

.. contents:: Table of Contents
Overview
==================

Nrpe is used for monitoring remote hosts.

To install the nrpe client on a remote host, you can use the nrpe.sh file in /script directory.

The script content is below:

.. code-block:: bash
   :linenos:

      #!/bin/bash
      #Info: This script installs a NRPE client, following [1]
      #[1] https://support.nagios.com/kb/article.php?id=515

      #Nagious server, that will monitor this client node
      NAGIOS_MON_HOST='1.2.3.4'
      NAGIOS_HOME='/usr/local/nagios/'

      function detect_distro(){
      if [ -f /etc/centos-release ]; then
		DISTRO='centos'
		DISTRO_VER=$(grep VERSION_ID /etc/os-release | tr -d '"' | cut -f2 -d= | cut -f1 -d.)

      #opensuse,debian,slackware, ubuntu
	      elif [ -f /etc/os-release ]; then
		DISTRO=$(grep -m 1 ID /etc/os-release | cut -f2 -d= | tr -d '"')
		DISTRO_VER=$(grep VERSION_ID /etc/os-release | tr -d '"' | cut -f2 -d= | cut -f1 -d.)
	      else
		echo "Error: Failed to detect distribution"; exit 1;
	      fi
      }

      function install_deps(){
      if [ ${DISTRO} == 'centos' ]; then
       yum install -y gcc glibc glibc-common openssl openssl-devel perl wget
      elif [ ${DISTRO} == 'ubuntu' ]; then
      export DEBIAN_FRONTEND=noninteractive
      if [ ${DISTRO_VER} -eq 18 ]; then
      apt-add-repository universe
      fi
      apt-get install -y autoconf automake gcc libc6 libmcrypt-dev make libssl-dev wget openssl make
      fi
      }

      function install_nrpe(){
      NRPE_VER='3.2.1'

      if [ $(grep -m 1 -c '^nagios:' /etc/passwd) -eq 0 ]; then
      useradd -s /bin/false nagios
      fi

      pushd ${HOME}
      if [ ! -f nrpe-${NRPE_VER}.tar.gz ]; then
      wget --no-check-certificate https://github.com/NagiosEnterprises/nrpe/archive/nrpe-${NRPE_VER}.tar.gz
         fi

      tar xzf nrpe-${NRPE_VER}.tar.gz
      rm -f nrpe-${NRPE_VER}.tar.gz

      pushd nrpe-nrpe-${NRPE_VER}/

      if [ $(which systemctl 2>/dev/null | grep -c yum) -eq 1 ]; then
        ./configure --enable-command-args --with-init-type=systemd
      else
        ./configure --enable-command-args
      fi

      make all install install-groups-users install-plugin install-config install-init
      popd
      rm -f nrpe-nrpe-${NRPE_VER}/
      popd
      }

      function config_nrpe(){
        sed -i "/^allowed_hosts=/s/\$/,${NAGIOS_MON_HOST}/" ${NAGIOS_HOME}/etc/nrpe.cfg
      sed -i 's/^dont_blame_nrpe=.*/dont_blame_nrpe=1/g'  ${NAGIOS_HOME}/etc/nrpe.cfg

      #Standard command found in source/package plugins
      cat >> ${NAGIOS_HOME}/etc/nrpe.cfg <<CMD_EOF
      command[check_disk_root]=${CUSTOM_PLUGINS_HOME}/check_disk -w 30% -c 10% -p /
      CMD_EOF

      cat >> ${NAGIOS_HOME}/etc/nrpe.cfg <<CMD_EOF
      command[check_linuxdiskspace]=${CUSTOM_PLUGINS_HOME}/check_linuxdiskspace
      CMD_EOF

      #Linux S.M.A.R.T Checks
      #NOTE: we may have /dev/vda1 for virtual disk
      for sd in $(find /dev -type b -name 'sd[a-z][0-9]' | cut -f3 -d/); do
      echo "command[check_linux_smart_${sd}]=${CUSTOM_PLUGINS_HOME}/check_ide_smart -d /dev/${sd}" >> ${NAGIOS_HOME}/etc/nrpe.cfg
      done


      if [ $(which systemctl 2>/dev/null | grep -c systemctl) -eq 1 ]; then
      systemctl enable nrpe.service
      systemctl start nrpe
      else
      chkconfig --set nrpe on
      service nrpe start
      fi
      }

      function install_plugins_source(){
      PLUG_VER='2.3.1'

      if [ ${DISTRO} == 'centos' ]; then
         yum install -y gcc glibc glibc-common make gettext automake autoconf wget openssl-devel net-snmp net-snmp-utils epel-release perl-Net-SNMP
      elif [ ${DISTRO} == 'ubuntu' ]; then
      apt-get install -y autoconf gcc libc6 libmcrypt-dev make libssl-dev wget bc gawk dc build-essential snmp libnet-snmp-perl gettext
      fi

      pushd ${HOME}
         wget --no-check-certificate https://github.com/nagios-plugins/nagios-plugins/archive/release-${PLUG_VER}.tar.gz
         tar xzf release-${PLUG_VER}.tar.gz
         rm -f release-${PLUG_VER}.tar.gz

         pushd nagios-plugins-release-${PLUG_VER}/
         ./tools/setup
         ./configure
         make
         make install
         popd
         rm -rf nagios-plugins-release-${PLUG_VER}/
         popd

      NAGIOS_PLUGINS_HOME='/usr/local/nagios/libexec/'
      }

  
      function install_plugins(){
      install_plugins_source
      }

      function test_nrpe(){
        if [ ! -f ${NAGIOS_HOME}/etc/nrpe.cfg ]; then
        echo 'Error: nrpe.cfg is missing!'
         fi

      OUT=$(${NAGIOS_HOME}/libexec/check_nrpe -H 127.0.0.1)
      if [ "${OUT}" == "NRPE v${NRPE_VER}" ]; then
         echo "NRPE Test OK"
      else
         echo "NRPE Test FAILED"
         exit 1;
      fi
      }

      detect_distro;
      install_deps;
      install_nrpe;
      install_plugins;
      config_nrpe;

      test_nrpe;

      

