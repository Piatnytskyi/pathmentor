import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split

df = pd.read_csv('dataset.csv', sep='\t', low_memory=False)

print(df.columns.tolist())

def desplay_unique():
    for column in ['title', 'experience', 'salary']:
        print(f'Unique values in {column}:\n{df[column].unique()}\n')

def display_unique_skills():
    unique_skills = set()
    for row in df['skill_set']:
        if pd.notna(row) and row:
            unique_skills.update(row.split(', '))

    print(f'Unique skills:\n{unique_skills}\n')

display_unique_skills()

print(df.head())

print('Max values: \n', df.drop(df.columns[0], axis=1).max(numeric_only=True).astype(object), sep='', end='\n\n')
print('Min values: \n', df.drop(df.columns[0], axis=1).min(numeric_only=True).astype(object), sep='', end='\n\n')

print(df.isnull().sum())

print('===== Preparing =====')

df = df.drop(df.columns[0], axis=1)
df = df.dropna()

skill_map = {
    'C': 'C/C++',
    'C++': 'C/C++',
    'Javascript': 'JavaScript/TypeScript',
    'Javascript/Typescript': 'JavaScript/TypeScript',
    'C#': 'C#/.NET',

    'Scikit-learn': 'scikit-learn',
    'Scikit-Learn': 'scikit-learn',

    'Fast.ai': 'fastai',
    'Fastai': 'fastai',

    'Azure SQL Database':'Microsoft Azure SQL Database',
    
    'Azure Notebook':'Azure Notebooks',

    'Azure Machine Learning Studio':'Azure Machine Learning',
    'Azure Machine Learning Workbench':'Azure Machine Learning',

    'IBM Cloud Compose':'IBM Cloud Databases',
    'IBM Cloud Compose for PostgreSQL':'IBM Cloud Databases',
    'IBM Cloud Compose for MySQL':'IBM Cloud Databases',

    'Google Cloud BigTable':'Google Cloud Bigtable',

    'Google Cloud AI Platform Notebooks': 'Google Cloud Notebooks (AI Platform / Vertex AI)',
    'Google Cloud Machine Learning Engine': 'Google Cloud AI Platform / Google Cloud ML Engine',

    'Leaflet / Folium':'Leaflet',

    'Visual Studio':'Visual Studio / Visual Studio Code',
    'Visual Studio Code':'Visual Studio / Visual Studio Code',
    'Visual Studio Code (VSCode)':'Visual Studio / Visual Studio Code',

    'Jupyter (JupyterLab': 'JupyterLab',
    'Jupyter Notebooks': 'Jupyter Notebook',
    'JupyterHub/Binder': 'Binder / JupyterHub',

    'IBM AI Ethics tools (AI Fairness 360':'IBM AI Ethics tools (AI Fairness 360)',
    'Amazon AI Ethics Tools (Clarify':'Amazon AI Ethics Tools (Clarify)',
    'Google Responsible AI Toolkit (LIT':'Google Responsible AI Toolkit (LIT)',
    'Microsoft Responsible AI Resources (Fairlearn':'Microsoft Responsible AI Resources (Fairlearn)'
}

remove_list = ['Click to write Choice 13', 'No / None', 'Other', 'etc', 'etc)', 'I have not used any cloud providers']

def map_and_remove_skills(skill_set, skill_map, remove_list):
    skills = skill_set.split(', ')
    mapped_skills = [skill_map.get(skill, skill) for skill in skills if skill not in remove_list]

    return ', '.join(mapped_skills)

df['skill_set'] = df['skill_set'].apply(lambda x: map_and_remove_skills(x, skill_map, remove_list))

display_unique_skills()

def categorize_salary(salary):
    lower_bound = int(salary // 500) * 500
    upper_bound = lower_bound + 500
    return f"{lower_bound}-{upper_bound}"

df['salary'] = df['salary'].apply(categorize_salary)

desplay_unique()

df.to_csv('prepared_dataset.csv', sep='\t', index=True)

train_df, test_df = train_test_split(df, test_size=0.2, random_state=42)

def get_unique_counts(df, columns):
    counts = {}
    for column in columns:
        counts[column] = df[column].value_counts()
    return counts

# Function to get unique skill counts
def get_unique_skill_counts(df):
    skill_count = {}
    for row in df['skill_set']:
        if pd.notna(row) and row:
            skills = row.split(', ')
            for skill in skills:
                skill_count[skill] = skill_count.get(skill, 0) + 1
    return skill_count

# Get counts for both train and test sets
train_counts = get_unique_counts(train_df, ['title', 'experience', 'salary'])
train_skill_counts = get_unique_skill_counts(train_df)

test_counts = get_unique_counts(test_df, ['title', 'experience', 'salary'])
test_skill_counts = get_unique_skill_counts(test_df)

# Function to print side-by-side counts
def print_side_by_side_counts(train_counts, test_counts, label):
    print(f"===== {label} Counts =====")
    for key in set(train_counts.keys()).union(test_counts.keys()):
        train_count = train_counts.get(key, 0)
        test_count = test_counts.get(key, 0)
        print(f"{key}, {train_count}, {test_count}")

# Display counts
for column in ['title', 'experience', 'salary']:
    print_side_by_side_counts(train_counts[column], test_counts[column], column)

print_side_by_side_counts(train_skill_counts, test_skill_counts, 'Skill')
