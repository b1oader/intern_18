from rest_framework.serializers import HyperlinkedModelSerializer, PrimaryKeyRelatedField, ValidationError, HyperlinkedRelatedField
from .models import Type, Hero, Fight


class TypeSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = Type
        fields = ['id', 'name']


class HeroSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = Hero
        fields = ['id', 'first_name', 'last_name', 'hero_type', 'won_matches', 'lost_matches', 'existence']
        

class FightSerializer(HyperlinkedModelSerializer):
    hero_1 = HyperlinkedRelatedField(queryset=Hero.objects.filter(existence=True), view_name='hero-detail', read_only=False)
    hero_2 = HyperlinkedRelatedField(queryset=Hero.objects.filter(existence=True), view_name='hero-detail', read_only=False)

    class Meta:
        model = Fight
        fields = ['id', 'hero_1', 'hero_2', 'result', 'fight_date', 'kill_loser']

    def validate(self, data):
        instance = Fight(**data)
        instance.clean()
        return data
        