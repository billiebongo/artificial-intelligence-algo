import numpy as np

class Factor:


    def __init__(self, variables, array):
        '''create a Factor object, specify the Factor name (a string)
        and its scope (an ORDERED list of variable objects).'''

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
        ''' return a NEW expanded factor for multi'''
        copy_array = np.copy(self.array)
        print(new_var_set)
        print(var_to_expand_on)
        axis = new_var_set.index(var_to_expand_on[0]) #assuming only expand on one new var
        arr = np.expand_dims(self.array, axis=axis)
        array = np.concatenate((arr, arr), axis = axis)

        return Factor(name, new_var_set, array)

    def sumout(self, name,var):
        """ sums out variable from factor"""
        var_idx = self.variables.index(var)

        return Factor(name, self.variables.remove(var),self.array.sum(axis=var_idx))


    def return_uncommon_variables(self, variables):
        uncommon=[]
        for variable in variables:
            if variable not in self.variables:
                uncommon.append(variable)
        return uncommon




    #def __repr__(self):
    #    return ""