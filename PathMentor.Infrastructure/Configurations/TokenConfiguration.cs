using System.ComponentModel.DataAnnotations;

namespace PathMentor.Infrastructure.Configurations
{
    public class TokenConfiguration
    {
        [Required]
        public string TokenSecret { get; set; }
        [Required]
        public double TokenExpirationMinutes { get; set; }
        [Required]
        public string Issuer { get; set; }
        [Required]
        public string Audience { get; set; }
    }
}
