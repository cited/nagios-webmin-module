#!/usr/bin/perl

require './nagios-lib.pl';
&ReadParse();
&error_setup($text{'start_err'});

my ($err, $out) = exec_cmd('systemctl stop nrpe');
&error($out) if ($err);

&redirect("");
