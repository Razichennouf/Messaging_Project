<html>
<body>

<pre>
<h2>Setting up environment Staging and security essentials on remote machine</h2>
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
	  PasswordAuthentification yes /*We change it to*/ => PasswordAuthentification no : the raison behind this is sometimes Malicious movers could try to        	   <b>brute force passwords</b> but if we have the ssh keys we dont need to login to our system with a password.
    We change the default ssh port
      => $ sudo nano /etc/ssh/sshd_config
      	   Port 5000
    Restart our ssh daemon so configuration file changes take place.
      => $ sudo service sshd restart 
    Instead of using Iptables based on debian or firewall-cmd based on fedora we are going to install <b>ufw</b> the easiest way to <b>manage</b> our firewall       rules.
    We now setup a few rules here => Here we are allowing rules for certain ports
      => $sudo ufw default allow outgoing "outgoing traffic"
      => $sudo ufw default deny  incoming "incoming traffic"
      => $sudo ufw allow ssh
		rules updated
      => $sudo ufw allow 5000
		rules updated
   For security matters we do not allow port 80 and http traffic yet until we are sure everything is working the way that we wanted to.
      => $ sudo ufw enable 
   To check the status of the port we allowed or disawllowed
      => $ sudo ufw status 
<h2>Local machine</h2>
   Now we are GENERATING ssh keys -b 4096 encryption"
      => $ ssh-keygen -b 4096
   Copying our public key to the remote machine
      => $ ssh-copy-id coreyms@45.33.123.214
<h2>Technical overview</h2>
    * Connecting <b>web application</b> to <b>web servers</b> * 
    Our Stack we are going to use is NGINX & GUNICORN WSGI
      <b>Gunicorn</b> is a pure-Python HTTP server for WSGI applications. It allows you to run any Python application concurrently by running multiple Python             rocesses within a single dyno. It provides a perfect balance of performance, flexibility, and configuration simplicity
      <b>WSGI</b> stands for "Web Server Gateway Interface". It is used to forward requests from a web server (such as Apache or NGINX) to a backend Python web application or framework. From there, responses are then passed back to the webserver to reply to the requestor
</pre>	
</body>
</html>
