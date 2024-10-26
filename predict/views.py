from django.shortcuts import render

from .forms import HealthDataForm  # Import the form


def index(request):
    return render(request, 'predict/index.html')


def results(request):
    return render(request, 'predict/result.html')


def submit_health_data(request):
    if request.method == 'POST':
        form = HealthDataForm(request.POST)  # Create a form instance with the submitted data
        if form.is_valid():
            # Extract data from the form
            diet = form.cleaned_data['diet']
            stress = form.cleaned_data['stress']
            activity = form.cleaned_data['activity']
            sleep = form.cleaned_data['sleep']
            biometrics = form.cleaned_data['biometrics']  # e.g., BP:120/80, Glucose:90
            medications = form.cleaned_data['medications']
            family_history = form.cleaned_data['family_history']
            comments = form.cleaned_data['comments']

            # Example: Parse biometrics
            bp, glucose = parse_biometrics(biometrics)

            # Calculate the risk profile
            risk_profile = calculate_risk_profile(diet, stress, activity, sleep, bp, glucose)

            # Render results
            return render(request, 'predict/result.html', {'risk_profile': risk_profile})
    else:
        form = HealthDataForm()  # Create a new empty form

    return render(request, 'predict/index.html', {'form': form})  # Pass the form to the template


def parse_biometrics(biometrics):
    try:
        bp_data = biometrics.split(", ")
        bp = int(bp_data[0].split(":")[1].split("/")[0])  # Systolic BP
        glucose = int(bp_data[1].split(":")[1])  # Glucose level
        return bp, glucose
    except (IndexError, ValueError):
        return None, None


def calculate_risk_profile(diet, stress, activity, sleep, bp, glucose):
    # Example scoring logic for risk profile
    risk_score = 0

    # Diet: Assign points based on the type of diet (simplified)
    if "healthy" in diet.lower():
        risk_score -= 1
    elif "unhealthy" in diet.lower():
        risk_score += 2

    # Stress levels
    risk_score += stress  # Higher stress = higher risk

    # Physical Activity
    if activity < 3:
        risk_score += 2  # Inactive lifestyle

    # Sleep
    if sleep < 7:
        risk_score += 1  # Less than 7 hours of sleep

    # Blood Pressure and Glucose (simplified criteria)
    if bp > 130:  # Assuming 130 is a threshold
        risk_score += 3
    if glucose > 100:  # Assuming 100 is a threshold
        risk_score += 3

    # Generate a risk profile based on the score
    if risk_score <= 3:
        return "Low Risk"
    elif risk_score <= 6:
        return "Moderate Risk"
    else:
        return "High Risk"
