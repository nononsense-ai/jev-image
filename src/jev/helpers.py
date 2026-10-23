from dotenv import load_dotenv
from PIL import Image as PILImage
from PIL import ImageOps
from typesafe_sdk import Image, TypeSafeClient


def make_client() -> TypeSafeClient:
    load_dotenv()
    return TypeSafeClient(headers={"TypeSafe-Danger-Zone-Images": "true"})


def fit(picture: PILImage.Image) -> Image:
    picture = ImageOps.exif_transpose(picture).convert("RGB")
    picture.thumbnail((1568, 1568))
    if min(picture.size) < 280:
        picture = ImageOps.scale(picture, 280 / min(picture.size))
    if max(picture.size) > 1568:
        raise ValueError(f"{picture.size} is too elongated. Crop or pad it first")
    return Image.from_pil(picture)


def load(path) -> Image:
    return fit(PILImage.open(path))


def crop_to(photo: PILImage.Image, edges):
    w, h = photo.size
    return photo.crop(
        (
            (round(edges["left"] * w)),
            (round(edges["top"] * h)),
            (round(edges["right"] * w)),
            (round(edges["bottom"] * h)),
        )
    )
