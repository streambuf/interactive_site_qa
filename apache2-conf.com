User askmoiseev
DirectoryIndex index.html
WSGIPythonPath /home/max/askmoiseev
<VirtualHost *:8080>
        ServerName askmoiseev
        ServerAlias www.askmoiseev
        DocumentRoot /home/max/askmoiseev
        ErrorLog /var/log/askmoiseev/error_log
        CustomLog /var/log/askmoiseev/access_log combined
        WSGIScriptAlias / /home/max/askmoiseev/askmoiseev/wsgi.py
        <Directory /home/max/askmoiseev/askmoiseev>
            Order deny,allow
            Allow from all
        </Directory>
</VirtualHost>
