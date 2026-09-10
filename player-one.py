
def welcome():
    user_name = input(f'Hello, what is your chosen name?')
    return user_name

user_name = welcome()

def build_character(user_name):
    player = {
        "name" : user_name,
        "hp" : 100,
        "max_hp" :100,
        "gold" : 50,
        "inventory" : ["rusty shovel", "knife", "old phone"]
    }
    return player

def display_stats(player):
    print(f'n\             {player['name']} Status              ')
    print(f' {player['hp']} / {player['max_hp']} ')
    print(f' Gold: {player['gold']}')

#def display_inventory(player):
    #print (f' {player['inventory']} ')
    
def main():
    welcome()
    build_character(user_name)
    display_stats(player)

main()
    
