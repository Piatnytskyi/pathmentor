namespace PathMentor.Core.Entities
{
    public class Salary
    {
        public Guid Id { get; set; }
        public required string Range { get; set; }
        public required ICollection<Interaction> Interactions { get; set; }

    }
}