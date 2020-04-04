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
