Deploying a release
===================

Releases are located in the `/dist` directory. For instructions on how to create
a release from Git, see the HACKING file. To install all the projects required
dependencies, manually extract the `requirements.txt` file from the tarball of
your choice.

Deploying to Heroku
-------------------

To deploy a release to [Heroku][] you will additionally need a
[Procfile][heroku-procfile], found in `/dist`, a
[`requirements.txt` file][requirements file] and a
[`runtime.txt` file][heroku-runtime-file], both found in the project
root. Either manually extract these files from the tarball or download them from
the Git repository.

Because Heroku apps use an [ephemeral filesystem][], it is not possible to use
SQLite for the database backend. Changes to the database would be lost every
time the app is restarted.

**Requirements:** [Heroku Toolbelt][]. Access to a supported external database service.

This is an adaptation of
[Heroku's getting started guide][heroku-getting-started-with-python].

First you need to log in to your Heroku account using the client.

    $ heroku login

Copy the required files mentioned earlier to some directory and cd to it. The
result might look like this:

    $ ls
    Procfile  runtime.txt  Writers_Choice-1.0.tar.gz

You will also need a configuration file for the project. As a sample
`production.ini` from the tarball can be used. Customize it according to the
[Configuration](README.html#configuration) section in the README.

Create and activate a new virtualenv.

    $ virtualenv venv
    $ source venv/bin/activate

Initialize a new Git repo in this directory. Add the project files and commit.

    $ git init
    $ git add Procfile production.ini requirements.txt runtime.txt Writers_Choice-1.0.tar.gz 
    $ git commit

Create a new Heroku application. This sets up a new Git remote that you can push
to to update the app.

    $ heroku create --region eu

Push your new application. This will take a few minutes as it triggers the
Heroku machine to download and install all the project's dependencies.

    $ git push heroku master

After the installation is finished the app should start automatically. Before
you can use it you need to initialize the database. One way is to use a
[one-off dyno][heroku-one-off-dyno] to execute the initialization script:

    $ heroku run initialize_Writers_Choice_db production.ini   

This completes the deployment process.

[heroku]: https://www.heroku.com/
[requirements file]: http://www.pip-installer.org/en/latest/requirements.html
[heroku-procfile]: https://devcenter.heroku.com/articles/procfile "Process Types and the Procfile | Heroku Dev Center"
[heroku-runtime-file]: https://devcenter.heroku.com/articles/python-runtimes "Specifying a Python Runtime | Heroku Dev Center"
[ephemeral filesystem]: https://devcenter.heroku.com/articles/dynos#ephemeral-filesystem
[heroku toolbelt]: https://toolbelt.heroku.com/
[heroku-getting-started-with-python]: https://devcenter.heroku.com/articles/python
[heroku-one-off-dyno]: https://devcenter.heroku.com/articles/one-off-dynos "One-Off Dynos | Heroku Dev Center"
