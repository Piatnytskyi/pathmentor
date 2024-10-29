import json
import os
from bson import ObjectId
from dotenv import dotenv_values
import pandas as pd
from pymongo import MongoClient
from sklearn.model_selection import train_test_split
from tqdm import tqdm

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
main_database = client[configuration['database']]
staging_database = client[configuration['staging_database']]

required_staging_collections = [
    configuration['interactions_train_collection'],
    configuration['interactions_test_collection']
]

for collection in required_staging_collections:
    if collection not in staging_database.list_collection_names():
        staging_database.create_collection(collection)

train_collection = staging_database[configuration['interactions_train_collection']]
test_collection = staging_database[configuration['interactions_test_collection']]

train_latest_entry = train_collection.find_one(sort=[('_id', -1)])
test_latest_entry = test_collection.find_one(sort=[('_id', -1)])

if train_latest_entry and test_latest_entry:
    latest_entry_id = max(train_latest_entry['_id'], test_latest_entry['_id'])
else:
    latest_entry_id = None

print("Latest entry ID in stage:", latest_entry_id)

if latest_entry_id is None:
    interactions_cursor = main_database[configuration['interactions_collection']].find()
else:
    interactions_cursor = main_database[configuration['interactions_collection']].find({'_id': {'$gt': latest_entry_id}})
interactions_df = pd.DataFrame(list(interactions_cursor))
interactions_cursor.close()

print("Interactions found:", len(interactions_df))
print("Interactions head:")
print(interactions_df.head())

if len(interactions_df) == 0:
    print("No interactions found. Ending script.")
    exit()

skills_cursor = main_database[configuration['skills_collection']].find()
skills_dict = {}
for skill in skills_cursor:
    skills_dict[str(skill['_id'])] = skill['skill']
skills_cursor.close()

tqdm.pandas()

interactions_df['context_skill'] = interactions_df['context_skill'].progress_apply(lambda x: [skills_dict[str(skill_id)] for skill_id in x])
interactions_df['label_skill'] = interactions_df['label_skill'].progress_apply(lambda x: skills_dict[str(x)])

print("Denormalized interactions:")
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

train_collection.insert_many(train_df.to_dict(orient='records'))
test_collection.insert_many(test_df.to_dict(orient='records'))

print("Train and test interactions inserted into staging database")
