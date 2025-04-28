from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserProfile, Post, Problem, Campaign, Donation, Sponsor, Comment

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name')

class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = UserProfile
        fields = ('id', 'user', 'phone', 'cnic', 'registration_date')

class PostSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)

    class Meta:
        model = Post
        fields = ('id', 'title', 'content', 'author', 'date', 'image_url')

class CommentSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ('id', 'problem', 'author', 'text', 'date')

class ProblemSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    votes_count = serializers.SerializerMethodField()

    class Meta:
        model = Problem
        fields = ('id', 'title', 'description', 'author', 'date', 'votes', 'image_url', 'comments', 'votes_count')

    def get_votes_count(self, obj):
        return obj.votes.count()

class CampaignSerializer(serializers.ModelSerializer):
    class Meta:
        model = Campaign
        fields = ('id', 'title', 'description', 'target_amount', 'collected_amount', 'start_date', 'end_date', 'image_url')

class DonationSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    campaign = CampaignSerializer(read_only=True)

    class Meta:
        model = Donation
        fields = ('id', 'campaign', 'user', 'amount', 'transaction_id', 'purpose', 'privacy_option', 'date')

class SponsorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sponsor
        fields = ('id', 'name', 'email', 'phone', 'fund_type', 'amount', 'date') 