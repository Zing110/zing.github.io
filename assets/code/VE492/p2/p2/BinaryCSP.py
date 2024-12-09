# Hint: from collections import deque
from Interface import *
from collections import deque

# = = = = = = = QUESTION 1  = = = = = = = #


def consistent(assignment, csp, var, value):
    """
    Checks if a value assigned to a variable is consistent with all binary constraints in a problem.
    Do not assign value to var.
    Only check if this value would be consistent or not.
    If the other variable for a constraint is not assigned,
    then the new value is consistent with the constraint.

    Args:
        assignment (Assignment): the partial assignment
        csp (ConstraintSatisfactionProblem): the problem definition
        var (string): the variable that would be assigned
        value (value): the value that would be assigned to the variable
    Returns:
        boolean
        True if the value would be consistent with all currently assigned values, False otherwise
    """
    # TODO: Question 1
    for constraint in csp.binaryConstraints:
        if constraint.affects(var):
            other_var = constraint.otherVariable(var)
            if assignment.isAssigned(other_var) and not constraint.isSatisfied(value, assignment.assignedValues[other_var]):
                return False
    return True


def recursiveBacktracking(assignment, csp, orderValuesMethod, selectVariableMethod, inferenceMethod):
    """
    Recursive backtracking algorithm.
    A new assignment should not be created.
    The assignment passed in should have its domains updated with inferences.
    In the case that a recursive call returns failure or a variable assignment is incorrect,
    the inferences made along the way should be reversed.
    See maintainArcConsistency and forwardChecking for the format of inferences.

    Examples of the functions to be passed in:
    orderValuesMethod: orderValues, leastConstrainingValuesHeuristic
    selectVariableMethod: chooseFirstVariable, minimumRemainingValuesHeuristic
    inferenceMethod: noInferences, maintainArcConsistency, forwardChecking

    Args:
        assignment (Assignment): a partial assignment to expand upon
        csp (ConstraintSatisfactionProblem): the problem definition
        orderValuesMethod (function<assignment, csp, variable> returns list<value>):
            a function to decide the next value to try
        selectVariableMethod (function<assignment, csp> returns variable):
            a function to decide which variable to assign next
        inferenceMethod (function<assignment, csp, variable, value> returns set<variable, value>):
            a function to specify what type of inferences to use
    Returns:
        Assignment
        A completed and consistent assignment. None if no solution exists.
    """
    # TODO: Question 1
    if assignment.isComplete():
        return assignment
    var = selectVariableMethod(assignment, csp)
    for value in orderValuesMethod(assignment, csp, var):
        if consistent(assignment, csp, var, value):
            assignment.assignedValues[var] = value
            oldDomain = assignment.varDomains[var]
            assignment.varDomains[var] = {value}
            inferences = inferenceMethod(assignment, csp, var, value) 
            if inferences is not None:
                result = recursiveBacktracking(assignment, csp, orderValuesMethod, selectVariableMethod, inferenceMethod)
                if result is not None:
                    return result
            assignment.assignedValues[var] = None
            assignment.varDomains[var] = oldDomain
            if not inferences == None:
                for i_var, i_val in inferences:
                    assignment.varDomains[i_var].add(i_val)
    return None
                        
    

def eliminateUnaryConstraints(assignment, csp):
    """
    Uses unary constraints to eleminate values from an assignment.

    Args:
        assignment (Assignment): a partial assignment to expand upon
        csp (ConstraintSatisfactionProblem): the problem definition
    Returns:
        Assignment
        An assignment with domains restricted by unary constraints. None if no solution exists.
    """
    domains = assignment.varDomains
    for var in domains:
        for constraint in (c for c in csp.unaryConstraints if c.affects(var)):
            for value in (v for v in list(domains[var]) if not constraint.isSatisfied(v)):
                domains[var].remove(value)
                # Failure due to invalid assignment
                if len(domains[var]) == 0:
                    return None
    return assignment


def chooseFirstVariable(assignment, csp):
    """
    Trivial method for choosing the next variable to assign.
    Uses no heuristics.
    """
    for var in csp.varDomains:
        if not assignment.isAssigned(var):
            return var


# = = = = = = = QUESTION 2  = = = = = = = #


def minimumRemainingValuesHeuristic(assignment, csp):
    """
    Selects the next variable to try to give a value to in an assignment.
    Uses minimum remaining values heuristic to pick a variable. Use degree heuristic for breaking ties.

    Args:
        assignment (Assignment): the partial assignment to expand
        csp (ConstraintSatisfactionProblem): the problem description
    Returns:
        the next variable to assign
    """
    nextVar = None
    domains = assignment.varDomains

    # TODO: Question 2
    minRemainingValues = float('inf')
    maxDegree = -1

    for var in domains:
        if not assignment.isAssigned(var):
            remainingValues = len(domains[var])
            degree = sum(constraint.affects(var) and not assignment.isAssigned(constraint.otherVariable(var)) for constraint in csp.binaryConstraints)

            if remainingValues < minRemainingValues or (remainingValues == minRemainingValues and degree > maxDegree):
                nextVar = var
                minRemainingValues = remainingValues
                maxDegree = degree

    return nextVar




def orderValues(assignment, csp, var):
    """
    Trivial method for ordering values to assign.
    Uses no heuristics.
    """
    return list(assignment.varDomains[var])


# = = = = = = = QUESTION 3  = = = = = = = #


def leastConstrainingValuesHeuristic(assignment, csp, var):
    """
    Creates an ordered list of the remaining values left for a given variable.
    Values should be attempted in the order returned.
    The least constraining value should be at the front of the list.

    Args:
        assignment (Assignment): the partial assignment to expand
        csp (ConstraintSatisfactionProblem): the problem description
        var (string): the variable to be assigned the values
    Returns:
        list<values>
        a list of the possible values ordered by the least constraining value heuristic
    """
    # TODO: Question 3
    constraint_counts = {}

    # Iterate over all the remaining values of the variable
    for val in assignment.varDomains[var]:
        constraint_count = 0
        # Get the constraints that affect the variable
        for constraint in csp.binaryConstraints:
            if constraint.affects(var):
                # Get the other variable involved in the constraint
                other_var = constraint.otherVariable(var)
                # Iterate over all the remaining values of the other variable
                for other_val in assignment.varDomains[other_var]:
                    # If the value is not consistent with the constraint, increase the count
                    if not constraint.isSatisfied(val, other_val):
                        constraint_count += 1
        # Store the count for the value
        constraint_counts[val] = constraint_count

    # Sort the dictionary by the count in ascending order and extract the keys
    sorted_values = sorted(constraint_counts, key=constraint_counts.get)
    
    return sorted_values
def noInferences(assignment, csp, var, value):
    """
    Trivial method for making no inferences.
    """
    return set([])


# = = = = = = = QUESTION 4  = = = = = = = #


def forwardChecking(assignment, csp, var, value):
    """
    Implements the forward checking algorithm.
    Each inference should take the form of (variable, value)
    where the value is being removed from the domain of variable.
    This format is important so that the inferences can be reversed
    if they result in a conflicting partial assignment.
    If the algorithm reveals an inconsistency,
    any inferences made should be reversed before ending the function.

    Args:
        assignment (Assignment): the partial assignment to expand
        csp (ConstraintSatisfactionProblem): the problem description
        var (string): the variable that has just been assigned a value
        value (string): the value that has just been assigned
    Returns:
        set< tuple<variable, value> >
        the inferences made in this call or None if inconsistent assignment
    """
    inferences = set([])

    # TODO: Question 4
    for constraint in filter(lambda x: x.affects(var), csp.binaryConstraints):
        # Get the other variable involved in the constraint
        other = constraint.otherVariable(var)
        # Check if the value is in the domain of the other variable
        if value in assignment.varDomains[other]:
            # Check if there is more than one value left in the domain of the other variable
            if len(assignment.varDomains[other]) > 1:
                # Add the inference to the set
                inferences.add((other, value))
                # Remove the value from the domain of the other variable
                assignment.varDomains[other].remove(value)
            else:
                # If no value can be assigned to the other variable, reverse the inferences
                for (v, val) in inferences:
                    assignment.varDomains[v].add(val)
                # Return None to indicate an inconsistent assignment
                return None

    # Return the inferences made in this call
    return inferences


# = = = = = = = QUESTION 5  = = = = = = = #


def revise(assignment, csp, var1, var2, constraint):
    """
    Helper function to maintainArcConsistency and AC3.
    Remove values from var2 domain if constraint cannot be satisfied.
    Each inference should take the form of (variable, value)
    where the value is being removed from the domain of variable.
    This format is important so that the inferences can be reversed
    if they result in a conflicting partial assignment.
    If the algorithm reveals an inconsistency,
    any inferences made should be reversed before ending the function.

    Args:
        assignment (Assignment): the partial assignment to expand
        csp (ConstraintSatisfactionProblem): the problem description
        var1 (string): the variable with consistent values
        var2 (string): the variable that should have inconsistent values removed
        constraint (BinaryConstraint): the constraint connecting var1 and var2
    Returns:
        set<tuple<variable, value>>
        the inferences made in this call or None if inconsistent assignment
    """
    inferences = set([])

    # TODO: Question 5
    for val2 in assignment.varDomains[var2]:
        # Initialize a flag to check if the value satisfies the constraint
        isValueSatisfied = False
        # Iterate over all the values in the domain of var1
        for val1 in assignment.varDomains[var1]:
            # Check if the constraint is satisfied
            if constraint.isSatisfied(val1, val2):
                isValueSatisfied = True
                break
        # If the value does not satisfy the constraint, add it to the inferences
        if not isValueSatisfied:
            inferences.add((var2, val2))

    # If all the values in the domain of var2 are inconsistent, return None
    if len(inferences) == len(assignment.varDomains[var2]):
        return None

    # Remove the inconsistent values from the domain of var2
    for (v, val) in inferences:
        assignment.varDomains[v].remove(val)

    # Return the inferences made in this call
    return inferences


def maintainArcConsistency(assignment, csp, var, value):
    """
    Implements the maintaining arc consistency algorithm.
    Inferences take the form of (variable, value)
    where the value is being removed from the domain of variable.
    This format is important so that the inferences can be reversed
    if they result in a conflicting partial assignment.
    If the algorithm reveals an inconsistency,
    and inferences made should be reversed before ending the function.

    Args:
        assignment (Assignment): the partial assignment to expand
        csp (ConstraintSatisfactionProblem): the problem description
        var (string): the variable that has just been assigned a value
        value (string): the value that has just been assigned
    Returns:
        set<<variable, value>>
        the inferences made in this call or None if inconsistent assignment
    """
    inferences = set([])
    domains = assignment.varDomains

    # TODO: Question 5
    #  Hint: implement revise first and use it as a helper function"""
    queue = deque()

    def enqueueConstraints(constraints, variable):
        for constraint in constraints:
            if constraint.affects(variable):
                otherVar = constraint.otherVariable(variable)
                if not assignment.isAssigned(otherVar):
                    queue.append((variable, otherVar, constraint))

    enqueueConstraints(csp.binaryConstraints, var)

    while queue:
        var1, var2, constraint = queue.pop()
        temp = revise(assignment, csp, var1, var2, constraint)
        if temp is None:
            for (v, val) in inferences:
                assignment.varDomains[v].add(val)
            return None
        if len(temp):
            inferences = inferences.union(temp)
            enqueueConstraints(csp.binaryConstraints, var2)

    return inferences


# = = = = = = = QUESTION 6  = = = = = = = #


def AC3(assignment, csp):
    """
    AC3 algorithm for constraint propagation.
    Used as a pre-processing step to reduce the problem
    before running recursive backtracking.

    Args:
        assignment (Assignment): the partial assignment to expand
        csp (ConstraintSatisfactionProblem): the problem description
    Returns:
        Assignment
        the updated assignment after inferences are made or None if an inconsistent assignment
    """
    inferences = set([])

    # TODO: Question 6
    #  Hint: implement revise first and use it as a helper function"""
    queue = deque()
    # Initialize the queue with all arcs in the CSP
    for var in csp.varDomains:
        for constraint in csp.binaryConstraints:
            if constraint.affects(var):
                queue.append((var, constraint.otherVariable(var), constraint))

    # Iterate over all the arcs in the CSP
    while queue:
        var1, var2, constraint = queue.pop()
        temp_inferences = revise(assignment, csp, var1, var2, constraint)
        # If the revise function returns None, return None
        if temp_inferences is None:
            for inference in inferences:
                assignment.varDomains[inference[0]].add(inference[1])
            return None
        # If the revise function returns a set of inferences, add them to the set
        if len(temp_inferences):
            inferences = inferences.union(temp_inferences)            
            for constraint in csp.binaryConstraints:
                if constraint.affects(var2):
                    otherVar = constraint.otherVariable(var2)
                    if not assignment.isAssigned(otherVar):
                        queue.append((var2, otherVar, constraint))

    return assignment    



def solve(csp, orderValuesMethod=leastConstrainingValuesHeuristic,
          selectVariableMethod=minimumRemainingValuesHeuristic,
          inferenceMethod=forwardChecking, useAC3=True):
    """
    Solves a binary constraint satisfaction problem.

    Args:
        csp (ConstraintSatisfactionProblem): a CSP to be solved
        orderValuesMethod (function): a function to decide the next value to try
        selectVariableMethod (function): a function to decide which variable to assign next
        inferenceMethod (function): a function to specify what type of inferences to use
        useAC3 (boolean): specifies whether to use the AC3 pre-processing step or not
    Returns:
        dictionary<string, value>
        A map from variables to their assigned values. None if no solution exists.
    """
    assignment = Assignment(csp)

    assignment = eliminateUnaryConstraints(assignment, csp)
    if assignment is None:
        return assignment

    if useAC3:
        assignment = AC3(assignment, csp)
        if assignment is None:
            return assignment

    assignment = recursiveBacktracking(assignment, csp, orderValuesMethod, selectVariableMethod, inferenceMethod)
    if assignment is None:
        return assignment

    return assignment.extractSolution()
