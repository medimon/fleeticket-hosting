from rest_framework import serializers
from .models import Ticket
from .models import CustomUser


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id','username', 'first_name', 'last_name', 'email', 'role']

class TicketSerializer(serializers.ModelSerializer):
    userFr = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all())
    userDz = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all(), required=False, allow_null=True)
    # user = UserSerializer(read_only=True) 

    class Meta:
        model = Ticket
        fields = '__all__'



