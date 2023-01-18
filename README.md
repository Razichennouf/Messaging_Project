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
   Installing and implementing <b>Virtualenv</b>
      Why ? it is a way that you can separete different python environments for different projects 
      e.g say you have multiple projects Django or Flask each one of these projects may be using a different version of Django or different version of Flask 
        now if you go and upgrade that package and youre global size packages then it could brake a couple of your websites it would be <b>better</b> if the 	     projects had an <b>isolated</b> environment where they had only the <b>Dependencies</b> and the <b>Packages</b> that they need and the specific                 versions that they needed
      Installing the Virualenv
	$ pip install virtualenv
      Creating our First environment
        $ mkdir Project_Flask
        $ virualenv project1_env
      Creating a Venv with specific Python version
        $ virualenv -p /usr/bin/python2.6 Py2.6_env
      Activating Our newly created Virtualenv using the <b>activate</b> binary from source function
        $ source Project1_env/bin/activate
      How to check ?
        It will now add <b>(Project1_env)</b> to your prompt and it is the only indicator that we are in the Virtual environment
      How to <b>Wrap</b> all packages and the version numbers to use in another project to a text file
      	$ pip freeze --local > requirements.txt
      How to leave the virtual environment to global environment
      	$ deactivate
<h2>Technical overview</h2>
    * Connecting <b>web application</b> to <b>web servers</b> * * Our Stack we are going to use are NGINX & GUNICORN WSGI *
      <b>Gunicorn</b> is a pure-Python HTTP server for WSGI applications. It allows you to run any Python application concurrently by running multiple Python             rocesses within a single dyno. It provides a perfect balance of performance, flexibility, and configuration simplicity
      <b>WSGI</b> stands for "Web Server Gateway Interface". It is used to forward requests from a web server (such as Apache or NGINX) to a backend Python web application or framework. From there, responses are then passed back to the webserver to reply to the requestor

<h1>Let's Get started !</h1>
     Creating the Python file
        $ mousepad Flask_Project.py
	  from flask import Flask
	  app = FLask(__name__)
	  @app.route("/")
	  def hello():
	      return "hello World!"
     Adding a environment variable to the <b>File</b> that we want to be our flask application
         Linux : $ export FLASK_APP=Flask_Project.py
	 Windows : set Flask_Project.py
     Running your FLASK app
        $ flask run
     Enabeling FLASK_DEBUG Mode
        $ export FLASK_DEBUG=1
        Why we need  DEBUG Mode ? : To automatically reload our project without restarting the web server
     To run the Flask Appp using $ Python
     	if __name__ = '__name__':
 	   app.run(debug=True)
	 $ Python3 Flask_Project.py
     <b>Why ?</b> www.facebook.com/login.py =  www.facebook.com/ 
         @app.route(/)
	 @app.route(/index.py)
	 def login():
	     return <Content>;
     <b>Hint : </b>To prevent errors making a GET requests on the server racine "/" while using <b>render_template</b> module you should create a directory 		called <b>templates</b> and put all your html format into it.  
     	       <b>Beware !</b> in flask there are predefined directories (Statically defined) that searches into it for example 
	           <link rel="stylesheet" href="<b>css/style.css</b>"> => it does'nt work so you should create :
		      $ mkdir static
		      $ move css static
		    so the point is that the root folder is predefined / => static , templates (render_template) ect ...
<h1>Database setup</h1>
    $ pip install flask-sqlalchemy
    $ mousepad __ini__
    	db = SQLAlchemy()
	DB_NAME = ".database.db" => we set the database file as a hidden file we add "."
    	app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
   	db.init_app(app)
<h1>Authentication</h1>
 <b>LDAP</b> authentication involves verifying provided usernames and passwords by connecting with a directory service that uses  the LDAP protocol. Some directory-servers that use LDAP in this manner are OpenLDAP, MS Active Directory, and OpenDJ.
<b>Quote</b> : An authentication method is a process of confirming an identity.
  As proceeding with the <b>Isolation</b> of the environment with virtualenv now we are going to install the <b>LDAP3</b> 
  <b>My approach to ldap authentification and data migration from sql database to LDAP ldif</b>
  	Script bash or batch automated to migrate data every time sql query triggered via lambda function
  $ pip install python-ldap
  $ apt-get install build-essential python3-dev libldap2-dev libsasl2-dev slapd ldap-utils tox lcov valgrind

LDAP url format :https://ldap.com/ldap-urls/

To start the connection on a SSL socket:
	>>> server = Server('ipa.demo1.freeipa.org', use_ssl=True, get_info=ALL)
	>>> conn = Connection(server, 'uid=admin,cn=users,cn=accounts,dc=demo1,dc=freeipa,dc=org', 'Secret123', auto_bind=True)
	>>> print(conn)
	ldaps://ipa.demo1.freeipa.org:636 - ssl - user: uid=admin,cn=users,cn=accounts,dc=demo1,dc=freeipa,dc=org - bound - open - <local: 192.168.1.101:51438 - remote: 209.132.178.99:636> - tls not started - listening - SyncStrategy - internal decoder

You need to create your certificate to use it on LDAP and all other protocols likes SSL
<b>LDAP namespace Structure</b> : https://www.informit.com/articles/article.aspx?p=101405&seqNum=7
<h1>App security</h1>
   1) First we have to setup and put the password hashed into our database 
 	hint : the SHA1 is deprecated so please do not use it anymore since 2004 computers could break into those hashes
   2) Secondly we have to print account status login globally f.e if e-mail isnt into the database please do not print an error 
        like 'Email does not exist' here you are guiding the hacker and checking if the email exists into your database or no
	so try to use global and general terms like 'Email or Password incorrect'.
   3) We register those routers with <b>blueprints</b> to counter traversal and make no prefixes all from root route
       app.register_blueprint(views, url_prefix='/')
       app.register_blueprint(auth, url_prefix='/')
    4) 
 <b>Commands may be helpfull</b> : systemctl daemon-reload ; dpkg-reconfigure slapd <= in case forgotten password
<h1>Cloud deployment</h1>
1) configure and enable virtual host
       sudo nano /etc/apache2/sites-available/webApp.conf
	<VirtualHost *:80>
		ServerName ip
		ServerAdmin email@mywebsite.com
		WSGIScriptAlias / /var/www/webApp/webapp.wsgi
		<Directory /var/www/webApp/webApp/>
			Order allow,deny
			Allow from all
		</Directory>
		Alias /static /var/www/webApp/webApp/static
		<Directory /var/www/webApp/webApp/static/>
			Order allow,deny
			Allow from all
		</Directory>
		ErrorLog ${APACHE_LOG_DIR}/error.log
		LogLevel warn
		CustomLog ${APACHE_LOG_DIR}/access.log combined
	</VirtualHost>
2)      sudo a2ensite webApp 
	  systemctl reload apache2
3)   Implement the GUNICORN .wsgi file with the configuration
	    #!/usr/bin/python
		import sys
		import logging
		logging.basicConfig(stream=sys.stderr)
		sys.path.insert(0,"/var/www/webApp/")

		from webApp import app as application
		application.secret_key = 'Add your secret key'
	     # Restart your apache server : $ systemctl reload apache2
    <b>CI/CD Pipeline</b> : https://www.youtube.com/watch?v=NwzJCSPSPZs&ab_channel=BlockExplorer
</pre>	
</body>
</html>
