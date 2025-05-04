# -*- coding: utf-8 -*-
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from collections import Counter
import MarkovChainSimulation as mks

def flatten_matrix_to_df(matrix):
    
    '''Flattens the matrix of the simulation storing it to a dataframe'''
    
    array = []
    
    for l in matrix:
        for element in l:
            array.append(element)

    return pd.DataFrame(array, columns=['period', 'status', 'product'])


def sperate_df_into_return_reasons(df):

    '''Get index (periods) of failures'''

    idx_cr = df[df['status'] == 1]['period']
    idx_eou = df[df['status'] == 2]['period']
    idx_eol = df[df['status'] == 3]['period']
    idx_all = df[df['status'].isin([1,2,3])]['period']
    
    return idx_cr, idx_eou, idx_eol, idx_all


def count_quantities_of_return_reasons(idx_cr, idx_eou, idx_eol, idx_all):
    
    '''Calculate the frequency of each period seperately for each return reason'''
    
    c_cr =  Counter(idx_cr)
    c_eou = Counter(idx_eou)
    c_eol =  Counter(idx_eol)
    c_all = Counter(idx_all)
    
    return c_cr, c_eou, c_eol, c_all
    

def create_plot(c_cr, c_eou, c_eol, c_all):
    
    '''Visualize the frequency of the periods by return reasons'''

    # unique values for abscissa
    unique_values = sorted(set(c_all))

    # frequency
    freq_reason_1 = [c_cr.get(w, 0) for w in unique_values]
    freq_reason_2 = [c_eou.get(w, 0) for w in unique_values]
    freq_reason_3 = [c_eol.get(w, 0) for w in unique_values]

    # create plot
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # stacked bar plot
    ax.bar(unique_values, freq_reason_1, label='CR', color='white', edgecolor='black', hatch='//')
    ax.bar(unique_values, freq_reason_2, bottom=freq_reason_1, label='EoU', color='white', edgecolor='black', hatch='\\\\')
    ax.bar(unique_values, freq_reason_3, bottom=np.array(freq_reason_1) + np.array(freq_reason_2), label='EoL', color='white', edgecolor='black', hatch='xx')

    # set ax
    ax.set_xlabel('period')
    xticks = [i for i in range(0, 18)]
    ax.set_xticks(xticks)
    
    # adjust y
    total_heights = np.array(freq_reason_1) + np.array(freq_reason_2) + np.array(freq_reason_3)
    max_height = total_heights.max()
    ax.set_ylim(0, max_height * 1.05)

    
    # change labels
    ax.set_xticklabels([str(i + 1) for i in xticks])
    ax.set_ylabel('frequency')
    ax.set_title('Distribution of periods by state')
    ax.legend()
    
    # plot
    plt.show()


def create_statistical_characteristics(idx_cr, idx_eou, idx_eol):
    
    '''Calculate mean and std'''
    
    statistical_characteristics = {}

    for j, i in enumerate([idx_cr, idx_eou, idx_eol]):
        statistical_characteristics[j] = {"mean":np.mean(i), "std":np.std(i)}

    return statistical_characteristics
    
def main():
    matrix = mks.simulate_markov_chain(1000000)
    df = flatten_matrix_to_df(matrix)
    idx_cr, idx_eou, idx_eol, idx_all = sperate_df_into_return_reasons(df)
    c_cr, c_eou, c_eol, c_all = count_quantities_of_return_reasons(idx_cr, idx_eou, idx_eol, idx_all)
    create_plot(c_cr, c_eou, c_eol, c_all)
    stat_characteristics = create_statistical_characteristics(idx_cr, idx_eou, idx_eol)

if __name__ == "__main__":
    main()







