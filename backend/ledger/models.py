from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
import datetime

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, first_name=None, last_name=None):
        if not email:
            raise ValueError('Users must have an email address')
        
        email_address = email
        normalized_email = self.normalize_email(email_address)
        
        user = self.model()
        user.email = normalized_email
        user.first_name = first_name
        user.last_name = last_name
        
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, first_name=None, last_name=None):
        if not email:
            raise ValueError('Users must have an email address')
        
        email_address = email
        normalized_email = self.normalize_email(email_address)
        
        user = self.model()
        user.email = normalized_email
        user.first_name = first_name
        user.last_name = last_name
        user.is_admin = True
        user.is_staff = True
        user.set_password(password)
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    email = models.CharField(max_length=255, unique=True)
    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    
    date_joined = models.DateTimeField(default=datetime.datetime.now)
    
    objects = UserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    def __str__(self):
        return self.email + " - " + str(self.first_name) + " " + str(self.last_name)
    
    def get_full_name(self):
        full_name = self.first_name + " " + self.last_name
        return full_name
    
    def get_short_name(self):
        return self.first_name
    
    def has_perm(self, perm, obj=None):
        return True
    
    def has_module_perms(self, app_label):
        return True
    
    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        db_table = 'users_table'


class LedgerItem(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    
    contents = models.TextField(max_length=1000)
    
    created_datetime = models.DateTimeField(default=datetime.datetime.now)
    
    is_deleted = models.BooleanField(default=False)
    item_id = models.AutoField(primary_key=True)
    
    def __str__(self):
        content_preview = ""
        if len(self.contents) > 50:
            for i in range(50):
                content_preview = content_preview + self.contents[i]
            content_preview = content_preview + "..."
        else:
            content_preview = self.contents
        
        return "Ledger Item #" + str(self.item_id) + " - " + content_preview
    
    def save(self, *args, **kwargs):
        print("Saving ledger item...")
        super(LedgerItem, self).save(*args, **kwargs)
        print("Ledger item saved!")
    
    def get_author_email(self):
        return self.author.email
    
    def get_author_name(self):
        return self.author.first_name + " " + self.author.last_name
    
    def get_contents(self):
        return self.contents
    
    def get_created_date(self):
        return self.created_datetime
    
    class Meta:
        verbose_name = 'Ledger Item'
        verbose_name_plural = 'Ledger Items'
        db_table = 'ledger_items_table'
        ordering = ['-created_datetime']