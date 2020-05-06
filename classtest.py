import unittest
from test2 import ingredients

# Note: the class must be called Test
class Test(unittest.TestCase):
  
  def test_classic_smoothie(self):
    self.assertEqual(ingredients("Classic"), "banana,honey,ice,mango,peach,pineapple,strawberry,yogurt")

  def test_without_strawberry(self):
    self.assertEqual(ingredients("Classic,-strawberry"), "banana,honey,ice,mango,peach,pineapple,yogurt")

  def test_just_desserts(self):
    self.assertEqual(ingredients("Just Desserts"), "banana,cherry,chocolate,ice cream,peanut")

  def test_without_ice_cream_and_peanut(self):
    self.assertEqual(ingredients("Just Desserts,-ice cream,-peanut"), "banana,cherry,chocolate")


Test.test_classic_smoothie()
Test.test_without_strawberry()
Test.test_just_desserts()
Test.test_without_ice_cream_and_peanut()
