#!/usr/bin/perl

require './nagios-lib.pl';
&error_setup($text{'manual_err'});
&ReadParseMime();

# Work out the file
@files = get_cfg_files(get_nagios_home().'/etc/objects');
&indexof($in{'file'}, @files) >= 0 || &error($text{'manual_efile'});
$in{'data'} =~ s/\r//g;
$in{'data'} =~ /\S/ || &error($text{'manual_edata'});

# Write to it
&open_lock_tempfile(DATA, ">$in{'file'}");
&print_tempfile(DATA, $in{'data'});
&close_tempfile(DATA);

&webmin_log("manual", undef, $in{'file'});
&redirect("");
