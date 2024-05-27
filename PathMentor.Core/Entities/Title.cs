namespace PathMentor.Core.Entities
{
    public class Title
    {
        public Guid Id { get; set; }
        public required string Name { get; set; }
        public required ICollection<Interaction> Interactions { get; set; }

    }
}