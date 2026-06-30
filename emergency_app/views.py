
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

from .models import UserProfile, EmergencyReport
from .forms import RegisterForm, EmergencyReportForm
from .nigeria_locations import NIGERIA_LOCATIONS


def home(request):
    return render(request, "home.html")


def login_view(request):

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(request, user)

            return redirect("/dashboard/")

    return render(request, "login.html")


def logout_view(request):

    logout(request)

    return redirect("/")


def register(request):

    form = RegisterForm()

    if request.method == "POST":

        form = RegisterForm(request.POST)

        if form.is_valid():

            data = form.cleaned_data

            try:

                User.objects.create_user(
                    username=data["username"],
                    email=data["email"],
                    password=data["password"]
                )

                form.save()

                return redirect("/login/")

            except Exception as e:

                print("REGISTRATION ERROR:")
                print(e)

        else:

            print("FORM ERRORS:")
            print(form.errors)

    return render(
        request,
        "register.html",
        {
            "form": form,
            "states_data": NIGERIA_LOCATIONS
        }
    )


@login_required
def dashboard(request):

    total_reports = EmergencyReport.objects.filter(
        user=request.user
    ).count()

    pending_reports = EmergencyReport.objects.filter(
        user=request.user,
        status="Pending"
    ).count()

    resolved_reports = EmergencyReport.objects.filter(
        user=request.user,
        status="Resolved"
    ).count()

    in_progress_reports = EmergencyReport.objects.filter(
        user=request.user,
        status="In Progress"
    ).count()

    return render(
        request,
        "dashboard.html",
        {
            "total_reports": total_reports,
            "pending_reports": pending_reports,
            "resolved_reports": resolved_reports,
            "in_progress_reports": in_progress_reports,
        }
    )


@login_required
def report_emergency(request):

    if request.method == "POST":

        form = EmergencyReportForm(request.POST)

        if form.is_valid():

            report = form.save(commit=False)

            report.user = request.user

            report.latitude = request.POST.get("latitude")
            report.longitude = request.POST.get("longitude")

            report.save()

            return redirect("/my-reports/")

    else:

        form = EmergencyReportForm()

    return render(
        request,
        "report_emergency.html",
        {
            "form": form,
            "states_data": NIGERIA_LOCATIONS
        }
    )


@login_required
def my_reports(request):

    reports = EmergencyReport.objects.filter(
        user=request.user
    ).order_by("-id")

    return render(
        request,
        "my_reports.html",
        {
            "reports": reports
        }
    )


@login_required
def profile(request):

    profile = UserProfile.objects.filter(
        username=request.user.username
    ).first()

    return render(
        request,
        "profile.html",
        {
            "profile": profile
        }
    )


@login_required
def report_detail(request, report_id):

    report = EmergencyReport.objects.get(
        id=report_id,
        user=request.user
    )

    return render(
        request,
        "report_detail.html",
        {
            "report": report
        }
    )


@login_required
def emergency_contacts(request):

    return render(
        request,
        "emergency_contacts.html"
    )


@login_required
def response_guidelines(request):

    return render(
        request,
        "response_guidelines.html"
    )


@login_required
def track_dispatch(request):

    report = None

    if request.method == "POST":

        tracking_id = request.POST.get(
            "tracking_id"
        )

        report = EmergencyReport.objects.filter(
            tracking_id=tracking_id,
            user=request.user
        ).first()

    return render(
        request,
        "track_dispatch.html",
        {
            "report": report
        }
    )

