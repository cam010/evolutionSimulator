# var1 = Prey minimum reproduction chance: 1 #
# var2 = Prey maximum reproduction chance: 100 #
# var3 = Prey minimum offspring amount: 1 #
# var4 = Prey maximum offspring amount: 5
# var5 = Prey minimum chance of spontaneous death: 1 #
# var6 = Prey maximum chance of spontaneous death: 100 #
# var7 = Prey minimum starting energy level: 1 #
# var8 = Prey maximum starting energy level: 20
# var9 = Prey minimum, minimum energy level to survive: 1 #
# var10 = Prey maximum, minimum energy level to survive: 5 
# var11 = Prey minimum defence level: 0 #
# var12 = Prey maximum defence level: 100 #

# var13 = Predator minimum reproduction chance: 1 #
# var14 = Predator maximum reproduction chance: 100 #
# var15 = Predator minimum offspring amount: 1 #
# var16 = Predator maximum offspring amount: 5
# var17 = Predator minimum chance of spontaneous death: 1 #
# var18 = Predator maximum chance of spontaneous death: 100 #
# var19 = Predator minimum starting energy level: 2 #
# var20 = Predator maximum starting energy level: 20
# var21 = Predator minimum, minimum energy level to survive: 1 #
# var22 = Predator maximum, minimum energy level to survive: 5 
# var23 = Predator minimum attack level: 1 #
# var24 = Predator maximum attack level: 100 #

# var25 = Minimum percetage amount of energy shared between prey each turn (percentage meaning x/preycount): 0% # obsolete and not used
# var26 = amount of energy given to each prey per turn

# var27 = Mutation chance: 5%

# var28 = starting predator count: 100_000
# var29 = starting prey count: 100_000

# var30 = proportion of energy absorbed from consumption of prey: 0.5

# var31 = chance of surplus predator attacking: 50%

# var32 = generation to stop simulation on

# var33 = energy taken from predators each turn



class Variables:
    # in future, can custom add variables from terminal
    def __init__(self):
        self.set_variables()
    
    def set_variables(self):
        self.var1 = 1 #
        self.var2 = 70 # 
        self.var3 = 1 #
        self.var4 = 5
        self.var5 = 1 #
        self.var6 = 100 #
        self.var7 = 1 #
        self.var8 = 20 
        self.var9 = 1 #
        self.var10 = 5
        self.var11 = 0 #
        self.var12 = 100 #
        
        
        self.var13 = 1 #
        self.var14 = 100 #
        self.var15 = 1 #
        self.var16 = 3
        self.var17 = 1 #
        self.var18 = 100 # 
        self.var19 = 2 #
        self.var20 = 15
        self.var21 = 1 #
        self.var22 = 5 
        self.var23 = 1 #
        self.var24 = 100 #
        # self.var25 = 0 # defunct
        self.var26 = 10
        self.var27 = 5
        self.var28 = 1000
        self.var29 = 1000
        self.var30 = 0.3
        self.var31 = 0
        self.var32 = 45
        self.var33 = 3
        