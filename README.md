# klog
## A simple Syslog server with a funky name

#### Currently an Alpha build. It barely works so don't use it in the real world
A simple syslog server that also allow for processing of messages and forwarding onto an SMTP source.
Addons can be written by making a *.py file in the ./addons/ folder, A template is provided at ./template.py.

This is my most ambitious project to date and I wanted to have a flexible yet easy to use syslog server.

Note: SMTP doesn't actually work at the moment, should be working in 0.5

Note2: spawning module_handle.py is hardcoded as python being python3

Currently to get this working you will need to:
 - Setup ./conf/configurator.ini
 - Run "python buffer_server.py" (endless loop)
 - Run "Python klog.py" (endless loop)
 - It won't do much more than receive the message and log it, need to write addons and implement smtp
 
####How this should work eventually (kind of does now)
When a UDP syslog message comes in on the specified port klog will:
 - read the message and write it to a global and local log
 - Spawn module_handle in a seperate process to digest the message
 - Try to find an IP or hostname in the addons
 - If a match is found then buffer_client will send the information to the server
 - If the buffer hasn't send a digest for X minutes then an email is sent

#### Listed below is the changelog
Pre Release
 - 0.0 - syslog server done (StackOverflow style)
 - 0.1 - added module handle, basic features and testing implemented
 - 0.2 - Actually readable, regexes and optimisations
 - 0.3 - Added smtp relay, serious regex overhaul, basic buffer code (need to merge), configurator template done. Class written for syslog dissecting and addons
 - 0.4 - Configurator implemented smtp_handle and buffer client/server, ADDONS WORKING WOOOOO


###Roadmap (Predicted)
 - Actually usable                          (0.5)
 - Write some addons                        (0.5)
 - Email implemented with email buffers     (0.5)
 - Buffer server needs some logs            (0.5)
 - Add as a systemd service                 (0.6)
 - Serious brute force tested               (0.7)
 - MySQL read and write                     (0.8)
 - Ability to forward messages              (1.0)
 - Ability to scale                         (1.0)
