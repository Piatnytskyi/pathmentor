namespace PathMentor.Contracts.Kaggle.Responses
{
    public class CompetitionResponse
    {
        public string? NameNullable { get; set; }
        public string? DescriptionNullable { get; set; }
        public string? UrlNullable { get; set; }
        public required string Ref { get; set; }
        public required string Name { get; set; }
        public bool HasName { get; set; }
        public required string Description { get; set; }
        public bool HasDescription { get; set; }
        public int TotalBytes { get; set; }
        public required string Url { get; set; }
        public bool HasUrl { get; set; }
        public DateTime CreationDate { get; set; }
    }
}