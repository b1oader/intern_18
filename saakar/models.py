from django.db import models
from django.utils import timezone


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
        return self.first_name + ' ' + self.last_name


class Fight(models.Model):
    RESULTS = (
        ('H1', 'Hero 1 won'),
        ('H2', 'Hero 2 won'),
    )
    hero_1 = models.ForeignKey(Hero, related_name='hero_1')
    hero_2 = models.ForeignKey(Hero, related_name='hero_2')
    result = models.CharField(max_length=2, choices=RESULTS)
    fight_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.hero_1} vs {self.hero_2}'
    
    def save(self, *args, **kwargs):
        first_hero = Hero.objects.get(id=self.hero_1.id)
        second_hero = Hero.objects.get(id=self.hero_2.id)
        if self.result == 'H1':
            first_hero.won_matches += 1
            second_hero.lost_matches += 1
        else:
            second_hero.won_matches += 1
            first_hero.lost_matches += 1
        first_hero.save()
        second_hero.save()
        super(Fight, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        first_hero = Hero.objects.get(id=self.hero_1.id)
        second_hero = Hero.objects.get(id=self.hero_2.id)
        if self.result == 'H1':
            first_hero.won_matches -= 1
            second_hero.lost_matches -= 1
        else:
            second_hero.won_matches -= 1
            first_hero.lost_matches -= 1
        first_hero.save()
        second_hero.save()
        super(Fight, self).delete(*args, **kwargs)
