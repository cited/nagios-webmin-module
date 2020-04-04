.. This is a comment. Note how any initial comments are moved by
   transforms to after the document title, subtitle, and docinfo.

.. demo.rst from: http://docutils.sourceforge.net/docs/user/rst/demo.txt

.. |EXAMPLE| image:: static/yi_jing_01_chien.jpg
   :width: 1em

***************************
Main Configuration Files
***************************

.. contents:: Table of Contents

Editing Files
==============

To access the Main Conf file editor, click the Objects icon as show below.

      .. image:: _static/nagios-main-tab.png

      
  
From here you can edit any existing file within the /usr/local/nagios/etc directory.


      .. image:: _static/nagios-conf-select.png 
      

Once you have completed any edits, click the Save and Close button and restart Nagios.
     

Adding New File
===================

Any new file added to the directory will appear in the editor drop-downn.


Restart Nagios
=============

For the edits to register, you must restart Nagios.

This can be done via Servers > Nagios in your control panel.

It can also be done via command line using::

    systemctl restart nagios.service
    
 

Conf Location
===============

By default, all main conf files are saved to /usr/local/nagios/etc   




