from typing import cast

from PIL import Image as PILImage
from typesafe_sdk import Box, Noul, NoulAnswer, TypeSafeClient

from jev.helpers import crop_to, fit, load, make_client

SIDES = ["left", "right", "top", "bottom"]
PAD = 0.05


def cut_off_sides(client: TypeSafeClient, crop):
    """Return the sides of the crop that the mug seems to continue past"""
    result = client.system_one(
        state={"crop": fit(crop)},
        questions={
            side: Noul(
                instructions=f"Does the mug in `crop` continue past the {side} edge of the image"
            )
            for side in SIDES
        },
    )
    return [side for side in SIDES if result.nouls[side].noul > 0.5]


def main() -> None:
    img = "assets/kitchen-mug-edge.png"
    photo = PILImage.open(img)

    with make_client() as client:
        answer = client.system_one(
            state={"photo": load(img)},
            questions={"mug": Box(instructions="the coffee mug in `photo`")},
            model="jev-preview",
        ).boxes["mug"]
        edges = {s: getattr(answer.box, s) for s in SIDES}

        for _ in range(2):
            crop = crop_to(photo, edges)
            cut = cut_off_sides(client, crop)
            if not cut:
                break
            for side in cut:
                sign = -1 if side in ("left", "right") else 1
                edges[side] = min(1.0, max(0.0, edges[side] + sign * PAD))

        crop.save("assets/edge_mug.png")
        print(edges)

if __name__ == "__main__":
    main()