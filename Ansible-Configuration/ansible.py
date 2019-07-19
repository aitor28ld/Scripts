#!/usr/bin/env python
import commands
import sys

# Path vars
dir_path = '/etc/ansible/'
log_path = '/var/log/'
user = commands.getoutput('whoami')

# Check out for SSH Keys
def check_sshkey():
    print '{INFO} -- Cheking for private/public key pair for ssh'
    keys = commands.getoutput('ls /home/'+user+'/.ssh/ |grep -v "authorized_keys\|known_hosts"')
    if keys != '':
        print '{INFO} -- SSH Keys exists'
    else:
        print '{INFO} -- Making ssh keys'
        commands.getoutput('ssh-keygen -t rsa')

# Check Linux distribution
def check_distro():
    distro = commands.getoutput('cat /etc/os-release |grep -i "NAME" | grep -v PRETTY').split("=")[1]
    return distro

# Update the SO 
def updates():
    distro = check_distro()
    print "{INFO} -- Updating System"
    if 'Debian' in distro:
        commands.getoutput('sudo apt-get update && apt-get upgrade -y')
    elif 'CentOS' in distro:
        commands.getoutput('sudo yum check-update && yum update -y')
    else:
        print "{ERROR} -- No Linux distribution found"

# Check if Ansible is installed
def check_install():
    distro = check_distro()
    if 'Debian' in distro:
        installed = commands.getoutput('dpkg -s ansible | grep Status').split(":")[1].strip()
    elif 'CentOS' in distro:
        installed = commands.getoutput('yum -q info ansible | grep Repo').split(":")[1].strip()

    if installed == 'install ok installed' or installed == 'installed':
        print "{INFO} -- Ansible package already installed"
    else:
        print "{WARN} -- Ansible package not installed, installing..."
        if 'Debian' in distro:
            commands.getoutput('sudo apt-get install ansible -y')
        elif 'CentOS' in distro:
            commands.getoutput('sudo yum install ansible -y')

# Make all Ansible configuration files a backup
def backup_files(dir_path=dir_path):
    dir_files = commands.getoutput('ls '+dir_path).splitlines()
    if "old" not in dir_files:
        for data in dir_files:
            commands.getoutput('sudo mv '+dir_path+data+' '+dir_path+data+'.old')
            print "{INFO} -- "+data+" renamed"
    else:
        print "{WARN} -- Files already renamed"

# Create Ansible log directory
def ansible_log(log=log_path):
    ansible_dir = commands.getoutput('ls '+log).splitlines()
    if 'ansible' in ansible_dir:
        print '{INFO} -- Log directory already exists'
    else:
        print '{WARN} -- Log directory not exist. Creating...'
        commands.getoutput('sudo mkdir -p /var/log/ansible')

# Create a hosts file for Ansible (Only 1 host)
def create_config(dir_path=dir_path):
    hostname = raw_input('Hostname of the destiny server: ').split(".")[0]
    ip = raw_input('IP of the destiny server: ')
    commands.getoutput('rm hosts')
    commands.getoutput('echo "[default] \n'+hostname+' ansible_ssh_host='+ip+'">> hosts')
    commands.getoutput('sudo cp hosts ansible.cfg '+dir_path)


def deploy_sshkey(user=user):
    pubkey = commands.getoutput('cat ~/.ssh/id_rsa.pub')
    print "{INFO} -- Now run next Ansible command \nansible-playbook main.yml --ask-pass --extra-vars 'pubkey=\""+pubkey+"\" username=\""+user+"\"'"


if __name__ == "__main__":
    check_sshkey()
    updates()
    check_install()
    ansible_log()
    backup_files()
    create_config()
    deploy_sshkey()
