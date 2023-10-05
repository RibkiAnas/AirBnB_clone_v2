# Puppet for setup
# Install Nginx if it not already installed
package { 'nginx':
  ensure => installed,
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
  content => '<html><head></head><body>Alx swe School</body></html>',
}

# Create a symbolic link to the test folder
file { '/data/web_static/current':
  ensure => link,
  target => '/data/web_static/releases/test',
  force  => true,
}

# Update the Nginx configuration to serve the content of /data/web_static/current/ to hbnb_static
file_line { 'nginx_config':
  path  => '/etc/nginx/sites-enabled/default',
  line  => 'location /hbnb_static { alias /data/web_static/current/; }',
  after => 'listen 80 default_server;',
}

# Restart Nginx after updating the configuration
service { 'nginx':
  ensure    => running,
  enable    => true,
  subscribe => File_line['nginx_config'],
}
