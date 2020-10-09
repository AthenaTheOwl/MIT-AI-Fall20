# MIT 6.034 Lab 3: Constraint Satisfaction Problems
# Written by 6.034 staff

from constraint_api import *
from test_problems import get_pokemon_problem


#### Part 1: Warmup ############################################################

def has_empty_domains(csp):
    """Returns True if the problem has one or more empty domains, otherwise False"""
    for domain in list(csp.domains.values()):
        if len(domain) == 0:
            return True
    return False


def check_all_constraints(csp):
    """Return False if the problem's assigned values violate some constraint,
    otherwise True"""
    if csp.assignments == {}:
        return True
    for constraint in csp.get_all_constraints():
        var1 = csp.get_assignment(constraint.var1)
        var2 = csp.get_assignment(constraint.var2)
        if var1 is not None and var2 is not None:
            if not constraint.check(var1, var2):
                return False
    return True


#### Part 2: Depth-First Constraint Solver #####################################

def solve_constraint_dfs(problem):
    """
    Solves the problem using depth-first search.  Returns a tuple containing:
    1. the solution (a dictionary mapping variables to assigned values)
    2. the number of extensions made (the number of problems popped off the agenda).
    If no solution was found, return None as the first element of the tuple.
    """
    if has_empty_domains(problem):
        return None, 1
    extensions = 0
    solution = [problem]
    while len(solution) > 0:
        node = solution.pop(0)
        extensions += 1
        if not has_empty_domains(node) and check_all_constraints(node):
            nextvar = node.pop_next_unassigned_var()
            additions = []
            if nextvar is None:
                return node.assignments, extensions
            for value in node.get_domain(nextvar):
                additions.append(node.copy().set_assignment(nextvar, value))
            solution = additions + solution
    return None, extensions


# QUESTION 1: How many extensions does it take to solve the Pokemon problem
#    with DFS?

# Hint: Use get_pokemon_problem() to get a new copy of the Pokemon problem
#    each time you want to solve it with a different search method.

ANSWER_1 = 20


#### Part 3: Forward Checking ##################################################

def eliminate_from_neighbors(csp, var):
    """
    Eliminates incompatible values from var's neighbors' domains, modifying
    the original csp.  Returns an alphabetically sorted list of the neighboring
    variables whose domains were reduced, with each variable appearing at most
    once.  If no domains were reduced, returns empty list.
    If a domain is reduced to size 0, quits immediately and returns None.
    """
    eliminations = []
    pcopy = csp.copy()
    for neighbor in csp.get_neighbors(var):
        constraints = csp.constraints_between(neighbor, var)
        if len(constraints) > 1:
            csp.set_domain(neighbor, [])
            return None
        else:
            for val1 in csp.get_domain(neighbor):
                count = 0
                for val2 in csp.get_domain(var):
                    if constraints[0].check(val1, val2):
                        count += 1
                if count == 0:
                    pcopy.eliminate(neighbor, val1)
                    csp.set_domain(neighbor, pcopy.get_domain(neighbor))
                    if len(csp.get_domain(neighbor)) == 0:
                        return None
                    eliminations.append(neighbor)
    return sorted(list(set(eliminations)))


# Because names give us power over things (you're free to use this alias)
forward_check = eliminate_from_neighbors


def solve_constraint_forward_checking(problem):
    """
    Solves the problem using depth-first search with forward checking.
    Same return type as solve_constraint_dfs.
    """
    if has_empty_domains(problem):
        return None, 1
    extensions = 0
    solution = [problem]
    while len(solution) > 0:
        node = solution.pop(0)
        extensions += 1
        if not has_empty_domains(node) and check_all_constraints(node):
            nextvar = node.pop_next_unassigned_var()
            additions = []
            if nextvar is None:
                return node.assignments, extensions
            for value in node.get_domain(nextvar):
                csp = node.copy().set_assignment(nextvar, value)
                forward_check(csp, nextvar)
                additions.append(csp)
            solution = additions + solution
    return None, extensions


# QUESTION 2: How many extensions does it take to solve the Pokemon problem
#    with DFS and forward checking?

ANSWER_2 = 9


#### Part 4: Domain Reduction ##################################################

def domain_reduction(csp, queue=None):
    """
    Uses constraints to reduce domains, propagating the domain reduction
    to all neighbors whose domains are reduced during the process.
    If queue is None, initializes propagation queue by adding all variables in
    their default order. 
    Returns a list of all variables that were dequeued, in the order they
    were removed from the queue.  Variables may appear in the list multiple times.
    If a domain is reduced to size 0, quits immediately and returns None.
    This function modifies the original csp.
    """
    if queue == None:
        queue = csp.get_all_variables()
    dequeue = []
    while len(queue) > 0:
        var = queue.pop(0)
        fc = forward_check(csp, var)
        if fc is None:
            return None
        queue = queue + fc
        dequeue.append(var)
    return dequeue


# QUESTION 3: How many extensions does it take to solve the Pokemon problem
#    with DFS (no forward checking) if you do domain reduction before solving it?

ANSWER_3 = 6


def solve_constraint_propagate_reduced_domains(problem):
    """
    Solves the problem using depth-first search with forward checking and
    propagation through all reduced domains.  Same return type as
    solve_constraint_dfs.
    """
    if has_empty_domains(problem):
        return None, 1
    extensions = 0
    solution = [problem]
    while len(solution) > 0:
        node = solution.pop(0)
        extensions += 1
        if not has_empty_domains(node) and check_all_constraints(node):
            nextvar = node.pop_next_unassigned_var()
            additions = []
            if nextvar is None:
                return node.assignments, extensions
            for value in node.get_domain(nextvar):
                csp = node.copy().set_assignment(nextvar, value)
                domain_reduction(csp, [nextvar])
                additions.append(csp)
            solution = additions + solution
    return None, extensions

# QUESTION 4: How many extensions does it take to solve the Pokemon problem
#    with forward checking and propagation through reduced domains?

ANSWER_4 = 7


#### Part 5A: Generic Domain Reduction #########################################

def propagate(enqueue_condition_fn, csp, queue=None):
    """
    Uses constraints to reduce domains, modifying the original csp.
    Uses enqueue_condition_fn to determine whether to enqueue a variable whose
    domain has been reduced. Same return type as domain_reduction.
    """
    if queue is None:
        queue = csp.get_all_variables()
    dequeue = []
    while len(queue) > 0:
        var = queue.pop(0)
        fc = forward_check(csp, var)
        if fc is None:
            return None
        for v in fc:
            if enqueue_condition_fn(csp, v):
                queue.append(v)
        dequeue.append(var)
    return dequeue

def condition_domain_reduction(csp, var):
    """Returns True if var should be enqueued under the all-reduced-domains
    condition, otherwise False"""
    return True

def condition_singleton(csp, var):
    """Returns True if var should be enqueued under the singleton-domains
    condition, otherwise False"""
    return len(csp.get_domain(var)) == 1


def condition_forward_checking(csp, var):
    """Returns True if var should be enqueued under the forward-checking
    condition, otherwise False"""
    return False


#### Part 5B: Generic Constraint Solver ########################################

def solve_constraint_generic(problem, enqueue_condition=None):
    """
    Solves the problem, calling propagate with the specified enqueue
    condition (a function). If enqueue_condition is None, uses DFS only.
    Same return type as solve_constraint_dfs.
    """
    if has_empty_domains(problem):
        return None, 1
    extensions = 0
    solution = [problem]
    while len(solution) > 0:
        node = solution.pop(0)
        extensions += 1
        if not has_empty_domains(node) and check_all_constraints(node):
            nextvar = node.pop_next_unassigned_var()
            if nextvar is None:
                return node.assignments, extensions
            additions = []
            for val in node.get_domain(nextvar):
                csp = node.copy().set_assignment(nextvar, val)
                if enqueue_condition is not None:
                    propagate(enqueue_condition, csp, [nextvar])
                additions.append(csp)
            solution = additions + solution
    return None, extensions

# QUESTION 5: How many extensions does it take to solve the Pokemon problem
#    with forward checking and propagation through singleton domains? (Don't
#    use domain reduction before solving it.)

ANSWER_5 = 8


#### Part 6: Defining Custom Constraints #######################################

def constraint_adjacent(m, n):
    """Returns True if m and n are adjacent, otherwise False.
    Assume m and n are ints."""
    return m-1 == n or m+1 == n


def constraint_not_adjacent(m, n):
    """Returns True if m and n are NOT adjacent, otherwise False.
    Assume m and n are ints."""
    return m-1 != n and m+1 != n


def all_different(variables):
    """Returns a list of constraints, with one difference constraint between
    each pair of variables."""
    constraint_list = []
    for i in range(len(variables)):
        for j in range(i+1, len(variables)):
            constraint_list.append(Constraint(variables[i], variables[j], constraint_different))
    return constraint_list


#### SURVEY ####################################################################

NAME = 'Vignesh Gopalakrishnan'
COLLABORATORS = None
HOW_MANY_HOURS_THIS_LAB_TOOK = 5
WHAT_I_FOUND_INTERESTING = 'Setting up different ways of solving constraint satisfaction problems'
WHAT_I_FOUND_BORING = 'Got stuck a few times in coding certain things like the elimination from neighbors'
SUGGESTIONS = None
