from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.contrib.auth.tokens import default_token_generator

User = get_user_model()

class CustomerRegistrationSerializer(serializers.ModelSerializer):
    groups = serializers.SlugRelatedField(
        many=True,
        queryset=Group.objects.filter(name='Customer'),
        slug_field='name',
        required=False
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'middle_name', 'phone_number', 'address',
                  'lga', 'state', 'country', 'password', 'groups']
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def create(self, validated_data):
        email = validated_data['email']
        validated_data['username'] = email
        
        # Create the user without saving it
        user = User(**validated_data)
        user.is_active = False
        
        # Generate verification token
        token_generator = default_token_generator
        token = token_generator.make_token(user)
        print(token)
        
        user.save()  # Save the user before adding to groups
        
        group = Group.objects.get(name='Customer')
        user.groups.add(group)
        
        return user


class StaffRegistrationSerializer(serializers.ModelSerializer):
    groups = serializers.SlugRelatedField(
        many=True,
        queryset=Group.objects.filter(name='Staff'),
        slug_field='name',
        required=False
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'middle_name', 'phone_number', 'address',
                  'lga', 'state', 'country', 'password', 'groups']
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def create(self, validated_data):
        email = validated_data['email']
        validated_data['username'] = email
        user = User.objects.create_user(**validated_data)
        user.is_staff = True
        group = Group.objects.get(name='Staff')
        user.groups.add(group)
        return user



class LogoutSerializer(serializers.Serializer):
    refresh_token = serializers.CharField()

    def validate(self, attrs):
        refresh_token = attrs.get('refresh_token')

        if refresh_token:
            attrs['refresh_token'] = refresh_token
        else:
            raise serializers.ValidationError('Refresh token is required')

        return attrs
