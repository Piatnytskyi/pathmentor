import json
import os
from bson import ObjectId
import pandas as pd
from dotenv import dotenv_values
from pymongo import MongoClient
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
database = client[configuration['database']]

required_collections = [
    configuration['skills_collection'],
    configuration['interactions_collection']
]

for collection in required_collections:
    if collection not in database.list_collection_names():
        database.create_collection(collection)

unique_skills_ids = {}
for skill in tqdm(unique_skills, desc="Inserting skills"):
    result = database[configuration['skills_collection']].insert_one({"skill": skill})
    unique_skills_ids[skill] = result.inserted_id

for _, row in tqdm(interactions_df.iterrows(), total=interactions_df.shape[0], desc=f"Inserting into {configuration['interactions_collection']}"):
    interaction = row.to_dict()
    interaction['label_skill'] = ObjectId(unique_skills_ids[interaction['label_skill']])
    interaction['context_skill'] = [ObjectId(unique_skills_ids[skill]) for skill in interaction['context_skill']]
    database[configuration['interactions_collection']].insert_one(interaction)

print("Interactions and skills have been successfully inserted.")
