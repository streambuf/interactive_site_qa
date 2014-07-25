from django.db import models
from django.core.mail import send_mail
from django.utils import timezone
from django.utils.translation import gettext as _
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser

class UserManager(BaseUserManager):
	def create_user(self, email, password = None, **kwargs):
		if not email:
			raise ValueError(_('Users must have an email address'))
 
		user = self.model(
			email = UserManager.normalize_email(email),
			**kwargs
		)
 
		user.set_password(password)
		user.save(using = self._db)
		return user
 
	def create_superuser(self, email, password, **kwargs):
		user = self.create_user(email,
			password = password,
			**kwargs
		)
		user.is_admin = True
		user.save(using = self._db)
		return user

class User(AbstractBaseUser):
	username = models.CharField(max_length=25, unique = True)
	email = models.CharField(max_length=75, unique = True)
	reg_date = models.DateTimeField(_('reg_date'), default=timezone.now)
	user_rating = models.IntegerField(default='0')
	avatar = models.ImageField(upload_to='avatars', default='avatars/default.png')
	is_active = models.BooleanField(default = True, verbose_name = _('is active'))
	is_admin = models.BooleanField(default = False, verbose_name = _('is admin'))
	def __unicode__(self):  
		if self.avatar is None:
			return "None"
		elif self.avatar.name is None:
			return "None"
		else:
			return self.avatar.name		
		
	USERNAME_FIELD = 'username'

	REQUIRED_FIELDS = [
		'email', 'password',
	]
	
	objects = UserManager()
    
	def get_absolute_url(self):
		return "/users/%s/" % urlquote(self.email)
 
	def get_short_name(self):
		return self.username
 
	def email_user(self, subject, message, from_email=None):
		send_mail(subject, message, from_email, [self.email])
	
	def has_perm(self, perm, obj=None):
		return True
 
	def has_module_perms(self, app_label):
		return True
 
	@property
	def is_staff(self):
		return self.is_admin	
 
	class Meta:
		verbose_name = _('user')
		verbose_name_plural = _('users')
