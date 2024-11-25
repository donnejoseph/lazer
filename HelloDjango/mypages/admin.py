from django.contrib import admin
from .models import StocksFormSubmission, Review

@admin.register(StocksFormSubmission)
class StocksFormSubmissionAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'agreement', 'submitted_at')

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('name',   'text',)
