from django.db import models
from django.contrib.auth.hashers import make_password, check_password
from faker import Faker
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone

fake = Faker()
fakeFarsi = Faker('fa_IR')

# Create your models here.
class Person(models.Model):
    first_name = models.CharField(max_length=50)
    farsi_name = models.CharField(max_length=50, blank=True, null=True)
    fb_id = models.CharField(max_length=100, unique=True, blank=True, null=True)
    father = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL)
    generation = models.IntegerField(blank=True, null=True)

    papa = models.IntegerField(blank=True, null=True)

    tree_width = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return f"{self.first_name} ({self.id})"

    def save(self, *args, **kwargs):
        if self.father:
            self.generation = self.father.generation + 1
        else:
            self.generation = 1
        super().save(*args, **kwargs)

class RenderedTree(models.Model):
    tree = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class VisitorInfo(models.Model):
    # Define your VisitorInfo model fields here
    # For example:
    ip_address = models.GenericIPAddressField(protocol='both')
    user_agent = models.TextField(blank=True, null=True)
    visited_at = models.DateTimeField(auto_now_add=True)

class Request(models.Model):
    request = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now, editable=False)

    def __str__(self):
        return f"{self.request} - {self.timestamp}"


class CustomUserManager(BaseUserManager):
    def create_user(self, username, password=None):
        if not username:
            raise ValueError('Users must have a username')

        user = self.model(username=username)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password):
        user = self.create_user(username, password=password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class Login(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=128, default="visitor", unique=True) 
    password = models.CharField(max_length=128)  # Adjust the max_length as needed

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    last_login = models.DateTimeField(auto_now=True)
    date_joined = models.DateTimeField(default=timezone.now)
    
    objects = CustomUserManager()

    USERNAME_FIELD = 'username'

    REQUIRED_FIELDS = []

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        # Hash the password before saving
        if not self.password.startswith('pbkdf2_sha256'):
            self.password = make_password(self.password)
        super(Login, self).save(*args, **kwargs)


# Generate example data
# for _ in range(100):
#     first_name = fake.first_name()
#     last_name = fake.last_name()
#     farsi_name = fakeFarsi.first_name() + " " + fakeFarsi.first_name()
#     fb_id = fake.uuid4()
#     gen = 1

#     # Create a person without a father for the first one
#     if _ == 0:
#         person = Person.objects.create(first_name=first_name, last_name=last_name, farsi_name=farsi_name, fb_id=fb_id, generation=1)
#     else:
#         # Randomly select a father from existing persons
#         father = random.choice(Person.objects.all())
#         gen = father.generation + 1
#         person = Person.objects.create(first_name=first_name, last_name=last_name, farsi_name=farsi_name, fb_id=fb_id, father=father, generation=(father.generation + 1))

#     print(f"Created person: {person.first_name} {person.last_name} (Father: {person.father}) -- Gen: "+str(gen))