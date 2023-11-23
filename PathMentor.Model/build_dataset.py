from decimal import Decimal
import zipfile
from kaggle.api.kaggle_api_extended import KaggleApi
import numpy as np
import pandas as pd

kaggle_api = KaggleApi()
kaggle_api.authenticate()

kaggle_api.dataset_download_files('kaggle/kaggle-survey-2018', unzip=True)
kaggle_api.competition_download_files('kaggle-survey-2020')
with zipfile.ZipFile('kaggle-survey-2020.zip', 'r') as zip_ref:
    zip_ref.extractall()
kaggle_api.competition_download_files('kaggle-survey-2021')
with zipfile.ZipFile('kaggle-survey-2021.zip', 'r') as zip_ref:
    zip_ref.extractall()
kaggle_api.competition_download_files('kaggle-survey-2022')
with zipfile.ZipFile('kaggle-survey-2022.zip', 'r') as zip_ref:
    zip_ref.extractall()

df_2018 = pd.read_csv('multipleChoiceResponses.csv', low_memory=False, header=[0,1])
questions_2018 = pd.DataFrame(list(zip(df_2018.columns.get_level_values(0), df_2018.columns.get_level_values(1))))
df_2020 = pd.read_csv('kaggle_survey_2020_responses.csv', low_memory=False, header=[0,1])
questions_2020 = pd.DataFrame(list(zip(df_2020.columns.get_level_values(0), df_2020.columns.get_level_values(1))))
df_2021 = pd.read_csv('kaggle_survey_2021_responses.csv', low_memory=False, header=[0,1])
questions_2021 = pd.DataFrame(list(zip(df_2021.columns.get_level_values(0), df_2021.columns.get_level_values(1))))
df_2022 = pd.read_csv('kaggle_survey_2022_responses.csv', low_memory=False, header=[0,1])
questions_2022 = pd.DataFrame(list(zip(df_2022.columns.get_level_values(0), df_2022.columns.get_level_values(1))))

df_2018.columns = df_2018.columns.droplevel(1)
df_2020.columns = df_2020.columns.droplevel(1)
df_2021.columns = df_2021.columns.droplevel(1)
df_2022.columns = df_2022.columns.droplevel(1)

df_2018.dropna(subset=['Q6'], inplace=True)
df_2020.dropna(subset=['Q5'], inplace=True)
df_2021.dropna(subset=['Q5'], inplace=True)
df_2022.dropna(subset=['Q23'], inplace=True)

def get_cols_with_prefix(df, prefix):
    return [col for col in df.columns.values if col.startswith(prefix)]

BINARY_COLUMNS_2018 = (
    get_cols_with_prefix(df_2018, "Q13_Part")+
    get_cols_with_prefix(df_2018, "Q14_Part")+
    get_cols_with_prefix(df_2018, "Q15_Part")+
    get_cols_with_prefix(df_2018, "Q16_Part")+
    get_cols_with_prefix(df_2018, "Q19_Part")+
    get_cols_with_prefix(df_2018, "Q21_Part")+
    get_cols_with_prefix(df_2018, "Q27_Part")+
    get_cols_with_prefix(df_2018, "Q28_Part")+
    get_cols_with_prefix(df_2018, "Q29_Part")+
    get_cols_with_prefix(df_2018, "Q30_Part")
)
df_2018[BINARY_COLUMNS_2018] = df_2018[BINARY_COLUMNS_2018].notnull().astype(int)

BINARY_COLUMNS_2020 = (
    get_cols_with_prefix(df_2020, "Q7_Part")+
    get_cols_with_prefix(df_2020, "Q9_Part")+
    get_cols_with_prefix(df_2020, "Q10_Part")+
    get_cols_with_prefix(df_2020, "Q14_Part")+
    get_cols_with_prefix(df_2020, "Q16_Part")+
    get_cols_with_prefix(df_2020, "Q26_A_Part")+
    get_cols_with_prefix(df_2020, "Q27_A_Part")+
    get_cols_with_prefix(df_2020, "Q28_A_Part")+
    get_cols_with_prefix(df_2020, "Q29_A_Part")+
    get_cols_with_prefix(df_2020, "Q31_A_Part")+
    get_cols_with_prefix(df_2020, "Q34_A_Part")+
    get_cols_with_prefix(df_2020, "Q35_A_Part")
)
df_2020[BINARY_COLUMNS_2020] = df_2020[BINARY_COLUMNS_2020].notnull().astype(int)

BINARY_COLUMNS_2021 = (
    get_cols_with_prefix(df_2021, "Q7_Part")+
    get_cols_with_prefix(df_2021, "Q9_Part")+
    get_cols_with_prefix(df_2021, "Q10_Part")+
    get_cols_with_prefix(df_2021, "Q14_Part")+
    get_cols_with_prefix(df_2021, "Q16_Part")+
    get_cols_with_prefix(df_2021, "Q27_A_Part")+
    get_cols_with_prefix(df_2021, "Q28_A_Part")+
    get_cols_with_prefix(df_2021, "Q29_A_Part")+
    get_cols_with_prefix(df_2021, "Q30_A_Part")+
    get_cols_with_prefix(df_2021, "Q31_A_Part")+
    get_cols_with_prefix(df_2021, "Q32_A_Part")+
    get_cols_with_prefix(df_2021, "Q34_A_Part")+
    get_cols_with_prefix(df_2021, "Q37_A_Part")+
    get_cols_with_prefix(df_2021, "Q38_A_Part")
)
df_2021[BINARY_COLUMNS_2021] = df_2021[BINARY_COLUMNS_2021].notnull().astype(int)

BINARY_COLUMNS_2022 = (
    get_cols_with_prefix(df_2022, "Q12_")+
    get_cols_with_prefix(df_2022, "Q13_")+
    get_cols_with_prefix(df_2022, "Q14_")+
    get_cols_with_prefix(df_2022, "Q15_")+
    get_cols_with_prefix(df_2022, "Q17_")+
    get_cols_with_prefix(df_2022, "Q31_")+
    get_cols_with_prefix(df_2022, "Q33_")+
    get_cols_with_prefix(df_2022, "Q34_")+
    get_cols_with_prefix(df_2022, "Q35_")+
    get_cols_with_prefix(df_2022, "Q36_")+
    get_cols_with_prefix(df_2022, "Q37_")+
    get_cols_with_prefix(df_2022, "Q38_")+
    get_cols_with_prefix(df_2022, "Q39_")+
    get_cols_with_prefix(df_2022, "Q40_")+
    get_cols_with_prefix(df_2022, "Q41_")
)
df_2022[BINARY_COLUMNS_2022] = df_2022[BINARY_COLUMNS_2022].notnull().astype(int)

roles_map = {
'Machine Learning Engineer':'Data Scientist',
'Machine Learning/ MLops Engineer':'Data Scientist',
'Research Assistant':'Data Scientist',
'Principal Investigator':'Data Scientist',
'Research Scientist':'Data Scientist',

'DBA/Database Engineer':'Data Engineer',
'Data Architect':'Data Engineer',
'Data Administrator':'Data Engineer',

'Marketing Analyst':'Data Analyst',
'Data Journalist':'Data Analyst',
'Business Analyst':'Data Analyst',
'Salesperson':'Data Analyst',
'Data Analyst (Business, Marketing, Financial, Quantitative, etc)':'Data Analyst',

'Student':np.nan,
'Teacher / professor':np.nan,
'Not employed':np.nan,
'Currently not employed':np.nan,
'Consultant':np.nan,
'Other':np.nan,
'Product/Project Manager':np.nan,
'Product Manager':np.nan,
'Program/Project Manager':np.nan,
'Project Manager':np.nan,
'Manager (Program, Project, Operations, Executive-level, etc)':np.nan,
'Chief Officer':np.nan,
'Manager':np.nan,
'Developer Advocate': np.nan,
'Developer Relations/Advocacy': np.nan,
'Engineer (non-software)': np.nan,
'Statistician':np.nan,
}

df_2018['Q6'] = df_2018['Q6'].apply(lambda role: roles_map.get(role, role))
df_2020['Q5'] = df_2020['Q5'].apply(lambda role: roles_map.get(role, role))
df_2021['Q5'] = df_2021['Q5'].apply(lambda role: roles_map.get(role, role))
df_2022['Q23'] = df_2022['Q23'].apply(lambda role: roles_map.get(role, role))

experience_map = {
    '0-1':'< 1 years',
    '1-2':'1-3 years',
    '2-3':'1-3 years',
    '3-4':'3-5 years',
    '4-5':'3-5 years',
    '5-10':'5-10 years',
    '10-15':'10-20 years',
    '15-20':'10-20 years',
    '20-25':'20+ years',
    '25-30':'20+ years',
    '30 +':'20+ years',

    '1-2 years':'1-3 years',

    'nan':np.nan,
    'I have never written code': np.nan,
}

df_2018['Q8'] = df_2018['Q8'].apply(lambda tool: experience_map.get(str(tool), tool))
df_2020['Q6'] = df_2020['Q6'].apply(lambda tool: experience_map.get(str(tool), tool))
df_2021['Q6'] = df_2021['Q6'].apply(lambda tool: experience_map.get(str(tool), tool))
df_2022['Q11'] = df_2022['Q11'].apply(lambda tool: experience_map.get(str(tool), tool))

def get_skill_from_column_name(questions_df, column):
    q = questions_df.loc[column,"Question"]
    sp = q.split(" - Selected Choice - ")
    skills = sp[1] if len(sp)>1 else column
    return skills

def get_skill_dict_with_prefix(df, questions_df, prefix):
    return {get_skill_from_column_name(questions_df, column):column for column in get_cols_with_prefix(df, prefix )}

def get_skills_for_participant(row, skills):
    skills_list = []
    for skills_dict in skills:
        for skill, col_name in skills_dict.items():
            if row[col_name] == 1:
                skills_list.append(skill.strip())
    return ', '.join(skills_list)

questions_2018_df = pd.DataFrame(questions_2018)
questions_2018_df.columns=["Q", "Question"]
questions_2018_df.set_index("Q", inplace=True)

skills_2018=[
    get_skill_dict_with_prefix(df_2018, questions_2018_df, "Q13_Part"),
    get_skill_dict_with_prefix(df_2018, questions_2018_df, "Q14_Part"),
    get_skill_dict_with_prefix(df_2018, questions_2018_df, "Q15_Part"),
    get_skill_dict_with_prefix(df_2018, questions_2018_df, "Q16_Part"),
    get_skill_dict_with_prefix(df_2018, questions_2018_df, "Q19_Part"),
    get_skill_dict_with_prefix(df_2018, questions_2018_df, "Q21_Part"),
    get_skill_dict_with_prefix(df_2018, questions_2018_df, "Q27_Part"),
    get_skill_dict_with_prefix(df_2018, questions_2018_df, "Q28_Part"),
    get_skill_dict_with_prefix(df_2018, questions_2018_df, "Q29_Part"),
    get_skill_dict_with_prefix(df_2018, questions_2018_df, "Q30_Part")
]

df_2018['skill_set'] = df_2018.apply(lambda row: get_skills_for_participant(row, skills_2018), axis=1)

questions_2020_df = pd.DataFrame(questions_2020)
questions_2020_df.columns=["Q", "Question"]
questions_2020_df.set_index("Q", inplace=True)

skills_2020=[
    get_skill_dict_with_prefix(df_2020, questions_2020_df, "Q7_Part"),
    get_skill_dict_with_prefix(df_2020, questions_2020_df, "Q9_Part"),
    get_skill_dict_with_prefix(df_2020, questions_2020_df, "Q10_Part"),
    get_skill_dict_with_prefix(df_2020, questions_2020_df, "Q14_Part"),
    get_skill_dict_with_prefix(df_2020, questions_2020_df, "Q16_Part"),
    get_skill_dict_with_prefix(df_2020, questions_2020_df, "Q26_A_Part"),
    get_skill_dict_with_prefix(df_2020, questions_2020_df, "Q27_A_Part"),
    get_skill_dict_with_prefix(df_2020, questions_2020_df, "Q28_A_Part"),
    get_skill_dict_with_prefix(df_2020, questions_2020_df, "Q29_A_Part"),
    get_skill_dict_with_prefix(df_2020, questions_2020_df, "Q31_A_Part"),
    get_skill_dict_with_prefix(df_2020, questions_2020_df, "Q34_A_Part"),
    get_skill_dict_with_prefix(df_2020, questions_2020_df, "Q35_A_Part")
]

df_2020['skill_set'] = df_2020.apply(lambda row: get_skills_for_participant(row, skills_2020), axis=1)

questions_2021_df = pd.DataFrame(questions_2021)
questions_2021_df.columns=["Q", "Question"]
questions_2021_df.set_index("Q", inplace=True)

skills_2021=[
    get_skill_dict_with_prefix(df_2021, questions_2021_df, "Q7_Part"),
    get_skill_dict_with_prefix(df_2021, questions_2021_df, "Q9_Part"),
    get_skill_dict_with_prefix(df_2021, questions_2021_df, "Q10_Part"),
    get_skill_dict_with_prefix(df_2021, questions_2021_df, "Q14_Part"),
    get_skill_dict_with_prefix(df_2021, questions_2021_df, "Q16_Part"),
    get_skill_dict_with_prefix(df_2021, questions_2021_df, "Q27_A_Part"),
    get_skill_dict_with_prefix(df_2021, questions_2021_df, "Q28_A_Part"),
    get_skill_dict_with_prefix(df_2021, questions_2021_df, "Q29_A_Part"),
    get_skill_dict_with_prefix(df_2021, questions_2021_df, "Q30_A_Part"),
    get_skill_dict_with_prefix(df_2021, questions_2021_df, "Q31_A_Part"),
    get_skill_dict_with_prefix(df_2021, questions_2021_df, "Q32_A_Part"),
    get_skill_dict_with_prefix(df_2021, questions_2021_df, "Q34_A_Part"),
    get_skill_dict_with_prefix(df_2021, questions_2021_df, "Q37_A_Part"),
    get_skill_dict_with_prefix(df_2021, questions_2021_df, "Q38_A_Part"),
]

df_2021['skill_set'] = df_2021.apply(lambda row: get_skills_for_participant(row, skills_2021), axis=1)

questions_2022_df = pd.DataFrame(questions_2022)
questions_2022_df.columns=["Q", "Question"]
questions_2022_df.set_index("Q", inplace=True)

skills_2022=[
    get_skill_dict_with_prefix(df_2022, questions_2022_df, "Q12_"),
    get_skill_dict_with_prefix(df_2022, questions_2022_df, "Q13_"),
    get_skill_dict_with_prefix(df_2022, questions_2022_df, "Q14_"),
    get_skill_dict_with_prefix(df_2022, questions_2022_df, "Q15_"),
    get_skill_dict_with_prefix(df_2022, questions_2022_df, "Q17_"),
    get_skill_dict_with_prefix(df_2022, questions_2022_df, "Q31_"),
    get_skill_dict_with_prefix(df_2022, questions_2022_df, "Q33_"),
    get_skill_dict_with_prefix(df_2022, questions_2022_df, "Q34_"),
    get_skill_dict_with_prefix(df_2022, questions_2022_df, "Q35_"),
    get_skill_dict_with_prefix(df_2022, questions_2022_df, "Q36_"),
    get_skill_dict_with_prefix(df_2022, questions_2022_df, "Q37_"),
    get_skill_dict_with_prefix(df_2022, questions_2022_df, "Q38_"),
    get_skill_dict_with_prefix(df_2022, questions_2022_df, "Q39_"),
    get_skill_dict_with_prefix(df_2022, questions_2022_df, "Q40_"),
    get_skill_dict_with_prefix(df_2022, questions_2022_df, "Q41_")
]

df_2022['skill_set'] = df_2022.apply(lambda row: get_skills_for_participant(row, skills_2022), axis=1)

df_dou_2023 = pd.read_csv('https://raw.githubusercontent.com/devua/csv/master/salaries/2023_june_raw.csv', sep=';', decimal=',', low_memory=False)
df_dou_2023['Experience Years'] = df_dou_2023['Загальний стаж роботи за нинішньою ІТ-спеціальністю'].apply(Decimal)
df_dou_2023['Salary'] = df_dou_2023['Зарплата / дохід у $$$ за місяць, лише ставка після сплати податків'].apply(Decimal)

roles_conditions = {
    'Data Scientist': (df_dou_2023['Спеціалізація'] == 'Data Science, Machine Learning, AI, Big Data, Data Engineer') & ((df_dou_2023['Ваша посада Data Science'] == 'Data Scientist') | (df_dou_2023['Ваша посада Data Science'] == 'Machine / Deep Learning Engineer') | (df_dou_2023['Ваша посада Data Science'] == 'Research Engineer')),
    'Data Engineer': (df_dou_2023['Спеціалізація'] == 'Data Science, Machine Learning, AI, Big Data, Data Engineer') & (df_dou_2023['Ваша посада Data Science'] == 'Data Engineer / Big Data Engineer'),
    'Data Analyst': (df_dou_2023['Спеціалізація'] == 'Analyst (Business, Data, System etc)') & ((df_dou_2023['Ваша посада Analyst'] == 'Data Analyst') | (df_dou_2023['Ваша посада Analyst'] == 'Business Analyst')),
    'Software Engineer': df_dou_2023['Спеціалізація'] == 'Software Engineer'
}

adjusted_experience_ranges = {
    "< 1 years": (0, 1),
    "1-3 years": (1, 3),
    "3-5 years": (3, 5),
    "5-10 years": (5, 10),
    "10-20 years": (10, 20),
    "20+ years": (20, Decimal('inf')),
}

median_salaries_by_role_and_exp = {}
for role, condition in roles_conditions.items():
    filtered_role_data = df_dou_2023[condition]
    median_salaries_by_role = {}

    for range_name, (lower_bound, upper_bound) in adjusted_experience_ranges.items():
        salaries_in_range = filtered_role_data[
            (filtered_role_data['Experience Years'] >= lower_bound) &
            (filtered_role_data['Experience Years'] <= upper_bound)
        ]['Salary']
        median_salaries_by_role[range_name] = salaries_in_range.median() if len(salaries_in_range) >= 30 else 'Insufficient data'
    median_salaries_by_role_and_exp[role] = median_salaries_by_role

for role, median_salaries in median_salaries_by_role_and_exp.items():
    filled = None
    for range_name in adjusted_experience_ranges:
        if median_salaries[range_name] != 'Insufficient data':
            filled = median_salaries[range_name]
            break
    
    for range_name in adjusted_experience_ranges:
        if median_salaries[range_name] == 'Insufficient data':
            median_salaries[range_name] = filled
        else:
            filled = median_salaries[range_name]

def get_salary_from_experience_and_title(title, experience_range):
    median_salaries_for_title = median_salaries_by_role_and_exp.get(title, {})
    return median_salaries_for_title.get(experience_range, np.nan)

df_2018['salary'] = df_2018.apply(lambda row: get_salary_from_experience_and_title(row['Q6'], row['Q8']), axis=1)
df_2020['salary'] = df_2020.apply(lambda row: get_salary_from_experience_and_title(row['Q5'], row['Q6']), axis=1)
df_2021['salary'] = df_2021.apply(lambda row: get_salary_from_experience_and_title(row['Q5'], row['Q6']), axis=1)
df_2022['salary'] = df_2022.apply(lambda row: get_salary_from_experience_and_title(row['Q23'], row['Q11']), axis=1)

df_2018 = df_2018[['Q6','Q8', 'salary', 'skill_set']]
df_2020 = df_2020[['Q5','Q6', 'salary', 'skill_set']]
df_2021 = df_2021[['Q5','Q6', 'salary', 'skill_set']]
df_2022 = df_2022[['Q23','Q11', 'salary', 'skill_set']]

df_2018 = df_2018.rename(columns={'Q6':'title','Q8':'experience'})
df_2020 = df_2020.rename(columns={'Q5':'title','Q6':'experience'})
df_2021 = df_2021.rename(columns={'Q5':'title','Q6':'experience'})
df_2022 = df_2022.rename(columns={'Q23':'title','Q11':'experience'})

merged_df = pd.concat([df_2018, df_2020, df_2021, df_2022], ignore_index=True)

merged_df.to_csv('dataset.csv', sep='\t')
