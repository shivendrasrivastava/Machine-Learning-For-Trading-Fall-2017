"""
Template for implementing QLearner  (c) 2015 Tucker Balch
"""

import numpy as np
import random as rand

class QLearner(object):

    def __init__(self, \
        num_states=100, \
        num_actions = 4, \
        alpha = 0.2, \
        gamma = 0.9, \
        rar = 0.5, \
        radr = 0.99, \
        dyna = 0, \
        verbose = False):
        self.Q = [[0] * num_actions for i in range(num_states)]
        self.memory = []
        self.verbose = verbose
        self.num_actions = num_actions
        self.s = 0
        self.a = 0
        self.rar = rar
        self.radr = radr
        self.dyna = dyna
        self.num_states = num_states
        self.alpha = alpha
        self.gamma = gamma

    def querysetstate(self, s):
        """
        @summary: Update the state without updating the Q-table
        @param s: The new state
        @returns: The selected action
        """
        self.s = s

        action = self.Q[s].index(max(self.Q[s])) if self.rar <= rand.random() else rand.randint(0, self.num_actions-1)
        self.a = action
        self.rar *= self.radr
        if self.verbose:
            print "s =", s,"a =",action
        return action

    def query(self,s_prime,r):
        """
        @summary: Update the Q table and return an action
        @param s_prime: The new state
        @param r: The ne state
        @returns: The selected action
        """
        s = self.s
        a = self.a
        # Add a pair of [s, a, s', r] to the memory
        # for Dyna-Q
        self.memory.append([s, a, s_prime, r])
        next_action = self.Q[s_prime].index(max(self.Q[s_prime]))
        self.Q[s][a] = (1 - self.alpha) * self.Q[s][a] + self.alpha * (r + self.gamma * self.Q[s_prime][next_action])

        # if @dyna == 0, then it is normal version, and will not enter the loop
        # the value of @dyna means how many extra random updates take place.
        for i in range(self.dyna):
            [s_d, a_d, s_prime_d, r_d] = self.memory[rand.randint(0, len(self.memory) - 1)]
            next_action_d = self.Q[s_prime_d].index(max(self.Q[s_prime_d]))
            self.Q[s_d][a_d] = (1 - self.alpha) * self.Q[s_d][a_d] + self.alpha * (r_d + self.gamma * self.Q[s_prime_d][next_action_d])


        self.s = s_prime
        self.a = next_action if self.rar <= rand.random() else rand.randint(0, self.num_actions-1)
        self.rar *= self.radr

        if self.verbose:
            print "s =", s_prime,"a =",action,"r =",r

        return next_action
    def author(self):
        return 'schou33'

if __name__=="__main__":
    print "Remember Q from Star Trek? Well, this isn't him"
