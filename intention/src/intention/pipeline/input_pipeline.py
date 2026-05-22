from intention.interpretation.intention_grounder import IntentionGrounder
from intention.interpretation.profile_instantiator import ProfileInstantiator
from intention.interpretation.separator import QueryIntentionSeparator
from intention.interpretation.validator import ProfileValidator


class InputInterpretationPipeline:
    def __init__(
        self,
        separator: QueryIntentionSeparator,
        grounder: IntentionGrounder,
        instantiator: ProfileInstantiator,
        validator: ProfileValidator,
    ) -> None:
        self.separator = separator
        self.grounder = grounder
        self.instantiator = instantiator
        self.validator = validator

    def run(self, input_id: str, user_input: str) -> dict:
        query_profile, raw_intention = self.separator.separate(user_input)
        grounded_intention = self.grounder.ground(raw_intention)
        operational_profile = self.instantiator.instantiate(input_id, grounded_intention)
        validated_profile = self.validator.validate(operational_profile)

        return {
            "input_id": input_id,
            "user_input": user_input,
            "query_profile": query_profile.model_dump(),
            "raw_intention": raw_intention.model_dump(),
            "grounded_intention": grounded_intention.model_dump(),
            "operational_intention_profile": validated_profile.model_dump(),
        }
