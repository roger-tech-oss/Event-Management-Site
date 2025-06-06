from django.shortcuts import render, get_object_or_404, redirect
from .models import Event, Registration, Venue
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.core.mail import EmailMessage
from .forms import EventForm
from django.contrib.auth.models import User
from django.conf import settings
from django.db.models import Q
from decimal import Decimal, InvalidOperation
from django.http import JsonResponse
from django.template.loader import render_to_string
from xhtml2pdf import pisa
from io import BytesIO
from django.views.decorators.csrf import csrf_exempt
from django.utils.html import strip_tags
from .utils import get_razorpay_client

def home(request):
    events = Event.objects.all()
    return render(request, 'events/home.html', {'events': events})

def event_detail(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    other_events = Event.objects.exclude(pk=event_id).order_by('date')[:4]
    return render(request, 'events/event_detail.html', {
        'event': event,
        'other_events': other_events
    })

@login_required
def register_for_event(request, event_id):
    event = get_object_or_404(Event, pk=event_id)

    if request.method == 'POST':
        try:
            tickets = int(request.POST.get('tickets', 1))
            if tickets < 1:
                messages.error(request, "Please select at least one ticket.")
                return redirect('event_detail', event_id=event.id)

            # Ensure correct price format
            amount = int(round(float(event.price) * tickets * 100))  # paise

            # Simulate Razorpay response
            order_id = f"DUMMY_ORDER_{event.id}_{tickets}"

            request.session['registration'] = {
                'event_id': event.id,
                'tickets': tickets,
                'razorpay_order_id': order_id
            }

            # Dummy checkout page (create dummy_checkout.html)
            return render(request, 'events/dummy_checkout.html', {
                'event': event,
                'tickets': tickets,
                'order_id': order_id,
                'amount_rupees': amount / 100
            })

        except (ValueError, TypeError):
            messages.error(request, "Invalid input. Try again.")
            return redirect('event_detail', event_id=event.id)

    return redirect('event_detail', event_id=event.id)


@login_required
def checkout(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    razorpay_client = get_razorpay_client()

    if request.method == "POST":
        num_tickets = int(request.POST.get("num_tickets", 1))
        amount = int(float(event.price) * num_tickets)

        payment = razorpay_client.order.create({
            "amount": amount,
            "currency": "INR",
            "payment_capture": "1"
        })

        context = {
            "event": event,
            "order_id": payment["id"],
            "razorpay_key": settings.RAZORPAY_KEY_ID,
            "amount": amount,
            "num_tickets": num_tickets
        }
        return render(request, "payment_summary.html", context)

    return render(request, "checkout.html", {"event": event})

@csrf_exempt
@login_required
def payment_success(request):
    registration = request.session.get('registration')
    if not registration or request.method != "POST":
        return redirect('/')

    event = get_object_or_404(Event, pk=registration['event_id'])

    payment_id = request.POST.get('razorpay_payment_id', '')
    if payment_id.startswith("dummy"):
        Registration.objects.create(user=request.user, event=event, tickets=registration['tickets'])
        send_ticket_email(request.user.email, event)
        messages.success(request, 'Payment successful! Ticket sent to your email.')
        del request.session['registration']
        return redirect('home')

    try:
        razorpay_client = get_razorpay_client()
        params_dict = {
            'razorpay_order_id': request.POST['razorpay_order_id'],
            'razorpay_payment_id': payment_id,
            'razorpay_signature': request.POST['razorpay_signature']
        }
        razorpay_client.utility.verify_payment_signature(params_dict)

        Registration.objects.create(user=request.user, event=event, tickets=registration['tickets'])
        send_ticket_email(request.user.email, event)
        messages.success(request, 'Payment successful! Ticket sent to your email.')
        del request.session['registration']
        return redirect('home')

    except Exception as e:
        messages.error(request, f"Payment verification failed: {e}")
        return redirect('home')


def logout_view(request):
    logout(request)
    return redirect('home')

def register_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 != password2:
            messages.error(request, "Passwords do not match")
            return redirect('register_user')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken")
            return redirect('register_user')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered")
            return redirect('register_user')

        user = User.objects.create_user(username=username, email=email, password=password1)
        messages.success(request, "Account created successfully. Please login.")
        return redirect('login')

    return render(request, 'events/register.html')

@login_required
def create_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.organizer = request.user
            event.save()
            return redirect('event_list')
    else:
        form = EventForm()
    return render(request, 'events/create_event.html', {'form': form})

def event_list(request):
    query = request.GET.get('q')
    venue_filter = request.GET.get('venue')
    date_filter = request.GET.get('date')
    events = Event.objects.all()

    if query:
        events = events.filter(Q(title__icontains=query) | Q(description__icontains=query))
    if venue_filter:
        events = events.filter(venue_id=venue_filter)
    if date_filter:
        events = events.filter(date__date=date_filter)

    venues = Venue.objects.all()
    return render(request, 'events/event_list.html', {
        'events': events,
        'venues': venues,
        'query': query or '',
        'selected_venue': venue_filter or '',
        'selected_date': date_filter or '',
    })

@login_required
def edit_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if event.organizer != request.user:
        return redirect('event_list')

    if request.method == 'POST':
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            return redirect('event_list')
    else:
        form = EventForm(instance=event)
    return render(request, 'events/edit_event.html', {'form': form})

@login_required
def delete_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if event.organizer != request.user:
        return redirect('event_list')
    if request.method == 'POST':
        event.delete()
        return redirect('event_list')
    return render(request, 'events/confirm_delete.html', {'event': event})

@login_required
def rsvp_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if request.method == 'POST':
        tickets = request.POST.get('tickets')
        registration, created = Registration.objects.get_or_create(
            event=event, attendee=request.user,
            defaults={'tickets': tickets}
        )
        if not created:
            registration.tickets += int(tickets)
            registration.save()
        return redirect('event_list')
    return render(request, 'events/rsvp_event.html', {'event': event})

@login_required
def user_dashboard(request):
    events = Event.objects.filter(organizer=request.user)
    return render(request, 'events/user_dashboard.html', {'events': events})

def event_detail_json(request, event_id):
    event = Event.objects.get(id=event_id)
    suggestions = Event.objects.filter(date=event.date).exclude(id=event_id)[:3]
    return JsonResponse({
        "name": event.name,
        "description": event.description,
        "date": str(event.date),
        "location": event.location,
        "image_url": event.image_url.url if event.image_url else '',
        "suggestions": [
            {
                "name": e.name,
                "image_url": e.image_url.url if e.image_url else ''
            } for e in suggestions
        ]
    })

def send_ticket_email(user_email, event):
    html = render_to_string('events/ticket_template.html', {
        'event': event,
        'price': event.price,
        'time': event.event_time,
    })
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)

    if not pdf.err:
        email = EmailMessage(
            subject=f"Your Ticket for {event.title}",
            body=strip_tags(html),
            from_email="noreply@eventzone.com",
            to=[user_email],
        )
        email.content_subtype = "plain"
        email.encoding = 'utf-8'
        email.attach(f"{event.title}_ticket.pdf", result.getvalue(), 'application/pdf')
        email.send()

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('home')
        messages.error(request, 'Invalid username or password.')
    return render(request, 'events/login.html')
