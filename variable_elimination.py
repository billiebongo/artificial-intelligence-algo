
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
    print(factor.__dict__)
    var_index = factor.variables.index(variable)
    restricted_arr = np.take(factor.array, value, axis=var_index)
    restricted_var = copy.deepcopy(factor.variables)
    restricted_var.remove(variable)
    restricted_factor = Factor(restricted_var, restricted_arr)
    print(restricted_factor.__dict__)
    print("RESTR")
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
    print("MULTIPLYING")
    print(factor1.variables)
    print(factor2.variables)
    print(factor1.array)
    print(factor2.array)
    copy1 = copy.deepcopy(factor1)
    copy2 = copy.deepcopy(factor2)

    combined_var = factor1.variables + list(set(factor2.variables) - set(factor1.variables))
    sorted_var = sorted(combined_var)
    for var in sorted_var:
        if var not in factor1.variables:
            copy1.variables.insert(sorted_var.index(var), var)
            copy1.array = np.expand_dims(copy1.array,
                                       axis=sorted_var.index(var))
        if var not in factor2.variables:

            copy2.variables.insert(sorted_var.index(var), var)
            copy2.array = np.expand_dims(copy2.array,
                                       axis=sorted_var.index(var))


    product_arr = np.multiply(copy1.array, copy2.array)
    product_factor = Factor(sorted_var, product_arr)
    print("MULTIPLYING RESULTS")
    print(product_factor.array)
    print(product_factor.variables)
    return product_factor



#def sumout(factor, variable):

 #   return factor.sumout("sum_fact",variable)

def normalizedFactor(factor):
    #factor.variables should be only one
    return Factor(factor.variables,factor.array / np.sum(factor.array))

def resultFactor(factorList, queryVariables, orderedListOfHiddenVariables,EvidenceList):

    for f in factorList:
        print(f.variables)
    factors_to_remove = []
    for factor in factorList:
        flag=0
        #restrict

        for var in EvidenceList:
            print("RIDDING OF EVIDENCE" + var)
            print("FACTOR IS")
            print(factor.variables)
            if var in factor.variables:
                flag=1 #indicate to remove old factor
                print("YES EVID IN FACTOR")
                print(var+"is in")
                print(factor.variables)

                #factor, var, vALUE
                new_factor = restrict(factor, var, EvidenceList[var])
        if flag==1:
            factors_to_remove.append(factor)
            print("factor b4 restrict")
            print(factor.variables)
            print("new factor after restrict")
            print(new_factor.variables)
            factorList.append(new_factor)

    factorList=[x for x in factorList if x not in factors_to_remove]
    print("FACTOR LIST NOW AFTER results")
    for j in factorList:
        print(j.variables)


    for hiddenVariable in orderedListOfHiddenVariables:
        #find factors containing hiddenVariable
        factors_with_hidden_var=[]
        print("STARTING NEW HIDDEN VAR")

        for f in factorList:
            print("HIDDEN VAR:"+hiddenVariable)
            print("F IS")
            print(f.variables)
            if hiddenVariable in f.variables:

                print(hiddenVariable)
                factors_with_hidden_var.append(f)

                #factorList.remove(f) IMPT: CANNOT REMOVE WHEN ITERATING@!!


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

        print(hiddenVariable)
        print("new factor added")
        print(new_factor.variables)
        for f in factorList:
            print(f.variables)
        #remove old factors from factorList
        print("CHECK THIS NOW")
        print(len(factorList))
        print(len(factors_with_hidden_var))
        factorList=[x for x in factorList if x not in factors_with_hidden_var]
        print(len(factorList))

    for f in factorList:
        print(f.variables)
        print(f.array)

    new_factor =  factorList[0]

    for i in range(len(factorList) - 1):

        new_factor = multiply(new_factor, factorList[i + 1])

    new_factor = normalizedFactor(new_factor)

    return new_factor



f1=Factor(["S"],np.array([0.95,0.05]))
f2=Factor(["M"], np.array([27/28, 1/28]))
f3=Factor(["NA"], np.array([0.7,0.3]))
f4=Factor(["B", "S"], np.array([[0.9, 0.4],[0.1,0.6]]))
f5=Factor(["M","NA", "NH"],
          np.array([[[1,0],[0.5,0.5]],[[0.6,0.4],[0.2, 0.8]]]))
f6=Factor(["FH","M",  "NH", "S"],
          np.array([[[[1,0.5],[0.8,0.25]],
                     [[0.6,0.1],[0.35,0.01]]],

                    [[[0,0.5],[0.2,0.75]],[[0.4,0.9],[0.65,0.99]]]]))

def run_q1():
    print("***********QUESTION 1************")
    factorList=[f1,f2,f3,f4,f5,f6]
    queryVariables = {"FH":1}
    EvidenceList = {}
    orderedListofHiddenVariables = getOrderedListOfHiddenVariables(queryVariables.keys(), EvidenceList.keys())
    result=resultFactor(factorList,queryVariables,orderedListofHiddenVariables, EvidenceList)
    print(result.variables, result.array)
    test=[[[0.32,0.48],[0.14,0.06]],[[0.36,0.54],[0.07,0.03]]]
    #n=sum_out(Factor(["A","B","C"], test), 'B')
   # print(n.array)
    #print(n.variables)

def run_q2():
    """Fido is howling. You look out the window and see that the moon is
    full. What is probability that Fido is sick? P(S|FH=t, M=t )"""
    print("***********QUESTION 2************")
    factorList=[f1,f2,f3,f4,f5,f6]
    queryVariables = {"S":1}
    EvidenceList = {"FH":1, "M":1}
    orderedListofHiddenVariables = getOrderedListOfHiddenVariables(queryVariables.keys(), EvidenceList.keys())
    result=resultFactor(factorList,queryVariables,orderedListofHiddenVariables, EvidenceList)
    print("SOLUTION")
    print(result.variables, result.array)


def run_q3():
    """You walk to the kitchen and
    see that Fido has not eaten and his food bowl is full. Given this new information,
    what is the probability that Fido is sick?"""
    print("***********QUESTION 3************")
    factorList=[f1,f2,f3,f4,f5,f6]
    queryVariables = {"S":1}
    EvidenceList = {"B":1}
    orderedListofHiddenVariables = getOrderedListOfHiddenVariables(queryVariables.keys(), EvidenceList.keys())
    result=resultFactor(factorList,queryVariables,orderedListofHiddenVariables, EvidenceList)
    print("SOLUTION")
    print(result.variables, result.array)



def run_test_input():
    """ Run test input with verified results to test correctness of program"""
    t1=Factor(["E"],np.array([0.9997,0.0003]))
    t2=Factor(["B"],np.array([0.9999, 0.0001]))
    t3=Factor(["E","R"],np.array([[0.9998,0.0002],[0.1,0.9]]))
    t4=Factor(["A", "B", "E"],np.array([[[0.99,0.8],[0.05,0.04]],[[0.01,0.2],[0.95,0.96]]]))
    t5=Factor(["A","W"],np.array([[0.6,0.4],[0.2,0.8]]))
    t6=Factor(["A","G"],np.array([[0.96,0.04],[0.6,0.4]]))
    EvidenceList={"W":1,"G":1}
    queryVariables={"B":1}
    factorList=[t1,t2,t3,t4,t5,t6]
    orderedListofHiddenVariables=["R","E","A"]
    result=resultFactor(factorList,queryVariables,orderedListofHiddenVariables, EvidenceList)
    print(result.__dict__)

#run_q1()

#run_q2()

#run_test_input()

run_q3()