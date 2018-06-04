from rest_framework.routers import DefaultRouter
from saakar.views import TypeViewSet, HeroViewSet, FightViewSet

router = DefaultRouter()
router.register('Type',TypeViewSet)
router.register('Hero',HeroViewSet)
router.register('Fight',FightViewSet)