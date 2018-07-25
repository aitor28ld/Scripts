#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Scripts to automatize the installation of Apache Guacamole Server and Client

import subprocess

pwd = subprocess.getoutput('users')

# Important packages
subprocess.call(["apt","install","maven","openjdk-8-jdk","libcairo2-dev","libjpeg62-turbo-dev","libpng-dev","libossp-uuid-dev","gcc","make","tomcat8","tomcat8-admin","tomcat8-user","-y"])

guancenc = ["libavcodec-dev","libavutil-dev","libswscale-dev"]
rdp = "libfreerdp-dev"
ssh = ["libpango1.0-dev","libssh2-1-dev"]
telnet = ["libpango1.0-dev","libtelnet-dev"]
vnc = ["libvncserver-dev","libpulse-dev"]
openssl = "libssl-dev"
oggvorbis = "libvorbis-dev"
webp = "libvorbis-dev"

subprocess.call(["apt","install","libavcodec-dev","libavutil-dev","libswscale-dev","libpango1.0-dev","libssh2-1-dev","libssl-dev","-y"])

# Install Apache-Guacamole Server
#subprocess.call(["wget","https://www.apache.org/dist/guacamole/0.9.14/source/guacamole-server-0.9.14.tar.gz"])

#subprocess.call(["tar","-xzf","guacamole-server-0.9.14.tar.gz"])

#subprocess.check_call(["./configure","--with-init-dir=/etc/init.d"],cwd="/home/"+pwd+"/guacamole-server-0.9.14")

#subprocess.check_call(["make"], cwd="guacamole-server-0.9.14")
#subprocess.check_call(["make","install"], cwd="guacamole-server-0.9.14")
#subprocess.check_call(["ldconfig"], cwd="guacamole-server-0.9.14")

# Install Apache-Guacamole Client
#subprocess.check_call(["wget","https://www.apache.org/dist/guacamole/0.9.14/source/guacamole-client-0.9.14.tar.gz"], cwd="/home/"+pwd+"/")

#subprocess.call(["tar","-zxf","guacamole-client-0.9.14.tar.gz"])

#subprocess.check_call(["mvn","package"], cwd="/home/"+pwd+"/guacamole-client-0.9.14")

#subprocess.call(["mkdir","/var/lib/tomcat8/webapps"])
#subprocess.call(["mv","~/guacamole-client-0.9.14/guacamole/target/guacamole-0.9.14.war","~/guacamole-client-0.9.14/guacamole/target/guacamole.war"])
#subprocess.call(["cp","~/guacamole-client-0.9.14/guacamole/target/guacamole.war","/var/lib/tomcat8/webapps/guacamole.war"])

# Apache-Guacamole Server Configuration
#subprocess.call(["mkdir","/etc/guacamole","/usr/share/tomcat8/.guacamole"])


# Fix this issues
propierties = """echo '
guacd-hostname: localhost
guacd-port: 4822
user-mapping: /etc/guacamole/user-mapping.xml
auth-provider: net.sourceforge.guacamole.net.basic.BasicFileAuthenticationProvider
basic-user-mapping: /etc/guacamole/user-mapping.xml '
 > /etc/guacamole/guacamole.propierties"""

print(subprocess.check_output(propierties, shell=True))

#subprocess.call(["ln","-s","/etc/guacamole/guacamole.propierties","/usr/share/tomcat8/.guacamole/"])

user = input("Enter your user: ")
passwd = input("Enter your password: ")
password = subprocess.call(["printf","'%s'","'"+passwd+"'","|","md5sum"])

clientip = input("Enter ip of your client: ")
clientuser = input("Enter user of your client: ")
print(clientuser)

subprocess.call(["echo","""
<user-mapping>
  <authorize
    username='"""+user+"""'
    password='"""+password+"""'
    encoding="md5">
   <connection name="SSH">
    <protocol>ssh</protocol>
    <param name="hostname">"""+clientip+"""</param>
    <param name="port">22</param>
    <param name="username">'"""+clientuser+"""'</param>
   </connection>
  </authorize>
</user-mapping>
""",">","/etc/guacamole/user-mapping.xml"])

subprocess.call(["chmod","600","/etc/guacamole/user-mapping.xml"])
subprocess.call(["chown","tomcat8:tomcat8","/etc/guacamole/user-mapping.xml"])

subprocess.call(["/etc/init.d/tomcat8","restart"])
subprocess.call(["/etc/init.d/guacd","restart"])

print("Now you can access to http://localhost:8080/guacamole and log in")
