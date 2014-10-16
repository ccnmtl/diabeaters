Diabeaters
==========

[![Build Status](https://travis-ci.org/ccnmtl/diabeaters.png)](https://travis-ci.org/ccnmtl/diabeaters)

Developed by the Columbia Center For New Media Teaching and Learning. 

Released under GPL2. 

Contact anders@columbia.edu, jonah@ccnmtl.columbia.edu, or
mjanelli@columbia.edu if you have more questions.

Quickstart Installation
============
    # These installation notes are abridged.
    # They assume you have a database configured and running
    # Please modify settings_shared.py for alternative configurations

    git clone git://github.com/ccnmtl/Diabeaters.git diabeaters
    cd diabeaters
    ./bootstrap.py
    createdb diabeaters # create a postgres database instance. 
    mkdir /var/www/diabeaters
    mkdir /var/www/diabeaters/uploads
     # will also import the fixtures, which include the project's flat pages
    ./manage.py syncdb
    # imports the diabeaters site content
    ./manage.py import_diabeaters 
    # for a development installation. See the django docs and this project's apache/ dir for production deployment 
    ./manage.py runserver  

Content Import
==============

From a running site, visit /import in the browser and upload a zip
file which was provided by an export from another Dieabeaters site.

Content Export
==============

From a running site, visit /export in the browser.  A zip file will be
downloaded which you can upload to another Diabeaters site to import
all the content and site structure.
