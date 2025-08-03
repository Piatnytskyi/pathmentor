class SkillsPredictionQuery:
    def __init__(
        self,
        skills: list[str],
        title: str,
        experience: str,
        salary: str,
        count: int = 10
    ):
        self.skills = skills
        self.title = title
        self.experience = experience
        self.salary = salary
        self.count = count
