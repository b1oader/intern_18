from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet, GenericViewSet
from rest_framework.permissions import IsAdminUser, AllowAny
from .serializers import TypeSerializer, HeroSerializer, FightSerializer, RankingSerializer, DeadHeroSerializer
from .models import Type, Hero, Fight
from rest_framework.mixins import CreateModelMixin, ListModelMixin, RetrieveModelMixin, DestroyModelMixin


class CustomModelViewSet(CreateModelMixin,
                                ListModelMixin,
                                RetrieveModelMixin,
                                DestroyModelMixin,
                                GenericViewSet):
    """
    Custom viewset with create, list, retrieve and destroy actions.
    """
    pass


class TypeViewSet(ModelViewSet):
    """
    Type CRUD, for admin user.
    """
    permission_classes = (IsAdminUser,)
    serializer_class = TypeSerializer
    queryset = Type.objects.all()


class HeroViewSet(ModelViewSet):
    """
    Hero CRUD, for admin user.
    """
    permission_classes = (IsAdminUser,)
    serializer_class = HeroSerializer
    queryset = Hero.objects.all()


class FightViewSet(CustomModelViewSet):
    """
    Fight create, read, delete, for admin user.
    """
    permission_classes = (IsAdminUser,)
    serializer_class = FightSerializer
    queryset = Fight.objects.all()


class RankingViewSet(ReadOnlyModelViewSet):
    """
    Global ranking heroes, readonly, for any user.
    """
    permission_classes = (AllowAny,)
    serializer_class = RankingSerializer
    queryset = Hero.objects.all().order_by('-won_matches', 'lost_matches')


class DeadHeroViewSet(ReadOnlyModelViewSet):
    """
    List of dead heroes with death date, readonly, for admin user.
    """
    permission_classes = (IsAdminUser,)
    serializer_class = DeadHeroSerializer
    queryset = Hero.objects.filter(existence=False).order_by('-won_matches', 'lost_matches')