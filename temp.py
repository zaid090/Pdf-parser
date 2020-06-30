# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import matplotlib.pyplot as plt
import numpy as np

def plot_barchart( passed, failed, subjects, type='a'):
    
    colors=[(1, 0, 0), (0, 1, 0)]
    index = np.arange(len(passed))
    if type == 'p':
        plt.bar(index, passed, 0.5, color=colors[1])
        plt.xticks(index, subjects)
    elif type == 'f':
        plt.bar(index, failed, 0.5, color=colors[0])
        plt.xticks(index, subjects)
    else:
        plt.bar(index, failed, 0.25, label="Failed", color=colors[0])
        plt.bar(index+0.25, passed, 0.25, label="Passed", color=colors[1])
        plt.xticks(index+(0.25/2), subjects)
        plt.legend()
    plt.title("Subject Wise Analysis")
    plt.grid(True)
    plt.show()
    
def plot_pie( data, label, title="Grade Analysics"):
    
    plt.pie(data, labels= label, autopct = "%.1f%%")
    plt.title(title)
    plt.show()
    
'''def plot_pie(data=[0, 0], title="Result"):
    
    plt.pie(data, labels= ['Pass', 'KT'], colors=((0,1,0),(1,0,0)), autopct = "%.1f%%")
    plt.title(title)
    plt.show()
'''
   
"""plot_pie([56, 23, 2], ["Passed", "Failed", "Dont Know"], "Mathematics")
plot_barchart([12, 34, 56, 23, 67], [3, 5, 4, 2, 7], ["Maths", "Science", "fd", "hdsj", "jsd"], 'p')
plot_barchart([12, 34, 56, 23], [3, 5, 4, 2], ["Maths", "Science", "fd", "hdsj"], 'f')
plot_barchart([12, 34, 56, 23, 67], [3, 5, 4, 2, 7], ["Maths", "Science", "fd", "hdsj", "jsd"], )"""
