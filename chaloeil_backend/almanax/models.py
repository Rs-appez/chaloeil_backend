from enum import Enum
from typing import override
from django.db import models


class Job(Enum):
    BREEDER = "Breeder"
    HANDYMAN = "Handyman"
    MINER = "Miner"
    FARMER = "Farmer"
    LUMBERJACK = "Lumberjack"
    HUNTER = "Hunter"
    JEWELLER = "Jeweller"
    FISHERMAN = "Fisherman"
    ALCHEMIST = "Alchemist"
    SHOEMAKER = "Shoemaker"
    TAILOR = "Tailor"
    CARVER = "Carver"
    ARTIFICER = "Artificer"
    SMITH = "Smith"


class AlmanaxEntry(models.Model):
    day = models.PositiveSmallIntegerField()
    month = models.PositiveSmallIntegerField()
    bonus = models.CharField(max_length=510)
    resource = models.CharField(max_length=255)
    resource_quantity = models.SmallIntegerField()
    resource_image_url = models.URLField(max_length=500, blank=True, null=True)
    reward = models.PositiveSmallIntegerField()

    @override
    def __str__(self) -> str:
        return f"Almanax Entry for {self.date}"


class EconomyEntry(AlmanaxEntry):
    job = models.CharField(
        max_length=50, choices=[(job.value, job.value) for job in Job]
    )

    @override
    def __str__(self) -> str:
        return f"Economy for {self.job}"
