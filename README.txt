Writer's Choice README
======================
Writer's Choice is a simple blog-like Content Management System written in Python
using the [Pyramid][] web application framework. It presents "articles" and has a
web interface for creating and editing them. Articles are written and stored in
[Markdown][] and are automatically compiled to HTML for presentation.

It uses SQLAlchemy as the persistent storage mechanism. Currently SQLite and MySQL
are supported as database backends.

There is a simple authentication mechanism to allow only a privilegied user to add
and edit articles. Authentication is implemented using Mozilla [Persona][] which
allows for password free logins.

[pyramid]: https://pyramid.readthedocs.org/
[markdown]: https://daringfireball.net/projects/markdown/
[persona]: https://persona.org/

Setting up for development
--------------------------
**Requirements:** Git, Python 3. I use Python 3.3. Older versions might work but
are not supported.

Create and activate a new [virtualenv][]. In this example we'll create a plain
virtualenv for simplicity, but you could also use virtualenvwrapper if you want.

    $ virtualenv wc-dev
    $ cd wc-dev
	$ source bin/activate

Clone this repository containing the latest development version.

    $ git clone git@gitorious.org:writers-choice/writers-choice.git

Install dependencies from PyPI and execute some setup magic.
    
    $ python setup.py develop

There might be some build errors while installing the dependencies, which I think
you can safely ignore.

Pick a suitable sample configuration file (`development.ini` or `production.ini`)
and customize it according to the section Configuration below. In this example
we'll assume you use `development.ini`.  Run the magic script to initialize the
database with the tables and some sample data.

    $ initialize_Writers_Choice_db development.ini

Run the tests.

    $ python setup.py test -q

If you have `nose` and `coverage` installed you can use ut to check the project's
amazing test coverage.

    $ nosetests

Start the application using the included HTTP server.

    $ pserve --reload development.ini

[virtualenv]: http://www.virtualenv.org/en/latest/

Configuration
-------------
The application is configured using a [Paste Deploy file][]. Two sample files are
available in the repo: `development.ini` and `production.ini`. `development.ini` is
suitable for development because it enables a debug toolbar with some fancy
monitoring tools. `production.ini` on the other hand is suitable for production
because it disables said tools, which makes the application faster and more
secure. The most interesting settings that a user of this application would
probably want to configure are described below.

### sqlalchemy.url
This is a URL that describes how SQLAlchemy should connect to the database. For
MySQL the format is `mysql+mysqlconnector://username:password@db_host/db_name`
where `mysqlconnector` is a particular type of driver that communicates with the
database host. Other drivers might work but `mysqlconnector` is the recommended
one.

For SQLite the format is `sqlite:///%(here)s/filename.sqlite` where `%(here)`
expands to the path of the directory containing the configuration file.

### debugtoolbar.hosts
When running in development mode, this specifies which hosts are allowed to use the
debug toolbar. By default this is only localhost.

Protip: When developing on a remote machine you can leave this to default and use
SSH tunnels to route the HTTP requests from your client machine through the remote
so that it looks to the application like they are coming from localhost.

### site_name
Shown in the HTML title and in the big header.

### admin_email
This is the e-mail address that the site administrator logs in with. Anyone can
authenticate with Persona but the administrator is the only user that actually
gains some privilegies from it.

### persona.secret
A string used as the cryptographic signing key for the cookies. This is the only
thing that prevents anyone from impersonating anyone on the site (including the
admin) so it must be kept secret. I have no idea how long it can or should be but
64 alphanumeric characters seems to work for my installation.

### persona.audiences
The URL(s), separated by a space, of your web app. This is a requirement for
Persona to be secure and must be hard-coded in the configuration. If this field is
blank (and the underlying library would have allowed it to be, which it doesn't),
another website that the user has previously logged in to could reuse their
identity assertions on your site, effectively impersonating a user.

Protocol (HTTP/HTTPS) and port (default 80) matters. This is one reason for an
application to have several URLs.

### persona.siteName
Optional. A site name to present to the user during login.

### [server:main] host
Which hosts the HTTP server should respond to. Defaults to 0.0.0.0 (everyone).

### [server:main] port
Which port the HTTP server should listen on. Can be an integer, or a placeholder if
you don't know it until the application is started (as is the case with Heroku). In
that case you can set the port to:

    port = %(http_port)s

and then run the application like this:

    pserve production.ini http_port=6543

[paste deploy file]: http://pythonpaste.org/deploy/
