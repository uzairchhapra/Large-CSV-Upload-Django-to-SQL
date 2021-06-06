from django.conf import settings
from sqlalchemy import create_engine

DATABASES = getattr(settings, "DATABASES", {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'uploaddata',
        'USER': 'test',
        'PASSWORD': 'Abc@12345',
        'HOST': '208.91.198.197',   # Or an IP Address that your DB is hosted on
        'PORT': '3306',
    }
})

db = DATABASES['default']['NAME']
user = DATABASES['default']['USER']
passoword = DATABASES['default']['PASSWORD']
host = DATABASES['default']['HOST']
port = DATABASES['default']['PORT']


def getEngine():
    engine = create_engine(
        f"mysql+pymysql://{user}:{passoword}@{host}:{port}/{db}")
    return engine
