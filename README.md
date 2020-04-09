# DHTTPFS
## The Decrypting HTTP File Server

HTTP server that serves a local directory with encrypted files and unencrypts them on request time.

It's intended to run locally, and based on python's built-in HTTP server - do not use in production.

## Usage

Usage is similar to `http.server` (old `SimpleHTTPServer` in python2):

    $ python3 -m dhttpfs.server --help
    usage: server.py [-h] [--bind BIND] [--directory DIRECTORY] [port]
    
    positional arguments:
      port                  port [default: 8000]
    
    optional arguments:
      -h, --help            show this help message and exit
      --bind BIND, -b BIND  bind address [default: localhost only]
      --directory DIRECTORY, -d DIRECTORY

## Supported encryption methods:

  - GPG symmetric
