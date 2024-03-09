import json
import os
import pandas as pd
from dotenv import dotenv_values
from sklearn.model_selection import train_test_split
from database.mongodb_factory import MongoDBFactory
from database.pathmentor_repository import PathMentorRepository

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

environment = os.getenv('ENVIRONMENT', 'dev')
configuration_files = {
    'dev': 'config_dev.json',
    'test': 'config_test.json',
    'prod': 'config_prod.json'
}

configuration_file = configuration_files.get(environment)
configuration = None
with open(configuration_file) as file:
    configuration = json.load(file)

secrets = dotenv_values(".env")

repository = PathMentorRepository(configuration, secrets, MongoDBFactory())
repository.clear_collection(configuration['train_collection'])
repository.clear_collection(configuration['test_collection'])

repository.store_records(configuration['train_collection'], train_df.to_dict('records'))
repository.store_records(configuration['test_collection'], test_df.to_dict('records'))
