import pandas as pd
from sklearn.model_selection import train_test_split
from core.interaction_tf_record_builder import InteractionTFRecordBuilder
from core.skill_tf_record_builder import SkillTFRecordBuilder

def generate_interactions_from_chunk(chunk):
    interactions = []

    for index, row in chunk.iterrows():
        skill_set = row['skill_set'].split(', ')
        if len(skill_set) < 2:
            continue

        for label_skill in skill_set:
            context_skill = [skill for skill in skill_set if skill != label_skill]

            interaction = {
                'context_user_title': row['title'],
                'context_user_experience': row['experience'],
                'context_user_salary': row['salary'],
                'context_skill': context_skill,
                'label_skill': label_skill
            }

            interactions.append(interaction)
    
    return interactions

interactions = []
for chunk in pd.read_csv('../bin/prepared_dataset.csv', sep='\t', chunksize=10000):
    interactions.extend(generate_interactions_from_chunk(chunk))

interactions_df = pd.DataFrame(interactions)

print("Interactions built:")
print(interactions_df.head())

train_df, test_df = train_test_split(interactions_df, test_size=0.2, random_state=42, stratify=interactions_df[['label_skill']])

def check_missing_values(original, train, column_name):
    original_unique = set(original[column_name].unique())
    train_unique = set(train[column_name].unique())
    if not original_unique.issubset(train_unique):
        missing_values = original_unique - train_unique
        raise ValueError(f"Training set is missing values for '{column_name}': {missing_values}")

check_missing_values(interactions_df, train_df, 'context_user_title')
check_missing_values(interactions_df, train_df, 'context_user_experience')
check_missing_values(interactions_df, train_df, 'context_user_salary')

print("Interactions train split:")
print(train_df.head())

print("Interactions test split:")
print(test_df.head())

def serialize_interaction_from_row(builder, row):
    return builder.serialize_interaction(
        context_user_title=str.encode(row['context_user_title']),
        context_user_experience=str.encode(row['context_user_experience']),
        context_user_salary=str.encode(row['context_user_salary']),
        context_skill=[str.encode(skill) for skill in row['context_skill']],
        label_skill=str.encode(row['label_skill'])
    )

train_builder = InteractionTFRecordBuilder('../bin/interactions_train.tfrecord')
for index, row in train_df.iterrows():
    train_builder.write_example(serialize_interaction_from_row(train_builder, row))
train_builder.close()

test_builder = InteractionTFRecordBuilder('../bin/interactions_test.tfrecord')
for index, row in test_df.iterrows():
    test_builder.write_example(serialize_interaction_from_row(test_builder, row))
test_builder.close()

unique_skills = interactions_df['label_skill'].unique()
skills_df = pd.DataFrame(unique_skills, columns=['skill'])

print("Skills:")
print(skills_df.head())

skill_builder = SkillTFRecordBuilder('../bin/skills.tfrecord')
for index, row in skills_df.iterrows():
    skill_builder.write_example(skill_builder.serialize_skill(str.encode(row['skill'])))
skill_builder.close()
