<h1>Setting up environment Staging and security essentials</h2>

    Updating system : Now if we are using bare bones ubuntu server we need to do couple of things to do the setup first so Like updating the kernel ect ..
      => $ apt update && apt upgrade -y
    Change the hostname
      => $ hostnamect set-hostname flask-server
    Set this host name into our host file Override /etc/resolv.conf dns file
      => $ echo 45.33.123.214  Flask-Server >> /etc/hosts
    Now we set a limited user to our machine while we are logged into root	
      => $ adduser razi : Complete the work for user creation.
      => $ adduser razi sudo 'or' in RHEL adduser razi wheel 'or' useradd -aG razi wheel	
    Verify public key existance so we could connect to our Web server.
      => $ ls ~/.ssh
	  authorized_keys
    Change the permissions on the directory .ssh
      => $ sudo chmod 700 ~/.ssh/
    Change the permissions on the files inside .ssh/*
      => $ sudo chmod 600 ~/.ssh/*
    we Disallow "ROOT" Logins over ssh
      => $ sudo nano /etc/ssh/sshd_config
	  PermitRootLogin yes  /*We change it to*/ => PermitRootLogin No
	  PubKeyAuthentification yes
	  PermitEmptyPasswords no
	  PasswordAuthentification yes /*We change it to*/ => PasswordAuthentification no : the raison behind this is sometimes Malicious movers could try to        		'brute force passwords' but if we have the ssh keys we dont need to login to our system with a password.
    Restart our ssh daemon so configuration file changes take place.
      => $ sudo service sshd restart 
    Instead of using Iptables based on debian or firewall-cmd based on fedora we are going to install <b>ufw</b> the easiest way to <b>manage</b> our firewall       rules.

