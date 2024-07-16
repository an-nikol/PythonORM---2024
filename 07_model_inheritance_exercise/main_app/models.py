from datetime import datetime, timedelta

from django.core.exceptions import ValidationError
from django.db import models

# Task 01.
class BaseCharacter(models.Model):
    class Meta:
        abstract = True

    name = models.CharField(
        max_length=100,
    )

    description = models.TextField()


class Mage(BaseCharacter):
    elemental_power = models.CharField(
        max_length=100,
    )

    spellbook_type = models.CharField(
        max_length=100,
    )


class Assassin(BaseCharacter):
    weapon_type = models.CharField(
        max_length=100,
    )

    assassination_technique = models.CharField(
        max_length=100,
    )


class DemonHunter(BaseCharacter):
    weapon_type = models.CharField(
        max_length=100,
    )

    demon_slaying_ability = models.CharField(
        max_length=100,
    )


class TimeMage(Mage):
    time_magic_mastery = models.CharField(
        max_length=100,
    )

    temporal_shift_ability = models.CharField(
        max_length=100,
    )


class Necromancer(Mage):
    raise_dead_ability = models.CharField(
        max_length=100,
    )


class ViperAssassin(Assassin):
    venomous_strikes_mastery = models.CharField(
        max_length=100,
    )

    venomous_bite_ability = models.CharField(
        max_length=100,
    )


class ShadowbladeAssassin(Assassin):
    shadowstep_ability = models.CharField(
        max_length=100,
    )


class VengeanceDemonHunter(DemonHunter):
    vengeance_mastery = models.CharField(
        max_length=100,
    )

    retribution_ability = models.CharField(
        max_length=100,
    )


class FelbladeDemonHunter(DemonHunter):
    felblade_ability = models.CharField(
        max_length=100,
    )

# Task 02.

class UserProfile(models.Model):
    username = models.CharField(max_length=70, unique=True)
    email = models.EmailField(unique=True)
    bio = models.TextField(blank=True, null=True)

class Message(models.Model):
    sender = models.ForeignKey(UserProfile, related_name='sent_messages', on_delete=models.CASCADE)
    receiver = models.ForeignKey(UserProfile, related_name='received_messages', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def mark_as_read(self):
        self.is_read = True

    def reply_to_message(self, reply_content: str):
        return Message.objects.create(sender=self.receiver, receiver=self.sender, content=reply_content)

    def forward_message(self, receiver: UserProfile):
        return Message.objects.create(sender=self.receiver, receiver=receiver, content=self.content)


# Task 03.

class StudentIDField(models.PositiveIntegerField):

    # for type validation (must be int)
    def to_python(self, value) -> int or None:
        try:
            return int(value)
        except ValueError:
            raise ValueError('Invalid input for student ID')


    # for validation what integer must be(value before being saved in the DB)

    def get_prep_value(self, value):
        cleaned_value = self.to_python(value)

        if cleaned_value <= 0:
            raise ValidationError(f'ID cannot be less than or equal to zero')

        return cleaned_value


class Student(models.Model):
    name = models.CharField(max_length=100)
    student_id = StudentIDField()


# Task 04.

class MaskedCreditCardField(models.CharField):

    # predefined innit method because the attribute max_length is there
    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 20

        super().__init__(*args, **kwargs)

    # calling to_python to validate
    def to_python(self, value) -> str:
        # first check - check if it is a str
        if not isinstance(value, str):
            raise ValidationError('The card number must be a string')

        # second check - check if it contains only ints
        if not value.isdigit():
            raise ValidationError('The card number must contain only digits')

        # third check - check if it is exatly 16 digits
        if len(value) != 16:
            raise ValidationError('The card number must be exactly 16 characters long')

        # always return a value to be saved in the DB
        return f"****-****-****-{value[-4:]}"


class CreditCard(models.Model):
    card_owner = models.CharField(max_length=100)
    # using our customised field
    card_number = MaskedCreditCardField()

# Task 05.

class Hotel(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)

class Room(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    number = models.CharField(max_length=100, unique=True)
    capacity = models.PositiveIntegerField()
    total_guests = models.PositiveIntegerField()
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)

    def clean(self):
        if self.total_guests > self.capacity:
            raise ValidationError('Total guests are more than the capacity of the room')

    def save(self, *args, **kwargs):
        """
        clean method is not called independently.
        We have to call it inside the save method.
        In constrast to full_clean method, but only when forms are concerned
        """

        self.clean()

        # always when predefining the save method we should super save it.
        super().save(*args, **kwargs)

        return f"Room {self.number} created successfully"


class BaseReservation(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()

    def reservation_period(self):
        reservation_period = (self.end_date - self.start_date).days
        return reservation_period

    def calculate_total_cost(self):
        total_cost = round(self.room.price_per_night * self.reservation_period(), 2)
        return total_cost



    @property
    # in case of overlap
    def is_available(self) -> bool:

        # take all reservations that overlap
        reservations = self.__class__.objects.filter(
            room=self.room,
            end_date__gte=self.start_date,
            start_date__lte=self.end_date,
        )

        return not reservations.exists() # no reservations -> True

    def clean(self):
        if self.start_date>= self.end_date:
            raise ValidationError("Start date cannot be after or in the same end date")

        if not self.is_available:
            raise ValidationError(f"Room {self.room.number} cannot be reserved")
    class Meta:
        abstract = True

class RegularReservation(BaseReservation):
        def save(self, *args, **kwargs):

            super().clean()


            super().save(*args, **kwargs)

            return f'Regular reservation for room {self.room.number}'


class SpecialReservation(BaseReservation):
    # could avoid repetition with property
    def save(self, *args, **kwargs):
        # calls the clean method in the base class
        super().clean()

        # calls the save method in the Models class, because it is not in the base class
        super().save(*args, **kwargs)

        return f'Special reservation for room {self.room.number}'

    def extend_reservation(self, days: int):
        # try to extend the reservations ( still not saved in the DB)
        self.end_date += timedelta(days=days) # use timedelta when adding days, years etc

        # check if it is available
        if not self.is_available:
            raise ValidationError('Error during extending reservation')

        # then we save it in the DB
        self.save()

        return f"Extended reservation for room {self.room.number} with {days} days"