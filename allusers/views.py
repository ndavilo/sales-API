from rest_framework import generics, permissions
from .serializers import CustomerRegistrationSerializer, StaffRegistrationSerializer, LogoutSerializer
from rest_framework_simplejwt.tokens import BlacklistedToken, OutstandingToken
from rest_framework import status
from rest_framework.response import Response
from django.db import IntegrityError
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import get_user_model
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.generics import UpdateAPIView
from rest_framework.permissions import IsAuthenticated

class CustomerRegistrationAPIView(generics.CreateAPIView):
    serializer_class = CustomerRegistrationSerializer
    permission_classes = [permissions.AllowAny]  # Customize permissions if needed

class StaffRegistrationAPIView(generics.CreateAPIView):
    serializer_class = StaffRegistrationSerializer
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]  # Customize permissions if needed


from rest_framework import generics

class LogoutView(generics.GenericAPIView):
    serializer_class = LogoutSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        refresh_token = serializer.validated_data['refresh_token']

        # Add the token to the blacklist
        try:
            outstandingToken = OutstandingToken.objects.get(token=refresh_token)
            blacklistedToken = BlacklistedToken.objects.create(token=outstandingToken)
            blacklistedToken.save()
            return Response({"detail": "Logout successful"}, status=status.HTTP_200_OK)
        except OutstandingToken.DoesNotExist:
            return Response({"detail": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)
        except IntegrityError:
            return Response({"detail": "Token already blacklisted."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

@api_view(['POST'])
@permission_classes([AllowAny])
def activate_user(request):
    token = request.data.get('token')
    username = request.data.get('username')
    
    User = get_user_model()
    
    try:
        user = User.objects.get(username=username)
        #print(default_token_generator.make_token(user))
    except User.DoesNotExist:
        return Response({'detail': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)
    
    if default_token_generator.check_token(user, token):
        # Token is valid, activate the user
        user.is_active = True
        user.save()
        return Response({'detail': 'User activated successfully.'}, status=status.HTTP_200_OK)
    else:
        # Invalid token
        print(default_token_generator.make_token(user))#sent to the email
        return Response({'detail': 'Invalid token.'}, status=status.HTTP_400_BAD_REQUEST)

class UserDeleteView(generics.DestroyAPIView):
    queryset = get_user_model().objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

    def delete(self, request, *args, **kwargs):
        user = self.get_object()
        if user.is_superuser or user == self.request.user:
            user.is_active = False
            user.save()
            return Response({'detail': 'User deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({'detail': 'You do not have permission to delete this user.'}, status=status.HTTP_403_FORBIDDEN)
        

class UserUpdateView(UpdateAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = CustomerRegistrationSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user 