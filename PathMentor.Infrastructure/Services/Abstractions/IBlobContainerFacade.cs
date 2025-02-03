namespace PathMentor.Infrastructure.Services.Abstractions
{
    public interface IBlobContainerFacade
    {
        Task<Uri> UploadBlobAsync(string blobName, Stream stream, string? storedPolicyName = null);
    }
}