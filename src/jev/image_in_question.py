from typing import cast

from typesafe_sdk import Noul, NoulAnswer

from jev.helpers import load, make_client


def main() -> None:
    with make_client() as client:
        result = client.system_one(
            state={
                "door": load("assets/door.png"),
            },
            questions={
                "same_person": Noul(
                    instructions=[
                        "Is the person in the `door` the same as in this badge photo?",
                        load("assets/badge.png"),
                    ]
                )
            },
        )
        is_same_person = cast(NoulAnswer, result.answers["same_person"])
        if is_same_person.noul >= 0.8:
            print("The person in the door is same as the person in the badge")
        else:
            print("The person in the door is not same as the person in the badge")
        print(is_same_person)


if __name__ == "__main__":
    main()
