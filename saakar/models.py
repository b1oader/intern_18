from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError


class Type(models.Model):
    name = models.CharField(max_length=20, blank=False)

    def __str__(self):
        return self.name


class Hero(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20, blank=True)
    hero_type = models.ForeignKey(Type, on_delete=models.CASCADE)
    won_matches = models.PositiveSmallIntegerField(default=0)
    lost_matches = models.PositiveSmallIntegerField(default=0)
    existence = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}({self.hero_type})'


class FightQuerySet(models.QuerySet):

    def delete(self, *args, **kwargs):
        for obj in self:
            first_hero = Hero.objects.get(id=obj.hero_1.id)
            second_hero = Hero.objects.get(id=obj.hero_2.id)
            if obj.result == 'H1':
                first_hero.won_matches -= 1
                second_hero.lost_matches -= 1
                if obj.kill_loser is True:
                    second_hero.existence = True
            else:
                second_hero.won_matches -= 1
                first_hero.lost_matches -= 1
                if obj.kill_loser is True:
                    first_hero.existence = True
            first_hero.save()
            second_hero.save()
        super(FightQuerySet, self).delete(*args, **kwargs)


class Fight(models.Model):
    RESULTS = (
        ('H1', 'Hero 1 won'),
        ('H2', 'Hero 2 won'),
    )
    hero_1 = models.ForeignKey(Hero, related_name='hero_1', limit_choices_to={'existence': True})
    hero_2 = models.ForeignKey(Hero, related_name='hero_2', limit_choices_to={'existence': True})
    result = models.CharField(max_length=2, choices=RESULTS)
    fight_date = models.DateTimeField(default=timezone.now)
    kill_loser = models.BooleanField(default=False)
    objects = FightQuerySet.as_manager()

    def __str__(self):
        return f'{self.hero_1} vs {self.hero_2}'
    
    def clean(self):
        fights_straight = Fight.objects.filter(hero_1=self.hero_1, hero_2=self.hero_2)
        fights_reverse = Fight.objects.filter(hero_1=self.hero_2, hero_2=self.hero_1)
        if self.hero_1.hero_type != self.hero_2.hero_type:
            raise ValidationError('Heroes type must be the same')
        if self.hero_1 == self.hero_2:
            raise ValidationError('Heroes must be different')
        if fights_straight or fights_reverse:
            raise ValidationError('Fight already exists')
        
    def save(self, *args, **kwargs):
        first_hero = Hero.objects.get(id=self.hero_1.id)
        second_hero = Hero.objects.get(id=self.hero_2.id)
        if self.result == 'H1':
            first_hero.won_matches += 1
            second_hero.lost_matches += 1
            if self.kill_loser is True:
                second_hero.existence = False
        else:
            second_hero.won_matches += 1
            first_hero.lost_matches += 1
            if self.kill_loser is True:
                first_hero.existence = False
        first_hero.save()
        second_hero.save()
        super(Fight, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        first_hero = Hero.objects.get(id=self.hero_1.id)
        second_hero = Hero.objects.get(id=self.hero_2.id)
        if self.result == 'H1':
            first_hero.won_matches -= 1
            second_hero.lost_matches -= 1
            if self.kill_loser is True:
                second_hero.existence = True
        else:
            second_hero.won_matches -= 1
            first_hero.lost_matches -= 1
            if self.kill_loser is True:
                first_hero.existence = True
        first_hero.save()
        second_hero.save()
        super(Fight, self).delete(*args, **kwargs)
