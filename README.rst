mt-compono
----------

Minimalist content management system written for `La Mediatheque <http://www.lamediatheque.be>`_.


Requirements
------------

- `Python <http://www.python.org>`_ 2.x superior to 2.5 and Django
- `Django <http://www.djangoproject.org>`_  >= 1.1.1
- `Couchdbkit <http://www.couchdbkit.org>`_ >= 0.4.2
- `CouchDB <http://couchdb.apache.org>`_ >= 0.11

Installation
------------

Build Apache CouchDB
++++++++++++++++++++

Here we build Apache CouchDB in development mode. We use the trunk version 
waiting 0.11 is released::

	$ git clone git://github.com/benoitc/couchdb.git
	$ cd couchdb
	$ ./bootstrap
	$ ./configure && make && make dev
	
Launch couchdb :

  $ ./utils/run -a etc/couchdb/goldorak_dev.ini
	
Don't forget to install dependencies first : spidermonkey 1.7, icu4c & erlang. On debian/ubuntu systems do::

	$ apt-get install automake autoconf libtool help2man
	$ apt-get install build-essential erlang libicu-dev libmozjs-dev libcurl4-openssl-dev

Installation of Compono
+++++++++++++++++++++++

Install from sources::

  $ git clone git@github.com:benoitc/mt-compono
  $ python setup.py install

Configure your Django Project
-----------------------------

Here we will show what to edit in your settings file. First you need to add
`mt-compono` and `couchdbkit` to your lists of applications::

  INSTALLED_APPS = (
      ...
      'couchdbkit.ext.django',
      'mtcompono',
  )
  
And allow register the CouchDB database associated::

  COUCHDB_DATABASES = (
       ('mtcompono', "http://127.0.0.1:5984/yourdb"),
  )

Add the fallback middleware. .This middleware process unkown urls and send them back to compono:

  MIDDLEWARE_CLASSES = (
      ...
      'mtcompono.middleware.ComponoFallbackMiddleware',
  )

Then Edit your main `urls.py` file and add it to your pattern::

  urlpatterns = pattern('',
      ...
      url('^', include('mtcompono.urls')),
  )

that's it.

mtcompono media path
--------------------

If you want to serve mt-compono media (needed for its admin), copy the `mtcompono/media` folder where you want. You can even customize url by setting `MTCOMPONO_MEDIA_URL` in your settings file::

  MTCOMPONO_MEDIA_URL = '/media/mtcompono' # without trailing slash
  
In development you can configure the media root by settings `MTCOMPONO_MEDIA_ROOT`, but it's generally not needed.