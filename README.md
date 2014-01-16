Writer's Choice README
======================

Writer's Choice is a simple blog-like Content Management System written in
Python using the [Pyramid][] web application framework. It presents "articles"
and has a web interface for creating and editing them. Articles are written and
stored in [Markdown][] and are automatically compiled to HTML for presentation.

It uses SQLAlchemy as the persistent storage mechanism. Currently SQLite and
PostgreSQL are supported as database backends.

There is a simple authentication mechanism to allow only a privilegied user to
add and edit articles. Authentication is implemented using Mozilla [Persona][]
which allows for password free logins.

[pyramid]: https://pyramid.readthedocs.org/
[markdown]: https://daringfireball.net/projects/markdown/
[persona]: https://persona.org/

Setting up for development
--------------------------

**Requirements:** Git, Python 3. I use Python 3.3. Older versions might work but
are not supported.

Create and activate a new [virtualenv][]. In this example we'll create a plain
virtualenv for simplicity, but you could also use [virtualenvwrapper][] if you
want. Using virtualenvwrapper is actually what I recommend if you have more than
one or two virtualenv's on your system.

    $ virtualenv wc-dev
    $ cd wc-dev
	$ source bin/activate

Clone this repository to get the latest development version.

    $ git clone git@gitorious.org:writers-choice/writers-choice.git
    $ cd writers_choice

Install dependencies from PyPI and execute some setup magic.
    
    $ python setup.py develop

Pick a suitable sample configuration file (`development.ini` or
`production.ini`) and customize it according to the section
[Configuration](#configuration "Configuration") below. In this example we'll
assume `development.ini`.  Run the magic script to initialize the database with
the tables and some sample data.

    $ initialize_Writers_Choice_db development.ini

Run the tests.

    $ python setup.py test -q

With Pyramid 1.5 and pyramid_chameleon 0.1 the tests prints a deprecation
warning, which you may ignore for now.

If you want to see the project's amazing test coverage, install the `nose` and
`coverage` packages and run `nosetests`.

    $ pip install nose coverage
    $ nosetests

Start the application using Pyramid's included HTTP server [waitress][].

    $ pserve --reload development.ini

[virtualenv]: http://www.virtualenv.org/en/latest/
[virtualenvwrapper]: http://virtualenvwrapper.readthedocs.org/
[waitress]: http://docs.pylonsproject.org/projects/waitress/

Configuration
-------------

The application is configured using a [Paste Deploy file][]. Two sample files
are shipped with the application: `development.ini` and
`production.ini`. `development.ini` is suitable for development because it
enables a debug toolbar with some fancy monitoring tools. `production.ini` on
the other hand is suitable for production because it disables said tools, which
makes the application faster and more secure. The most interesting settings that
a user of this application would probably want to configure are described below.

### sqlalchemy.url

This is a URL that describes how SQLAlchemy should connect to the database. For
PostgreSQL the format is `postgres://username:password@db_host/db_name`.  This
uses the default *DBAPI driver* [psycopg2][]. Others are available and might
work but are not tested.

For SQLite the format is `sqlite:///%(here)s/filename.sqlite` where `%(here)`
expands to the path of the directory containing the configuration file.

### debugtoolbar.hosts

When running in development mode, this specifies which hosts are allowed to use
the debug toolbar. Because the debug toolbar allow the user to execute arbitrary
Python code, this is by default set to localhost only.

Protip: When developing on a remote machine you can leave this to default value
and use SSH tunnels to route the HTTP requests from your client machine through
the remote so that it looks to the application like they are coming from
localhost. That way you don't have to open the server to the Internet.

### site_name

Shown in the HTML title and in the big header.

### admin_email

This is the e-mail address that the site administrator logs in with. Anyone can
authenticate with Persona but the administrator is the only user that actually
gains some privilegies from it.

### persona.secret

A string used as the cryptographic signing key for the cookies. This is the only
thing that prevents anyone from impersonating anyone on the site (including the
admin) so it must be kept secret. I have no idea how long it can or should be
but 64 alphanumeric characters seems to work for my installation.

### persona.audiences

The URL(s), separated by a space, of your web app. This is a requirement for
Persona to be secure and must be hard-coded in the configuration. If this field
is blank (and the underlying library would have allowed it to be, which it
doesn't), another website that the user has previously logged in to using
Persona could reuse their identity assertions on your site, effectively
impersonating the poor user.

Protocol (HTTP/HTTPS) and port (default 80) matters. This is one reason for an
application to have several URLs.

### persona.siteName

Optional. A site name to present to the user during login.

### [server:main] host

Which hostname or IP address the HTTP server should listen on. Defaults to
0.0.0.0 (all IP addresses on this host).

### [server:main] port

Which port the HTTP server should listen on. Can be an integer, or a placeholder
if you don't know it until the application is started (as is the case with
Heroku). In that case you can set the port to:

    port = %(http_port)s

and then run the application like this:

    $ pserve production.ini http_port=6543

[paste deploy file]: http://pythonpaste.org/deploy/
[psycopg2]: http://docs.sqlalchemy.org/en/rel_0_8/dialects/postgresql.html#module-sqlalchemy.dialects.postgresql.psycopg2

Bugs and limitations
====================

Important bugs in the latest release that are subjectively really important.

* There is no way to edit pages. Sorry about that. You'll have to talk to the
  database manually for now.

* MySQL works as database backend for some providers but not for others since
  the application doesn't handle lost connections. This may not be a problem for
  busy apps or apps using a self-hosted MySQL server but since for example
  ClearDB has a timeout of 80 seconds and my app is very unbusy this doesn't
  work in my use case. PostgreSQL seems to work better. It also seems to have
  better support in Python in general.
  
  Because of this, PostgreSQL is "officially supported" from Writer's Choice
  version 1.2 and later and MySQL is no longer supported.

* Trailing newlines in the article body get removed when the article is
  saved. This could be fixed without too much work but since keeping trailing
  newlines isn't really a feature I'm letting this pass for the time being.

* Requirements are a bit bloated. Not all of them are required for running the
  app. Some are only used for development, testing or not at all.
