
MENU = {"Classic":["strawberry", "banana", "pineapple", "mango", "peach",
                      "honey","ice", "yogurt"], 
        "Forest Berry":["strawberry", "raspberry", "blueberry", "honey", "ice",
                           "yogurt"], 
        "Freezie":["blackberry", "blueberry", "black currant", "grape juice",
                        "frozen yogurt"],
        "Greenie":["green apple", "kiwi", "lime", "avocado", "spinach",
                        "ice", "apple juice"],
        "Vegan Delite":["strawberry", "passion fruit", "pineapple", "mango",
                             "peach", "ice", "soy milk"],
        "Just Desserts":["banana", "ice cream", "chocolate", "peanut",
                              "cherry"]}
def which_smoothie(order):
  for k in MENU:
    if k == order:
      return MENU[k]
  
def ingredients(order):
    order = order.split(",")
    print(order)
    ingredients = which_smoothie(order[0])
    for allergies in order[1:]:
        print(allergies)
        if allergies[1:] in ingredients:
            ingredients.remove(allergies[1:])
    ingredients = sorted(ingredients)
    ingredients =','.join(ingredients)
    return ingredients

test = ingredients("Just Desserts,-ice cream,-peanut")
print(test)
