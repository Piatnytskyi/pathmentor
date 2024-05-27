using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Metadata.Builders;
using PathMentor.Core.Entities;

public class Skillonfiguration : IEntityTypeConfiguration<Skill>
{
    public void Configure(EntityTypeBuilder<Skill> builder)
    {
        builder.HasIndex(e => e.Name).IsUnique();

        builder.HasMany(s => s.ContextInteractions)
            .WithMany(i => i.ContextSkills);

        builder.HasMany(s => s.LabelInteractions)
            .WithOne(i => i.LabelSkill)
            .HasForeignKey(i => i.LabelSkillId)
            .IsRequired();
    }
}