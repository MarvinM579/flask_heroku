Flask Heroku
============

What is this?
-------------

A template to get your [Flask](http://flask.pocoo.org/) app running on
[heroku](https://www.heroku.com/) as fast as possible. For added
convenience, the templates use [`HTML5
Boilerplate`](https://github.com/paulirish/html5-boilerplate), and the
[`formalize`](http://formalize.me/) project's JavaScript and CSS is also
included to help make your forms more aesthetically pleasing.

All of the CSS stylesheets are written using the [Less
CSS](http://lesscss.org/) syntax, since I rarely write out my
stylesheets using vanilla CSS anymore. If you're using Mac OS X for
development, make sure to check out [incident57's
Less.app](http://incident57.com/less/).


Why should I use this?
----------------------

Everything I've learned from writing and maintaining the [Flask
Engine](https://github.com/zachwill/flask-engine) template for Google
App Engine has made its way into this repo, too. The goal is to make a
simple repo that can be cloned and added to for the majority of projects
going forward, while also staying minimal in size and complexity.


Instructions
------------

First, you'll need to clone the repo.

    $ git clone git@github.com:zachwill/flask_heroku.git
    $ cd flask_heroku

Second, let's download `pip`, `virtualenv`, and the [`heroku` Ruby
gem](http://devcenter.heroku.com/articles/using-the-cli).

    $ sudo easy_install pip
    $ sudo pip install virtualenv
    $ gem install heroku

Now, you can setup an isolated environment with `virtualenv`.

    $ virtualenv --no-site-packages env
    $ source env/bin/activate

Then, let's get the requirements installed in your isolated test
environment.

    $ pip install -r requirements.txt

Now, you can run the application locally.

    $ python bootstrap.py

Or, to test the production configuration, simply run:

    $ python bootstrap.py --gevent

If you haven't [signed up for heroku](https://api.heroku.com/signup), go
ahead and do that. You should then be able to [add your SSH key to
heroku](http://devcenter.heroku.com/articles/quickstart), and also
`heroku login` from the commandline.

Now, to upload your application, you'll first need to do the
following:

    $ heroku create --stack cedar
    $ git push heroku master

This should return a URL, and you can then view your application in
your web browser of choice.

And, to deactivate `virtualenv` (once you've finished coding), you
simply run the following command:

    $ deactivate


Reactivating the Virtual Environment
------------------------------------

If you haven't worked with `virtualenv` before, you'll need to
reactivate the environment everytime you close or reload your terminal.

    $ source env/bin/activate

If you don't reactivate the environment, then you'll probably receive a
screen full of errors when trying to run the application locally.


Adding Requirements
-------------------

In the course of creating your application, you may find yourself
installing various Python modules with `pip` -- in which case you'll
need to update the `requirements.txt` file. One way that this can be
done is with `pip freeze`.

    $ pip freeze > requirements.txt