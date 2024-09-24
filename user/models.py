from django.db import models
from django.contrib.auth.models import  BaseUserManager, AbstractBaseUser, PermissionsMixin


class AllUser(BaseUserManager):
    def create_user(self, username, phone, password=None, first_name=None, last_name=None):
        if not phone:
            raise ValueError("Need Phone")
        
        if not username:
            raise ValueError("Need Username")
                
        if not first_name:
            raise ValueError("Need Name")
        
        if not last_name:
            raise ValueError("Need Family Name")

        user = self.model(
            phone=phone,
            username=username,
            first_name=first_name,
            last_name=last_name,
        )
        user.is_active = True
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staff(self, username, phone, password, first_name, last_name):
        user = self.create_user(
            phone=phone,
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name,
        )
        user.is_staff = True
        user.is_active  = True
        user.is_superuser = False        
        user.save(using=self._db)
        return user

    def create_superuser(self, username, phone, password, first_name, last_name):
        user = self.create_user(
            phone=phone,
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name,
        )
        user.is_staff = True
        user.is_active  = True
        user.is_superuser = True        
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    username     = models.CharField(max_length=11, unique=True)
    phone        = models.CharField(max_length=11, unique=True)
    first_name   = models.CharField(max_length=30, null=True, blank=True)
    last_name    = models.CharField(max_length=50, null=True, blank=True)
    is_active    = models.BooleanField(default=True, null=False)
    is_staff     = models.BooleanField(default=False, null=False)
    is_superuser = models.BooleanField(default=False, null=False)

    objects = AllUser()

    USERNAME_FIELD  = 'phone'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']
    
    def __str__(self):
        return f"{self.phone}"
    
    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True


class Profile(models.Model):
    user       = models.OneToOneField(User, on_delete=models.CASCADE)
    phone      = models.CharField(max_length=30)
    username   = models.CharField(max_length=30)
    first_name = models.CharField(max_length=30, null=True, blank=True)
    last_name  = models.CharField(max_length=50, null=True, blank=True)
    
    @property
    def fullName(self) -> str:
        return f"{self.first_name} {self.last_name}"
    
    def __str__(self) -> str:
        return f"{self.user.username}"
