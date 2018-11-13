
import numpy as np
from factor import Factor

#t and f only

# factor should be n dimensional array

def restrict(factor, variable, value):

    #for i in range(variable):
    #    factor[]
    return factor.array.take(value, variable)

def multiply(factor1, factor2):
    """ merge on common variables. for one common var ONLY """
    uncommon1 =factor1.return_uncommon_variables(factor2.get_variables())

    uncommon2 =factor2.return_uncommon_variables(factor1.get_variables())
    print(factor1.variables)
    print(uncommon1+factor1.variables)

    new_var_set = sorted(uncommon1+factor1.variables)
    print(new_var_set)
    f3 = factor1.expand("f3", uncommon1, new_var_set)
    print(f3.array)
    f4 = factor2.expand("f4", uncommon2, new_var_set)
    print(f4.array)
    f5=np.multiply(f3.array,f4.array)

    return f5


def sumout(factor, variable):

    return

def normalize(factor):
    return

def inference(factorList, queryVariables, orderedListOfHiddenVariables,
              EvidenceList):
    return


f1 = np.array([[[0.1, 0.9], [0.3, 0.7]], [[0.6, 0.4], [0.3, 0.7]]])
f2 = np.array([[[0.2, 0.8], [0.2, 0.8]], [[0.1, 0.9], [0.2, 0.8]]])
#factora = np.array([[[1, 2], [3, 4]], [[5, 6], [7, 8]]])
factorb = np.array([[[[1, 2], [3, 4]], [[5, 6], [7, 8]]], [[[9, 10], [11, 12]], [[13, 14], [15, 16]]]])


var_list=["A","B", "C"]
variable=0
value =0

Factor(1,2,3)

f1=Factor("f1", ["A","B"], np.array([[0.8, 0.2], [0.9,0.1]]))
f2=Factor("f2",["B", "C"],np.array([[0.4, 0.6], [0.7,0.3]]))

restrictedFactor = restrict(f1,0, 0)
#print(restrictedFactor)

productFactor = multiply(f1, f2)
print(productFactor)

#resultFactor = sumout(factor, variable)

#normalizedFactor = normalize(factor)

#resultFactor = inference(factorList, queryVariables,
                         #orderedListOfHiddenVariables, EvidenceList)

