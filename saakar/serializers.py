from django.db.models import Q
from rest_framework.serializers import (
                                    HyperlinkedModelSerializer, 
                                    PrimaryKeyRelatedField, 
                                    ValidationError, 
                                    HyperlinkedRelatedField,
                                    ModelSerializer,
                                    StringRelatedField,
                                    SerializerMethodField,
                                    DateTimeField,
                                    BooleanField
                                    )
from .models import Type, Hero, Fight


class TypeSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = Type
        fields = ['id', 'name']


class HeroSerializer(HyperlinkedModelSerializer):
    existence = BooleanField(initial=True)
    class Meta:
        model = Hero
        fields = ['id', 'first_name', 'last_name', 'hero_type', 'won_matches', 'lost_matches', 'existence']
        

class FightSerializer(HyperlinkedModelSerializer):
    hero_1 = HyperlinkedRelatedField(queryset=Hero.objects.filter(existence=True), view_name='hero-detail', read_only=False)
    hero_2 = HyperlinkedRelatedField(queryset=Hero.objects.filter(existence=True), view_name='hero-detail', read_only=False)
    fight_date = DateTimeField(format="%Y-%m-%d %H:%M:%S")
    class Meta:
        model = Fight
        fields = ['id', 'hero_1', 'hero_2', 'result', 'fight_date', 'kill_loser']

    def validate(self, data):
        instance = Fight(**data)
        instance.clean()
        return data

class RankingSerializer(ModelSerializer):
    hero_type = StringRelatedField()
    full_name = SerializerMethodField('get_fullname')

    def get_fullname(self, obj):
        if obj.last_name != '':
            full_name = f'{obj.first_name} {obj.last_name}'
        else:
            full_name = obj.first_name
        return full_name

    class Meta:
        model = Hero
        fields = ['full_name', 'hero_type', 'won_matches', 'lost_matches']


class DeadHeroSerializer(HyperlinkedModelSerializer):
    dead_date = SerializerMethodField('get_lostdate')

    def get_lostdate(self, obj):
        try:
            hero_fights = Fight.objects.filter(Q(hero_1=obj)|Q(hero_2=obj))
            lastfight_date = hero_fights.latest('fight_date').fight_date.strftime("%Y-%m-%d %H:%M:%S")
        except Fight.DoesNotExist:
            lastfight_date = None
        return lastfight_date

    class Meta:
        model = Hero
        fields = ['first_name', 'last_name', 'hero_type', 'won_matches', 'lost_matches', 'dead_date']