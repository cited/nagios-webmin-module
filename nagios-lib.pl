BEGIN { push(@INC, ".."); };
use WebminCore;

init_config();

sub get_nagios_config{
  my $lref = &read_file_lines($config{'nagios_config'});
  my @rv;
  my $lnum = 0;
  foreach my $line (@$lref) {
      my ($n, $v) = split(/\s+/, $line, 2);
      if ($n) {
        push(@rv, { 'name' => $n, 'value' => $v, 'line' => $lnum });
        }
      $lnum++;
      }
  return @rv;
}

sub get_nagios_home(){
  return '/usr/local/nagios';
}

sub get_nagios_version(){
	my %version;
  my $nagios_home = get_nagios_home();

  &open_execute_command(CMD, $nagios_home.'/bin/nagios -h', 1);
  while(my $line = <CMD>) {
    if ($line =~ /Nagios Core ([0-9\.]+)$/i) {
  		$version{'number'} = $1;
      last;
  	}
  }
  close(CMD);

  return %version;
}

sub nagios_is_running(){
  my $rv = 0;
  my $nagios_bin = get_nagios_home().'/bin/nagios';

  &open_execute_command(CMD, '/bin/ps -ef', 1);
  while(my $line = <CMD>) {
    if ($line =~ /$nagios_bin/i) {
  		$rv = 1;
      last;
  	}
  }
  close(CMD);

	return $rv;
}


sub nrpe_is_running(){
  my $rv = 0;
  my $nrpe_bin = get_nagios_home().'/bin/nrpe';

  &open_execute_command(CMD, '/bin/ps -ef', 1);
  while(my $line = <CMD>) {
    if ($line =~ /$nrpe_bin/i) {
  		$rv = 1;
      last;
  	}
  }
  close(CMD);

	return $rv;
}



sub get_cfg_files{
  my $dirpath = $_[0];
  my @files;

  opendir(DIR, $dirpath) or die $!;
  my @cfg_files = grep {
      /\.cfg$/             		              # ends in .cfg
      && -f $dirpath.'/'.$_   # its a file
    } readdir(DIR);
  closedir(DIR);

  #make file have full path name
  @cfg_files = map { $dirpath.'/'.$_} @cfg_files;
  push(@files, @cfg_files);

  return @files;
}


sub exec_cmd{
	my $cmd = $_[0];
	my $cmd_out='';

	my $rv = &execute_command($cmd, undef, \$cmd_out, \$cmd_out, 0, 0);
	if($cmd_out){
  	$cmd_out = &html_escape($cmd_out);
  	$cmd_out =~ s/[\r\n]/<\/br>/g;
  	print $cmd_out;
  }
  return $rv;
}

sub download_file{
	my $url = $_[0];

	my ($proto, $x, $host, $path) = split('/', $url, 4);
	my @paths = split('/', $url);
	my $filename = $paths[-1];
	if($filename eq ''){
		$filename = 'index.html';
	}

	my $port = 80;
	if($proto eq 'https'){
		$port = 443;
	}

	&error_setup(&text('install_err3', $url));
	my $tmpfile = &transname($filename);
	$progress_callback_url = $url;
	&http_download($host, $port, '/'.$path, $tmpfile, \$error, \&progress_callback);

	if($error){
		print &html_escape($error);
		return '';
	}
	return $tmpfile;
}
