# -*- coding: utf-8 -*-
import numpy as np
import MarkovChainModule as mkm

np.random.seed(42)

# create data
def simulate_markov_chain(runs=1000, custom_parameters=None):
    
    '''Creates a time-indexed sequence of states for a product until it is
    in the state of EoL. 
    '''

    matrix = []
    
    if custom_parameters:
        parameters = custom_parameters
    else:
        parameters = {'state':0, 't':0}
    
    # number of simulations
    for n in range(runs):
        
        state = parameters['state']
        
        # point of time t
        t = parameters['t'] 
        
        #l = [(t, state, n)] 
        l = [] 
        
        # start life cycle
        while True:
        
            # produt is in the state of EoL
            if state == 3:
                break
    
            else:
    
                # get transition matrix based on current status
                P = mkm.get_transition_matrix(t)
    
                # calcuate new status
                new_state = mkm.next_state(state, P)
                
                #  remanufactured
                if state == 2 and new_state == 0:
                                        
                    # safe state
                    l.append((t, new_state, n))
                    
                    # reset period
                    t = 0


                # commerical return back to market
                elif state == 1 and new_state == 0:
                    
                    # safe state
                    l.append((t, new_state, n))

                    # reset period
                    t = 0
                    
                else:

                    # safe state
                    l.append((t, new_state, n))
                    
                    # next period
                    t += 1 
        
                state = new_state
    
        matrix.append(l)

    return matrix

if __name__ == "__main__":
    example = simulate_markov_chain(custom_parameters={'state':0, 't':0})







