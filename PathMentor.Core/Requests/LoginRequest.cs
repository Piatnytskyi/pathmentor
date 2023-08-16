using System.ComponentModel.DataAnnotations;

namespace PathMentor.Core.Requests
{
    public class LoginRequest
    {
        [Required]
        [StringLength(254, MinimumLength = 3)]
        public string Username { get; set; }

        [Required]
        [DataType(DataType.Password)]
        [StringLength(254, MinimumLength = 6)]
        public string Password { get; set; }
    }
}
