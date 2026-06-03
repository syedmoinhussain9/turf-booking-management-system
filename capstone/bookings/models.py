from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.utils import timezone

# Create your models here.


class User(AbstractUser):
    member_id = models.CharField(max_length=20, unique=True, blank=True, null=True)
    identity_card_number = models.CharField(max_length=20, unique=True, blank=True, null=True)
    strike_count = models.IntegerField(default=0)
    is_banned = models.BooleanField(default=False)
    profile_picture_url = models.URLField(max_length=500, blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.strike_count >= 3:
            self.is_banned = True
            self.is_active = False
        else:
            self.is_banned = False
            self.is_active = True

        is_new = self.pk is None

        super().save(*args, **kwargs)

        if is_new and not self.member_id and not self.is_superuser:
            generated_id = f"KOL-2026-{self.id:04d}"

            User.objects.filter(pk=self.pk).update(member_id=generated_id)

            self.member_id = generated_id
            self.refresh_from_db(fields=['member_id'])

    def __str__(self):
        return f"{self.username} ({self.member_id or 'No ID'})"


class Sport(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Turf(models.Model):
    name = models.CharField(max_length=50, unique=True)
    supported_sports = models.ManyToManyField(Sport, related_name="turfs")

    def __str__(self):
        return self.name


class Booking(models.Model):
    STATUS_CHOICES = [
        ('CONFIRMED', 'Confirmed'),
        ('CANCELLED', 'Cancelled'),
        ('COMPLETED', 'Completed'),
    ]

    turf = models.ForeignKey(Turf, on_delete=models.CASCADE, related_name="bookings")
    sport = models.ForeignKey(Sport, on_delete=models.CASCADE, related_name="bookings")
    captain = models.ForeignKey(User, on_delete=models.CASCADE, related_name="captained_bookings")
    teammates = models.ManyToManyField(User, related_name="team_bookings")

    date = models.DateField(default=timezone.now)
    start_time = models.TimeField()
    end_time = models.TimeField()

    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='CONFIRMED')
    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        super().clean()

        if self.start_time and self.end_time and self.start_time >= self.end_time:
            raise ValidationError(
                {'end_time': "The session end time must be after the start time."})

        if self.turf and self.sport:
            if not self.turf.supported_sports.filter(id=self.sport.id).exists():
                raise ValidationError(
                    {'sport': f"The turf '{self.turf.name}' does not support {self.sport.name}."})

        if self.turf and self.date and self.start_time and self.end_time:
            overlapping_bookings = Booking.objects.filter(
                turf=self.turf,
                date=self.date,
                status='CONFIRMED',
                start_time__lt=self.end_time,
                end_time__gt=self.start_time
            )

            if self.pk:
                overlapping_bookings = overlapping_bookings.exclude(pk=self.pk)

            if overlapping_bookings.exists():
                raise ValidationError(
                    "This turf is already reserved during your selected time window."
                )

    def save(self, *args, **kwargs):
        if not kwargs.get('force_insert') and not kwargs.get('force_update'):
            self.full_clean()

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.sport.name} at {self.turf.name} | {self.date} ({self.start_time})"
