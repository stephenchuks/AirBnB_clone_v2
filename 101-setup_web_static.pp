# File: /etc/puppet/manifests/0-setup_web_servers.pp

package { 'nginx':
  ensure => 'installed',
}

file { '/data/':
  ensure => 'directory',
}

file { '/data/web_static/':
  ensure => 'directory',
}

file { '/data/web_static/releases/':
  ensure => 'directory',
}

file { '/data/web_static/shared/':
  ensure => 'directory',
}

file { '/data/web_static/releases/test/index.html':
  content => '<html><head></head><body>Holberton School</body></html>',
  mode    => '0644',
  owner   => 'root',
  group   => 'root',
}

file { '/data/web_static/current':
  ensure  => 'link',
  target  => '/data/web_static/releases/test/',
  owner   => 'root',
  group   => 'root',
  require => [
    File['/data/web_static/releases/test/index.html'],
    File['/data/web_static/releases/'],
    File['/data/web_static/shared/'],
  ],
}

