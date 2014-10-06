Lottery-demo
============

Getting started
---------------

* git clone git@github.com:ToeKnee/Lottery-demo.git
* cd Lottery-demo
* virtualenv env
* source env/bin/activate
* pip install -r requirements.txt
* cd src
* ./manage.py collectstatic --link --noinput
* ./manage.py compress  # Or change COMPRESS_OFFLINE to False
* ./manage.py migrate
* ./manage.py test
* ./manage.py createsuperuser
* ./manage.py runserver

Usage
-----

After creating an admin user, log-in and create a Lottery.  If the
lottery is active and the dates are appropriate, it will show up on
the home page and /lottery page.

There is currently no register or log-in page, so it all has to be
done through the admin.


Other info
----------

You can override any setting by creating a local_settings.py file.
