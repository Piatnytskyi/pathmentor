using Microsoft.EntityFrameworkCore;

namespace PathMentor.Data.Entities
{
    [Index(nameof(Name), IsUnique = true)]
    public class Title
    {
        public Guid Id { get; set; }
        public required string Name { get; set; }
        public required ICollection<Interaction> Interactions { get; set; }

    }
}