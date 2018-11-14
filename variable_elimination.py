
import numpy as np
from factor import Factor
import copy

#t and f only

# factor should be n dimensional array

def getOrderedListOfHiddenVariables(query_keys, evid_keys):
    order=["B", "FH", "M", "NA", "NH", "S"]
    hidden_var=[]
    for o in order:
        if o not in query_keys and o not in evid_keys:
            hidden_var.append(o)
    print("HIDDEN")
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
    print("MY MY MY")
    print(factor.variables)
    print(copy.deepcopy(factor.variables))
    print(variable)
    result_var = copy.deepcopy(factor.variables)
    result_var.remove(variable)
    result_factor = Factor(result_var, result_arr)
    print(result_var)
    print("TESINF SUMMING OUT")
    print(result_factor.array)
    print(result_factor.variables)
    print("testend")
    return result_factor

def multiply(factor1, factor2):
    """ merge on common variables. for one common var ONLY """

    copy1 = copy.deepcopy(factor1)
    copy2 = copy.deepcopy(factor2)
    print(type(factor1.variables))
    print(factor1.__dict__)
    combined_var = factor1.variables + list(set(factor2.variables) - set(factor1.variables))
    sorted_var = sorted(combined_var)
    for var in sorted_var:
        if var not in factor1.variables:
            print(var)
            copy1.variables.insert(sorted_var.index(var), var)
            copy1.array = np.expand_dims(copy1.array,
                                       axis=sorted_var.index(var))
        if var not in factor2.variables:
            print(var)
            copy2.variables.insert(sorted_var.index(var), var)
            copy2.array = np.expand_dims(copy2.array,
                                       axis=sorted_var.index(var))

    product_arr = np.multiply(copy1.array, copy2.array)
    product_factor = Factor(sorted_var, product_arr)
    print("TESINF PDT FCT")
    print(product_factor.array)
    print(product_factor.variables)
    return product_factor



#def sumout(factor, variable):

 #   return factor.sumout("sum_fact",variable)

def normalizedFactor(factor):
    #factor.variables should be only one
    return Factor(factor.variables,factor.array / np.sum(factor.array))

def resultFactor(factorList, queryVariables, orderedListOfHiddenVariables,EvidenceList):


    for evidence in EvidenceList:
        #restrict
        print("no evide")
        for factor in factorList:
            if evidence[0] in factor.variables:
                new_factor=restrict(factor, evidence[0], evidence[1])
                factorList.remove(factor)
                factorList.append(new_factor)

    for hiddenVariable in orderedListOfHiddenVariables:
        #find factors containing hiddenVariable
        factors_with_hidden_var=[]
        print("STARTING NEW HIDDEN VAR")

        for f in factorList:
            print("HIDDEN VAR:"+hiddenVariable)
            print("F IS")
            print(f.variables)
            if hiddenVariable in f.variables:
                print("YES INSIDE")
                print(hiddenVariable)
                factors_with_hidden_var.append(f)
                print("FACTOR W HIDDEN VAR, mneeds to be rempved")
                print(f.variables)

                #factorList.remove(f) IMPT: CANNOT REMOVE WHEN ITERATING@!!
                for i in factorList:
                    print(i.variables)
                print("$$$$")

        print("HELLO FROM THE OTHER SIDE")
        for j in factors_with_hidden_var:
            print(j.variables)
        if len(factors_with_hidden_var)>1:
            new_factor=factors_with_hidden_var[0]
            for i in range(len(factors_with_hidden_var)-1):
                print(i)
                print("BEEP")
                print( factors_with_hidden_var[i+1])
                new_factor = multiply(new_factor, factors_with_hidden_var[i+1])
            print(hiddenVariable+"!!!!!!!!!!!!!!!!!!!!!!!!")
            print(new_factor.variables)
            new_factor=sum_out(new_factor, hiddenVariable)
            print("new faxtor var")
            print(new_factor.variables)
            print(new_factor.variables)
            factorList.append(new_factor)
        else:
            new_factor=sum_out(factors_with_hidden_var[0], hiddenVariable)

            factorList.append(new_factor)
        print("SUMMING OUT MUST NOT CONTAIN THE HIDDEN. hidden var is :")
        print(hiddenVariable)
        print("new factor added")
        print(new_factor.variables)

        print("new factor list shouldnt have hidden vae############")
        for f in factorList:
            print(f.variables)
        #remove old factors from factorList
        print("CHECK THIS NOW")
        print(len(factorList))
        print(len(factors_with_hidden_var))
        factorList=[x for x in factorList if x not in factors_with_hidden_var]
        print(len(factorList))

    print("shit")
    for f in factorList:
        print(f.variables)
        print(f.array)

    print("HELLO")
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
print("WHAT")
print(result.variables, result.array)
#test=[[[0.32,0.48],[0.14,0.06]],[[0.36,0.54],[0.07,0.03]]]
#n=sum_out(Factor(["A","B","C"], test), 'B')
#print(n.array)
#print(n.variables)


