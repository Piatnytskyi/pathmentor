using Azure.Storage.Blobs;
using Azure.Storage.Sas;
using PathMentor.Infrastructure.Services.Abstractions;

namespace PathMentor.Infrastructure.Services.Implementations
{
    public class BlobContainerFacade : IBlobContainerFacade
    {
        private readonly BlobContainerClient _blobContainerClient;

        public string Name {
            get => _blobContainerClient.Name;
        }

        public Uri Uri {
            get => _blobContainerClient.Uri;
        }   

        public BlobContainerFacade(BlobContainerClient blobContainerClient)
        {
            _blobContainerClient = blobContainerClient;
            _blobContainerClient.CreateIfNotExists();
        }

        public Uri GenerateSasUri(BlobContainerSasPermissions permissions, DateTimeOffset expiresOn = default)
        {
            BlobSasBuilder sasBuilder = new BlobSasBuilder()
            {
                BlobContainerName = _blobContainerClient.Name,
                Resource = "c"
            };

            if (expiresOn == default)
                expiresOn = DateTimeOffset.UtcNow.AddHours(1);
                
            sasBuilder.ExpiresOn = expiresOn;
            sasBuilder.SetPermissions(permissions);

            return _blobContainerClient.GenerateSasUri(sasBuilder);
        }

        public async Task<Uri> UploadBlobAsync(string blobName, string filePath, bool overwrite = true, string? storedPolicyName = null)
        {
            BlobClient blobClient = _blobContainerClient.GetBlobClient(blobName);
            await blobClient.UploadAsync(filePath, overwrite);

            if (blobClient.CanGenerateSasUri)
            {
                BlobSasBuilder sasBuilder = new BlobSasBuilder()
                {
                    BlobContainerName = _blobContainerClient.Name,
                    BlobName = blobClient.Name,
                    Resource = "b"
                };

                if (storedPolicyName == null)
                {
                    sasBuilder.ExpiresOn = DateTimeOffset.UtcNow.AddHours(1);
                    sasBuilder.SetPermissions(BlobContainerSasPermissions.Read);
                }
                else
                {
                    sasBuilder.Identifier = storedPolicyName;
                }

                return blobClient.GenerateSasUri(sasBuilder);
            }
            else
            {
                throw new InvalidOperationException("BlobClient must be authorized with shared key credentials to create a service SAS.");
            }
        }
    }
}