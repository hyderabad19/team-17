import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE','PracticeProject.settings')

import django
django.setup()

import random
from firstapp.models import User
from faker import Faker


def userInfo(n=5):
    fakegen = Faker()
    for i in range(n):
        ffirst_name = fakegen.name()
        llast_name = fakegen.name()
        eemail = fakegen.name()
        li = ['@gmail.com','@yahoo.com']
        eemail = eemail + random.choice(li)
        t = User.objects.get_or_create(first_name=ffirst_name,last_name=llast_name,email=eemail)[0]
        t.save()
if __name__ == '__main__':
    print("Doing Stuff")
    userInfo()
    print("End of doing Stuff")
