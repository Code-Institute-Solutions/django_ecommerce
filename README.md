# Django E-commerce

A small e-commerce app using Django 2

# Step by Step

*Note: Some steps may be slightly different depending on your OS/virtualenv choice. This assumes Ubuntu Linux and [virtualenvwrapper's mkproject](https://virtualenvwrapper.readthedocs.io/en/latest/command_ref.html#project-directory-management)*

**IMPORTANT: Throughout this document, `<venv_name>` refers to your root virtualenv directory (i.e. where `manage.py` lives), while `<project_name>` refers to the directory created by the initial `django-admin startproject` command (i.e. where `settings.py` lives). Be sure to create all your apps in the correct directories!**

---

### Initial Setup:

- Create a virtualenv/environment to work in

		mkproject -p python3 <venv_name>
- Install Django:
		
		pip install django
- Create a new Django project
		
		cd <venv_name>
		django-admin startproject <project_name> .
- Create `.gitignore`:

		touch <venv_name>/.gitignore
- Populate `.gitignore` w/ content:

		*.sqlite3
		*.pyc
		__pycache__
- Create `README.md`:

		touch README.md
- Test run: 

		cd <venv_name>
		python manage.py runserver

		# Visit http://127.0.0.1:8000, verify project is running
- Stop server and run initial migrations:

		ctrl+C
		python manage.py migrate

- Create superuser:

		python manage.py createsuperuser
		python manage.py runserver

		# Enter username, email, password
		# Visit http://127.0.0.0:8000/admin/, verify superuser login

- Initialize git and push initial commit:

		ctrl+C
		git init
		git add .
		git commit -m "initial commit"
		git remote add origin git@github.com:<username>/<repo_name>.git
		git push -u origin master

---

### Initial Authentication Setup with [django-allauth](https://django-allauth.readthedocs.io/en/latest):

- Install `django-allauth`:

		pip install django-allauth
- Update settings per [docs here](https://django-allauth.readthedocs.io/en/latest/installation.html) We're not using any social providers at this point. **Make sure to add `SITE_ID = 1`**
- Add allauth URLs to `<project_name>/urls.py`

		from django.urls import path, include

		urlpatterns = [
			# ...
			path('accounts/', include('allauth.urls')),
			# ...
		]

- Run allauth migrations:

		python manage.py migrate
- Run the server and navigate to http://127.0.0.1:8000/admin/sites/ and update the default example.com site:

		python manage.py runserver

		# Domain Name: 127.0.0.1:8000
		# Display Name: localhost
- Logout of the admin (so we can test login in a moment)
- Add additional allauth config in `settings.py`:

		# Additional django-allauth settings:

		AUTHENTICATION_BACKENDS = (
			# Needed to login by username in Django admin, regardless of `allauth`
			'django.contrib.auth.backends.ModelBackend',
			# `allauth` specific authentication methods, such as login by e-mail
			'allauth.account.auth_backends.AuthenticationBackend',
		)

		# Log emails to console in dev
		EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

		ACCOUNT_AUTHENTICATION_METHOD = 'username_email'
		ACCOUNT_EMAIL_REQUIRED = True
		ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
		ACCOUNT_SIGNUP_EMAIL_ENTER_TWICE = True
		ACCOUNT_USERNAME_MIN_LENGTH = 4
		LOGIN_URL = '/accounts/login/'
		LOGIN_REDIRECT_URL = '/'

		SITE_ID = 1
- Navigate to http://127.0.0.1:8000/accounts/login/ and login w/ the superuser. You'll be redirected to `/accounts/confirm-email/` if allauth is set up properly
- Navigate to http://127.0.0.1:8000/admin/ and login w/ the superuser
- Create an `EmailAddress` in the `ACCOUNTS` app in the admin, tied to your superuser's user ID (use the search icon) and mark it as `verified` and `primary`. The email itself doesn't matter, as long as it's not blank
- Logout of the admin again, navigate back to http://127.0.0.1:8000/accounts/login/ and login with the superuser again. Now you will get a 404 as allauth attempts to redirect you to `/` which currently has no URL
- Create allauth templates directory:

		mkdir <venv_name>/templates
		mkdir <venv_name>/templates/allauth
- Freeze requirements:

		pip freeze > <venv_name>/requirements.txt
- Commit:

		git add .
		git commit -m "initial allauth setup"
		git push

---

### Home App Setup:

- Create `home` app:
		
		cd <venv_name>
		python manage.py startapp home
- Add `home` app to `INSTALLED_APPS`
- Add root templates directory in settings.py:

		TEMPLATES = [
			{
				'BACKEND': 'django.template.backends.django.DjangoTemplates',
				'DIRS': [os.path.join(BASE_DIR, 'templates')],
				'APP_DIRS': True,
				...
			}
		]
- Create `home` templates directory:

		cd <venv_name>/home
		mkdir templates/ && mkdir templates/home/
- Create `home` views (see file in this repo)
- Create `home` urls (see file in this repo):
		
		touch <venv_name>/home/urls.py
- Create index template (see file in this repo):
	
		touch <venv_name>/home/templates/home/index.html
- Create base template (see file in this repo):

		touch <venv_name>/templates/base.html
- Include `home` urls in `<project_name>/urls.py`:

		urlpatterns = [
			# ...
			path('', include('home.urls')),
			# ...
		]
- Commit:

		git add .
		git commit -m "home app setup"
		git push

---

### Products App Setup:

- Create `products` app:
		
		cd <venv_name>
		python manage.py startapp products
- Add `products` app to `INSTALLED_APPS`
- Create `products` templates directory:

		cd <venv_name>/products
		mkdir templates/ && mkdir templates/products/
- Create `products` models (see file in this repo)
- Create `products` tests (see file in this repo)
- Create `products` views (see file in this repo)
- Create `products` urls (see file in this repo):
		
		touch <venv_name>/products/urls.py
- Create products template (see file in this repo):
	
		touch <venv_name>/products/templates/products/products.html
- Include `products` urls in `<project_name>/urls.py`:

		urlpatterns = [
			# ...
			path('products', include('products.urls')),
			# ...
		]
- Install `Pillow` for image uploads and freeze requirements:

		cd <venv_name>
		pip install pillow
		pip freeze > requirements.txt
- Make migrations and migrate `products` app:

		python manage.py makemigrations products
		python manage.py migrate products
- Commit:

		git add .
		git commit -m "products app setup"
		git push

---

### Cart App Setup:

- Create `cart` app:
		
		cd <venv_name>
		python manage.py startapp cart
- Add `cart` app to `INSTALLED_APPS`
- Create `cart` templates directory:

		cd <venv_name>/cart
		mkdir templates/ && mkdir templates/cart/
- Create `cart` contexts (see file in this repo)
- Create `cart` views (see file in this repo)
- Create `cart` urls (see file in this repo):
		
		touch <venv_name>/cart/urls.py
- Create cart template (see file in this repo):
	
		touch <venv_name>/cart/templates/cart/cart.html
- Include `cart` urls in `<project_name>/urls.py`:

		urlpatterns = [
			# ...
			path('cart', include('cart.urls')),
			# ...
		]
- Commit:

		git add .
		git commit -m "cart app setup"
		git push

---

### Search App Setup:

- Create `search` app:
		
		cd <venv_name>
		python manage.py startapp search
- Add `search` app to `INSTALLED_APPS`
- Create `search` templates directory:

		cd <venv_name>/search
		mkdir templates/ && mkdir templates/search/
- Create `search` views (see file in this repo)
- Create `search` urls (see file in this repo):
		
		touch <venv_name>/search/urls.py
- Include `search` urls in `<project_name>/urls.py`:

		urlpatterns = [
			# ...
			path('search', include('search.urls')),
			# ...
		]
- Commit:

		git add .
		git commit -m "search app setup"
		git push
