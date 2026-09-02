from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .forms import EventsForm, registerForm, EventEditForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Events
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.db.models import Q
import json
from datetime import datetime

# from django.http import HttpResponse
"""
# My Events CRUD App testing
"""

def index(request):

    return render(request, "esapp/index.html")
    # dict key:value  ,above key=>'title'


# def ex(request):

#     return render(request, "esapp/ex.html")
#     # dict key:value  ,above key=>'title'


def events(request):
    if request.user.is_authenticated:
        events = Events.objects.all().order_by("-date").filter(user=request.user)
        # (new 1st user specific Events)

        return render(request, "esapp/events.html", {"events": events})

    else:
        events = Events.objects.all().order_by("-date")  # (descending - new 1st)
    return render(request, "esapp/events.html", {"events": events})


class EventDetailView(View):
    def get(self, request, pk):
        eventD = Events.objects.get(pk=pk)

        return render(
            request,
            "esapp/eventdetail.html",
            {
                "event": eventD,
            },
        )


@method_decorator(login_required, name="dispatch")
class create(View):
    def get(self, request):
        form = EventsForm()
        return render(
            request,
            "esapp/create-event.html",
            {"form": form},
        )

    def post(self, request):
        form = EventsForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.user = request.user
            event.save()
            messages.success(request, "New Event Scheduled Successfully!")
        else:
            return render(request, "esapp/create-event.html", {"form": form})

        return render(request, "esapp/create-event.html", {"form": form})
        # pass blank form



# user  login
def login_user(request):
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "").strip()

        if not username or not password:
            messages.error(request, "Both username and password are required.")
            return render(request, "esapp/login.html")

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if (
                user.is_staff
                or user.is_superuser
                or user.groups.filter(name="Managers").exists()
            ):
                messages.success(request, "You have been logged in successfully.")
                return redirect("dashboard")
            else:
                messages.success(request, "You have been logged in successfully.")
            return redirect("index")

        else:
            messages.error(request, "Invalid username or password.")
            return render(request, "esapp/login.html")
    else:
        return render(request, "esapp/login.html")


def logout_user(request):
    logout(request)
    messages.success(request, "You Are Now LogedOut")
    return redirect("index")


def register(request):
    if request.method == "POST":
        form = registerForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=password)
            messages.success(request, "You Are Now Registered")
            login(request, user)
        # redirect('login')
    else:
        form = registerForm()
    return render(request, "esapp/register.html", {"form": form})


# Admin staff / Organizers


@login_required
def dashboard(request):
    events = Events.objects.all()
    return render(request, "esapp/dashboard.html", {"events": events})


@login_required
def manage_events(request):

    search_term = request.GET.get("search","").strip()
    #status = request.GET.get("statusFilter")
    cat = request.GET.get("statusFilter", "").strip()
    
    if search_term:
       # events = Events.objects.filter ( Q (title__icontains=search_term) | Q(category__icontains=cat))
        events = Events.objects.filter( Q(title__icontains=search_term) | Q(description__icontains=search_term)
            | Q(category__icontains=cat)
        )
    elif cat:
        events = Events.objects.filter( Q(title__icontains=search_term) & Q(category__icontains=cat))

    else:    
        
        # fetch events data
        events = Events.objects.all().order_by("-date")
    return render(
        request, "esapp/manage-events.html", {"user": request.user, "events": events}
    )


def event_edit(request, id):
    event = get_object_or_404(Events, id=id)

    if request.method == "POST":
        form = EventEditForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            messages.success(request, "Event updated Successfully")
            return redirect("manageE")
    else:
        form = EventEditForm(instance=event)

    return render(request, "esapp/event_edit.html", {"form": form})


def event_delete(request, id):
    event = get_object_or_404(Events, id=id)

    if request.method == "POST":
        event.delete()
        messages.success(request, "Event Deleted Successfully")
        return redirect("dashboard")

    return render(request, "esapp/event_confirm_delete.html", {"event": event})


# regs
@login_required
def my_registrations(request):
    events = request.user.registered_events.all()
    return render(request, "esapp/my_registrations.html", {"events": events})


@login_required
def cancel_registration(request, event_id):
    event = get_object_or_404(Events, id=event_id)

    if request.user not in event.registered_users.all():
        messages.error(request, "You are not registered for this event.")
        return redirect("my_registrations")

    if request.method == "POST":
        event.registered_users.remove(request.user)
        messages.success(request, "Registration cancelled successfully.")

    return redirect("my_registrations")



# Handle view API



def event_list_view(request):
    # Serialize events to JSON, handling datetime and ForeignKey fields
    events_qs = Events.objects.all()
    events_data = []
    for ev in events_qs:
        events_data.append({
            'id': ev.id,
            'title': ev.title,
            'description': ev.description,
            'date': ev.date.isoformat(),  # ens str
            'category': ev.category,
            'user': ev.user.username if ev.user else None,  # assuming user FK
        })
    events_json = json.dumps(events_data)
    return render(request, 'esapp/events.html', {'events_json': events_json})


from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json


@csrf_exempt
@require_http_methods(["POST"])
def event_create(request):
    data = json.loads(request.body)
    event = Events.objects.create(
        title=data['title'],
        date=data['date'],
        description=data.get('description', ''),
        user=data.user['user'],
        category=data.category['category']
    )
    return JsonResponse({
        'id': event.id,
        'title': event.title,
        'date': event.date,
        'description': event.description,
        'user':event.user,
        'category':event.category
    })

@csrf_exempt
@require_http_methods(["DELETE"])
def event_delete(request, id):
    Events.objects.filter(id=id).delete()
    return JsonResponse({'status': 'ok'}) 



# new API test vews

import json
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from .models import Events

@csrf_exempt
@require_http_methods(["GET"])
def api_event_list(request):
    events = Events.objects.all()
    data = [{
        'id': ev.id,
        'title': ev.title,
        'description': ev.description,
        'date': ev.date.isoformat(),
        'category': ev.category,
        'status': ev.status,
        'user': ev.user.username if ev.user else None,
    } for ev in events]
    return JsonResponse(data, safe=False)



@csrf_exempt
@login_required
@require_http_methods(["POST"])
def api_event_create(request):
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)

    # Validate required fields
    if not data.get('title') or not data.get('date'):
        return JsonResponse({'error': 'Title and date are required'}, status=400)

    # Convert date string to Python date object
    try:
        date_obj = datetime.strptime(data['date'], '%Y-%m-%d').date()
    except (ValueError, KeyError):
        return JsonResponse({'error': 'Invalid date format. Use YYYY-MM-DD.'}, status=400)

    try:
        event = Events.objects.create(
            title=data['title'],
            date=date_obj,              # im passing date object, not string
            description=data.get('description', ''),
            location=data.get('location', 'Pakistan'),
            category=data.get('category', 'OTHER'),
            status=data.get('status', 'draft'),
            user=request.user
        )
        return JsonResponse({
            'id': event.id,
            'title': event.title,
            'date': event.date.isoformat(),   # now works
            'description': event.description,
            'category': event.category,
            'status': event.status,
            'user': event.user.username
        }, status=201)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)
    

@csrf_exempt
@login_required
@require_http_methods(["DELETE"])
def api_event_delete(request, id):
    try:
        event = Events.objects.get(id=id)
    except Events.DoesNotExist:
        return JsonResponse({'error': 'Event not found'}, status=404)
    if event.user != request.user:
        return JsonResponse({'error': 'Not allowed'}, status=403)
    event.delete()
    return JsonResponse({'status': 'ok'})