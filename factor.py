import numpy as np

class Factor:

    '''Class for defining factors. A factor is a function that is over
    an ORDERED sequence of variables called its scope. It maps every
    assignment of values to these variables to a number. In a Bayes
    Net every CPT is represented as a factor. Pr(A|B,C) for example
    will be represented by a factor over the variables (A,B,C). If we
    assign A = a, B = b, and C = c, then the factor will map this
    assignment, A=a, B=b, C=c, to a number that is equal to Pr(A=a|
    B=b, C=c). During variable elimination new factors will be
    generated. However, the factors computed during variable
    elimination do not necessarily correspond to conditional
    probabilities. Nevertheless, they still map assignments of values
    to the variables in their scope to numbers.
    Note that if the factor's scope is empty it is a constaint factor
    that stores only one value. add_values would be passed something
    like [[0.25]] to set the factor's single value. The get_value
    functions will still work.  E.g., get_value([]) will return the
    factor's single value. Constaint factors migth be created when a
    factor is restricted.'''

    def __init__(self, name, variables, array):
        '''create a Factor object, specify the Factor name (a string)
        and its scope (an ORDERED list of variable objects).'''
        self.name = name
        self.variables = variables
        self.array = array

    def get_variables(self):
        '''returns copy of scope...you can modify this copy without affecting
           the factor object'''
        return self.variables

    def return_indices(self, variable):
        '''given list of variables, return a pair (indices of what )'''
        for i in range(len(self.variables)):
            if variable == var:
                return i
        raise Exception("variable in not factor's list of variables!")

    def expand(self, name, var_to_expand_on, new_var_set):
        ''' return a NEW expanded factor'''
        copy_array = np.copy(self.array)
        print(new_var_set)
        print(var_to_expand_on)
        axis = new_var_set.index(var_to_expand_on[0]) #assuming only expand on one new var
        arr = np.expand_dims(self.array, axis=axis)
        array = np.concatenate((arr, arr), axis = axis)

        return Factor(name, new_var_set, array)

    def sumout(self, var):
        


    def return_uncommon_variables(self, variables):
        uncommon=[]
        for variable in variables:
            if variable not in self.variables:
                uncommon.append(variable)
        return uncommon




    #def __repr__(self):
    #    return ""