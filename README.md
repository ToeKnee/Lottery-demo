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
* ./manage.py runserver
