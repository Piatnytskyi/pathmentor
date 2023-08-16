using PathMentor.Data.Models;

namespace PathMentor.Core.Responses
{
    public class AuthenticationTokensResponse
    {
        public SerializedJWTToken AccessToken { get; set; }
        public SerializedJWTToken RefreshToken { get; set; }
    }
}
