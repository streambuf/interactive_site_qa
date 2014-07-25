from django.contrib.auth.backends import ModelBackend

from ask.models import User

class UserBackend(ModelBackend):
    def get_user(self, user_id):
        try:
            user = User.objects.get(pk = user_id)
            if user.is_active:
                return user
            return None
        except User.DoesNotExist:
            return None
