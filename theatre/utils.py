import os
import uuid

from django.utils.text import slugify

from .models import Play


def play_image_file_path(instance: "Play", filename: str) -> str:
    """Generate file path for uploading play images."""
    _, extension = os.path.splitext(filename)
    unique_filename = f"{slugify(instance.title)}-{uuid.uuid4()}{extension}"

    return os.path.join("uploads", "plays", unique_filename)
