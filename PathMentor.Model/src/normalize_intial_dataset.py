import json
import os
from bson import ObjectId
import pandas as pd
from dotenv import dotenv_values
from pymongo import MongoClient
from sklearn.model_selection import train_test_split
from tqdm import tqdm

def generate_interactions_from_chunk(chunk):
    interactions = []

    for _, row in chunk.iterrows():
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

unique_skills = interactions_df['label_skill'].unique()
skills_df = pd.DataFrame(unique_skills, columns=['skill'])

print("Skills:")
print(skills_df.head())

secrets = dotenv_values(".env")

environment = os.getenv('ENVIRONMENT', 'dev')
configuration_files_names = {
    'dev': 'config_dev.json',
    'test': 'config_test.json',
    'prod': 'config_prod.json'
}

configuration_file = configuration_files_names.get(environment)
configuration = None
with open(configuration_file) as file:
    configuration = json.load(file)

client = MongoClient(secrets['SRV_URI'])
database = client[configuration['staging_database']]

required_collections = [
    configuration['skills_collection'],
    configuration['interactions_train_collection'],
    configuration['interactions_test_collection']
]
existing_collections = database.list_collection_names()
for collection in required_collections:
    if collection not in existing_collections:
        database.create_collection(collection)
    database[collection].delete_many({})

unique_skills_ids = {}
for skill in tqdm(unique_skills, desc="Inserting skills"):
    result = database.skills.insert_one({"skill": skill})
    unique_skills_ids[skill] = result.inserted_id

def insert_interactions(dataframe, collection_name, unique_skills_ids):
    for _, row in tqdm(dataframe.iterrows(), total=dataframe.shape[0], desc=f"Inserting into {collection_name}"):
        interaction = row.to_dict()
        interaction['label_skill'] = unique_skills_ids[interaction['label_skill']]
        interaction['context_skill'] = [ObjectId(unique_skills_ids[skill]) for skill in interaction['context_skill']]
        database[collection_name].insert_one(interaction)

insert_interactions(train_df, configuration['interactions_train_collection'], unique_skills_ids)
insert_interactions(test_df, configuration['interactions_test_collection'], unique_skills_ids)

print("Interactions and skills have been successfully inserted.")
