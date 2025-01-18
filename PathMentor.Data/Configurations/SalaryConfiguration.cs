using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Metadata.Builders;
using PathMentor.Core.Entities;

public class SalaryConfiguration : IEntityTypeConfiguration<Salary>
{
    public void Configure(EntityTypeBuilder<Salary> builder)
    {
        builder.Property(s => s.Range).HasMaxLength(100).IsRequired();
        builder.HasIndex(s => s.Range).IsUnique();
    }
}