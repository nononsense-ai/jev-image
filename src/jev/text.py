from dotenv import load_dotenv
from typesafe_sdk import (
    Choice,
    ChoiceAnswer,
    Noul,
    NoulAnswer,
    Score,
    ScoreAnswer,
    TypeSafeClient,
)
from typing import cast


def main() -> None:
    load_dotenv()

    with TypeSafeClient() as client:
        result = client.system_one(
            state="I was charged twice. Please fix this ASAP",
            questions={
                "billing": Noul(instructions="Is this ticket about billing?"),
                "tone": Choice(
                    instructions="What is the customer's tone?",
                    criteria={
                        "calm": None,
                        "frustrated": None,
                        "angry": None,
                    },
                ),
                "urgency": Score(
                    instructions="How urgent is this ticket",
                    criteria=["Can wait", "this week", "today"],
                ),
            },
        )

        answers = result.answers
        is_billing = cast(NoulAnswer, answers["billing"])
        tone = cast(ChoiceAnswer, answers["tone"])
        urgency = cast(ScoreAnswer, answers["urgency"])

        print(f"is_billing: {is_billing}")
        print(f"is_billing: {tone}")
        print(f"is_billing: {urgency}")


if __name__ == "__main__":
    main()