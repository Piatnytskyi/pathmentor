using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;
using Microsoft.Azure.Functions.Worker;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.Logging;

namespace PathMentor.Functions
{
    public class PathMentorTrainHttpTrigger
    {
        private readonly ILogger<PathMentorTrainHttpTrigger> _logger;
        private readonly IConfiguration _configuration;

        public PathMentorTrainHttpTrigger(
            ILogger<PathMentorTrainHttpTrigger> logger,
            IConfiguration configuration)
        {
            _logger = logger;
            _configuration = configuration;
        }

        [Function(nameof(PathMentorTrainHttpTrigger))]
        public async Task<IActionResult> Run([HttpTrigger(AuthorizationLevel.Function, "get")] HttpRequest req)
        {
            
            return new OkResult();
        }
    }
}
