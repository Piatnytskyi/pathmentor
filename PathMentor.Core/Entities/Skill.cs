namespace PathMentor.Core.Entities
{
    public class Skill
    {
        public Guid Id { get; set; }
        public required string Name { get; set; }
        public required ICollection<Interaction> ContextInteractions { get; set; }
        public required ICollection<Interaction> LabelInteractions { get; set; }
    }
}