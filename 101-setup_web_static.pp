# Puppet for setup
# Define the nginx config variable
$nginx_conf = "server {
    listen 80 default_server;
    listen [::]:80 default_server;
    add_header X-Served-By ${hostname};
    root   /var/www/html;
    index  index.html index.htm;
    location /hbnb_static {
        alias /data/web_static/current;
        index index.html index.htm;
    }
    location /redirect_me {
        return 301 https://www.linkedin.com/in/anas-ribki/;
    }
    error_page 404 /404.html;
    location /404 {
      root /var/www/html;
      internal;
    }
}"

# Install nginx if it not already installed
package { 'nginx':
  ensure   => 'present',
  provider => 'apt'
}

# Create the folders if they don't already exist
file { ['/data', '/data/web_static', '/data/web_static/releases', '/data/web_static/shared', '/data/web_static/releases/test']:
  ensure => directory,
  owner  => 'ubuntu',
  group  => 'ubuntu',
}

# Create a fake HTML file to test the Nginx configuration
file { '/data/web_static/releases/test/index.html':
  ensure  => present,
  owner   => 'ubuntu',
  group   => 'ubuntu',
  mode    => '0644',
  content => "this webpage is found in data/web_static/releases/test/index.htm \n"
}

# Create a symbolic link to the test folder
file { '/data/web_static/current':
  ensure => link,
  target => '/data/web_static/releases/test',
  force  => true,
}

# Give ownership of the /data/ folder to the ubuntu user AND group
exec { 'chown -R ubuntu:ubuntu /data/':
  path => '/usr/bin/:/usr/local/bin/:/bin/'
}

# Create the /var/www folder if it doesn't exist
file { '/var/www':
  ensure => directory,
}

# Create the /var/www/html folder if it doesn't exist
file { '/var/www/html':
  ensure => directory,
}

# Create a fake HTML file in /var/www/html
file { '/var/www/html/index.html':
  ensure  => present,
  owner   => 'root',
  group   => 'root',
  mode    => '0644',
  content => "This is my first upload in /var/www/index.html***\n"
}

# Create a fake HTML file for error page
file { '/var/www/html/404.html':
  ensure  => present,
  owner   => 'root',
  group   => 'root',
  mode    => '0644',
  content => "Ceci n'est pas une page - Error page\n"
}

# Update the Nginx configuration to serve the content of /data/web_static/current/ to hbnb_static
file { '/etc/nginx/sites-available/default':
  ensure  => present,
  owner   => 'root',
  group   => 'root',
  mode    => '0644',
  content => $nginx_conf,
}

# Restart Nginx after updating the configuration
service { 'nginx':
  ensure    => running,
  enable    => true,
  subscribe => File['/etc/nginx/sites-available/default'],
}
