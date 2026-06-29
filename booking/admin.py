from django.contrib import admin
from .models import UserProfile, Service, PortfolioItem, PortfolioImage, PortfolioVideo, ClientBooking

@admin.action(description="Approve selected workers")
def approve_workers(modeladmin, request, queryset):
    queryset.update(approval_status='approved')

@admin.action(description="Decline selected workers")
def decline_workers(modeladmin, request, queryset):
    queryset.update(approval_status='declined')

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'user_type', 'approval_status', 'hourly_rate')
    list_filter = ('user_type', 'approval_status')
    search_fields = ('user__username', 'user__email', 'skills')
    actions = [approve_workers, decline_workers]
    
    # Custom read-only fields or layout can be added here if needed

admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Service)
admin.site.register(PortfolioItem)
admin.site.register(PortfolioImage)
admin.site.register(PortfolioVideo)
admin.site.register(ClientBooking)
