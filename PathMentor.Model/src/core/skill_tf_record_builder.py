from core.tf_record_builder import TFRecordBuilder

class SkillTFRecordBuilder(TFRecordBuilder):
    def serialize_skill(self, skill):
        example = self.serialize_example(skill=skill)
        return example
