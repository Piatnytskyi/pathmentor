using PathMentor.Data.Models;
using System;
using System.ComponentModel.DataAnnotations;

namespace PathMentor.Data.Entities
{
    public class SerializedRefreshJWTToken : SerializedJWTToken
    {
        [Key]
        public Guid Id { get; set; }

        public Guid UserId { get; set; }
        public User User { get; set; }
    }
}
