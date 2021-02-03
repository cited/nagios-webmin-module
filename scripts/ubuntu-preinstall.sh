# !/bin/bash -e
# nagios-webmin-module Pre-Install Script for CentOS and Ubuntu
# For use on Ubuntu box only
# Usage:
# wget https://raw.githubusercontent.com/cited/nagios-webmin-module/master/scripts/pre-install.sh
# chmod +x pre-installer
# ./pre-installer.sh

function install_webmin(){

	

	echo "deb http://download.webmin.com/download/repository sarge contrib" > /etc/apt/sources.list.d/webmin.list
	wget -qO - http://www.webmin.com/jcameron-key.asc | apt-key add -
	apt-get -y update
	apt-get -y install webmin
	
}	

function download_nagios_webmin_module(){
pushd /tmp/
	wget https://github.com/cited/nagios-webmin-module/archive/master.zip
	unzip master.zip
	mv nagios-webmin-module-master nagios
	tar -czf /opt/nagios.wbm.gz nagios
	rm -rf nagios master.zip
popd
  
}

function download_certbot_module(){
pushd /tmp/
	wget https://github.com/cited/Certbot-Webmin-Module/archive/master.zip
	unzip master.zip
	mv Certbot-Webmin-Module-master certbot
	tar -czf /opt/certbot.wbm.gz certbot
	rm -rf certbot master.zip
popd
}

function install_apache(){
	
		apt-get -y install apache2
	
}

function install_nagios_webmin_module(){
pushd /opt/
        
       	/usr/share/webmin/install-module.pl nagios.wbm.gz
        
popd
        echo -e "Nagios Module is now installed. Go to Servers > Nagios to complete installation"
	
}

function install_certbot_module(){
pushd /opt/
	
	/usr/share/webmin/install-module.pl certbot.wbm.gz
  popd
        echo -e "Certbot is now installed. Go to Servers > Certbot to complete installation"
	
}

function get_deps(){

		apt-get -y install wget unzip



}

function install_apache(){

		apt-get -y install apache2



}

get_deps;
install_webmin;
install_apache;
download_nagios_webmin_module;
download_certbot_module;
install_certbot_module;
install_nagios_webmin_module;
