from rest_framework.routers import DefaultRouter
from saakar.views import TypeViewSet, HeroViewSet, FightViewSet, RankingViewSet, DeadHeroViewSet

router = DefaultRouter()
router.register('GlobalRanking', RankingViewSet, 'GlobalRanking')
router.register('DeadHeroes', DeadHeroViewSet, 'DeadHeroes')
router.register('Type', TypeViewSet)
router.register('Hero', HeroViewSet)
router.register('Fight', FightViewSet)
