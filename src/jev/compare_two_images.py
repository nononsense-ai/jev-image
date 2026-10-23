from typesafe_sdk import Noul, NoulAnswer
from jev.helpers import load, make_client
from typing import cast

def main() -> None:
    with make_client() as client:
        result = client.system_one(
            state={"door": load("assets/person-in-door.png"), "badge": load("assets/badge.png")},
            questions={
                "same_person": Noul(instructions="Is the person in the `door` the same as `badge` ?")
            }
        )
        is_same_person = cast(NoulAnswer, result.answers["same_person"])
        if is_same_person.noul >= 0.8:
            print("Yes, it is the same person")
        else:
            print("No, it is a different person")
        print(is_same_person)

if __name__ == "__main__":
    main()