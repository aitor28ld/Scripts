#!/bin/bash

# Main Packages
apt install libcairo2-dev libjpeg62-turbo-dev libpng-dev libossp-uuid-dev gcc make tomcat8 tomcat8-admin tomcat8-user

clear

# SSH & Guancec
apt install libavcodec-dev libavutil-dev libswscale-dev libpango1.0-dev libssh2-1-dev libssl-dev

clear

# Download Server package
user=$(whoami)
cd /home/$user
wget https://www.apache.org/dist/guacamole/0.9.14/source/guacamole-server-0.9.14.tar.gz

# Unzip Server package
tar -xzf guacamole-server-0.9.14.tar.gz
cd guacamole-server-0.9.14

# Auto-configuration
./configure --with-init-dir=/etc/init.d

clear

# Compilation and install
make
make install
ldconfig

clear

# Download Client package
cd /home/$user
wget https://www.apache.org/dist/guacamole/0.9.14/source/guacamole-client-0.9.14.tar.gz

# Unzip Client package
tar -zxf guacamole-client-0.9.14.tar.gz
cd guacamole-client-0.9.14

clear

# Install maven and openjdk8-jdk packages
apt install maven openjdk-8-jdk

clear

# Create .war file
mvn package

clear

# Copy .war file
mkdir /var/lib/tomcat8/webapps
mv guacamole-0.9.14.war guacamole.war
cp guacamole.war /var/lib/tomcat8/webapps/guacamole.war

# Restart tomcat8
/etc/init.d/tomcat8 restart

# Start guacd
/etc/init.d/guacd start

# Create main directories
mkdir /etc/guacamole /usr/share/tomcat8/.guacamole

# Create guacamole properties file
cd /etc/guacamole
touch guacamole.properties

echo "
guacd-hostname: localhost
guacd-port: 4822
user-mapping: /etc/guacamole/user-mapping.xml
auth-provider: net.sourceforge.guacamole.net.basic.BasicFileAuthenticationProvider
basic-user-mapping: /etc/guacamole/user-mapping.xml
" > guacamole.propierties

# Make a symbolic link to propierties file
ln -s guacamole.propierties /usr/share/tomcat8/.guacamole/

# Create user password
read -p "Define a user for administration panel: " paneluser
read -s -p "Define a user password: " userpassword
read -p "Define an IP for the host:" ip
read -p "Define a ssh user:" sshuser

password=$(prinft '%s' $userpassword | md5sum | cut -d ' ' -f 1)

echo '
<user-mapping>
  <authorize
    username="'$paneluser'"
    password="'$password'"
    encoding="md5">
   <connection name="SSH">
    <protocol>ssh</protocol>
    <param name="hostname">'$ip'</param>
    <param name="port">22</param>
    <param name="username">'$sshuser'</param>
   </connection>
  </authorize>
</user-mapping>
' > user-mapping.xml

# Give privilege to files
chmod 600 user-mapping.xml
chown tomcat8:tomcat8 user-mapping.xml

# Restart all main services
/etc/init.d/tomcat8 restart
/etc/init.d/guacd restart
