using Azure.Storage.Sas;

namespace PathMentor.Infrastructure.Services.Abstractions
{
    public interface IBlobContainerFacade
    {
        public string Name { get; }
        public Uri Uri { get; }
        public Uri GenerateSasUri(BlobContainerSasPermissions permissions, DateTimeOffset expiresOn = default);
        Task<Uri> UploadBlobAsync(string blobName, string filePath, bool overwrite = true, string? storedPolicyName = null);
    }
}