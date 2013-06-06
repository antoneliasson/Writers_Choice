Writer's Choice README
======================
Writer's Choice is a simple blog-like Content Management System written in Python
using the [Pyramid][] web application framework. It presents "articles" and has a web
interface for creating and editing them. Articles are written and stored in
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
**Requirements:** Git, Python 3. I use Python 3.3. Older versions might work but are
not supported.

Create and activate a new [virtualenv][]. In this example we'll create a plain
virtualenv for simplicity, but you could also use virtualenvwrapper if you want.

    $ virtualenv wc
    $ cd wc && source bin/activate

Clone this repository containing the latest development version.

    $ git clone git@gitorious.org:writers-choice/writers-choice.git

Install dependencies from PyPI and execute some setup magic.
    
    $ python setup.py develop

There might be some build errors while installing the dependencies, which I think you
can safely ignore.

Pick a suitable sample configuration file (`development.ini` or `production.ini`) and
customize it according to the section Configuration below. In this example we'll
assume you use `development.ini`.  Run the magic script to initialize the database
with some sample data.

    $ initialize_Writers_Choice_db development.ini

Run the tests.

    $ python setup.py test -q

If you have `nose` and `coverage` installed you can use ut to check the project's
amazing test coverage.

    $ nosetests

Start the application using the included HTTP server.

    $ pserve --reload development.ini

[virtualenv]: http://www.virtualenv.org/en/latest/

Deploying a release to Heroku
-----------------------------
Releases are located in subdirectories in the `/dist` directory. Each release consists
of a tarball containing the code and a [requirements file][] that describes which
additional packages are needed and which versions that this particular release was
tested with. To create a release from Git, see the HACKING file.

To deploy a release to Heroku you will additionally need a
[Procfile][heroku-procfile], found in `/dist`, and a
[`runtime.txt`file][heroku-runtime-file], found in the project root. Either manually
extract these files from the tarball or download them from Git.

[requirements file]: http://www.pip-installer.org/en/latest/requirements.html
[heroku-procfile]: https://devcenter.heroku.com/articles/procfile "Process Types and the
Procfile | Heroku Dev Center"
[heroku-runtime-file]: https://devcenter.heroku.com/articles/python-runtimes "Specifying a
Python Runtime | Heroku Dev Center"

Configuration
-------------
