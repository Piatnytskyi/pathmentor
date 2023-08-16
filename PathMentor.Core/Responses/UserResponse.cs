namespace PathMentor.Core.Responses
{
    public class UserResponse
    {
        public Guid Id { get; set; }

        public string UserName { get; set; }

        public string Email { get; set; }

        public bool EmailConfirmed { get; set; }
    }
}
