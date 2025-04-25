# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.contrib import admin
from .models import Subject, Category, Quiz, Question, Answer, CustomUser , Group , GroupInvitation , GroupQuiz , UserQuizResult
from django.contrib.auth.admin import UserAdmin

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('bio',)}),
    )

admin.site.register(CustomUser, CustomUserAdmin)

# Register your models here.
admin.site.register(Subject)
admin.site.register(Category)
admin.site.register(Quiz)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Group)
admin.site.register(GroupInvitation)
admin.site.register(GroupQuiz)
admin.site.register(UserQuizResult)
