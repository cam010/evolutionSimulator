# VAR1 = Prey minimum reproduction chance: 1 #
# VAR2 = Prey maximum reproduction chance: 100 #
# VAR3 = Prey minimum offspring amount: 1 #
# VAR4 = Prey maximum offspring amount: 5
# VAR5 = Prey minimum chance of spontaneous death: 1 #
# VAR6 = Prey maximum chance of spontaneous death: 100 #
# VAR7 = Prey minimum starting energy level: 1 #
# VAR8 = Prey maximum starting energy level: 20
# VAR9 = Prey minimum, minimum energy level to survive: 1 #
# VAR10 = Prey maximum, minimum energy level to survive: 5 
# VAR11 = Prey minimum defence level: 0 #
# VAR12 = Prey maximum defence level: 100 #

# VAR13 = Predator minimum reproduction chance: 1 #
# VAR14 = Predator maximum reproduction chance: 100 #
# VAR15 = Predator minimum offspring amount: 1 #
# VAR16 = Predator maximum offspring amount: 5
# VAR17 = Predator minimum chance of spontaneous death: 1 #
# VAR18 = Predator maximum chance of spontaneous death: 100 #
# VAR19 = Predator minimum starting energy level: 2 #
# VAR20 = Predator maximum starting energy level: 20
# VAR21 = Predator minimum, minimum energy level to survive: 1 #
# VAR22 = Predator maximum, minimum energy level to survive: 5 
# VAR23 = Predator minimum attack level: 1 #
# VAR24 = Predator maximum attack level: 100 #

# VAR25 = Minimum percetage amount of energy shared between prey each turn (percentage meaning x/preycount): 0% # obsolete and not used
# VAR26 = amount of energy given to each prey per turn

# VAR27 = Mutation chance: 5%

# VAR28 = starting predator count: 100_000
# VAR29 = starting prey count: 100_000

# VAR30 = proportion of energy absorbed from consumption of prey: 0.5

# VAR31 = chance of surplus predator attacking: 50%

# VAR32 = generation to stop simulation on

# VAR33 = energy taken from predators each turn



class Variables:
    # in future, can custom add VARiables from terminal
    def __init__(self):
        self.set_VARiables()
    
    def set_VARiables(self):
        self.VAR1 = 1 #
        self.VAR2 = 70 # 
        self.VAR3 = 1 #
        self.VAR4 = 5
        self.VAR5 = 1 #
        self.VAR6 = 100 #
        self.VAR7 = 1 #
        self.VAR8 = 20 
        self.VAR9 = 1 #
        self.VAR10 = 5
        self.VAR11 = 0 #
        self.VAR12 = 100 #
        
        
        self.VAR13 = 1 #
        self.VAR14 = 100 #
        self.VAR15 = 1 #
        self.VAR16 = 3
        self.VAR17 = 1 #
        self.VAR18 = 100 # 
        self.VAR19 = 2 #
        self.VAR20 = 15
        self.VAR21 = 1 #
        self.VAR22 = 5 
        self.VAR23 = 1 #
        self.VAR24 = 100 #
        # self.VAR25 = 0 # defunct
        self.VAR26 = 10
        self.VAR27 = 5
        self.VAR28 = 1000
        self.VAR29 = 1000
        self.VAR30 = 0.3
        self.VAR31 = 0
        self.VAR32 = 45
        self.VAR33 = 3
        