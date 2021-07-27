import random



class Roll:

    #Function for initializing the dice roll
    def roll(dice_string):
        print(dice_string)
        #converts the string to upper case, so d works just like D
        command = dice_string.upper()

        #splits the string into two separate string occupying
        #indexes of a size 2 array where the porton
        #of the string before the split char is held in 
        #the first index of the array and the second component is
        #held in index 1
        parts = command.split ('D')
        n_rolls = 1

        #if the num_dice is left empty, set to 1
        if parts[0] == '':
            n_rolls = 1
        #Otherwise the num_dice is the first section of the string
        else:
            n_rolls = int (parts[0])

        if parts[1] != '':
            sides = int (parts[1])    

        #array to hold the role values
        individual_rolls = []

        total = 0

        #Roll the dice
        for num_roll in range(n_rolls):
            roll = random.randint(1, sides)
            individual_rolls.append(roll)
            total += roll

        return individual_rolls, total


#     #Seems to deal with + - values, not sure why this works
#     def get_roll_info(self, s):
#         modifier = 0
#         faces = 10

#         if "+" in s:
#             modifier = int(s[s.find("+") + 1:])
#             faces = int (s[:s.find("+")])

#         elif "-" in s:
#             modifier - int(s[s.find ("-") + 1:])
#             faces = int (s[:s.find ("-")])

#         else:
#             faces = int(s)

#         return faces, modifier


# # Also not sure what this does
#     def roll_dice(self):
#         rolls = []

#         for j in range (self.nrolls):
#             rolls.append (random.randint(1, self.faces) + self.modifier)

#         #fix rolls
#         rolls = [self.faces if x > self.faces else x for x in rolls]
#         rolls = [1 if x < 1 else x for x in rolls]

#         return rolls    

