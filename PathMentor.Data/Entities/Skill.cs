using Microsoft.EntityFrameworkCore;

namespace PathMentor.Data.Entities
{
    [Index(nameof(Name), IsUnique = true)]
    public class Skill
    {
        public Guid Id { get; set; }
        public required string Name { get; set; }
        public required ICollection<Interaction> ContextInteractions { get; set; }
        public required ICollection<Interaction> LabelInteractions { get; set; }

    }
}