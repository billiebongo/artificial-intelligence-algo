
import numpy as np
from factor import Factor

#t and f only

# factor should be n dimensional array

def getOrderedListOfHiddenVariables(query_keys, evid_keys):
    order=["B", "FH", "M", "NA", "NH", "S"]
    hidden_var=[]
    for o in order:
        if o not in query_keys and o not in evid_keys:
            hidden_var.append(o)
    print(hidden_var)
    return hidden_var


def restrict(factor, variable, value):

    #for i in range(variable):
    #    factor[]
    #return Factor(,factor.array.take(value, variable))

    var_index = factor.variables.index(variable)
    restricted_arr = np.take(factor.array, value, axis=var_index)
    restricted_var = copy.deepcopy(factor.variables).pop(var_index)
    restricted_factor = Factor(restricted_var, restricted_arr)
    return restricted_factor

def sum_out(factor, variable):
    var_index = factor.variables.index(variable)
    result_arr = np.sum(factor.array, var_index)
    result_var = copy.deepcopy(factor.variables).pop(var_index)
    result_factor = Factor(result_var, result_arr)
    return result_factor

def multiply(factor1, factor2):
    """ merge on common variables. for one common var ONLY """

    copy1 = copy.deepcopy(factor1)
    copy2 = copy.deepcopy(factor2)
    combined_var = factor1.variables + list(set(factor2.variables) - set(factor1.variables))
    sorted_var = sorted(combined_var)
    for var in sorted_var:
        if var not in factor1.var:
            print(var)
            copy1.var.insert(sorted_var.index(var), var)
            copy1.arr = np.expand_dims(copy1.arr,
                                       axis=sorted_var.index(var))
        if var not in factor2.var:
            print(var)
            copy2.var.insert(sorted_var.index(var), var)
            copy2.arr = np.expand_dims(copy2.arr,
                                       axis=sorted_var.index(var))

    product_arr = np.multiply(copy1.arr, copy2.arr)
    product_factor = Factor(sorted_var, product_arr)
    return product_factor



#def sumout(factor, variable):

 #   return factor.sumout("sum_fact",variable)

def normalizedFactor(factor):
    #factor.variables should be only one
    return Factor(factor.variables,factor.array / np.sum(factor.array))

def resultFactor(factorList, queryVariables, orderedListOfHiddenVariables,EvidenceList):


    for evidence in EvidenceList:
        #restrict
        for factor in factorList:
            if evidence[0] in factor.variables:
                new_factor=restrict(factor, evidence[0], evidence[1])
                factorList.remove(factor)
                factorList.append(new_factor)

    for hiddenVariable in orderedListOfHiddenVariables:
        #find factors containing hiddenVariable
        factors_with_hidden_var=[]
        for f in factorList:
            if hiddenVariable in f.variables:
                factors_with_hidden_var.append(f)
                factorList.remove(f)
        if len(factors_with_hidden_var)>0:
            new_factor=factors_with_hidden_var[0]
            for i in range(len(factors_with_hidden_var)-1):
                print(i)
                new_factor = multiply(new_factor, factors_with_hidden_var[i+1])

        factorList.append(sum_out(new_factor))

    for factor in factorList:
        print(factor.__dict__)

    new_factor =  factorList[0]
    for i in range(len(factorList) - 1):
        new_factor = multiply(new_factor, factorList[i + 1])

    new_factor = normalizedFactor(new_factor)

    return new_factor






f1=Factor(["S"],np.array([0.05,0.95]))
f2=Factor(["M"], np.array([1/28,27/28]))
f3=Factor(["NA"], np.array([0.3,0.7]))
f4=Factor(["B", "S"], np.array([[0.9, 0.4],[0.1,0.6]]))
f5=Factor(["M","NA", "NH"], np.array([[[1,0],[0.5,0.5]],[[0.6,0.4],[0.2, 0.8]]]))
f6=Factor(["FH","M",  "NH", "S"], np.array([[[[1,0.5],[0.8,0.25]],[[0.6,0.1],[0.35,0.01]]],
                                            [[[0,0.5],[0.2,0.75]],[[0.4,0.9],[0.65,0.99]]]]))



factorList=[f1,f2,f3,f4,f5,f6]
queryVariables = {"FH":1}
EvidenceList = {}
orderedListofHiddenVariables = getOrderedListOfHiddenVariables(queryVariables.keys(), EvidenceList.keys())
result=resultFactor(factorList,queryVariables,orderedListofHiddenVariables, EvidenceList)



