.. This is a comment. Note how any initial comments are moved by
   transforms to after the document title, subtitle, and docinfo.

.. demo.rst from: http://docutils.sourceforge.net/docs/user/rst/demo.txt

.. |EXAMPLE| image:: static/yi_jing_01_chien.jpg
   :width: 1em

***************************
Ibject Configuration Files
***************************

.. contents:: Table of Contents

Editing Files
==============

To access the Objects file editor, click the Objects icon as show below.

      .. image:: _static/nagios-obects-tab.png

      
  
From here you can edit any existing file within the NAGIOS/obects directory.


      .. image:: _static/nagios-obect-select.png

     

Creating a New File
=====================

You can create a new service file from a template via the editor.

Enter a new filename.cfg and click the Create button.

Give your file a name that will make it easy to identify, such as myconf.cfg
   
      .. image:: _static/nagios-new-cfg.png 	
  

Click the Create button.
      
The Create button will load the template below.

      .. image:: _static/nagios-obect-select-new.png

The template is commented.

1.  Replace all instances of HOST with the host you have added.

2.  Click Save and Close

3.  Restart Nagios for the new cfg to register

.. code-block:: bash
   :linenos:

      # Host configuration file

      define host {
        use                          linux-server
        host_name                    <HOST>
        alias                         <HOST>
        address                       <IP>
        register                     1
      }

      define service {
      host_name                       <HOST>
      service_description             PING
      check_command                   check_ping!100.0,20%!500.0,60%
      max_check_attempts              2
      check_interval                  2
      retry_interval                  2
      check_period                    24x7
      check_freshness                 1
      contact_groups                  admins,slackmins
      notification_interval           2
      notification_period             24x7
      notifications_enabled           1
      register                        1
      }

      define service {
      host_name                       <HOST>
      service_description             Check SSH
      check_command                   check_ssh!-p 3838
      max_check_attempts              2
      check_interval                  2
      retry_interval                  2
      check_period                    24x7
      check_freshness                 1
      contact_groups                  admins
      notification_interval           2
      notification_period             24x7
      notifications_enabled           1
      register                        1
      }

      define service {
      host_name                       <HOST>
      service_description             Check HTTP
      check_command                   check_http
      max_check_attempts              2
      check_interval                  2
      retry_interval                  2
      check_period                    24x7
      check_freshness                 1
      contact_groups                  admins
      notification_interval           2
      notification_period             24x7
      notifications_enabled           1
      register                        1
      }


   
Restart Nagios
=============

For the new cfg to register, you must restart Nagios.

This can be done via Servers > Nagios in your control panel.

It can also be done via command line using::

    systemctl restart nagios.service
    
 

Edit Conf
=========

To edit a Conf File you have created, simply select the conf file from the drop down.

Make the required edits and click Save.


Conf Location
===============

By default, all conf files are saved to /usr/local/nagios/obejcts/

      .. image:: _static/domainmap-conf-location.png
      




