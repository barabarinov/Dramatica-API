from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models

from .utils import play_image_file_path


class Actor(models.Model):
    first_name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128)

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self) -> str:
        return self.full_name

    class Meta:
        ordering = ["first_name"]


class Genre(models.Model):
    name = models.CharField(max_length=128)

    def __str__(self) -> str:
        return self.name

    class Meta:
        ordering = ["name"]


class TheatreHall(models.Model):
    name = models.CharField(max_length=128, unique=True)
    rows = models.IntegerField()
    seats_in_row = models.IntegerField()

    @property
    def total_seating(self) -> int:
        return self.rows * self.seats_in_row

    def __str__(self) -> str:
        return self.name

    class Meta:
        ordering = ["name"]


class Play(models.Model):
    title = models.CharField(max_length=128)
    description = models.TextField()
    image = models.ImageField(null=True, upload_to=play_image_file_path)
    genres = models.ManyToManyField(Genre, blank=True, related_name="plays")
    actors = models.ManyToManyField(Actor, blank=True, related_name="plays")

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["title"]


class Performance(models.Model):
    play = models.ForeignKey(
        Play,
        on_delete=models.CASCADE,
        related_name="performances",
    )
    theatre_hall = models.ForeignKey(
        TheatreHall,
        on_delete=models.CASCADE,
        related_name="performances",
    )
    show_time = models.DateTimeField()

    def __str__(self) -> str:
        return f"{self.play.title} {self.show_time}"


class Reservation(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    def __str__(self) -> str:
        return str(self.created_at)

    class Meta:
        ordering = ["-created_at"]


class Ticket(models.Model):
    row = models.IntegerField()
    seat = models.IntegerField()
    performance = models.ForeignKey(
        Performance,
        on_delete=models.CASCADE,
        related_name="tickets",
    )
    reservation = models.ForeignKey(
        Reservation,
        on_delete=models.SET_NULL,
        related_name="tickets",
        null=True,
        blank=True,
    )

    @staticmethod
    def validate_ticket(
        row: int, seat: int, theatre_hall: TheatreHall, error_to_raise
    ) -> None:
        for ticket_attr_value, ticket_attr_name, theatre_hall_attr_name in [
            (row, "row", "rows"),
            (seat, "seat", "seats_in_row"),
        ]:
            count_attrs = getattr(theatre_hall, theatre_hall_attr_name)
            if not (1 <= ticket_attr_value <= count_attrs):
                raise error_to_raise(
                    {
                        ticket_attr_name: f"{ticket_attr_name} "
                        f"number must be in available range: "
                        f"(1, {theatre_hall_attr_name}): "
                        f"(1, {count_attrs})"
                    }
                )

    def clean(self) -> None:
        Ticket.validate_ticket(
            self.row,
            self.seat,
            self.performance.theatre_hall,
            ValidationError,
        )

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        self.full_clean()
        return super(Ticket, self).save(
            force_insert,
            force_update,
            using,
            update_fields,
        )

    def __str__(self) -> str:
        return f"{str(self.performance)} (row: {self.row}, seat: {self.seat})"

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['performance', 'row', 'seat'],
                name='unique_ticket'
            )
        ]
        ordering = ["row", "seat"]
