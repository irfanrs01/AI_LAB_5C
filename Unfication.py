def is_variable(x):
    return isinstance(x, str) and x.islower()

def occurs_check(var, x, subs):
    if var == x:
        return True
    elif isinstance(x, (list, tuple)):
        return any(occurs_check(var, xi, subs) for xi in x)
    elif x in subs:
        return occurs_check(var, subs[x], subs)
    return False

def unify_var(var, x, subs):
    if var in subs:
        return unify(subs[var], x, subs)
    elif x in subs:
        return unify(var, subs[x], subs)
    elif occurs_check(var, x, subs):
        return None
    else:
        subs[var] = x
        return subs

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


expr1 = input("Enter first expression as tuple: ")
expr2 = input("Enter second expression as tuple: ")

expr1 = eval(expr1)
expr2 = eval(expr2)

result = unify(expr1, expr2)
print("Unifier:", result)
