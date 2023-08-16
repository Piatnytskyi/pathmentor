using System.ComponentModel;
using System.ComponentModel.DataAnnotations;

namespace PathMentor.Core.Requests
{
    public class PaginationRequest
    {
        [DefaultValue(1)]
        [Required]
        public int Page { get; set; }

        [DefaultValue(10)]
        [Required]
        public int Count { get; set; }
    }
}
