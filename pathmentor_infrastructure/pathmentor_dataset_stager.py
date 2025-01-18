import pandas as pd
import psycopg
from sklearn.model_selection import train_test_split

class PathMentorDatasetStager:
    def stage(self, connection_string: str) -> None:
        with psycopg.connect(connection_string) as connection:
            with connection.cursor() as cursor:
                cursor.execute("""
                    CREATE SCHEMA IF NOT EXISTS staging
                """)

                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS staging.Titles (
                        Id UUID PRIMARY KEY,
                        Name VARCHAR(100),
                        CONSTRAINT "PK_Titles" PRIMARY KEY ("Id")
                    )
                """)
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS staging.Experiences (
                        Id UUID PRIMARY KEY,
                        Range VARCHAR(100),
                        CONSTRAINT "PK_Experiences" PRIMARY KEY ("Id")
                    )
                """)
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS staging.Salaries (
                        Id UUID PRIMARY KEY,
                        Range VARCHAR(100),
                        CONSTRAINT "PK_Salaries" PRIMARY KEY ("Id")
                    )
                """)
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS staging.Skills (
                        Id UUID PRIMARY KEY,
                        Name VARCHAR(100),
                        CONSTRAINT "PK_Skills" PRIMARY KEY ("Id")    
                    )
                """)
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS staging.InteractionSkill (
                        ContextInteractionsId UUID,
                        ContextSkillsId UUID,
                        PRIMARY KEY (ContextInteractionsId, ContextSkillsId)
                        CONSTRAINT "PK_InteractionSkill" PRIMARY KEY ("ContextInteractionsId", "ContextSkillsId"),
                        CONSTRAINT "FK_InteractionSkill_Interactions_ContextInteractionsId" FOREIGN KEY ("ContextInteractionsId") REFERENCES "Interactions" ("Id") ON DELETE CASCADE,
                        CONSTRAINT "FK_InteractionSkill_Skills_ContextSkillsId" FOREIGN KEY ("ContextSkillsId") REFERENCES "Skills" ("Id") ON DELETE CASCADE
                    )
                """)

                for table in ['staging.train_interactions', 'staging.test_interactions']:
                    cursor.execute(f"""
                        CREATE TABLE IF NOT EXISTS {table} (
                            "Id" uuid NOT NULL,
                            "TitleId" uuid NOT NULL,
                            "ExperienceId" uuid NOT NULL,
                            "SalaryId" uuid NOT NULL,
                            "LabelSkillId" uuid NOT NULL,
                            "Created" timestamp with time zone NOT NULL,
                            CONSTRAINT "PK_Interactions" PRIMARY KEY ("Id"),
                            CONSTRAINT "FK_Interactions_Experiences_ExperienceId" FOREIGN KEY ("ExperienceId") REFERENCES "Experiences" ("Id") ON DELETE CASCADE,
                            CONSTRAINT "FK_Interactions_Salaries_SalaryId" FOREIGN KEY ("SalaryId") REFERENCES "Salaries" ("Id") ON DELETE CASCADE,
                            CONSTRAINT "FK_Interactions_Skills_LabelSkillId" FOREIGN KEY ("LabelSkillId") REFERENCES "Skills" ("Id") ON DELETE CASCADE,
                            CONSTRAINT "FK_Interactions_Titles_TitleId" FOREIGN KEY ("TitleId") REFERENCES "Titles" ("Id") ON DELETE CASCADE
                        )
                    """)
                connection.commit()

                train_latest_entry = cursor.execute("SELECT MAX(Created) FROM staging.train_interactions").fetchone()
                test_latest_entry = cursor.execute("SELECT MAX(Created) FROM staging.test_interactions").fetchone()

                latest_created = max(train_latest_entry[0], test_latest_entry[0]) if train_latest_entry[0] and test_latest_entry[0] else None

                print("Latest latest created in stage:", latest_created)

                select_interactions_query = """
                    SELECT i.*, 
                        t.Name as context_user_title, 
                        e.Range as context_user_experience, 
                        s.Range as context_user_salary, 
                        sk.Name as label_skill
                    FROM Interactions i
                    JOIN Titles t ON i.TitleId = t.Id
                    JOIN Experiences e ON i.ExperienceId = e.Id
                    JOIN Salaries s ON i.SalaryId = s.Id
                    JOIN Skills sk ON i.LabelSkillId = sk.Id
                """
                if latest_created is not None:
                    select_interactions_query += " WHERE i.Created > %s"
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

                cursor.execute("""
                    INSERT INTO staging.Titles (Id, Name)
                    SELECT Id, Name FROM Titles
                    WHERE Id NOT IN (SELECT Id FROM staging.Titles)
                """)
                cursor.execute("""
                    INSERT INTO staging.Experiences (Id, Range)
                    SELECT Id, Range FROM Experiences
                    WHERE Id NOT IN (SELECT Id FROM staging.Experiences)
                """)
                cursor.execute("""
                    INSERT INTO staging.Salaries (Id, Range)
                    SELECT Id, Range FROM Salaries
                    WHERE Id NOT IN (SELECT Id FROM staging.Salaries)
                """)
                cursor.execute("""
                    INSERT INTO staging.Skills (Id, Name)
                    SELECT Id, Name FROM Skills
                    WHERE Id NOT IN (SELECT Id FROM staging.Skills)
                """)
                cursor.execute("""
                    INSERT INTO staging.InteractionSkill (ContextInteractionsId, ContextSkillsId)
                    SELECT ContextInteractionsId, ContextSkillsId FROM InteractionSkill
                    WHERE ContextInteractionsId NOT IN (SELECT ContextInteractionsId FROM staging.InteractionSkill)
                """)
                
                connection.commit()

                train_records = train_df.to_dict(orient='records')
                test_records = test_df.to_dict(orient='records')

                def insert_records(records, table_name):
                    for record in records:
                        cursor.execute(f"""
                            INSERT INTO {table_name} (Id, Created, TitleId, ExperienceId, SalaryId, LabelSkillId)
                            VALUES (%s, %s, %s, %s, %s, %s)
                        """, (record['id'], record['created'], record['titleid'], record['experienceid'], record['salaryid'], record['labelskillid']))

                insert_records(train_records, 'staging.train_interactions')
                insert_records(test_records, 'staging.test_interactions')

                connection.commit()

                print("Train and test interactions inserted into staging database")
