# import requests
from django.contrib.auth.hashers import check_password
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from incident.models import UserProfile, RegisterProfile
from django.contrib.auth.hashers import make_password
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import logout

# Create your views here.

# def get_city_country(pin_code):
#     # Example of using a mock API for demonstration
#     response = requests.get(f'http://api.example.com/pincode/{pin_code}')
#     if response.status_code == 200:
#         data = response.json()
#         return data['city'], data['country']
#     return None, None

# from django.contrib.auth import get_user_model
# from django.core.exceptions import ObjectDoesNotExist

# User = get_user_model()
# try:
#     user = User.objects.get(email="imvibhuti364@gmail.com")
#     print(f"User: {user.username}, Email: {user.email}")
# except ObjectDoesNotExist:
#     print("User does not exist.")


@login_required
def home(request):
    return render(request, "home.html")


# user = UserProfile.objects.get(email="imvibhuti364@gmail.com")
# print(check_password("#Qwerty@09", user.password))

# users = UserProfile.objects.filter(email="imvibhuti364@gmail.com")
# print(users.count())  # Should be 1 if only one user exists


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = UserProfile
        fields = (
            "user_type",
            "first_name",
            "last_name",
            "email",
            "address",
            "country",
            "city",
            "state",
            "pin_code",
            "phone_number",
            "password1",
            "password2",
        )


# Registration View
def signup_view(request):
    if request.method == "POST":
        print(request.POST)
        # Logic for signup
        form = CustomUserCreationForm(request.POST)
        try:
            if form.is_valid():
                user_type = form.cleaned_data.get("user_type")
                first_name = form.cleaned_data.get("first_name")
                last_name = form.cleaned_data.get("last_name")
                email = form.cleaned_data.get("email")
                address = form.cleaned_data.get("address")
                country = form.cleaned_data.get("country")
                city = form.cleaned_data.get("city")
                state = form.cleaned_data.get("state")
                pin_code = form.cleaned_data.get("pin_code")
                phone_number = form.cleaned_data.get("phone_number")
                password = form.cleaned_data.get("password1")

                # Create user instance
                user = UserProfile(
                    user_type=user_type,
                    first_name=first_name,
                    last_name=last_name,
                    email=email,
                    address=address,
                    country=country,
                    city=city,
                    state=state,
                    pin_code=pin_code,
                    phone_number=phone_number,
                    password=password,
                )
                if not user.username:
                    user.username = user.email
                # Save the user to the database
                user.save()

                # Redirect to the login page
                return redirect("login")
        except Exception as e:
            print("errorr:::", e)
        else:
            print(form.errors)
    else:
        form = CustomUserCreationForm()

    return render(request, "signup.html", {"form": form})


import logging

logger = logging.getLogger(__name__)


# Login View
def login_view(request):
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]
        print(request.POST)
        try:
            user = UserProfile.objects.get(email=email)

            # Check if the password matches the hashed password in the database
            if check_password(password, user.password):
                login(request, user)
                return redirect("home")
            else:
                return render(
                    request, "login.html", {"error": "Invalid email or password"}
                )

        except UserProfile.DoesNotExist:
            return render(request, "login.html", {"error": "Invalid email or password"})
    return render(request, "login.html")


def logout_view(request):
    logout(request)
    return redirect("login")


@login_required
def create_incident(request):
    if request.method == "POST":
        incident_type = request.POST.get("incident_type")
        incident_details = request.POST.get("incident_details")
        priority = request.POST.get("priority")
        status = request.POST.get("status")

        if not incident_type or not incident_details or not priority:
            messages.error(request, "Please fill in all required fields.")
        else:
            incident = RegisterProfile(
                reporter_name=request.user,
                incident_type=incident_type,
                incident_details=incident_details,
                priority=priority,
                status=status,
            )
            incident.save()
            return redirect("incident_list")

    return render(request, "create_incident.html")


@login_required
def edit_incident(request, incident_id):
    incident = get_object_or_404(
        RegisterProfile, incident_id=incident_id, reporter_name=request.user
    )
    # If the incident status is closed, redirect the user (since it cannot be edited)
    if incident.status == "Closed":
        messages.error(request, "You cannot edit a closed incident.")
        return redirect("incident_list")

    # Handle form submission (POST request)
    if request.method == "POST":
        incident_type = request.POST.get("incident_type")
        incident_details = request.POST.get("incident_details")
        priority = request.POST.get("priority")
        status = request.POST.get("status")

        # Basic validation
        if not incident_type or not incident_details or not priority:
            messages.error(request, "Please fill in all required fields.")
        else:
            # Update the incident fields with new values
            incident.incident_type = incident_type
            incident.incident_details = incident_details
            incident.priority = priority
            incident.status = status
            incident.save()

            # Redirect back to the list after successful update
            messages.success(request, "Incident updated successfully.")
            return redirect("incident_list")

    context = {"incident": incident}
    return render(request, "edit_incident.html", context)


@login_required
def incident_list(request):
    incidents = RegisterProfile.objects.filter(reporter_name=request.user)
    return render(request, "incident_list.html", {"incidents": incidents})


@login_required
def search_incident(request):
    if request.method == "GET":
        print(request.GET)
        query = request.GET.get("search")
        if query:
            try:
                incident = RegisterProfile.objects.get(
                    incident_id=query, reporter_name=request.user
                )
                print(incident)
                return redirect("edit_incident", incident_id=incident)
            except RegisterProfile.DoesNotExist:
                messages.error(request, "No incident found with that Incident ID.")
        else:
            messages.error(request, "Please enter an Incident ID.")
    return render(request, "search_incident.html")
