import factory
from django.conf import settings


class UserFactory(factory.DjangoModelFactory):
    FACTORY_FOR = settings.AUTH_USER_MODEL

    first_name = 'Joe'
    last_name = 'Bloggs'
    username = factory.LazyAttributeSequence(lambda a, n: '{0}-{1}-{2}'.format(a.first_name, a.last_name, n).lower())
    email = factory.LazyAttributeSequence(lambda a, n: '{0}+{1}@example.com'.format(a.username, n).lower())
    is_active = True

    @classmethod
    def _prepare(cls, create, **kwargs):
        password = kwargs.pop('password', None)
        user = super(UserFactory, cls)._prepare(create, **kwargs)
        if password:
            user.set_password(password)
            if create:
                user.save()
        return user


class AdminFactory(UserFactory):
    is_staff = True
    is_superuser = True
    is_active = True
