#Below statements will print user friendly list to choose
print("")
print("Select a fruit 'apple','banana','mango' or ")
print("Select a drink 'milk', 'water', 'juice' or ")
print("Select a veg 'carrot','beans','potato' ")
print("")

user_need = input("What do you like from the above list: ")

fruits = ["apple", "banana", "mango"]
vegs = ['carrot', 'beans', 'potato']
drinks = ['milk', 'water', 'juice']

# Below what_is_the_item function will retun is the entered item is what list.
def what_is_the_item(item):
    if item in fruits:
        print(item + " It's a fruit")
    elif item in drinks:
        print(item + " It's a drink")
    elif item in vegs:
        print(item + " It's a veg")
    else:
        print("Chosen the wrong option from the list given")


# Below merge_list function will print all the given list into a single list
def merge_list(*no_of_list):
#    full_list = list1 + list2 + list3
    full_list1 = no_of_list[0] + no_of_list[1] + no_of_list[2]
    print("This is the full list: ", full_list1)

# Functions will be called in this section
merge_list(fruits, vegs, drinks)
what_is_the_item(user_need)
