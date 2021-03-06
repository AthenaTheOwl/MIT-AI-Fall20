# MIT 6.034 Lab 5: Bayesian Inference
# Written by 6.034 staff

from nets import *


#### Part 1: Warm-up; Ancestors, Descendents, and Non-descendents ##############

def get_ancestors(net, var):
    "Return a set containing the ancestors of var"
    ancestors = set()
    for p in net.get_parents(var):
        ancestors.add(p)
        ancestors = ancestors.union(get_ancestors(net, p))
    return ancestors

def get_descendants(net, var):
    "Returns a set containing the descendants of var"
    descendants = set()
    for p in net.get_children(var):
        descendants.add(p)
        descendants = descendants.union(get_descendants(net, p))
    return descendants

def get_nondescendants(net, var):
    "Returns a set containing the non-descendants of var"
    non_descendants = set()
    descendants = get_descendants(net, var)
    for v in net.get_variables():
        if v not in descendants:
            non_descendants.add(v)
    non_descendants.remove(var)
    return non_descendants


#### Part 2: Computing Probability #############################################

def simplify_givens(net, var, givens):
    """
    If givens include every parent of var and no descendants, returns a
    simplified list of givens, keeping only parents.  Does not modify original
    givens.  Otherwise, if not all parents are given, or if a descendant is
    given, returns original givens.
    """
    simplified = {}
    parents = net.get_parents(var)
    descendants = get_descendants(net, var)
    given = set(givens.keys())
    if parents.issubset(given):
        for k in given.difference(parents):
            if k in descendants:
                return givens
        for k in given:
            if k in parents:
                simplified.setdefault(k, givens[k])
        return simplified
    return givens
    
def probability_lookup(net, hypothesis, givens=None):
    "Looks up a probability in the Bayes net, or raises LookupError"
    if givens is None:
        try:
            prob = net.get_probability(hypothesis)
            return prob
        except ValueError:
            raise LookupError
    simplified = simplify_givens(net, list(hypothesis)[0], givens)
    # print(net, hypothesis, givens, simplified)
    try:
        prob = net.get_probability(hypothesis, simplified)
        return prob
    except ValueError:
        raise LookupError

def probability_joint(net, hypothesis):
    "Uses the chain rule to compute a joint probability"
    variables = net.topological_sort()
    variables.reverse()
    conditionals = hypothesis.copy()
    prob = 1

    for v in variables:
        value = conditionals.pop(v)
        if conditionals == {}:
            term = probability_lookup(net, {v: value}, None)
        else:
            term = probability_lookup(net, {v: value}, conditionals)
        prob *= term
    return prob
    
def probability_marginal(net, hypothesis):
    "Computes a marginal probability as a sum of joint probabilities"
    joint_prob = net.combinations(net.get_variables(), hypothesis)
    prob = 0
    for j in joint_prob:
        prob += probability_joint(net, j)
    return prob

def probability_conditional(net, hypothesis, givens=None):
    "Computes a conditional probability as a ratio of marginal probabilities"
    if givens is None:
        return probability_marginal(net, hypothesis)

    for h in hypothesis:
        if h in givens:
            if hypothesis[h] != givens[h]:
                return 0

    numerator = probability_marginal(net, dict(hypothesis, **givens))
    denominator = probability_marginal(net, givens)
    return numerator / denominator
    
def probability(net, hypothesis, givens=None):
    "Calls previous functions to compute any probability"
    return probability_conditional(net, hypothesis, givens)

#### Part 3: Counting Parameters ###############################################

def number_of_parameters(net):
    """
    Computes the minimum number of parameters required for the Bayes net.
    """
    num_parameters = 0
    all_variables = net.get_variables()

    for v in all_variables:
        domain_v = len(net.get_domain(v)) - 1
        parents = net.get_parents(v)

        if len(parents) == 0:
            num_parameters += domain_v
        else:
            s = 1
            for p in parents:
                s *= len(net.get_domain(p))
            num_parameters += domain_v * s
    return num_parameters

#### Part 4: Independence ######################################################

def is_independent(net, var1, var2, givens=None):
    """
    Return True if var1, var2 are conditionally independent given givens,
    otherwise False. Uses numerical independence.
    """
    combinations = net.combinations([var1, var2])

    for c in combinations:
        if givens is None:
            prob_A = probability(net, {var1: c[var1]}, None)
            prob_A_B = probability(net, {var1: c[var1]}, {var2: c[var2]})

        else:
            prob_A = probability(net, {var1: c[var1]}, givens)
            prob_A_B = probability(net, {var1: c[var1]}, dict(givens, **{var2: c[var2]}))

        if not (approx_equal(prob_A, prob_A_B, epsilon=0.0000000001)):
            return False
    return True


def is_structurally_independent(net, var1, var2, givens=None):
    """
    Return True if var1, var2 are conditionally independent given givens,
    based on the structure of the Bayes net, otherwise False.
    Uses structural independence only (not numerical independence).
    """
    ancestors = get_ancestors(net, var1).union(get_ancestors(net, var2))

    if givens is not None:
        for g in givens:
            ancestors = get_ancestors(net, g).union(ancestors)
        givens_list = list(givens.keys())
    else:
        givens_list = []

    anc = list(ancestors)
    new_net = net.subnet(ancestors.union(set([var1, var2] + givens_list)))

    for a in ancestors:
        children_a = new_net.get_children(a)
        anc.remove(a)
        for b in anc:
            children_b = new_net.get_children(b)
            if len(children_a.intersection(children_b)) != 0:
                new_net.link(a, b)

    new_net = new_net.make_bidirectional()

    if givens is not None:
        for g in givens:
            new_net.remove_variable(g)

    path = new_net.find_path(var1, var2)

    if path is None:
        return True

    return False
