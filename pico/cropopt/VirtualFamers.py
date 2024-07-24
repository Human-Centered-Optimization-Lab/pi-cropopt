
from pico.pinsga2.pinsga2 import AutomatedDM


class YieldGreedyDM(AutomatedDM):

    def makeDecision(self, F):

        if F[0,0] < F[1, 0]:
            return "a"
        elif F[0,0] > F[1, 0]:
            return "b"
        else:
            return "c"


class RangedVirtualFarmer(AutomatedDM): 

    def __init__(self, lb, ub):
        self.lb = lb
        self.ub = ub


    def makeDecision(self, F): 

        sol1Yield = F[0, 0] * -1
        sol2Yield = F[1, 0] * -1

        sol1Wat     = F[0, 1] 
        sol2Wat     = F[1, 1] 


        sol1InWatBound = sol1Wat <= self.ub and sol1Wat >= self.lb
        sol2InWatBound = sol2Wat <= self.ub and sol2Wat >= self.lb
    

        # Are the solutions the same? 
        if sol1Wat == sol2Wat and sol1Yield == sol2Yield: 
            
            result = "c"

        # Are both solutions outside of bounds? 
        if not sol1InWatBound and not sol2InWatBound:

            # Which solution is closer to the irrigation bound? 
            sol1BoundDist = min(abs(sol1Wat - self.lb), abs(sol1Wat - self.ub))
            sol2BoundDist = min(abs(sol2Wat - self.lb), abs(sol2Wat - self.ub))

            if sol1BoundDist < sol2BoundDist: 
                result = "a"
            elif sol2BoundDist < sol1BoundDist: 
                result = "b"
            else: 
                result = "c"

        else: 

            # who ever is in bounds wins
            if sol1InWatBound and not sol2InWatBound: 
                # Sol 1 in, sol 2 out
                result = "a"
            elif sol2InWatBound and not sol1InWatBound : 
                # Sol 2 in, sol 1 out
                result = "b"
            elif sol1Yield > sol2Yield: 
                # Tie break: sol 1 has bigger yield 
                result = "a"
            elif sol1Yield < sol2Yield:  
                # Tie break: sol 2 has bigger yield 
                result = "b"
            else: 
                result = "c"

            
        print(f"{result}: {sol1Yield} {sol1Wat} versus {sol2Wat} {sol2Yield} ")
        return result

















