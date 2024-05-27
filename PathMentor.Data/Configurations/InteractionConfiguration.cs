using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Metadata.Builders;
using PathMentor.Core.Entities;

public class InteractionConfiguration : IEntityTypeConfiguration<Interaction>
{
    public void Configure(EntityTypeBuilder<Interaction> builder)
    {
        builder.HasMany(i => i.ContextSkills)
            .WithMany(s => s.ContextInteractions);

        builder.HasOne(i => i.LabelSkill)
            .WithMany(s => s.LabelInteractions)
            .HasForeignKey(i => i.LabelSkillId)
            .IsRequired();
    }
}