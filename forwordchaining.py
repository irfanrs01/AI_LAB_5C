def unify_var(var, x, subs):
    if var in subs:
        return unify(subs[var], x, subs)
    elif x in subs:
        return unify(var, subs[x], subs)
    elif var == x:
        return {}
    else:
        subs[var] = x
        return subs

def is_variable(x):
    return isinstance(x, str) and x.islower()

def unify(x, y, subs=None):
    if subs is None:
        subs = {}
    if x == y:
        return subs
    if is_variable(x):
        return unify_var(x, y, subs)
    if is_variable(y):
        return unify_var(y, x, subs)
    if isinstance(x, (list, tuple)) and isinstance(y, (list, tuple)):
        if len(x) != len(y):
            return None
        for xi, yi in zip(x, y):
            subs = unify(xi, yi, subs)
            if subs is None:
                return None
        return subs
    return None

def substitute(fact, subs):
    if isinstance(fact, (list, tuple)):
        return tuple(substitute(x, subs) for x in fact)
    elif fact in subs:
        return subs[fact]
    else:
        return fact

def forward_chain(kb_facts, kb_rules, query):
    wm = kb_facts.copy()
    while True:
        new_facts = []
        for rule in kb_rules:
            premises, conclusion = rule
            subs_list = [{}]
            for premise in premises:
                temp_subs_list = []
                for subs in subs_list:
                    for fact in wm:
                        subs_new = unify(substitute(premise, subs), fact, subs.copy())
                        if subs_new is not None:
                            temp_subs_list.append(subs_new)
                subs_list = temp_subs_list
            for subs in subs_list:
                inferred = substitute(conclusion, subs)
                if inferred not in wm and inferred not in new_facts:
                    new_facts.append(inferred)
        if not new_facts:
            break
        wm.extend(new_facts)
        if query in wm:
            return True, wm
    return query in wm, wm

kb_facts = [
    ('Sell','Robert','Missal'),
    ('Hostile','Robert'),
    ('American','Robert')
]

kb_rules = [
    ([('Sell','x','y'),('Hostile','x')], ('Criminal','x')),
    ([('American','x'),('Criminal','x')], ('Investigate','x'))
]

query = ('Investigate','Robert')

result, final_facts = forward_chain(kb_facts, kb_rules, query)
print("Query Result:", result)
print("Derived Facts:", final_facts)
