from rest_framework.viewsets import ModelViewSet
from .serializers import TypeSerializer, HeroSerializer, FightSerializer
from .models import Type, Hero, Fight


class TypeViewSet(ModelViewSet):
    serializer_class = TypeSerializer
    queryset = Type.objects.all()


class HeroViewSet(ModelViewSet):
    serializer_class = HeroSerializer
    queryset = Hero.objects.all()


class FightViewSet(ModelViewSet):
    serializer_class = FightSerializer
    queryset = Fight.objects.all()