#!/usr/bin/perl

require './nagios-lib.pl';
require '../webmin/webmin-lib.pl';	#for OS detection

foreign_require('apache', 'apache-lib.pl');
foreign_require('software', 'software-lib.pl');

$www_user = 'www-data';
$nrpe_ver = '3.2.1';

sub install_nagios_core{
	my $nagios_ver = '4.4.5';
	my $tmpfile = download_file('https://github.com/NagiosEnterprises/nagioscore/archive/nagios-'.$nagios_ver.'.tar.gz');

	exec_cmd('groupadd -r nagios');
	exec_cmd('usermod -a -G nagios '.$www_user);

	&apache::add_configured_apache_module('rewrite');
	&apache::add_configured_apache_module('cgi');
	&apache::restart_apache();

	my $sh_file = &transname('nagios.sh');
	open($fh, '>', $sh_file) or die "open:$!";
	printf $fh 'cd  /tmp'."\n";
	printf $fh 'tar -xf '.$tmpfile."\n";
	printf $fh 'cd /tmp/nagioscore-nagios-'.$nagios_ver."\n";
	if(-d '/etc/apache2/sites-enabled'){
		printf $fh './configure --with-httpd-conf=/etc/apache2/sites-enabled'."\n";
	}elsif(-d '/etc/httpd/conf.d/'){
		printf $fh './configure --with-httpd-conf=/etc/httpd/conf.d'."\n";
	}
	printf $fh 'make all install-groups-users install install-daemoninit install-commandmode install-config install-webconf'."\n";
	close $fh;
	exec_cmd('bash '.$sh_file);

	my $nag_pass;
	my @pw_chars = ("A".."Z", "a".."z", "0".."9", "_", "-");
	$nag_pass .= $pw_chars[rand @pw_chars] for 1..10;

	exec_cmd('echo "'.$nag_pass.'" | htpasswd -i -c /usr/local/nagios/etc/htpasswd.users nagiosmin');

	printf "<hr> Nagios HTTP password saved in <b>".$module_config_directory.'/auth.txt</b></br>';
	open($fh, '>>', $module_config_directory.'/auth.txt') or die "open:$!";
	print $fh 'nagiosmin http pass:'.$nag_pass."\n";
	close $fh;

	&unlink_file('/tmp/nagioscore-nagios-'.$nagios_ver);
}

sub install_nagios_plugins{
	my $plugins_ver = '2.3.1';
	my $tmpfile = download_file('https://github.com/nagios-plugins/nagios-plugins/archive/release-'.$plugins_ver.'.tar.gz');

	my $sh_file = &transname('plugins.sh');
	open($fh, '>', $sh_file) or die "open:$!";
	printf $fh 'cd  /tmp'."\n";
	printf $fh 'tar -xf '.$tmpfile."\n";
	printf $fh 'cd /tmp/nagios-plugins-release-'.$plugins_ver."\n";
	printf $fh './tools/setup'."\n";
	printf $fh './configure'."\n";
	printf $fh 'make'."\n";
	printf $fh 'make install'."\n";
	close $fh;

	exec_cmd('bash '.$sh_file);

	exec_cmd('systemctl restart nagios.service');
	&unlink_file('/tmp/nagios-plugins-release-'.$plugins_ver);
}

sub install_nagios_nrpe_service{
	my $sh_file = &transname('nrpe.sh');
	open($fh, '>', $sh_file) or die "open:$!";

	if(! -d '/tmp/nrpe-'.$nrpe_ver){
		my $tmpfile = download_file('https://github.com/NagiosEnterprises/nrpe/releases/download/nrpe-'.$nrpe_ver.'/nrpe-'.$nrpe_ver.'.tar.gz');
		printf $fh 'cd  /tmp'."\n";
		printf $fh 'tar -xf '.$tmpfile."\n";
		printf $fh 'cd nrpe-'.$nrpe_ver."\n";
		printf $fh './configure'."\n";
	}
	printf $fh 'cd /tmp/nrpe-'.$nrpe_ver."\n";
	printf $fh 'make nrpe install-daemon install-config install-init'."\n";
	close $fh;

	exec_cmd('bash '.$sh_file);
}

sub install_nagios_nrpe_plugin{

	my $sh_file = &transname('nrpe.sh');
	open($fh, '>', $sh_file) or die "open:$!";

	if(! -d '/tmp/nrpe-'.$nrpe_ver){
		my $tmpfile = download_file('https://github.com/NagiosEnterprises/nrpe/releases/download/nrpe-'.$nrpe_ver.'/nrpe-'.$nrpe_ver.'.tar.gz');
		printf $fh 'cd  /tmp'."\n";
		printf $fh 'tar -xf '.$tmpfile."\n";
		printf $fh 'cd nrpe-'.$nrpe_ver."\n";
		printf $fh './configure'."\n";
	}
	printf $fh 'cd /tmp/nrpe-'.$nrpe_ver."\n";
	printf $fh 'make check_nrpe install-plugin'."\n";
	close $fh;

	exec_cmd('bash '.$sh_file);
}

sub setup_checks{

	#Check for commands
	if (!&has_command('tar')) {
		print '<p>Warning: tar command is not found. Install it manually or '.
			  "<a href='../package-updates/update.cgi?mode=new&source=3&u=tar&redir=%2E%2E%2Fnagios%2Fsetup.cgi&redirdesc=Setup'>click here</a> to have it downloaded and installed.</p>";
	}

	if($osinfo{'real_os_type'} =~ /centos/i){	#CentOS
		my @pinfo = software::package_info('epel-release', undef, );
		if(!@pinfo){
			print "<p>Warning: EPEL repository is not installed. Install it manually or ".
					"<a href='../software/install_pack.cgi?source=3&update=epel-release&return=%2E%2E%2Fnagios%2Fsetup.cgi&returndesc=Setup&caller=nagios'>click here</a> to have it downloaded and installed.</p>";
		}
	}

	my @dep_pkgs;
	if(	( $osinfo{'real_os_type'} =~ /centos/i) or	#CentOS
			($osinfo{'real_os_type'} =~ /fedora/i)	or  #Fedora
			($osinfo{'real_os_type'} =~ /scientific/i)	){
		@dep_pkgs = ('httpd', 'httpd-tools', 'gcc', 'glibc', 'glibc-common', 'gd', 'gd-devel', 'perl', 'perl-Net-SNMP', 'make', 'gettext', 'automake', 'autoconf', 'openssl-devel', 'net-snmp', 'net-snmp-utils', 'krb5-devel');
	}elsif( ($osinfo{'real_os_type'} =~ /ubuntu/i) or
					($osinfo{'real_os_type'} =~ /debian/i) 	){	#ubuntu or debian
		@dep_pkgs = ('apache2', 'autoconf', 'gcc', 'libc6', 'make', 'unzip', 'php', 'libapache2-mod-php', 'libgd-dev', 'libwww-perl', 'libmcrypt-dev', 'libssl-dev', 'bc', 'gawk', 'dc', 'build-essential', 'snmp', 'libnet-snmp-perl', 'gettext', 'libkrb5-dev');
	}

	my @pkg_missing;
	foreach my $pkg (@dep_pkgs){
		my @pinfo = software::package_info($pkg);
		if(!@pinfo){
			push(@pkg_missing, $pkg);
		}
	}

	if(@pkg_missing){
		my $url_pkg_list = '';
		foreach my $pkg (@pkg_missing){
			$url_pkg_list .= '&u='.&urlize($pkg);
		}
		my $pkg_list = join(', ', @pkg_missing);

		print "<p>Warning: Missing Nagios dependencies - $pkg_list packages are not installed. Install them manually or ".
				"<a href='../package-updates/update.cgi?mode=new&source=3${url_pkg_list}&redir=%2E%2E%2Fnagios%2Fsetup.cgi&redirdesc=Setup'>click here</a> to have them installed.</p>";
	}

	if(! -d '/usr/local/nagios/'){
		print "<p>Nagios core not installed. ".
			  "<a href='setup.cgi?mode=install_nagios_core&return=%2E%2E%2Fnagios%2Fsetup.cgi&returndesc=Setup&caller=nagios'>Click here</a> install it";
	}

	if(! -f '/usr/local/nagios/libexec/check_apt'){
		print "<p>Nagios Plugins not installed. ".
			  "<a href='setup.cgi?mode=install_nagios_plugins&return=%2E%2E%2Fnagios%2Fsetup.cgi&returndesc=Setup&caller=nagios'>Click here</a> install it";
	}

	if(! -f '/usr/local/nagios/etc/nrpe.cfg'){
		print "<p>Nagios NRPE Service is not installed. ".
			  "<a href='setup.cgi?mode=install_nagios_nrpe_service&return=%2E%2E%2Fnagios%2Fsetup.cgi&returndesc=Setup&caller=nagios'>Click here</a> install it";
	}

	if(! -f '/usr/local/nagios/libexec/check_nrpe'){
		print "<p>Nagios NRPE Plugin is not installed. ".
			  "<a href='setup.cgi?mode=install_nagios_nrpe_plugin&return=%2E%2E%2Fnagios%2Fsetup.cgi&returndesc=Setup&caller=nagios'>Click here</a> install it";
	}

	print '<p>If you don\'t see any warnings above, you can complete setup by clicking '.
	  "<a href='setup.cgi?mode=cleanup&return=%2E%2E%2Fnagios%2F&returndesc=AcuGIS%20ES&caller=nagios'>here</a></p>";
}

#Remove all setup files
sub setup_cleanup{
	print "Completing Set Up....</br>";
	&unlink_file($module_root_directory.'/setup.cgi');
	&unlink_file('/tmp/nrpe-'.$nrpe_ver);
	print &js_redirect("index.cgi");
}


&ui_print_header(undef, $text{'setup_title'}, "");

if($ENV{'CONTENT_TYPE'} =~ /boundary=(.*)$/) {
	&ReadParseMime();
}else {
	&ReadParse(); $no_upload = 1;
}

my $mode = $in{'mode'} || "checks";
%osinfo = &detect_operating_system();

if(	( $osinfo{'real_os_type'} =~ /centos/i) or	#CentOS
		($osinfo{'real_os_type'} =~ /fedora/i)	or  #Fedora
		($osinfo{'real_os_type'} =~ /scientific/i)	){
	$www_user = 'apache';
}

if($mode eq "checks"){							setup_checks();
	&ui_print_footer('', $text{'index_return'});
	exit 0;
}elsif($mode eq "cleanup"){						setup_cleanup();
	&ui_print_footer('', $text{'index_return'});
	exit 0;
}elsif($mode eq "install_nagios_core"){				install_nagios_core();
}elsif($mode eq "install_nagios_plugins"){		install_nagios_plugins();
}elsif($mode eq "install_nagios_nrpe_service"){				install_nagios_nrpe_service();
}elsif($mode eq "install_nagios_nrpe_plugin"){				install_nagios_nrpe_plugin();
}else{
	print "Error: Invalid setup mode\n";
}

&ui_print_footer('setup.cgi', $text{'setup_title'});
