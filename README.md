Diabeaters
==========

Developed by the Columbia Center For New Media Teaching and Learning. 

Released under GPL2. 

Contact anders@columbia.edu, jonah@ccnmtl.columbia.edu, or
mjanelli@columbia.edu if you have more questions.

Installation
============

    git clone git://github.com/ccnmtl/Diabeaters.git diabeaters
    cd diabeaters
    ./bootstrap.py
    createdb diabeaters
    mkdir /var/www/diabeaters
    mkdir /var/www/diabeaters/uploads
    ./manage.py syncdb
    ./manage.py import_diabeaters
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
