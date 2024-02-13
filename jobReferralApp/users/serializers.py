from rest_framework import serializers
from users.models import User
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'password', 'email', 'is_employer', 'is_applicant', 'phoneNumber', 'avatar']
        extra_kwargs = {
            'password': {
                'write_only': True
            }
        }