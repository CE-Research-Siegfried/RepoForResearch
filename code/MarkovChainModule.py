# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd

_transition_matrix = None
    
def core_quality():
    
     operation_modus = np.random.choice([1, 0], p=[0.7, 0.3])
     
     if operation_modus == 1:
         return [0.8, 0.2]
     else:
         return [0.15, 0.85]
        
def remanufactureable(probabilites):
    
    return np.random.choice([1, 0], p=probabilites)

def geometrical_cdf_piecwise(t):
    
    p = 0.03610458219651225
    
    return 0.35 + 0.65*(1-(1-p)**(t-3))

def conditional_probability(F_t, F_t_1):
    return (F_t - F_t_1) / (1- F_t_1)

def create_transition_table():
    
    global _transition_matrix
    if _transition_matrix is None:

        # CDF
        wear_in = {0:0.15, 1:0.25, 2:0.32, 3:0.35} #F(0),F(1),F(2),F(3)
        random = {i:geometrical_cdf_piecwise(i) for i in range(4, 14)}
        wear_out = {14:0.65, 15:0.80, 16:1}
        merged = {**wear_in, **random, **wear_out}
        
        # data preperation
        df = pd.DataFrame.from_dict(merged, orient='index', columns=['cumulated'])
        df['cumulated_minus_1'] = df['cumulated'].shift(1, fill_value=0)
        df['conditional_probability'] =  df.apply(lambda row: conditional_probability(row['cumulated'], row['cumulated_minus_1']), axis=1)
        
        _transition_matrix = df.to_dict(orient='index')
    
    return _transition_matrix

def get_transition_matrix(t):
    
    '''Outputs the transition matrix in dependence of period t'''
    transition_table = create_transition_table()
    
    if t <= 2:
        
        '''Time frame, when CR are possible'''
        
        use_CR, use_EoU, use_EoL = 0.0914, transition_table[t]['conditional_probability'], 0 
        use_use = 1 - use_CR - use_EoU - use_EoL
        EoU_U = remanufactureable(core_quality())

        matrix = [[use_use, use_CR, use_EoU, use_EoL],
             [0.95, 0.0, 0.05, 0.00],
             [1-EoU_U, 0.0, 0.0, EoU_U],
             [0, 0.0, 0.0, 1]]
        
    elif t == 17:
        
        EoU_U = remanufactureable(core_quality())

        matrix = [[0, 0, 0, 0],
             [0.0, 0.0, 0.00, 0.00],
             [1-EoU_U, 0.0, 0.0, EoU_U],
             [0, 0.0, 0.0, 0]]
           
    else:
        
        '''Time frame, when CR are not possible'''
        
        use_CR = 0.0
        use_EoU = transition_table[t]['conditional_probability']
        use_EoL = 0
        use_use = 1 - use_CR - use_EoU - use_EoL
                
        EoU_U = remanufactureable(core_quality())

        matrix = [[use_use, use_CR, use_EoU, use_EoL],
             [0.95, 0.0, 0.05, 0.00],
             [EoU_U, 0.0, 0.0, 1-EoU_U],
             [0.00, 0.0, 0.0, 1]] 

    return matrix

def next_state(current_state, transition_matrix):
    
    '''Takes the current state of the Markov chain
    and outputs the consecutive state'''
    
    P = transition_matrix
    
    # outputs the next state based on transition probabilities
    next_state = np.random.choice([0, 1, 2, 3], p=P[current_state]) # 1-D array (accessing P via index)
    
    return next_state

    
if __name__ == '__main__':

    create_transition_table()
    get_transition_matrix(1)

    
    

    
    
    
    


    
    
    
    
