from django.db import models
from django.contrib.auth.models import User


class Student(models.Model):

    ROLE_CHOICES = [

        ("student", "Student"),

        ("teacher", "Teacher"),

    ]

    user = models.OneToOneField(

        User,

        on_delete=models.CASCADE,

        related_name="profile"

    )

    name = models.CharField(

        max_length=100

    )

    email = models.EmailField(

        unique=True

    )

    semester = models.CharField(

        max_length=20,

        blank=True,

        null=True

    )

    role = models.CharField(

        max_length=20,

        choices=ROLE_CHOICES,

        default="student"

    )

    created_at = models.DateTimeField(

        auto_now_add=True

    )

    class Meta:

        verbose_name = "User Profile"

        verbose_name_plural = "User Profiles"

        ordering = ["name"]

    def __str__(self):

        return f"{self.name} ({self.role})"


class Note(models.Model):

    STATUS_CHOICES = [

        ("Pending", "Pending"),

        ("Approved", "Approved"),

        ("Rejected", "Rejected"),

    ]

    SUBJECT_CHOICES = [

        ("DBMS", "DBMS"),

        ("OS", "Operating System"),

        ("CN", "Computer Network"),

        ("Python", "Python"),

        ("Java", "Java"),

        ("AI", "Artificial Intelligence"),

    ]

    teacher = models.ForeignKey(

        User,

        on_delete=models.CASCADE,

        related_name="uploaded_notes"

    )

    title = models.CharField(

        max_length=200

    )

    subject = models.CharField(

        max_length=100,

        choices=SUBJECT_CHOICES

    )

    semester = models.CharField(

        max_length=20

    )

    description = models.TextField(

        blank=True,

        null=True

    )

    file = models.FileField(

        upload_to="notes/"

    )

    status = models.CharField(

        max_length=20,

        choices=STATUS_CHOICES,

        default="Pending"

    )

    downloads = models.IntegerField(

        default=0

    )

    uploaded_at = models.DateTimeField(

        auto_now_add=True

    )

    updated_at = models.DateTimeField(

        auto_now=True

    )

    class Meta:

        ordering = ["-uploaded_at"]

    def __str__(self):

        return self.title


class Download(models.Model):

    student = models.ForeignKey(

        User,

        on_delete=models.CASCADE,

        related_name="downloads"

    )

    note = models.ForeignKey(

        Note,

        on_delete=models.CASCADE,

        related_name="download_history"

    )

    downloaded_at = models.DateTimeField(

        auto_now_add=True

    )

    class Meta:

        ordering = ["-downloaded_at"]

    def __str__(self):

        return f"{self.student.username} - {self.note.title}"


class Notification(models.Model):

    user = models.ForeignKey(

        User,

        on_delete=models.CASCADE,

        related_name="notifications"

    )

    title = models.CharField(

        max_length=100

    )

    message = models.TextField()

    is_read = models.BooleanField(

        default=False

    )

    created_at = models.DateTimeField(

        auto_now_add=True

    )

    class Meta:

        ordering = ["-created_at"]

    def __str__(self):

        return self.title


class Question(models.Model):

    student = models.ForeignKey(

        User,

        on_delete=models.CASCADE,

        related_name="questions"

    )

    note = models.ForeignKey(

        Note,

        on_delete=models.CASCADE,

        related_name="questions"

    )

    question = models.TextField()

    created_at = models.DateTimeField(

        auto_now_add=True

    )

    class Meta:

        ordering = ["-created_at"]

    def __str__(self):

        return self.question[:50]


class ContactMessage(models.Model):

    name = models.CharField(

        max_length=100

    )

    email = models.EmailField()

    message = models.TextField()

    created_at = models.DateTimeField(

        auto_now_add=True

    )

    class Meta:

        ordering = ["-created_at"]

    def __str__(self):

        return self.name