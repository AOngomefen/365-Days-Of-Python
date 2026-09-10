import random # import random pack

def guessing(skill):
	temp = ("shock", "magic", "speed", "flight", "art", "music") #tuple/list
	guess = random.choice(temp) # random choice degree
	print(guess)

	if guess != skill: # checks guess
    
		print("haha guessed wrong then?")
	else: 
		print("oh my you figured out my special skill (^0^!!)")
	
def main():

	skill = str(input("Try and guess my secret skill: ")) # get degree 
	guessing(skill) # calls function
	
	
main()
