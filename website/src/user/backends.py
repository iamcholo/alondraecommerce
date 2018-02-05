from user.models import CustomUser
class CustomUserBackend(object):

    def authenticate(self, username=None, password=None): 
        try:
            user =  CustomUser.objects.get(username=username)
            
            if user.check_password(password):
                return user
        except CustomUser.DoesNotExist:
            return None

    def get_user(self, user_id):
        
        try:
            return CustomUser.objects.get(pk=user_id)
        except CustomUser.DoesNotExist:
            return None