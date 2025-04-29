from decimal import Decimal
from pathlib import Path
import numpy as np
import pandas as pd
import pandas as pd
import psycopg
from tqdm import tqdm

##TODO: Extend with logging
class PathMentorDatasetBuilder:
    def build(self, output_path: Path) -> Path:
        output_folder = output_path.parent

        df_2018 = pd.read_csv(output_folder / 'multipleChoiceResponses.csv', low_memory=False, header=[0,1])
        questions_2018 = pd.DataFrame(list(zip(df_2018.columns.get_level_values(0), df_2018.columns.get_level_values(1))))
        df_2020 = pd.read_csv(output_folder / 'kaggle_survey_2020_responses.csv', low_memory=False, header=[0,1])
        questions_2020 = pd.DataFrame(list(zip(df_2020.columns.get_level_values(0), df_2020.columns.get_level_values(1))))
        df_2021 = pd.read_csv(output_folder / 'kaggle_survey_2021_responses.csv', low_memory=False, header=[0,1])
        questions_2021 = pd.DataFrame(list(zip(df_2021.columns.get_level_values(0), df_2021.columns.get_level_values(1))))
        df_2022 = pd.read_csv(output_folder / 'kaggle_survey_2022_responses.csv', low_memory=False, header=[0,1])
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

        merged_df.to_csv(output_path, sep='\t')
        return output_path

    def prepare(self, built_dataset_path: Path, output_path: Path) -> Path:
        df = pd.read_csv(built_dataset_path, sep='\t', low_memory=False)

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

            'Domino Data Lab': 'Domino Datalab',

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

        df.to_csv(output_path, sep='\t', index=True)
        return output_path

    def __generate_interactions_from_chunk(self, chunk):
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

    def normalize(self, prepared_dataset_path: Path, connection_string: str, force: bool = False) -> None:
        interactions = []
        for chunk in pd.read_csv(prepared_dataset_path, sep='\t', chunksize=10000):
            interactions.extend(self.__generate_interactions_from_chunk(chunk))

        interactions_df = pd.DataFrame(interactions)

        print("Interactions built:")
        print(interactions_df.head())

        unique_skills = interactions_df['label_skill'].unique()
        skills_df = pd.DataFrame(unique_skills, columns=['skill'])

        print("Skills:")
        print(skills_df.head())

        with psycopg.connect(connection_string) as connection:
            with connection.cursor() as cursor:
                if force:
                    print("Force flag provided, purging database tables.")
                    cursor.execute("TRUNCATE TABLE \"Skills\" CASCADE;")
                    cursor.execute("TRUNCATE TABLE \"Titles\" CASCADE;")
                    cursor.execute("TRUNCATE TABLE \"Experiences\" CASCADE;")
                    cursor.execute("TRUNCATE TABLE \"Salaries\" CASCADE;")
                
                cursor.execute("TRUNCATE TABLE \"Interactions\" CASCADE;")
                cursor.execute("TRUNCATE TABLE \"InteractionSkill\" CASCADE;")

                connection.commit()

                unique_skills_ids = {}
                for skill in tqdm(unique_skills, desc="Inserting skills"):
                    cursor.execute("SELECT \"Id\" FROM \"Skills\" WHERE \"Name\" = %s;", (skill,))
                    skill_id = cursor.fetchone()
                    if skill_id is None:
                        skill_id = cursor.execute("INSERT INTO \"Skills\" (\"Id\",\"Name\") VALUES (gen_random_uuid(), %s) RETURNING \"Id\";", (skill,)).fetchone()[0]
                    else:
                        skill_id = skill_id[0]
                    unique_skills_ids[skill] = skill_id

                connection.commit()

                interaction_ids = cursor.execute(f"SELECT gen_random_uuid() FROM generate_series(1, {interactions_df.shape[0] + 1})").fetchall()
                interaction_ids = [row[0] for row in interaction_ids]

                chunk_size = 2000
                chunks = [interactions_df[i:i + chunk_size] for i in range(0, interactions_df.shape[0], chunk_size)]
                for chunk in tqdm(chunks, desc="Inserting interactions"):
                    interaction_values = []
                    skills_values = []
                    
                    for index, interaction in chunk.iterrows():                    
                        cursor.execute("SELECT \"Id\" FROM \"Titles\" WHERE \"Name\" = %s;", (interaction['context_user_title'],))
                        title_id = cursor.fetchone()
                        if title_id is None:
                            title_id = cursor.execute("INSERT INTO \"Titles\" (\"Id\",\"Name\") VALUES (gen_random_uuid(), %s) RETURNING \"Id\";", (interaction['context_user_title'],)).fetchone()[0]
                        else:
                            title_id = title_id[0]
                        
                        cursor.execute("SELECT \"Id\" FROM \"Experiences\" WHERE \"Range\" = %s;", (interaction['context_user_experience'],))
                        experience_id = cursor.fetchone()
                        if experience_id is None:
                            experience_id = cursor.execute("INSERT INTO \"Experiences\" (\"Id\",\"Range\") VALUES (gen_random_uuid(), %s) RETURNING \"Id\";", (interaction['context_user_experience'],)).fetchone()[0]
                        else:
                            experience_id = experience_id[0]
            
                        cursor.execute("SELECT \"Id\" FROM \"Salaries\" WHERE \"Range\" = %s;", (interaction['context_user_salary'],))
                        salary_id = cursor.fetchone()
                        if salary_id is None:
                            salary_id = cursor.execute("INSERT INTO \"Salaries\" (\"Id\",\"Range\") VALUES (gen_random_uuid(), %s) RETURNING \"Id\";", (interaction['context_user_salary'],)).fetchone()[0]
                        else:
                            salary_id = salary_id[0]

                        label_skill_id = unique_skills_ids[interaction['label_skill']]

                        interaction_id = interaction_ids[index]
                        interaction_values.append(f"""
                            ('{interaction_id}', '{title_id}', '{experience_id}', '{salary_id}', '{label_skill_id}', NOW() AT TIME ZONE 'UTC')
                        """)

                        context_skill_ids = [unique_skills_ids[skill] for skill in interaction['context_skill']]
                        for context_skill_id in context_skill_ids:
                            skills_values.append(f"""
                                ('{interaction_id}', '{context_skill_id}')
                            """ )

                    interaction_query = f"""
                        INSERT INTO \"Interactions\" (
                            \"Id\", \"TitleId\", \"ExperienceId\", \"SalaryId\", \"LabelSkillId\", \"Created\"
                        ) VALUES {', '.join(interaction_values)}
                    """
                    cursor.execute(interaction_query)

                    skills_query = f"""
                        INSERT INTO \"InteractionSkill\" (
                            \"ContextInteractionsId\", \"ContextSkillsId\"
                        ) VALUES {', '.join(skills_values)}
                    """
                    cursor.execute(skills_query)
                    
                    connection.commit()

        print("Interactions and skills have been successfully inserted.")
