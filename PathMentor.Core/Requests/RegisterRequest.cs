using System.ComponentModel.DataAnnotations;

namespace PathMentor.Core.Requests
{
    public class RegisterRequest
    {
        [Required]
        [EmailAddress]
        [StringLength(254, MinimumLength = 3)]
        public string Email { get; set; }

        [Required]
        [StringLength(254, MinimumLength = 3)]
        public string UserName { get; set; }

        [Required]
        [StringLength(150)]
        public string FirstName { get; set; }

        [StringLength(150)]
        public string MiddleName { get; set; }

        [Required]
        [StringLength(150)]
        public string SurName { get; set; }

        [Required]
        [DataType(DataType.Password)]
        [StringLength(254, MinimumLength = 6)]
        public string Password { get; set; }

        [Required]
        [DataType(DataType.Password)]
        [Compare(nameof(Password))]
        public string ConfirmPassword { get; set; }
    }
}
