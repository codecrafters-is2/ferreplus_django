from django.contrib.auth.models import Group

def create_groups():
    Group.objects.get_or_create(name='admi')
    Group.objects.get_or_create(name='client')
    Group.objects.get_or_create(name='employee')

if __name__ == '__main__':
    create_groups()
