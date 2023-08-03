using System.ComponentModel.DataAnnotations;

namespace PathMentor.Infrastructure.Configurations
{
    public class AuthenticationConfiguration
    {
        [Required]
        public TokenConfiguration AccessToken { get; set; }

        public TokenConfiguration RefreshToken { get; set; }
    }
}
