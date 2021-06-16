"""
Django settings for app project.

Generated by 'django-admin startproject' using Django 2.2.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os
import environ

# environ.Env.read_env() -> set .env file
env = environ.Env()

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SMS_FOR_DJANGO_SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Django site에서 처리할 수 있는 host/domain 이름들을 표현하는 문자열 리스트
ALLOWED_HOSTS = []


# Application definition

# Django에서 사용하기 위해 설치된 모든 어플리케이션들의 목록
# python3 manage.py migrate 실행 시, 아래의 리스트로부터 필요한 db table를 조회해온 후 생성한다.
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'users.apps.UsersConfig',
    'postgres_composite_types',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# ROOT_URLCONF -> 최상위 URLconf를 정의하고 있는 모듈의 전체 임포트 경로.
#                 middleware에 의해 HttpRequest에 urlconf 속성이 설정된 경우, 해당 값이 ROOT_URLCONF 값을 대체함.
# ROOT_URLCONF와 연결된 모든 URLconf에서 urlpatterns의 path 탐색 후, 첫 번쨰로 매칭 성공한 path에 대해 path_info와 일치시킴.
# 그 후, view에 HttpRequest 객체, URL pattern 표현식에 해당하는 값들을 건내어 요청 처리를 위임함.
# 매칭된 URL pattern이 존재하지 않거나 매칭 중 예외가 발생한다면, 404가 발생하며 기본 error handling view가 실행되며, 따로 처리할 수도 있음.
ROOT_URLCONF = 'app.urls'

# Django에서 사용할 모든 template engines에 대한 설정들을 포함하고 있는 리스트. 모든 요소는 각각의 engine에 대한 설정을 담고 있는 딕셔너리다.
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',  # 사용할 template backend
        'DIRS': [os.path.join(BASE_DIR, "templates")],  # engine이 꼭 확인해야 하는 template source files directory
        'APP_DIRS': True,  # INSTALLED_APPS 내의 모든 template source files 들을 찾아보게 할건지
        'OPTIONS': {  # template이 request로부터 render될 때 사용되는 callable 객체의 경로. request object를 받은 후 병합할 context dict를 반환함.
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'app.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

# django에서 사용할 데이터베이스에 대한 설정 정보를 포함하는 딕셔너리.
# 기본 사용인 default는 구성되어야 하고, PostgreSQL, MySQL, MariaDB, Oracle 등 여러 유형의 데이터베이스 설정 또한 동시에 추가로 설정할 수 있다.
# 설정 값에 대한 자세한 정보는 https://docs.djangoproject.com/en/2.2/ref/settings/#databases에서 확인할 수 있다.
DATABASES = {
    'default': {
        'NAME': env('SMS_FOR_DJANGO_POSTGRESQL_NAME'),
        'ENGINE': 'django.db.backends.postgresql',
        'USER': env('SMS_FOR_DJANGO_POSTGRESQL_USER'),
        'PASSWORD': env('SMS_FOR_DJANGO_POSTGRESQL_PASSWORD'),
        'HOST': '127.0.0.1',
        'PORT': '5432',
    },

    'sqlite3': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

# TIME_ZONE -> datetime 등 시간과 관련된 여러 상황에서 사용할 표준 시간대
#              USE_TZ이 False이면, 해당 시간대를 강제적으로 django datatime와 관련된 모든 시간대에 사용되게 하고,
#              USE_TZ이 True면 template 및 form에 입력한 날짜를 해석할 때만 사용되는 시간대이다. (그 외에는 native 로컬 시간대를 사용)
TIME_ZONE = 'Asia/Seoul'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'

# STATICFILES_FINDERS는 다양한 위치에서 static file들을 찾는 방법을 정의하는 여러 finder의 리스트이다.
STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',  # STATICFILES_DIRS라는 설정 값에 지정된 리스트들에서 검색
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',  # INSTALLED_APPS에 설정된 각 app들의 static 하위 디렉토리에서 검색
]

# APPEND_SLASH = True -> url이 /로 끝나지 않고 모든 URLconf와 매칭되지 않는 경우, 끝에 /를 붙힌 후 리다이렉 함. (데이터 분실 위험 존재)
# CommonMiddleware라는 middleware가 설치되어있을 때만 사용된다 함.
APPEND_SLASH = False
