from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.db import models
from .models import Turf, Sport, Booking
from django.contrib.auth import get_user_model, login, logout, authenticate
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required, user_passes_test
import datetime
from django.utils import timezone

User = get_user_model()


def index(request):
    is_banned = False

    if request.user.is_authenticated:
        strike_count = getattr(request.user, 'strike_count', 0)
        is_banned_attr = getattr(request.user, 'is_banned', False)

        if strike_count >= 3 or is_banned_attr:
            is_banned = True

    context = {
        "turfs": Turf.objects.all(),
        "is_banned": is_banned
    }
    return render(request, "bookings/index.html", context)


def login_view(request):
    if request.method == "POST":
        u = request.POST.get("username")
        p = request.POST.get("password")
        user = authenticate(request, username=u, password=p)
        if user is not None:
            login(request, user)
            messages.success(request, f"Welcome back, {user.username}!")
            return redirect("index")
        else:
            messages.error(
                request, "Invalid username credentials or secure passcodes code structure.")
    return render(request, "bookings/login.html")


def register_view(request):
    if request.method == "POST":
        u = request.POST.get("username")
        p = request.POST.get("password")
        c = request.POST.get("password_confirm")

        if p != c:
            messages.error(
                request, "Verification mismatch error: Confirmed codes must match exactly.")
            return render(request, "bookings/register.html")

        if User.objects.filter(username=u).exists():
            messages.error(
                request, "Naming error: That selection choice username is already locked by another member.")
            return render(request, "bookings/register.html")

        new_user = User.objects.create_user(username=u, password=p)
        login(request, new_user)
        messages.success(request, "Account verification pipeline successful! Welcome aboard.")
        return redirect("index")

    return render(request, "bookings/register.html")


def logout_view(request):
    if request.method == "POST":
        logout(request)
        messages.success(request, "Session cleared successfully.")
    return redirect("index")


@login_required
def profile_view(request):
    user = request.user
    today = datetime.date.today()

    if request.method == "POST" and "update_avatar" in request.POST:
        url = request.POST.get("profile_picture_url", "").strip()
        user.profile_picture_url = url if url else None
        user.save()
        messages.success(request, "🎨 Your profile avatar has been updated successfully!")
        return redirect("user_profile")

    total_bookings = Booking.objects.filter(
        models.Q(captain=user) | models.Q(teammates=user)
    ).distinct()

    upcoming_matches = total_bookings.filter(date__gte=today, status='CONFIRMED').order_by('date', 'start_time')
    past_or_all_logs = total_bookings.order_by('-date')

    context = {
        'user': user,
        'booking_count': total_bookings.filter(status='CONFIRMED').count(),
        'upcoming_matches': upcoming_matches,
        'recent_matches': past_or_all_logs[:5],
    }
    return render(request, "bookings/profile.html", context)


@login_required
def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, captain=request.user)

    if booking.status != 'CONFIRMED':
        messages.error(request, "⚠️ This match is already settled or cancelled.")
    else:
        booking.status = 'CANCELLED'
        booking.save()
        messages.success(request, "🛑 Your turf reservation has been officially cancelled.")

    return redirect("user_profile")


@user_passes_test(lambda u: u.is_staff)
def admin_verification_dashboard(request):
    pending_verification = Booking.objects.filter(status='CONFIRMED').order_by('date')

    if request.method == "POST":
        booking_id = request.POST.get("booking_id")
        action = request.POST.get("action")
        booking = get_object_or_404(Booking, id=booking_id)

        if action == "complete":
            booking.status = 'COMPLETED'
            booking.save()
            messages.success(request, f"✅ Match {booking.id} verified as legitimately played!")

        elif action == "strike":
            booking.status = 'CANCELLED'
            booking.save()

            captain = booking.captain
            captain.strike_count += 1
            captain.save()

            messages.warning(
                request, f"⚠️ Attendance failure strike docked against {captain.username}. ({captain.strike_count}/3)")

        return redirect("admin_dashboard")

    return render(request, "bookings/admin_dashboard.html", {"bookings": pending_verification})


def check_player_availability(request):
    user_id = request.GET.get('user_id')
    date_str = request.GET.get('date')

    if not user_id or not date_str:
        return JsonResponse({'error': 'Missing parameters'}, status=400)

    try:
        player = User.objects.get(id=user_id)

        is_banned_flag = getattr(player, 'is_banned', False)

        if is_banned_flag or not player.is_active:
            return JsonResponse({'available': False, 'reason': 'banned'})

    except User.DoesNotExist:
        return JsonResponse({'error': 'Player not found'}, status=404)

    already_playing = Booking.objects.filter(
        date=date_str,
        status='CONFIRMED'
    ).filter(
        models.Q(captain_id=user_id) | models.Q(teammates__id=user_id)
    ).distinct().exists()

    return JsonResponse({'available': not already_playing})


def sandbox_dashboard(request):
    if request.method == "POST":
        captain_id = request.POST.get("captain")
        teammate_ids = request.POST.getlist("teammates")
        turf_id = request.POST.get("turf")
        sport_id = request.POST.get("sport")
        booking_date = request.POST.get("date")
        start_time = request.POST.get("start_time")
        end_time = request.POST.get("end_time")

        try:
            captain = User.objects.get(id=captain_id)
            turf = Turf.objects.get(id=turf_id)
            sport = Sport.objects.get(id=sport_id)

            valid_teammate_ids = [tid for tid in teammate_ids if tid]

            if len(valid_teammate_ids) > 9:
                messages.error(
                    request,
                    "🚫 Validation Failure: A session cannot exceed a maximum capacity of 9 teammates alongside 1 captain (10 players total)."
                )
                return redirect("sandbox_dashboard")

            if datetime.datetime.strptime(booking_date, "%Y-%m-%d").date() < datetime.date.today():
                messages.error(request, "🚫 Schedule Error: Cannot backdate a match into history records.")
                return redirect("sandbox_dashboard")

            turf_clash = Booking.objects.filter(
                turf=turf,
                date=booking_date,
                start_time=start_time,
                end_time=end_time,
                status='CONFIRMED'
            ).exists()

            if turf_clash:
                messages.error(
                    request,
                    f"🚫 Arena Schedule Conflict: {turf.name} is already reserved for the {start_time} to {end_time} time-slot on this date."
                )
                return redirect("sandbox_dashboard")

            if captain.is_banned or not captain.is_active:
                messages.error(request, f"🚫 Roster Policy Exception: Captain {captain.username} is banned.")
                return redirect("sandbox_dashboard")

            banned_squad_members = User.objects.filter(id__in=valid_teammate_ids, is_banned=True)
            if banned_squad_members.exists():
                banned_names = [u.username for u in banned_squad_members]
                messages.error(request, f"🚫 Roster Policy Exception: Banned players selected: {', '.join(banned_names)}")
                return redirect("sandbox_dashboard")

            all_involved_player_ids = [int(captain_id)] + [int(tid) for tid in valid_teammate_ids]

            conflicting_bookings = Booking.objects.filter(
                date=booking_date,
                status='CONFIRMED'
            ).filter(
                models.Q(captain_id__in=all_involved_player_ids) |
                models.Q(teammates__id__in=all_involved_player_ids)
            ).distinct()

            if conflicting_bookings.exists():
                offenders = []
                for b in conflicting_bookings:
                    if b.captain.id in all_involved_player_ids:
                        offenders.append(b.captain.username)
                    for t in b.teammates.all():
                        if t.id in all_involved_player_ids:
                            offenders.append(t.username)

                unique_offenders = list(set(offenders))
                messages.error(request, f"🚫 Policy Violation: Players already locked on this date: {', '.join(unique_offenders)}")
                return redirect("sandbox_dashboard")

            booking = Booking(
                captain=captain,
                turf=turf,
                sport=sport,
                date=booking_date,
                start_time=start_time,
                end_time=end_time,
                status='CONFIRMED'
            )
            booking.save()

            if valid_teammate_ids:
                squad = User.objects.filter(id__in=valid_teammate_ids)
                booking.teammates.add(*squad)

            messages.success(request, f"🎉 Success! Your turf session (Booking ID {booking.id}) has been successfully booked!")
            return redirect("index")

        except Exception as e:
            messages.error(request, f"❌ System Error: {str(e)}")

        return redirect("sandbox_dashboard")

    now = timezone.localtime(timezone.now())
    current_date = now.strftime("%Y-%m-%d")
    default_start = now.strftime("%H:00")
    default_end = (now + datetime.timedelta(hours=1)).strftime("%H:00")

    context = {
        "users": User.objects.filter(is_superuser=False).order_by("id"),
        "turfs": Turf.objects.all(),
        "sports": Sport.objects.all(),
        "recent_bookings": Booking.objects.all().order_by("-id")[:5],
        "date": current_date,
        "start_time": default_start,
        "end_time": default_end,
    }
    return render(request, "bookings/bookings.html", context)
