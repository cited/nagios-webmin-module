#!/usr/bin/perl

require './nagios-lib.pl';
&ReadParse();
&ui_print_header(undef, $text{'objects_title'}, "");

# Work out and show the files
@files = get_cfg_files(get_nagios_home().'/etc/objects');
$in{'file'} ||= $files[0];
&indexof($in{'file'}, @files) >= 0 || &error($text{'manual_efile'});

print &ui_form_start("create_cfg.cgi", 'post');
print "<b>$text{'create_cfg_file'}</b>".&ui_textbox("new_filename", '', 20, 0).&ui_submit($text{'create_ok'});
print &ui_form_end();

print &ui_form_start("edit_objects.cgi");
print "<b>$text{'manual_file'}</b>\n";
print &ui_select("file", $in{'file'}, [ map { [ $_ ] } @files ], 1, 0);
print &ui_submit($text{'manual_ok'});
print &ui_form_end();

# Show the file contents
print &ui_form_start("save_objects.cgi", "form-data");
print &ui_hidden("file", $in{'file'}),"\n";
$data = &read_file_contents($in{'file'});
print &ui_textarea("data", $data, 20, 80),"\n";
print &ui_form_end([ [ "save", $text{'save'} ] ]);

&ui_print_footer("", $text{'index_return'});
