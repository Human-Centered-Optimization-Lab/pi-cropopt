
from pico.pinsga2.pinsga2 import AutomatedDM


class YieldGreedyDM(AutomatedDM):

    def makeDecision(self, F):

        if F[0,0] < F[1, 0]:
            return "a"
        elif F[0,0] > F[1, 0]:
            return "b"
        else:
            return "c"




