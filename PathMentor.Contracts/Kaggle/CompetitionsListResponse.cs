namespace PathMentor.Contracts.Kaggle
{
    public class CompetitionsListResponse
    {
        public required List<CompetitionResponse> Files { get; set; }
        public string? NextPageToken { get; set; }
    }
}