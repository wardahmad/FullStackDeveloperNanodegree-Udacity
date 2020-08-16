$ which heroku
$ heroku login
$ python -m pip freeze > requirements.txt
$ touch setup.sh
$ touch Procfile

$ python -m pip install flask_script
$ python -m pip install flask_migrate
$ python -m pip install psycopg2-binary

$ touch manage.py

$ python manage.py db init
$ python manage.py db migrate
$ python manage.py db upgrade
$ python -m pip freeze > requirements.txt

$ heroku create name_of_your_app

$ git remote add heroku heroku_git_url
$ heroku addons:create heroku-postgresql:hobby-dev --app name_of_your_application
$ heroku config --app name_of_your_application

$ git push heroku master
$ heroku run python manage.py db upgrade --app name_of_your_application

$ FLASK_APP=app.py FLASK_DEBUG=true flask run
$ python test_app.py

$ heroku open
$ heroku config

https://pypi.org/project/autopep8/
$ python -m $ pip install --upgrade autopep8
--To modify a file in place (with aggressive level 2):--
$ autopep8 --in-place --aggressive --aggressive <filename>