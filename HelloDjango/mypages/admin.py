from django.contrib import admin
from .models import StocksFormSubmission

@admin.register(StocksFormSubmission)
class StocksFormSubmissionAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'agreement', 'submitted_at')
