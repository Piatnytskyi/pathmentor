import pandas as pd
import psycopg
from sklearn.model_selection import train_test_split
from tqdm import tqdm

class PathMentorDatabaseStager:
    def stage(self, connection_string: str) -> None:
        with psycopg.connect(connection_string) as connection:
            with connection.cursor() as cursor:
                cursor.execute("""
                    CREATE SCHEMA IF NOT EXISTS staging
                """)

                for table in ['train_interactions', 'test_interactions']:
                    cursor.execute(f"""
                        DROP TABLE IF EXISTS staging.{table} CASCADE
                    """)
                    cursor.execute(f"""
                        DROP TABLE IF EXISTS staging.{table}Skill CASCADE
                    """)

                connection.commit()

                for table in ['train_interactions', 'test_interactions']:
                    cursor.execute(f"""
                        CREATE TABLE IF NOT EXISTS staging.{table} (
                            "Id" uuid PRIMARY KEY,
                            "TitleId" uuid NOT NULL,
                            "ExperienceId" uuid NOT NULL,
                            "SalaryId" uuid NOT NULL,
                            "LabelSkillId" uuid NOT NULL,
                            "Created" timestamp with time zone NOT NULL,
                            CONSTRAINT "FK_{table}_Experiences_ExperienceId" FOREIGN KEY ("ExperienceId") REFERENCES "Experiences" ("Id") ON DELETE CASCADE,
                            CONSTRAINT "FK_{table}_Salaries_SalaryId" FOREIGN KEY ("SalaryId") REFERENCES "Salaries" ("Id") ON DELETE CASCADE,
                            CONSTRAINT "FK_{table}_Skills_LabelSkillId" FOREIGN KEY ("LabelSkillId") REFERENCES "Skills" ("Id") ON DELETE CASCADE,
                            CONSTRAINT "FK_{table}_Titles_TitleId" FOREIGN KEY ("TitleId") REFERENCES "Titles" ("Id") ON DELETE CASCADE
                        )
                    """)

                    cursor.execute(f"""
                        CREATE TABLE IF NOT EXISTS staging.{table}Skill (
                            "ContextInteractionsId" UUID,
                            "ContextSkillsId" UUID,
                            PRIMARY KEY ("ContextInteractionsId", "ContextSkillsId"),
                            CONSTRAINT "FK_{table}Skill_{table}_ContextInteractionsId" FOREIGN KEY ("ContextInteractionsId") REFERENCES staging.{table} ("Id") ON DELETE CASCADE,
                            CONSTRAINT "FK_{table}Skill_Skills_ContextSkillsId" FOREIGN KEY ("ContextSkillsId") REFERENCES "Skills" ("Id") ON DELETE CASCADE
                        )
                    """)

                connection.commit()

                cursor.execute("""
                    SELECT "Id", "Name" FROM "Titles"
                """)
                titles_df = pd.DataFrame(cursor.fetchall(), columns=[desc[0] for desc in cursor.description])

                cursor.execute("""
                    SELECT "Id", "Range" FROM "Experiences"
                """)
                experiences_df = pd.DataFrame(cursor.fetchall(), columns=[desc[0] for desc in cursor.description])

                cursor.execute("""
                    SELECT "Id", "Range" FROM "Salaries"
                """)
                salaries_df = pd.DataFrame(cursor.fetchall(), columns=[desc[0] for desc in cursor.description])

                cursor.execute("""
                    SELECT "Id", "Name" FROM "Skills"
                """)
                skills_df = pd.DataFrame(cursor.fetchall(), columns=[desc[0] for desc in cursor.description])

                train_latest_entry = cursor.execute("""SELECT MAX("Created") FROM staging.train_interactions""").fetchone()
                test_latest_entry = cursor.execute("""SELECT MAX("Created") FROM staging.test_interactions""").fetchone()

                latest_created = max(train_latest_entry[0], test_latest_entry[0]) if train_latest_entry[0] and test_latest_entry[0] else None

                print("Latest latest created in stage:", latest_created)

                select_interactions_query = """
                    SELECT t."Name" as context_user_title, 
                        e."Range" as context_user_experience, 
                        s."Range" as context_user_salary,
                        sk."Name" as label_skill,
                        array_agg(cs."Name") as context_skills
                    FROM "Interactions" i
                    JOIN "Titles" t ON i."TitleId" = t."Id"
                    JOIN "Experiences" e ON i."ExperienceId" = e."Id"
                    JOIN "Salaries" s ON i."SalaryId" = s."Id"
                    JOIN "Skills" sk ON i."LabelSkillId" = sk."Id"
                    LEFT JOIN "InteractionSkill" ints ON i."Id" = ints."ContextInteractionsId"
                    LEFT JOIN "Skills" cs ON ints."ContextSkillsId" = cs."Id"
                    GROUP BY i."Id", t."Id", e."Id", s."Id", sk."Id"
                """
                if latest_created is not None:
                    select_interactions_query += """ WHERE i."Created" > %s"""
                    cursor.execute(select_interactions_query, (latest_created,))
                else:
                    cursor.execute(select_interactions_query)
                interactions_df = pd.DataFrame(cursor.fetchall(), columns=[desc[0] for desc in cursor.description])

                print("Interactions found:", len(interactions_df))
                if len(interactions_df) == 0:
                    print("No interactions found. Ending script.")
                    exit()

                print("Interactions head:")
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

                train_records = train_df.to_dict(orient='records')
                test_records = test_df.to_dict(orient='records')

                def insert_records(records, table):
                    for record in tqdm(records, desc=f'Inserting into {table}'):
                        interaction_id = cursor.execute(f"""
                            INSERT INTO staging.{table} ("Id", "Created", "TitleId", "ExperienceId", "SalaryId", "LabelSkillId")
                            VALUES (gen_random_uuid(), NOW() AT TIME ZONE 'UTC', %s, %s, %s, %s) RETURNING \"Id\";
                        """, (titles_df[titles_df['Name'] == record['context_user_title']].iloc[0]['Id'],
                              experiences_df[experiences_df['Range'] == record['context_user_experience']].iloc[0]['Id'],
                              salaries_df[salaries_df['Range'] == record['context_user_salary']].iloc[0]['Id'],
                              skills_df[skills_df['Name'] == record['label_skill']].iloc[0]['Id'],)).fetchone()[0]

                        for skill in record['context_skills']:
                            cursor.execute(f"""
                                INSERT INTO staging.{table}Skill ("ContextInteractionsId", "ContextSkillsId")
                                VALUES (%s, %s)
                            """, (interaction_id, skills_df[skills_df['Name'] == skill].iloc[0]['Id']))

                        connection.commit()

                insert_records(train_records, 'train_interactions')
                insert_records(test_records, 'test_interactions')

                print("Train and test interactions inserted into staging database")
