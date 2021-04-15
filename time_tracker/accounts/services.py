from .models import User



class UserServices:

    def get_queryset(self,filter_data):
        return User.objects.filter(**filter_data)

    def get_user_dropdown_queryset(self,filter_data=None):
        return User.objects.filter(**filter_data)
            
    def get_user(self,id):
        return User.objects.get(id=id)
