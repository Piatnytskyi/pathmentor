using System;
using System.ComponentModel.DataAnnotations;

namespace PathMentor.Data.Models
{
    public class SerializedJWTToken
    {
        [Required]
        [StringLength(500)]
        public string Value { get; set; }
        public DateTime ExpirationTime { get; set; }
    }
}
