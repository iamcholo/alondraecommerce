from user_site import get_user_model
class UserSiteBackend(object):

    def authenticate(self, email=None, password=None):
        UserModel = get_user_model()

        if email is None:
            email = kwargs.get(UserModel.USERNAME_FIELD)

        try:
            user =  UserModel.objects.get(email=email)
            
            if user.check_password(password):
                return user
        except UserModel.DoesNotExist:
            UserModel().set_password(password)

    def get_user(self, user_id):
        UserModel = get_user_model()
        
        try:
            return UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None