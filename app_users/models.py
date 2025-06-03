from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.timezone import now
from app_persons.models import Person


class User(AbstractUser):
    code = models.CharField(max_length=50, null=True, blank=True)
    person = models.ForeignKey(
        Person, on_delete=models.CASCADE, related_name='users')
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_set',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_set',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )

class Audit(models.Model):
    action = models.CharField(max_length=255)
    service = models.CharField(max_length=255)
    model = models.CharField(max_length=255)
    instance = models.TextField()
    description = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='audit_user', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        user = self.user.username if self.user else None
        return f'{self.id}-USER:{user}-ACTION:{self.action}-SERVICE:{self.service}-MODEL:{self.model}'

class Module(models.Model):
    name = models.CharField(max_length=255)
    url = models.URLField(null=True, blank=True)
    background = models.ImageField(upload_to='background/', null=True, blank=True)
    icon = models.ImageField(upload_to='icon/', null=True, blank=True)
    is_active = models.BooleanField(default=True, null=True, blank=True)

    def __str__(self):
        return f'{self.id}-NAME:{self.name}'

    @staticmethod
    def token_is_valid(token):
        return Module.objects.filter(uuid=token, is_active=True).exists()

    class Meta:
        db_table = 'modules_user'

class SectionMenu(models.Model):
    module = models.ForeignKey('Module', on_delete=models.CASCADE, related_name='section_menu_module')
    name = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.id}-NAME:{self.name}'

    class Meta:
        db_table = 'section_menu_user'

class Menu(models.Model):
    section = models.ForeignKey('SectionMenu', on_delete=models.CASCADE, related_name='menu_section')
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    icon = models.TextField(null=True, blank=True, max_length=1000)
    url = models.CharField(max_length=255, null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.id} - NAME:{self.name}'

    class Meta:
        db_table = 'menu_user'

class SubMenu(models.Model):
    menu = models.ForeignKey('Menu', on_delete=models.CASCADE, related_name='submenu_menu')
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    icon = models.TextField(null=True, blank=True, max_length=1000)
    url = models.CharField(max_length=255, null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.id}-NAME:{self.name}'

    class Meta:
        db_table = 'submenu_user'

class UserRole(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='user_role_user')
    module = models.ForeignKey('Module', on_delete=models.CASCADE, related_name='user_role_module')
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.id} - USER:{self.user.username} - MODULE:{self.module.name}'

    class Meta:
        db_table = 'user_role_user'
        unique_together = ('user', 'module')

class UserAccess(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='user_access_user')
    menu = models.ForeignKey('Menu', on_delete=models.CASCADE, related_name='user_access_menu')
    sub_menu = models.ForeignKey('SubMenu', on_delete=models.CASCADE, related_name='user_access_submenu', null=True,
                                 blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.id}-USER:{self.user}-MENU:{self.menu}-SUBMENU:{self.sub_menu}'

    class Meta:
        db_table = 'user_access_user'

class ActionCode(models.Model):
    name = models.CharField(max_length=250)
    subject = models.CharField(max_length=250)
    message = models.TextField(null=True,blank=True)
    html = models.TextField(null=True,blank=True)
    is_active = models.BooleanField(default=True)
    error_message = models.TextField(max_length=500, null=True,blank=True)
    must_exist = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.id}-NAME:{self.name}-ESTADO:{self.is_active}'

    class Meta:
        db_table = 'action_code_user'

class AccessCode(models.Model):
    email = models.EmailField(null=True, blank=True)
    cellphone = models.CharField(max_length=12, null=True, blank=True)
    code = models.TextField(max_length=300)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    action = models.ForeignKey('ActionCode',on_delete=models.CASCADE, related_name='access_code_accion', null=True, blank=True)

    def is_valid(self):
        return now() < self.expires_at

    def __str__(self):
        return f'{self.id}-CODE:{self.code}-CREATED:{self.created_at}-EXPIRES:{self.expires_at}'

    class Meta:
        db_table = 'access_code_user'