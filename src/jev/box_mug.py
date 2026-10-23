from typing import cast

from PIL import Image as PILImage
from typesafe_sdk import Box, Noul, NoulAnswer

from jev.helpers import load, make_client


def main() -> None:
    with make_client() as client:
        result = client.system_one(
            state={"photo": load("assets/kitchen.png")},
            questions={
                "mug_visible": Noul(instructions="Is there a coffee mug in the photo?"),
                "mug": Box(instructions="the coffee mug in `photo`"),
            },
            model="jev-preview",
        )
        answers = result.answers
        is_mug_visible = cast(NoulAnswer, answers["mug_visible"])
        if is_mug_visible.noul > 0.5:
            answer = result.boxes["mug"]
            print(f"Box: {answer.box},\nConfidence: {answer.confidence}")

            print("Cropping image...")
            photo = PILImage.open("assets/kitchen.png")
            w, h = photo.size
            e = result.boxes["mug"].box
            photo.crop(
                (
                    round(e.left * w),
                    round(e.top * h),
                    round(e.right * w),
                    round(e.bottom * h),
                )
            ).save("assets/mug.png")
            print("Image cropped successfully!")


if __name__ == "__main__":
    main()
