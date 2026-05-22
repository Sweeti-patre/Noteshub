from django.shortcuts import (

    render,
    redirect,
    get_object_or_404

)

from django.contrib.auth.models import User

from django.contrib.auth import (

    authenticate,
    login,
    logout

)

from django.contrib import messages

from django.http import FileResponse

from .models import (

    Student,
    Note,
    Download,
    Notification,
    Question,
    ContactMessage

)




def home(request):

    return render(

        request,

        "home.html"

    )




def about(request):

    return render(

        request,

        "about.html"

    )




def signup_page(request):

    if request.method == "POST":

        username = request.POST.get(
            "username"
        )

        email = request.POST.get(
            "email"
        )

        password = request.POST.get(
            "password"
        )

        confirm_password = request.POST.get(
            "confirm_password"
        )

        role = request.POST.get(
            "role"
        )

        semester = request.POST.get(
            "semester"
        )

        if password != confirm_password:

            messages.error(

                request,

                "Passwords do not match"

            )

            return redirect(
                "signup"
            )

        if User.objects.filter(
            username=username
        ).exists():

            messages.error(

                request,

                "Username already exists"

            )

            return redirect(
                "signup"
            )

        if User.objects.filter(
            email=email
        ).exists():

            messages.error(

                request,

                "Email already exists"

            )

            return redirect(
                "signup"
            )

        user = User.objects.create_user(

            username=username,

            email=email,

            password=password

        )

        Student.objects.create(

            user=user,

            name=username,

            email=email,

            semester=semester,

            role=role

        )

        messages.success(

            request,

            "Signup successful"

        )

        return redirect(
            "login"
        )

    return render(

        request,

        "signup.html"

    )




def login_page(request):

    if request.method == "POST":

        username = request.POST.get(
            "username"
        )

        password = request.POST.get(
            "password"
        )

        user = authenticate(

            request,

            username=username,

            password=password

        )

        if user:

            login(

                request,

                user

            )

            try:

                profile = Student.objects.get(
                    user=user
                )

            except Student.DoesNotExist:

                messages.error(

                    request,

                    "Profile not found"

                )

                return redirect(
                    "login"
                )

            if profile.role == "teacher":

                return redirect(
                    "teacher_dashboard"
                )

            return redirect(
                "student_dashboard"
            )

        else:

            messages.error(

                request,

                "Invalid username/password"

            )

    return render(

        request,

        "login.html"

    )




def logout_page(request):

    logout(request)

    return render(

        request,

        "logout.html"

    )




def student_dashboard(request):

    student = Student.objects.get(

        user=request.user

    )

    notes = Note.objects.filter(

        status="Approved"

    )

    downloads_count = Download.objects.filter(

        student=request.user

    ).count()

    context = {

        "student": student,

        "notes": notes,

        "notes_count": notes.count(),

        "downloads_count": downloads_count,

    }

    return render(

        request,

        "studentdash.html",

        context

    )


def teacher_dashboard(request):

    profile = get_object_or_404(
        Student,
        user=request.user
    )

    if profile.role != "teacher":

        return redirect(
            "student_dashboard"
        )

    if request.method == "POST":

        title = request.POST.get(
            "title"
        )

        subject = request.POST.get(
            "subject"
        )

        semester = request.POST.get(
            "semester"
        )

        description = request.POST.get(
            "description"
        )

        file = request.FILES.get(
            "file"
        )

        Note.objects.create(

            teacher=request.user,

            title=title,

            subject=subject,

            semester=semester,

            description=description,

            file=file

        )

        return redirect(
            "teacher_dashboard"
        )

    notes = Note.objects.filter(

        teacher=request.user

    ).prefetch_related(

        "questions"

    )

    questions_count = Question.objects.filter(

        note__teacher=request.user

    ).count()

    return render(

        request,

        "teachersdash.html",

        {

            "notes": notes,

            "questions_count": questions_count

        }

    )

def download_note(request, note_id):

    note = get_object_or_404(

        Note,

        id=note_id

    )

    Download.objects.create(

        student=request.user,

        note=note

    )

    note.downloads += 1

    note.save()

    Notification.objects.create(

        user=request.user,

        title="Download",

        message=f"You downloaded {note.title}"

    )

    return FileResponse(

        note.file.open(),

        as_attachment=True

    )




def my_downloads(request):

    downloads = Download.objects.filter(

        student=request.user

    ).order_by(

        "-downloaded_at"

    )

    return render(

        request,

        "mydownload.html",

        {

            "downloads":
            downloads

        }

    )




def notifications(request):

    notifications = Notification.objects.filter(

        user=request.user

    ).order_by(

        "-created_at"

    )

    return render(

        request,

        "Notification.html",

        {

            "notifications":
            notifications

        }

    )




def notes_list(request):

    notes = Note.objects.all().order_by(

        "-uploaded_at"

    )

    return render(

        request,

        "noteslist.html",

        {

            "notes":
            notes

        }

    )




def profile(request):

    student = get_object_or_404(

        Student,

        user=request.user

    )

    context = {

        "student":
        student,

        "downloads_count":
        Download.objects.filter(
            student=request.user
        ).count(),

        "uploads_count":
        Note.objects.filter(
            teacher=request.user
        ).count(),

        "notifications_count":
        Notification.objects.filter(
            user=request.user
        ).count(),

        "notes_count":
        Note.objects.count(),

        "approved_notes":
        Note.objects.filter(

            teacher=request.user,

            status="Approved"

        ).count(),

        "total_downloads":
        Download.objects.filter(

            note__teacher=request.user

        ).count()

    }

    return render(

        request,

        "profile.html",

        context

    )




def update_profile(request):

    student = get_object_or_404(

        Student,

        user=request.user

    )

    if request.method == "POST":

        student.name = request.POST.get(
            "name"
        )

        student.email = request.POST.get(
            "email"
        )

        student.semester = request.POST.get(
            "semester"
        )

        student.save()

        request.user.email = student.email

        request.user.save()

        messages.success(

            request,

            "Profile updated"

        )

        return redirect(
            "profile"
        )

    return render(

        request,

        "updateprofile.html",

        {

            "student":
            student

        }

    )




def contact(request):

    if request.method == "POST":

        ContactMessage.objects.create(

            name=request.POST.get(
                "name"
            ),

            email=request.POST.get(
                "email"
            ),

            message=request.POST.get(
                "message"
            )

        )

        messages.success(

            request,

            "Message sent"

        )

        return redirect(
            "contact"
        )

    return render(

        request,

        "contact.html"

    )



def admin_dashboard(request):

    context = {

        "total_students":
        Student.objects.filter(
            role="student"
        ).count(),

        "total_teachers":
        Student.objects.filter(
            role="teacher"
        ).count(),

        "total_notes":
        Note.objects.count(),

        "notes":
        Note.objects.all(),

        "pending_notes":
        Note.objects.filter(
            status="Pending"
        )

    }

    return render(

        request,

        "admin.html",

        context

    )




def ask_question(request, note_id):

    note = get_object_or_404(

        Note,

        id=note_id

    )

    if request.method == "POST":

        question_text = request.POST.get(
            "question"
        )

        if question_text:

            Question.objects.create(

                student=request.user,

                note=note,

                question=question_text

            )

            Notification.objects.create(

                user=note.teacher,

                title="New Question",

                message=f"Question on {note.title}"

            )

            messages.success(

                request,

                "Question submitted"

            )

    return redirect(
        "student_dashboard"
    )




def my_upload(request):

    notes = Note.objects.filter(

        teacher=request.user

    ).order_by(

        "-uploaded_at"

    )

    return render(

        request,

        "myupload.html",

        {

            "notes":
            notes

        }

    )