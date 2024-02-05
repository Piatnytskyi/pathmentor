import numpy as np
import pandas as pd

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
    mapped_skills = set([skill_map.get(skill, skill) for skill in skills if skill not in remove_list])

    return ', '.join(sorted(mapped_skills))

df['skill_set'] = df['skill_set'].apply(lambda x: map_and_remove_skills(x, skill_map, remove_list))

df.replace('', np.nan, inplace=True)
df = df.dropna()

display_unique_skills()

def categorize_salary(salary):
    lower_bound = int(salary // 500) * 500
    upper_bound = lower_bound + 500
    return f"{lower_bound}-{upper_bound}"

df['salary'] = df['salary'].apply(categorize_salary)

desplay_unique()

df.to_csv('prepared_dataset.csv', sep='\t', index=True)
