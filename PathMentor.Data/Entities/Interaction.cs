using System.ComponentModel.DataAnnotations.Schema;

namespace PathMentor.Data.Entities
{
    public class Interaction
    {
        public Guid Id { get; set; }

        public Guid TitleId { get; set; }

        public required Title Title { get; set; }

        public Guid ExperienceId { get; set; }

        public required Experience Experience { get; set; }

        public Guid SalaryId { get; set; }

        public required Salary Salary { get; set; }

        public required ICollection<Skill> ContextSkills { get; set; }

        public Guid LabelSkillId { get; set; }

        public required Skill LabelSkill { get; set; }

        [DatabaseGenerated(DatabaseGeneratedOption.Identity)]
        public DateTime Created { get; set; }
    }
}