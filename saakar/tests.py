from django.test import TestCase
from .models import Hero, Type, Fight
from django.core.exceptions import ValidationError


class TypeTestCase(TestCase):

    def test_str_representation(self):
        test_obj = Type(name="ExampleTypeName")
        self.assertEqual(str(test_obj), test_obj.name)

class HeroTestCase(TestCase):

    def test_str_representation(self):
        Type.objects.create(name="Human")
        test_obj1 = Hero(first_name="John", last_name="Smith", hero_type_id=1)
        self.assertEqual(str(test_obj1), f'{test_obj1.first_name} {test_obj1.last_name}({test_obj1.hero_type})')


class FightTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        Type.objects.create(name="Human")
        Type.objects.create(name="Alien")
        Hero.objects.create(first_name="John", last_name="Smith", hero_type_id=1)
        Hero.objects.create(first_name="Joe", last_name="Dee", hero_type_id=2)
        
    def test_str_representation(self):
        test_obj1 = Fight(hero_1_id=1, hero_2_id=2)
        self.assertEqual(str(test_obj1), f'{test_obj1.hero_1} vs {test_obj1.hero_2}')


class FightCleanTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        Type.objects.create(name="Human")
        Type.objects.create(name="Alien")
        Hero.objects.create(first_name="John", last_name="Smith", hero_type_id=1)
        Hero.objects.create(first_name="Joe", last_name="Dee", hero_type_id=2)
        Hero.objects.create(first_name="Johny", last_name="Bravo", hero_type_id=1)

    def test_adding_the_same_heroes(self):
        instance = Fight(hero_1_id=1, hero_2_id=1)
        try:
            instance.full_clean()
            self.fail('Validation error should be raised')
        except ValidationError as a:
            self.assertEquals('Heroes must be different', ''.join(a.messages))

    def test_adding_heroes_with_different_type(self):
        instance = Fight(hero_1_id=1, hero_2_id=2)
        try:
            instance.full_clean()
            self.fail('Validation error should be raised')
        except ValidationError as a:
            self.assertEquals('Heroes type must be the same', ''.join(a.messages))

    def test_adding_heroes_if_fight_exists_straight(self):
        Fight.objects.create(hero_1_id=1, hero_2_id=3)
        instance = Fight(hero_1_id=1, hero_2_id=3)
        try:
            instance.full_clean()
            self.fail('Validation error should be raised')
        except ValidationError as a:
            self.assertEquals('Fight already exists', ''.join(a.messages)) 
    
    def test_adding_heroes_if_fight_exists_reverse(self):
        Fight.objects.create(hero_1_id=3, hero_2_id=1)
        instance = Fight(hero_1_id=1, hero_2_id=3)
        try:
            instance.full_clean()
            self.fail('Validation error should be raised')
        except ValidationError as a:
            self.assertEquals('Fight already exists', ''.join(a.messages))


class WonLostMatchesTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        Type.objects.create(name="Human")
        Type.objects.create(name="Alien")
        Hero.objects.create(first_name="John", last_name="Smith", hero_type_id=1)
        Hero.objects.create(first_name="Joe", last_name="Dee", hero_type_id=2)
        Hero.objects.create(first_name="Johny", last_name="Bravo", hero_type_id=1)
        Hero.objects.create(first_name="Billy", last_name="Kidman", hero_type_id=2)
        Fight.objects.create(hero_1_id=1, hero_2_id=3, result="H1")
        Fight.objects.create(hero_1_id=2, hero_2_id=4, result="H2")
    
    def test_save_method_addition_won_lost_matches_with_h1_result(self):
        test_obj1 = Hero.objects.get(id=1)
        test_obj2 = Hero.objects.get(id=3)
        self.assertEquals([1, 0], [test_obj1.won_matches, test_obj1.lost_matches])
        self.assertEquals([0, 1], [test_obj2.won_matches, test_obj2.lost_matches])

    def test_save_method_addition_won_lost_matches_with_h2_result(self):
        test_obj1 = Hero.objects.get(id=2)
        test_obj2 = Hero.objects.get(id=4)
        self.assertEquals([0, 1], [test_obj1.won_matches, test_obj1.lost_matches])
        self.assertEquals([1, 0], [test_obj2.won_matches, test_obj2.lost_matches])
    
    def test_delete_method_subtraction_won_lost_matches_with_h1_result(self):
        Fight.objects.get(id=1).delete()
        test_obj1 = Hero.objects.get(id=1)
        test_obj2 = Hero.objects.get(id=3)
        self.assertEquals([0, 0], [test_obj1.won_matches, test_obj1.lost_matches])
        self.assertEquals([0, 0], [test_obj2.won_matches, test_obj2.lost_matches])
    
    def test_delete_method_subtraction_won_lost_matches_with_h2_result(self):
        Fight.objects.get(id=2).delete()
        test_obj1 = Hero.objects.get(id=2)
        test_obj2 = Hero.objects.get(id=4)
        self.assertEquals([0, 0], [test_obj1.won_matches, test_obj1.lost_matches])
        self.assertEquals([0, 0], [test_obj2.won_matches, test_obj2.lost_matches])

    def test_delete_method_subtraction_won_lost_matches_queryset(self):
        Fight.objects.all().delete()
        #first fight heroes
        test_obj1 = Hero.objects.get(id=1)
        test_obj2 = Hero.objects.get(id=3)
        #second fight heroes
        test_obj3 = Hero.objects.get(id=2)
        test_obj4 = Hero.objects.get(id=4)
        self.assertEquals([0, 0], [test_obj1.won_matches, test_obj1.lost_matches])
        self.assertEquals([0, 0], [test_obj2.won_matches, test_obj2.lost_matches])
        self.assertEquals([0, 0], [test_obj3.won_matches, test_obj3.lost_matches])
        self.assertEquals([0, 0], [test_obj4.won_matches, test_obj4.lost_matches])


class ExistenceTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        Type.objects.create(name="Human")
        Type.objects.create(name="Alien")
        Hero.objects.create(first_name="John", last_name="Smith", hero_type_id=1)
        Hero.objects.create(first_name="Joe", last_name="Dee", hero_type_id=2)
        Hero.objects.create(first_name="Johny", last_name="Bravo", hero_type_id=1)
        Hero.objects.create(first_name="Billy", last_name="Kidman", hero_type_id=2)
        Fight.objects.create(hero_1_id=1, hero_2_id=3, result="H1", kill_loser=True)
        Fight.objects.create(hero_1_id=2, hero_2_id=4, result="H2", kill_loser=True)
    
    def test_save_method_killing_loser_with_h1_result(self):
        test_obj1 = Hero.objects.get(id=1)
        test_obj2 = Hero.objects.get(id=3)
        self.assertEquals(True, test_obj1.existence)
        self.assertEquals(False, test_obj2.existence)
    
    def test_save_method_killing_loser_with_h2_result(self):
        test_obj1 = Hero.objects.get(id=2)
        test_obj2 = Hero.objects.get(id=4)
        self.assertEquals(False, test_obj1.existence)
        self.assertEquals(True, test_obj2.existence)

    def test_delete_method_killing_loser_with_h1_result(self):
        Fight.objects.get(id=1).delete()
        test_obj1 = Hero.objects.get(id=1)
        test_obj2 = Hero.objects.get(id=3)
        self.assertEquals(True, test_obj1.existence)
        self.assertEquals(True, test_obj2.existence)

    def test_delete_method_killing_loser_with_h2_result(self):
        Fight.objects.get(id=2).delete()
        test_obj1 = Hero.objects.get(id=2)
        test_obj2 = Hero.objects.get(id=4)
        self.assertEquals(True, test_obj1.existence)
        self.assertEquals(True, test_obj2.existence)

    def test_delete_method_killing_loser_queryset(self):
        Fight.objects.all().delete()
        #first fight heroes
        test_obj1 = Hero.objects.get(id=1)
        test_obj2 = Hero.objects.get(id=3)
        #second fight heroes
        test_obj3 = Hero.objects.get(id=2)
        test_obj4 = Hero.objects.get(id=4)
        self.assertEquals(True, test_obj1.existence)
        self.assertEquals(True, test_obj2.existence)
        self.assertEquals(True, test_obj3.existence)
        self.assertEquals(True, test_obj4.existence)

