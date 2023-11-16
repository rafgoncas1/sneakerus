from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

class EmailBackend(ModelBackend):
    def authenticate(self, email, password, **kwargs):
        UserModel = get_user_model()
        print(UserModel.objects.all())
        print(UserModel.objects.get(email=email))
        try:
            user = UserModel.objects.get(email=email)
            print(user.check_password(password))
        except UserModel.DoesNotExist:
            return None
        
        if user.check_password(password):
            return user
        return None
    
    def get_user(self, user_id):
        UserModel = get_user_model()
        try:
            return UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None