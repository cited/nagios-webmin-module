#!/usr/bin/perl

require './nagios-lib.pl';
&ReadParse();
&ui_print_header(undef, $text{'manual_title'}, "");

# Work out and show the files
@files = get_cfg_files(get_nagios_home().'/etc');
$in{'file'} ||= $files[0];
&indexof($in{'file'}, @files) >= 0 || &error($text{'manual_efile'});

print &ui_form_start("edit_cfg.cgi");
print "<b>$text{'manual_file'}</b>\n";
print &ui_select("file", $in{'file'}, [ map { [ $_ ] } @files ], 1, 0);
print &ui_submit($text{'manual_ok'});
print &ui_form_end();

# Show the file contents
print &ui_form_start("save_cfg.cgi", "form-data");
print &ui_hidden("file", $in{'file'}),"\n";
$data = &read_file_contents($in{'file'});
print &ui_textarea("data", $data, 20, 80),"\n";
print &ui_form_end([ [ "save", $text{'save'} ] ]);

&ui_print_footer("", $text{'index_return'});
