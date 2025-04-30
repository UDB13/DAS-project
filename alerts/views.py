from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import DisasterAlert, UserPreference
from .forms import UserPreferenceForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.core.serializers.json import DjangoJSONEncoder
import json
from .utils import fetch_eonet_data
# Create your views here.

def home(request):

    # If user is logged in, redirect to their personalized alert list page
    if request.user.is_authenticated:
        return redirect('alert_list')

    # Get the filter choice from query params (?scope=india or ?scope=global)
    scope = request.GET.get('scope', 'india')  # default to 'india'

    if scope == 'global':
        alerts = DisasterAlert.objects.all().order_by('-timestamp')
    else:
        alerts = DisasterAlert.objects.filter(location__icontains='India').order_by('-timestamp')

    return render(request, 'home.html', {'alerts': alerts, 'scope': scope})

def map_view(request):

    # Default values for region and scope
    region = request.GET.get('region', 'Global')  # Default region is Global

    if request.user.is_authenticated and region == 'user':
        # Fetch the user preference if available, or create a new one
        preferences, created = UserPreference.objects.get_or_create(user=request.user)
        if preferences:
            alert_names = list(preferences.alert_types.values_list('name', flat=True))

            # Normalize event_type and alert_types by transforming them to lowercase
            alerts = DisasterAlert.objects.filter(location__icontains=preferences.region)
            
            # Filter the alerts based on the normalized event types
            alerts = [alert for alert in alerts if any(alert_type.lower() in alert.event_type.lower() for alert_type in alert_names)]
        else:
            alerts = DisasterAlert.objects.none()
    else:
        # For unauthenticated users, use the region passed through the URL
        alerts = DisasterAlert.objects.filter(location__icontains=region)
    
    alert_data = [
        {
            "title": alert.title,
            "latitude": alert.latitude,
            "longitude": alert.longitude,
            "event_type": alert.event_type,
            "source_url": alert.source_url
        }
        for alert in alerts if alert.latitude and alert.longitude
    ]

    return render(request, "alerts/map_view.html", {"alerts": json.dumps(alert_data), "region":region })

@login_required
def alert_list(request):

    scope = request.GET.get('scope', 'india')  # default to 'india'

    if scope == 'user':
        preferences, created = UserPreference.objects.get_or_create(user=request.user)
        print(f"User Preferences : {preferences.region}, Alert Types : {preferences.alert_types.values_list('name', flat=True)}")
        if preferences:
            alert_names = list(preferences.alert_types.values_list('name', flat=True))

            # Normalize event_type and alert_types by transforming them to lowercase
            alerts = DisasterAlert.objects.filter(location__icontains=preferences.region)
            
            # Filter the alerts based on the normalized event types
            alerts = [alert for alert in alerts if any(alert_type.lower() in alert.event_type.lower() for alert_type in alert_names)]

        else:
            alerts = DisasterAlert.objects.none()
    elif scope == 'global':
        alerts = DisasterAlert.objects.all()
    else:
        alerts = DisasterAlert.objects.filter(location__icontains='India')

    return render(request, 'alerts/alert_list.html', {
        'alerts': alerts,
        'scope': scope,
    })

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully! You can now log in.')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'alerts/register.html', {'form': form})

@login_required
def user_preferences_view(request):
    # Get or create a preference record for this user
    # pref, _ = UserPreference.objects.get_or_create(user=request.user)
    # if request.method == 'POST':
    #     form = UserPreferenceForm(request.POST, instance=pref)
    #     if form.is_valid():
    #         form.save()
    #         return redirect('alert_list')
    # else:
    #     form = UserPreferenceForm(instance=pref)

    # return render(request, 'alerts/user_preferences.html', {'form': form})

    try:
        user_preference = UserPreference.objects.get(user=request.user)
    except UserPreference.DoesNotExist:
        user_preference = None

    if request.method == "POST":
        form = UserPreferenceForm(request.POST, instance=user_preference)
        if form.is_valid():
            # Save the form (updates if instance is provided)
            user_preference = form.save(commit=False)
            user_preference.user = request.user  # Ensure user is assigned
            user_preference.save()
            form.save_m2m()  # Save ManyToMany fields
            return redirect('user_preferences')
    else:
        form = UserPreferenceForm(instance=user_preference)

    return render(request, 'alerts/user_preferences.html', {'form': form})