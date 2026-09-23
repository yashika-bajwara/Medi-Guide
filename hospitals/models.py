from django.db import models


class Hospital(models.Model):
    name = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    area = models.CharField(max_length=150, blank=True)
    address = models.TextField()

    latitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        blank=True,
        null=True
    )

    longitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        blank=True,
        null=True
    )

    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    description = models.TextField()

    facilities = models.TextField(
        help_text="Enter facilities separated by commas"
    )

    emergency = models.BooleanField(default=False)
    ambulance = models.BooleanField(default=False)

    rating = models.DecimalField(
        max_digits=2,
        decimal_places=1,
        default=4.0
    )

    image = models.ImageField(
        upload_to="hospitals/",
        blank=True,
        null=True
    )

    image_name = models.CharField(
        max_length=200,
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.name


class Treatment(models.Model):
    name = models.CharField(max_length=200)
    department = models.CharField(max_length=100)

    min_cost = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    max_cost = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    patients_treated = models.PositiveIntegerField(
        default=0
    )

    success_rate = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0
    )

    description = models.TextField()

    def average_cost(self):
        return (self.min_cost + self.max_cost) / 2

    def __str__(self):
        return self.name
class Treatment(models.Model):
    name = models.CharField(max_length=200)
    department = models.CharField(max_length=100)

    min_cost = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    max_cost = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    patients_treated = models.PositiveIntegerField(
        default=0
    )

    success_rate = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0
    )

    description = models.TextField()

    def average_cost(self):
        return (self.min_cost + self.max_cost) / 2

    def __str__(self):
        return self.name


class HospitalTreatment(models.Model):
    hospital = models.ForeignKey(
        Hospital,
        on_delete=models.CASCADE
    )

    treatment = models.ForeignKey(
        Treatment,
        on_delete=models.CASCADE
    )

    estimated_cost = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    available = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.hospital.name} - {self.treatment.name}"


class Review(models.Model):
    hospital = models.ForeignKey(
        Hospital,
        on_delete=models.CASCADE,
        related_name="reviews"
    )

    name = models.CharField(max_length=100)

    rating = models.PositiveIntegerField(
        default=5
    )

    comment = models.TextField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.name} - {self.hospital.name}"


class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.name} - {self.subject}"