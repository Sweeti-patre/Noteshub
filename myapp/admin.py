from django.contrib import admin

from .models import (
    Student,
    Note,
    ContactMessage,
    Download,
    Notification
)




@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):

    list_display = (
        'name',
        'email',
        'role',
        'semester'
    )

    list_filter = (
        'role',
        'semester'
    )

    search_fields = (
        'name',
        'email'
    )




@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):

    list_display = (
        'title',
        'subject',
        'semester',
        'teacher',
        'uploaded_at'
    )

    list_filter = (
        'semester',
        'subject'
    )

    search_fields = (
        'title',
        'subject'
    )




@admin.register(ContactMessage)

class ContactAdmin(
    admin.ModelAdmin
):

    list_display = (

        "name",

        "email",

        "created_at"

    )

    search_fields = (

        "name",

        "email"

    )



@admin.register(Download)
class DownloadAdmin(admin.ModelAdmin):

    list_display = (
        'student',
        'note',
        'downloaded_at'
    )

    search_fields = (
        'student__username',
        'note__title'
    )




@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):

    list_display = (
        'user',
        'message',
        'created_at'
    )

    search_fields = (
        'user__username',
        'message'
    )