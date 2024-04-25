from core.tf_record_builder import TFRecordBuilder

class InteractionTFRecordBuilder(TFRecordBuilder):
    def serialize_interaction(self, context_user_title, context_user_experience, context_user_salary, context_skill, label_skill):
        example = self.serialize_example(
            context_user_title=context_user_title,
            context_user_experience=context_user_experience,
            context_user_salary=context_user_salary,
            context_skill=context_skill,
            label_skill=label_skill
        )
        return example
