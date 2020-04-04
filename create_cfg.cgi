#!/usr/bin/perl
# Update a manually edited config file

require './nagios-lib.pl';
&error_setup($text{'manual_err'});
&ReadParse();

# Work out the file
my $obj_dir = get_nagios_home().'/etc/objects';
my $cfg_file = $obj_dir."/".$in{'new_filename'};

# Write to it
&copy_source_dest($module_root_directory."/template.cfg", $cfg_file)

&redirect("/nagios/edit_objects.cgi?file=".&urlize($cfg_file));
