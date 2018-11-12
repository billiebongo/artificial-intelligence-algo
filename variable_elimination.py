
import numpy as np

#t and f only

# factor should be n dimensional array

def restrict(factor, variable, value):

    #for i in range(variable):
    #    factor[]
    return factor.take(value, variable)

def multiply(factor1, factor2):
    """ merge on common variables """

    
    factor1.expand_dims()



    return


def sumout(factor, variable):
    return

def normalize(factor):
    return

def inference(factorList, queryVariables, orderedListOfHiddenVariables,
              EvidenceList):
    return


factora = np.array([[[0.1, 0.9], [0.3, 0.7]], [[0.6, 0.4], [0.3, 0.7]]])
factora = np.array([[[1, 2], [3, 4]], [[5, 6], [7, 8]]])
factorb = np.array([[[[1, 2], [3, 4]], [[5, 6], [7, 8]]], [[[9, 10], [11, 12]], [[13, 14], [15, 16]]]])

array([[[ 1,  2],
        [ 3,  4]],

       [[ 9, 10],
        [11, 12]]])

var_list=["A","B", "C"]
variable=0
value =0
restrictedFactor = restrict(factora, variable, value)
print(restrictedFactor)

#productFactor = multiply(factor1, factor2)

#resultFactor = sumout(factor, variable)

#normalizedFactor = normalize(factor)

#resultFactor = inference(factorList, queryVariables,
                         #orderedListOfHiddenVariables, EvidenceList)

