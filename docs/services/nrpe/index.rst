.. This is a comment. Note how any initial comments are moved by
   transforms to after the document title, subtitle, and docinfo.

.. demo.rst from: http://docutils.sourceforge.net/docs/user/rst/demo.txt

.. |EXAMPLE| image:: static/yi_jing_01_chien.jpg
   :width: 1em

**********************
Nrpe Service
**********************

.. contents:: Table of Contents
Overview
==================

Nrpe is installed as a service.

The service file is located under::

      /lib/systemd/system/nrpe.service
      
It has the contents below::

.. code-block:: bash
   :linenos:
   
      [Unit]
      Description=Nagios Remote Plugin Executor
      Documentation=http://www.nagios.org/documentation
      After=var-run.mount nss-lookup.target network.target local-fs.target time-sync.target
      Before=getty@tty1.service plymouth-quit.service xdm.service
      Conflicts=nrpe.socket

      [Install]
      WantedBy=multi-user.target

      [Service]
      Type=simple
      Restart=on-abort
      PIDFile=/usr/local/nagios/var/nrpe.pid
      RuntimeDirectory=nrpe
      RuntimeDirectoryMode=0755
      ExecStart=/usr/local/nagios/bin/nrpe -c /usr/local/nagios/etc/nrpe.cfg -f
      ExecReload=/bin/kill -HUP $MAINPID
      ExecStopPost=/bin/rm -f /usr/local/nagios/var/nrpe.pid
      TimeoutStopSec=60
      User=nagios
      Group=nagios
      PrivateTmp=true
      OOMScoreAdjust=-500

Start and Stop
==============

The Nrpe service can be started and stopped via the module or via command line.

To start and stop via the module, go to Servers > Nagios and click the Start or Stop button:

   .. image:: _static/nrpe-service.png

To start and stop via command line, as root, issue::

   service nrpe stop | start
