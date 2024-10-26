from django.contrib import messages
from django.contrib.auth import authenticate, login as user_login
from django.contrib.auth import logout as user_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404

from .models import HealthData


@login_required
def index(request):
    user_data = HealthData.objects.filter(user=request.user).first()
    errors = {}

    if request.method == 'POST':
        # Process the form submission
        form_data = request.POST

        # Add your form validation here and set `errors` if there are issues

        if not errors:
            # Save or update the user's health data
            HealthData.objects.update_or_create(
                user=request.user,
                defaults={
                    'diet': form_data.get('diet'),
                    'stress': form_data.get('stress'),
                    'activity': form_data.get('activity'),
                    'sleep': form_data.get('sleep'),
                    'biometrics': form_data.get('biometrics'),
                    'medications': form_data.get('medications'),
                    'family_history': form_data.get('family_history')
                }
            )
            return redirect('success_page')  # Replace 'success_page' with your success URL

    # If it's a GET request, pass the user's data to pre-fill the form
    context = {
        'form_data': user_data,
        'errors': errors
    }
    return render(request, 'predict/index.html', context)


def login(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            user_login(request, user)
            print(user)
            return redirect('index')
        else:
            return render(request, "predict/auth/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "predict/auth/login.html") if not request.user.is_authenticated else index(request)


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        confirm_password = request.POST["confirm_password"]

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return render(request, "predict/auth/register.html")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken.")
            return render(request, "predict/auth/register.html")

        # Create the user
        user = User.objects.create_user(username=username, password=password)
        user_login(request, user)
        return redirect('index')

    return render(request, "predict/auth/register.html")


def logout(request):
    user_logout(request)
    return redirect('index')


@login_required()
def results(request, health_data_id):
    health_data = get_object_or_404(HealthData, id=health_data_id)

    # Run AI analysis on the data
    ai_analysis_report = analyze_health_data(health_data)

    # Send data to template
    context = {
        'health_data': health_data,
        'ai_analysis_report': ai_analysis_report,
        # Chart data preparation here
    }

    return render(request, 'predict/result.html', context)


@login_required()
def analyze_health_data(health_data):
    """AI-based analysis based on the provided health data."""
    reports = []

    # AI analysis logic from your JavaScript code here, translated to Python

    # Stress Levels
    if health_data.stress > 7:
        reports.append("Your current stress levels are elevated, which can negatively affect your mental health...")
    else:
        reports.append("Your stress levels are within a manageable range...")

    # Physical Activity
    if health_data.activity < 3:
        reports.append("Your current physical activity level is below the recommended amount...")
    elif health_data.activity >= 3 and health_data.activity < 7:
        reports.append("Your physical activity levels are moderate...")
    else:
        reports.append("High levels of physical activity are commendable...")

    # Sleep Patterns
    if health_data.sleep < 6:
        reports.append("Your sleep duration is insufficient...")
    elif health_data.sleep >= 6 and health_data.sleep <= 8:
        reports.append("Your sleep duration is within the healthy range...")
    else:
        reports.append("Long sleep durations are observed...")

    # Family Medical History
    if 'cardiovascular' in health_data.family_history.lower():
        reports.append(
            "Given your family history of cardiovascular issues, it is essential to engage in regular monitoring...")
    elif 'diabetes' in health_data.family_history.lower():
        reports.append(
            "With a family history of diabetes, it is crucial to monitor your blood sugar levels regularly...")
    else:
        reports.append("No significant family medical predispositions were detected...")

    # Combine into one report
    return " ".join(reports)


@login_required
def submit_health_data(request):
    print(request.POST)
    if request.method == 'POST':
        # Extract each field from request.POST
        diet = request.POST.get('diet')
        stress = request.POST.get('stress')
        activity = request.POST.get('activity')
        sleep = request.POST.get('sleep')
        biometrics = request.POST.get('biometrics')
        medications = request.POST.get('medications')
        family_history = request.POST.get('family_history')

        # Basic validation (modify as needed for specific requirements)
        errors = {}
        try:
            stress = int(stress)
            if not (1 <= stress <= 10):
                errors['stress'] = 'Stress level must be between 1 and 10.'
        except (ValueError, TypeError):
            errors['stress'] = 'Invalid stress level.'

        try:
            activity = int(activity)
            if activity < 0:
                errors['activity'] = 'Activity hours cannot be negative.'
        except (ValueError, TypeError):
            errors['activity'] = 'Invalid activity hours.'

        try:
            sleep = int(sleep)
            if sleep < 0:
                errors['sleep'] = 'Sleep hours cannot be negative.'
        except (ValueError, TypeError):
            errors['sleep'] = 'Invalid sleep hours.'

        # Additional validation checks as needed
        if not diet:
            errors['diet'] = 'Dietary patterns field is required.'
        if not biometrics:
            errors['biometrics'] = 'Biometrics field is required.'
        if not medications:
            errors['medications'] = 'Current medications field is required.'
        if not family_history:
            errors['family_history'] = 'Family medical history field is required.'

        # If errors exist, re-render the form with error messages
        if errors:
            return render(request, 'predict/index.html', {
                'errors': errors,
                'form_data': {
                    'diet': diet,
                    'stress': stress,
                    'activity': activity,
                    'sleep': sleep,
                    'biometrics': biometrics,
                    'medications': medications,
                    'family_history': family_history,
                }
            })

        # Save to the database if no errors
        health_data = HealthData(
            user=request.user,
            diet=diet,
            stress=stress,
            activity=activity,
            sleep=sleep,
            biometrics=biometrics,
            medications=medications,
            family_history=family_history
        )
        health_data.save()
        # store the id of the saved data
        health_data_id = health_data.id
        return redirect('results', health_data_id=health_data_id)

    # Handle GET request by rendering an empty form
    return render(request, 'predict/index.html')
