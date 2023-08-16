using System;
using System.Collections.Generic;
using Microsoft.AspNetCore.Identity;

namespace PathMentor.Data.Entities
{
    public class User : IdentityUser<Guid>
    {
        public SerializedRefreshJWTToken? SerializedRefreshJWTToken { get; set; }
    }
}
