from typing import cast

from typesafe_sdk import Choice, ChoiceAnswer

from jev.helpers import load, make_client


def main() -> None:
    with make_client() as client:
        result = client.system_one(
            state={
                "hand": load("assets/fist.png"),
            },
            questions={
                "gesture": Choice(
                    instructions="Which gesture is the `hand` doing?",
                    criteria={
                        "thumbs_up": load("assets/thumbs_up.png"),
                        "open_hand": load("assets/open_hand.png"),
                        "none": "No hand or a hand matching none of the above",
                    },
                )
            },
        )
        gesture = cast(ChoiceAnswer, result.answers["gesture"])
        match gesture.choice:
            case "thumbs_up":
                print("Hand is doing thumbs up!")
            case "open_hand":
                print("It's open hand")
            case _:
                print("This gesture is not in the list")
        print(f"\n{gesture}")


if __name__ == "__main__":
    main()
