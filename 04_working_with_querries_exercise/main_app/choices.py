from django.db import models


class LaptopBrandChoices(models.TextChoices):
    ASUS = "Asus", "Asus"
    ACER = "Acer", "Acer"
    APPLE = "Apple", "Apple"
    LENOVO = "Lenovo", "Lenovo"
    DELL = "Dell", "Dell"


class OperatingSystemChoices(models.TextChoices):
    WINDOWS = "Windows", "Windows"
    MACOS = "MacOS", "MacOS"
    LINUX = "Linux", "Linux"
    CHROME_OS = "Chrome OS", "Chrome OS"