
def calc_batting(hits, at_bats):
    try:
        if at_bats > 0:
            avg_bat = float(hits/at_bats)

            return print(f"Batting Average: {avg_bat:.3f}")
        else: 
            return 0.000

    except ValueError:
        print("Value error.")

def menu():
    print("\nMENU OPTIONS\n")
    print("1 – Calculate batting average\n")
    print("2 - Exit program\n")
    choice = int(input("Menu Option: "))

    return choice
    
def main():
  print("Baseball Team Manager\n")
  while True:
      choice = int(menu())

      if choice == 1:
          print("Calculate batting average...\n")
          at_bats = int(input("Official number of at bats: \n"))
          hits = int(input("Number of hits: \n"))
          calc_batting(hits, at_bats)

      elif choice == 2: 
          print("\nBye!")

          break
  
      else:
          print("Invalid input.")


main()
