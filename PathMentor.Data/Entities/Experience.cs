using Microsoft.EntityFrameworkCore;

namespace PathMentor.Data.Entities
{
    [Index(nameof(Range), IsUnique = true)]
    public class Experience
    {
        public Guid Id { get; set; }
        public required string Range { get; set; }
        public required ICollection<Interaction> Interactions { get; set; }

    }
}