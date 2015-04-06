twitch-quote-bot
================

A bot mainly for Twitch channels, but can be used for other purposes as well.
 
The bot supports writing custom commands using Lua, and saves it's states in
 an sqlite database.


Current build status
====================

[![Build Status](https://travis-ci.org/lietu/twitch-quote-bot.svg?branch=master)](https://travis-ci.org/lietu/twitch-quote-bot)


Using the bot
=============
The documentation for using the bot, creating commands, 
etc. is in the GitHub [project wiki](https://github.com/lietu/twitch-quote-bot/wiki) at
[https://github.com/lietu/twitch-quote-bot/wiki](https://github.com/lietu/twitch-quote-bot/wiki).


Windows users
=============

You can totally just download a .zip with an .exe in it and you don't need to worry about any other requirements.

1. Go to [twitch-bot releases](https://github.com/lietu/twitch-bot/releases) page
1. Download the latest .zip, extract to where-ever you wish
1. Copy `settings.example.py` to `settings.py`, and edit it.
1. Check the [Getting an OAuth token for Twitch chat IRC access](https://github.com/lietu/twitch-bot#getting-an-oauth-token-for-twitch-chat-irc-access) -section for basic connectivity help. At least `USER`, `OAUTH_TOKEN` and `CHANNEL_LIST` should be edited.
1. Run `twitchbot.exe`
1. Profit!11eleven



Requirements
============
* Python 2.6/2.7/3.3/3.4 
* pip
* lua (5.1, 5.2 or luajit should work)

Python 3.1 and 3.2 don't work because of they broke backwards compatibility 
with unicode string literals. Thanks pals.

Optional:
* virtualenv
* virtualenvwrapper

How to install prerequisites in Ubuntu:
```
sudo apt-get install python-pip lua5.1 liblua5.1-dev
sudo pip install virtualenv virtualenvwrapper
```

And on RHEL/CentOS/Fedora/similar:
```
# Enable EPEL repos for python-pip, for CentOS 6
rpm -Uvh http://ftp.linux.ncsu.edu/pub/epel/6/i386/epel-release-6-8.noarch.rpm

yum -y install python-setuptools python-pip python-devel lua lua-devel gcc
pip install virtualenv virtualenvwrapper
```


For Qt frontend you'll also need to install PySide:
```
pip install PySide==1.2.2
```

Setup
=====

 1. Get the code from GitHub.
 1. (Optional) Create virtualenv
    ```
    source $(which virtualenvwrapper.sh)
    mkvirtualenv virtualenv
    # In the future, instead run: ```workon virtualenv```
    ```
 1. Install dependencies
    ```
    pip install -r requirements.txt
    # You might have to prepend sudo if not using virtualenv
    ```
 1. Copy settings.example.py to settings.py, and edit to needs
 1. Run the bot: ```python start.py```


Getting an OAuth token for Twitch chat IRC access
=================================================

You should visit these pages for help:

 * http://help.twitch.tv/customer/portal/articles/1302780-twitch-irc
 * http://twitchapps.com/tmi/


What if I want to stop using the bot?
=====================================

Getting rid of the bot itself is fairly easy, just stop it on the server you
 are running it on (press CTLR+C a few times)
 
However, you probably want access to your valued data as well. The bot's 
database is implemented using a very widely known engine called SQLite. 
There are plenty of tools you can use to take the bot.sqlite (default name) 
database and extract whatever data you want from it.
 
Quotes will probably be the only data actually useful outside of this bot, 
so there is a separate tool just for extracting them, dump_quotes.py.

Usage is fairly simple, call it and give it your channel's name (e.g. #lietu):
```
python dump_quotes.py "#lietu"
```

Notice the quotes in the example above, they are important to make sure your
 shell does not think you are writing a comment.

If you want to extract the quotes to a file, just redirect the output:
```
python dump_quotes.py "#lietu" > quotes.txt
```


Backup tool
===========

Your data is important, which is why there's a bundled backup tool with the 
bot.

The tool handles:
 * Keeping a given number of backups (e.g. 30)
 * Optionally compressing the backups (with gzip)
 
The settings for the backups are also in settings.py and should be fairly 
easy to understand.

To schedule the backups you need to use your crontab or other scheduling 
system. E.g. on linux, run:
```
crontab -e
```

Check the path to your python executable (usually /usr/bin/python):
```
which python
```

And add the following line (replace */path/to/* and */usr/bin/python* with the 
correct paths):
```
0 * * * *   /usr/bin/python /path/to/backup.py > /dev/null
```


Development environment
=======================

The development environment is built into the project via Vagrant.

To start using the development environment, install the following:

 * [Vagrant](https://www.vagrantup.com/)
 * [VirtualBox](https://www.virtualbox.org/)

After these are installed, you can boot up the Vagrant virtual machine.

Open a terminal, and change to the root directory of the project, 
then tell Vagrant to boot up the machine:

```
vagrant up
```

Once the VM is up, you can connect to it over SSH.

You can open your favorite SSH client (e.g. [KiTTY](http://www.9bis
.net/kitty/) on Windows) by using the IP address ```172.30.30.30```.

Alternatively on Linux and Mac OS X you can connect to it with:
```
vagrant ssh
```

User and password are both: ```vagrant```

To get to the development environment, you need to switch users:
```
sudo su - bot
```

Then activate the bot virtual environment:
```
workon bot
```

The source code is located on the virtual machine in /src, 
you might want to go there:
```
cd /src
```

Running tests
=============

When you have your Vagrant based development environment (or any other 
correctly set up environment) running, and you're in the root of the source 
folder you can run the unit tests via nose:
```
nosetests
```

If using the Vagrant VM in Windows, the shared folder causes some minor 
issues, you can work around that by telling nose to also include executable 
files in it's search for valid tests:
```
nosetests --exe
```

Code documentation
==================

You can generate HTML code documentation from the source code with Sphinx by
going to the docs/ folder and telling Sphinx to rebuild the HTML and run the
doctest tests embedded in the source at the same time:
```
make html doctests
```

On the Vagrant VM be sure to have activated the development virtualenv and 
run the command in ```/src/docs```


Salt Stack
==========

The development environment VM configuration is managed with Salt Stack.

If you make changes within the salt/ -directory, you can tell vagrant to 
apply the changes via Salt:
```
vagrant provision
```

Also if you pull changes from GitHub, you should probably run that command 
before trying to continue using the VM.


Building Windows .exe
=====================

To build the .exe for Windows use, you'll need a bit of extra help:

```
pip install cx_Freeze packaging
python setup.py build_exe
```


Qt UI Graphics attributions
===========================

Icons designed by [Freepik](http://www.flaticon.com/)

