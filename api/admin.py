from django.contrib import admin

from .models import Patient, Recommendation, Prediction, Appointment, Policy, TestResult, Watchlist

# Register your models here.
admin.site.register(Patient)
admin.site.register(Recommendation)
admin.site.register(Prediction)
admin.site.register(Appointment)
admin.site.register(Policy)
admin.site.register(TestResult)
admin.site.register(Watchlist)
