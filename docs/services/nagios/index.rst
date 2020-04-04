.. This is a comment. Note how any initial comments are moved by
   transforms to after the document title, subtitle, and docinfo.

.. demo.rst from: http://docutils.sourceforge.net/docs/user/rst/demo.txt

.. |EXAMPLE| image:: static/yi_jing_01_chien.jpg
   :width: 1em

**********************
Nagios Service
**********************

.. contents:: Table of Contents
Overview
==================

Nagios is installed as a service.

The service file is located under::

      /lib/systemd/system/nagios.service
      
It has the contents below::

.. code-block:: bash
   :linenos:
   
      [Unit]
      Description=Nagios Core 4.4.5
      Documentation=https://www.nagios.org/documentation
      After=network.target local-fs.target

      [Service]
      Type=forking
      ExecStartPre=/usr/local/nagios/bin/nagios -v /usr/local/nagios/etc/nagios.cfg
      ExecStart=/usr/local/nagios/bin/nagios -d /usr/local/nagios/etc/nagios.cfg
      ExecStop=/bin/kill -s TERM ${MAINPID}
      ExecStopPost=/bin/rm -f /usr/local/nagios/var/rw/nagios.cmd
      ExecReload=/bin/kill -s HUP ${MAINPID}

      [Install]
      WantedBy=multi-user.target

Start and Stop
==============

The Nagios service can be started and stopped via the module or via command line.

To start and stop via the module, go to Servers > Nagios and click the Start or Stop button:

   .. image:: _static/nagios-service.png

To start and stop via command line, as root, issue::

   service nagios stop | start
