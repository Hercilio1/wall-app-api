from rest_framework import generics
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from django.core.mail import EmailMessage
from django.template import loader
from .models import User
from .serializers import CreateUserSerializer, UserSerializer


class UserProfileView(APIView):
    permission_classes=[IsAuthenticated]
    serializer_class = UserSerializer

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)


class UserCreateView(generics.CreateAPIView):
    """
    Creates user accounts
    """
    queryset = User.objects.all()
    serializer_class = CreateUserSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)

        if response.status_code == status.HTTP_201_CREATED:
            user = response.data
            self.send_welcome_email(user['email'])

        return response

    def send_welcome_email(self, user_email):
        fromEmail = 'herciliomartins@gmail.com'
        subject = 'Welcome to Wall App!'
        template = loader.get_template('email/welcome.html')

        context = {'user_email': user_email}
        html_content = template.render(context)

        email = EmailMessage(subject, html_content, fromEmail, [user_email])
        email.content_subtype = 'html'

        email.send()
