from django.shortcuts import render
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from .models import UserProfile, Post, Problem, Campaign, Donation, Sponsor, Comment
from .serializers import (
    UserSerializer, UserProfileSerializer, PostSerializer,
    ProblemSerializer, CampaignSerializer, DonationSerializer,
    SponsorSerializer, CommentSerializer
)

# Create your views here.

def welcome_view(request):
    """Render the welcome page"""
    return render(request, 'welcome.html')

def send_welcome_email_urdu(user, profile):
    """Send a welcome email in Urdu with Islamic greeting"""
    subject = 'خوش آمدید - Chak64 پر آپ کا خیر مقدم ہے'
    
    # Create the email content in Urdu with Islamic greeting
    message = f"""
    السلام علیکم ورحمۃ اللہ وبرکاتہ
    
    {user.first_name or user.username} صاحب/صاحبہ،
    
    آپ کو Chak64 میں شامل ہونے پر ہماری طرف سے مبارکباد ہو۔
    
    آپ کا اکاؤنٹ کامیابی سے بن گیا ہے۔ آپ اب ہماری سروسز کا استعمال کر سکتے ہیں۔
    
    آپ کی رجسٹریشن کی تفصیلات:
    صارف نام: {user.username}
    ای میل: {user.email or 'نہیں دی گئی'}
    فون نمبر: {profile.phone}
    CNIC: {profile.cnic}
    
    ہماری ویب سائٹ پر جائیں: https://preview--link-the-worlds.lovable.app/
    
    ہم آپ کی خدمت میں حاضر ہیں۔
    
    جزاک اللہ خیراً
    
    Chak64 ٹیم
    """
    
    # Send the email
    send_mail(
        subject,
        message,
        settings.EMAIL_HOST_USER,
        [user.email] if user.email else [],
        fail_silently=False,
    )

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]

    def get_permissions(self):
        if self.action in ['register', 'verify']:
            return [permissions.AllowAny()]
        return [permissions.IsAdminUser()]

    @action(detail=False, methods=['post'])
    def register(self, request):
        serializer = UserProfileSerializer(data=request.data)
        if serializer.is_valid():
            user = User.objects.create_user(
                username=request.data['username'],
                email=request.data.get('email', ''),
                password=request.data['password']
            )
            profile = UserProfile.objects.create(
                user=user,
                phone=request.data['phone'],
                cnic=request.data['cnic']
            )
            
            # Send welcome email in Urdu
            if user.email:
                send_welcome_email_urdu(user, profile)
                
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'])
    def verify(self, request):
        cnic = request.query_params.get('cnic')
        try:
            profile = UserProfile.objects.get(cnic=cnic)
            return Response({'exists': True, 'user': UserSerializer(profile.user).data})
        except UserProfile.DoesNotExist:
            return Response({'exists': False})

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.AllowAny]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=False, methods=['get'])
    def recent(self, request):
        posts = Post.objects.order_by('-date')[:5]
        serializer = self.get_serializer(posts, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def date_range(self, request):
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        posts = Post.objects.filter(date__range=[start_date, end_date])
        serializer = self.get_serializer(posts, many=True)
        return Response(serializer.data)

class ProblemViewSet(viewsets.ModelViewSet):
    queryset = Problem.objects.all()
    serializer_class = ProblemSerializer
    permission_classes = [permissions.AllowAny]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=True, methods=['post'])
    def vote(self, request, pk=None):
        problem = self.get_object()
        if request.user in problem.votes.all():
            problem.votes.remove(request.user)
        else:
            problem.votes.add(request.user)
        return Response({'status': 'vote updated'})

    @action(detail=True, methods=['post'])
    def add_comment(self, request, pk=None):
        problem = self.get_object()
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(problem=problem, author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CampaignViewSet(viewsets.ModelViewSet):
    queryset = Campaign.objects.all()
    serializer_class = CampaignSerializer
    permission_classes = [permissions.AllowAny]

    @action(detail=True, methods=['get'])
    def donors(self, request, pk=None):
        campaign = self.get_object()
        donations = Donation.objects.filter(campaign=campaign)
        serializer = DonationSerializer(donations, many=True)
        return Response(serializer.data)

class DonationViewSet(viewsets.ModelViewSet):
    queryset = Donation.objects.all()
    serializer_class = DonationSerializer
    permission_classes = [permissions.AllowAny]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['get'])
    def user_donations(self, request):
        donations = Donation.objects.filter(user=request.user)
        serializer = self.get_serializer(donations, many=True)
        return Response(serializer.data)

class SponsorViewSet(viewsets.ModelViewSet):
    queryset = Sponsor.objects.all()
    serializer_class = SponsorSerializer
    permission_classes = [permissions.AllowAny]

    @action(detail=False, methods=['get'])
    def fund_types(self, request):
        return Response(dict(Sponsor.FUND_TYPES))

    @action(detail=False, methods=['get'])
    def reports(self, request):
        if not request.user.is_staff:
            return Response(status=status.HTTP_403_FORBIDDEN)
        # Add your reporting logic here
        return Response({'message': 'Reports endpoint'})
