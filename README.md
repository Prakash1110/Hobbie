## Django E-Learning App

Static  contains static files(like css, js and media), templates contain the html pages. For further information visit [Django documentation](https://docs.djangoproject.com/en/3.2/). 

#### For further information on various .py files:

- admin.py file is used to display your models in the Django admin panel. You can also customize your admin panel.
- manage.py is Django’s command-line utility for administrative tasks, click [here](https://docs.djangoproject.com/en/3.2/ref/django-admin/) for more info
  feeds.py is used for creating RSS Feeds with Django, click [here](https://docs.djangoproject.com/en/3.2/ref/contrib/syndication/) for more info
- forms.py is used for creating custom forms through models, click [here](https://docs.djangoproject.com/en/3.2/topics/forms/) for more info
- models.py is the single, definitive source of information about your data, click [here](https://docs.djangoproject.com/en/3.2/topics/db/models/) for more info
- urls.py is used for handling urls on website, click [here](https://docs.djangoproject.com/en/3.2/topics/http/urls/) for more info
- views.py contains Python function **that takes a Web request and returns a Web response**, click [here](https://docs.djangoproject.com/en/3.2/topics/http/views/) for more info
- base.py contains the settings of the project through which the website runs, click [here](https://docs.djangoproject.com/en/3.2/topics/settings/) for more info
- wsgi.py contains calling convention for web servers to forward requests to web applications or frameworks written in the **Python** programming language. click [here](https://docs.djangoproject.com/en/3.2/howto/deployment/wsgi/) for more info



## Documentation



### Installation and configuration 

Clone the repository

Using the console, navigate to the root directory in which your projects live and clone this project's repository:

```bash
git clone git@github.com:getHarsh/getHarsh.git
cd getHarsh
// make your python virtualenv
virtualenv -p python3 virtualenv
source virtualenv/bin/activate
```

with virtualenv activated and inside the project directory

```
pip install -r requirements.txt
./manage.py migrate
./manage.py createsuperuser
./manage.py runserver
```
