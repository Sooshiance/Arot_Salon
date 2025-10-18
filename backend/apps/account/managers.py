from django.contrib.auth.models import BaseUserManager


class AllUser(BaseUserManager):
    def create_user(
        self,
        username,
        email,
        phone,
        password=None,
        **kwargs,
    ):
        """"""
        if not username:
            raise ValueError("Need Username")
        
        if not email:
            raise ValueError("Need Email")
        
        if not phone:
            raise ValueError("Need Phone")

        user = self.model(
            username=username,
            email=self.normalize_email(email),
            phone=phone,
            **kwargs,
        )
        user.is_active = True
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staff(
        self,
        username,
        email,
        phone,
        password,
    ):
        """"""
        user = self.create_user(
            username,
            email,
            phone,
            password=password,
        )
        user.is_staff = True
        user.is_active = True
        user.is_superuser = False
        user.save(using=self._db)
        return user

    def create_superuser(
        self,
        username,
        email,
        phone,
        password,
    ):
        """"""
        user = self.create_user(
            username,
            email,
            phone,
            password=password,
        )
        user.is_staff = True
        user.is_active = True
        user.is_superuser = True
        user.save(using=self._db)
        return user
