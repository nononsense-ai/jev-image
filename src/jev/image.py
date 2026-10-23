from typing import cast

from typesafe_sdk import Choice, ChoiceAnswer, Noul, NoulAnswer

from jev.helpers import load, make_client


def main() -> None:
    with make_client() as client:
        result = client.system_one(
            state={"door": load("assets/door.png")},
            questions={
                "person_present": Noul(instructions="Is there a person in `door`?"),
                "carrying": Choice(
                    instructions="What is the person in the `door` carrying?",
                    criteria={
                        "package": "A box or parcel",
                        "bag": "A bag of groceries",
                        "nothing": "Empty hands",
                    },
                ),
            },
        )
        answers = result.answers
        is_person_present = cast(NoulAnswer, answers["person_present"])
        carrying = cast(ChoiceAnswer, answers["carrying"])

        if is_person_present.noul >= 0.8:
            print("Yes, there is a person in the door")
            match carrying.choice:
                case "package":
                    print("The person is carrying a package")
                case "bag":
                    print("The person is carrying a bag")
                case _:
                    print("The person is carrying nothing!")

        print(f"\n\n{is_person_present}")
        print(carrying)


if __name__ == "__main__":
    main()
