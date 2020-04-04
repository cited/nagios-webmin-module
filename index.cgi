#!/usr/bin/perl

require './nagios-lib.pl';

# Check if config file exists
if (! -r $config{'nagios_config'}) {
	&ui_print_header(undef, $text{'index_title'}, "", "intro", 1, 1);
	print &text('index_econfig', "<tt>$config{'nagios_config'}</tt>",
		    "$gconfig{'webprefix'}/config.cgi?$module_name"),"<p>\n";
	&ui_print_footer("/", $text{"index"});
	exit;
}

if(-f "$module_root_directory/setup.cgi"){
	&redirect('setup.cgi');
}

# Check if tomcat is the right version
%version = &get_nagios_version();
&ui_print_header(undef, $text{'index_title'}, "", "intro", 1, 1, 0,
	&help_search_link("Nagios", "nrpe"), undef, undef,
	'Nagios ver.'.$version{'number'}.'<br><a href="https://www.citedcorp.com" target="_blank">Cited, Inc.</a> &copy; 2020');



push(@links, "edit_cfg.cgi");
push(@titles, $text{'manual_title'});
push(@icons, "images/edit-file.png");

push(@links, "edit_objects.cgi");
push(@titles, $text{'objects_title'});
push(@icons, "images/objects.png");


&icons_table(\@links, \@titles, \@icons, 2);

print &ui_hr();
print &ui_buttons_start();

my $is_running = nagios_is_running();
if ($is_running == 1) {
	print &ui_buttons_row("stop.cgi", $text{'index_stop'}, $text{'index_stopmsg'});
}else {
	print &ui_buttons_row("start.cgi", $text{'index_start'}, $text{'index_startmsg'});
}
print &ui_buttons_end();


print &ui_buttons_start();

my $is_running = nrpe_is_running();
if ($is_running == 1) {
	print &ui_buttons_row("stop_nrpe.cgi", $text{'index_stop_nrpe'}, $text{'index_stopmsg_nrpe'});
}else {
	print &ui_buttons_row("start_nrpe.cgi", $text{'index_start_nrpe'}, $text{'index_startmsg_nrpe'});
}
print &ui_buttons_end();


&ui_print_footer("/", $text{"index_return"});
