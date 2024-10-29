using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Metadata.Builders;
using PathMentor.Core.Entities;

public class TitleConfiguration : IEntityTypeConfiguration<Title>
{
    public void Configure(EntityTypeBuilder<Title> builder)
    {
        builder.HasIndex(e => e.Name).IsUnique();
    }
}