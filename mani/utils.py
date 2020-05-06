import random
import webbrowser
import time

# Defining the items

fruits = ["apple", "banana", "mango"]
vegs = ['carrot', 'beans', 'potato']
drinks = ['milk', 'water', 'juice']

items = fruits+vegs+drinks

fruit_url="https://en.wikipedia.org/wiki/Fruit"

drink_url="https://en.wikipedia.org/wiki/Drink"

veg_url="https://en.wikipedia.org/wiki/Vegetable"

def what_is_the_item(category):
      if category in fruits:
            print("\n", category + " is a fruit")
            time.sleep(3)
            webbrowser.open(fruit_url)
      elif category in drinks:
            print("\n", category + " is a drink")
            time.sleep(3)
            webbrowser.open(drink_url)
      else:
            print("\n", category + " is a veg")
            time.sleep(3)
            webbrowser.open(veg_url)

                
print (items)

while True:
      item = items[random.randint(0, len(items)-1)]
      guess = str(input("\nI am thinking about an item from the above list. Can you guess it?\n \nIf you guess it right, I will display the category of the item:"))

      while True:
            if (item == guess.lower()):
                  break
            else:
                  guess = str(input("\nNope! Try again: "))

      print("\nYou guessed it right, I was thinking about: " , item)

      print(what_is_the_item(guess))
      
      ans=input("\nDo you want to play again? Hit Enter key or Type 'no' to add a new list:")

      list1=[]
      list2=[]
      list3=[]
      print("\n Enter 3 starters you like: ")
      for i in range(0,3):
            starter=str(input("\nEnter here: "))
            list1.append(starter)
      print(list1)

      print("\n Enter 3 Main Course you like: ")
      for i in range(0,3):
            main=str(input("\nEnter here: "))
            list2.append(main)
      print(list2)

      print("\n Enter 3 Desserts you like: ")
      for i in range(0,3):
            dessert=str(input("\nEnter here: "))
            list3.append(dessert)
      print(list3)

      food = list1+list2+list3

      print("\nNew list named Food: ", food)

      print("\nYou should cook: ", random.choice(list1)," ", random.choice(list2), " ", random.choice(list3))

      if ans.lower() == 'no':
            break
print ("\nIt was fun!, thanks for playing!")

