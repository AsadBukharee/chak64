from django.contrib import admin
from .models import UserProfile, Post, Problem, Campaign, Donation, Sponsor, Comment

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'cnic', 'registration_date')
    search_fields = ('user__username', 'phone', 'cnic')

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'date')
    list_filter = ('date',)
    search_fields = ('title', 'content')

@admin.register(Problem)
class ProblemAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'date', 'votes_count')
    list_filter = ('date',)
    search_fields = ('title', 'description')

    def votes_count(self, obj):
        return obj.votes.count()
    votes_count.short_description = 'Votes'

@admin.register(Campaign)
class CampaignAdmin(admin.ModelAdmin):
    list_display = ('title', 'target_amount', 'collected_amount', 'start_date', 'end_date')
    list_filter = ('start_date', 'end_date')
    search_fields = ('title', 'description')

@admin.register(Donation)
class DonationAdmin(admin.ModelAdmin):
    list_display = ('campaign', 'user', 'amount', 'date', 'privacy_option')
    list_filter = ('date', 'privacy_option')
    search_fields = ('user__username', 'campaign__title')

@admin.register(Sponsor)
class SponsorAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'fund_type', 'amount', 'date')
    list_filter = ('fund_type', 'date')
    search_fields = ('name', 'email', 'phone')

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('problem', 'author', 'date')
    list_filter = ('date',)
    search_fields = ('text', 'author__username', 'problem__title')
