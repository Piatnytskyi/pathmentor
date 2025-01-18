using Microsoft.Azure.Batch;

namespace PathMentor.Infrastructure.Configurations
{
    public class AzureBatchOptions
    {
        public required string BaseUrl { get; set; }
        public required string AccountName { get; set; }
        public required string KeyValue { get; set; }
        public required CloudPool CloudPool { get; set; }
    }
}
