from functions import Grammar, Rule, EMPTY


def is_n(string):
    return string.isalpha() and string.isupper() \
           or len(string) > 1


def make_doppelganger(n):
    return '^' + n


def find_empty_producing(grammar):
    n = set()
    for p in grammar.p:
        if p.is_empty():
            n.add(p.left)
    flag = True
    while flag:
        n_previous = set(n)
        for p in grammar.p:
            if all(_n in n for _n in p.right):
                n.add(p.left)
        if n == n_previous:
            flag = False
    return list(n)


def exclude_unreachable(grammar):
    new_grammar = Grammar()
    reachable = set()
    reachable.add(grammar.s)
    flag = True
    while flag:
        reachable_previous = set(reachable)
        for p in grammar.p:
            if p.left in reachable:
                for symbol in p.right:
                    if is_n(symbol):
                        reachable.add(symbol)
        if reachable == reachable_previous:
            flag = False
    new_grammar.n = [_n for _n in grammar.n if _n in reachable]
    new_grammar.p = [_p for _p in grammar.p if _p.left in reachable]
    new_grammar.t = grammar.t
    new_grammar.s = grammar.s

    return new_grammar


def algorithm_8_1(grammar):
    new_grammar = Grammar()
    new_grammar.t = grammar.t
    n = set(grammar.n)
    n_empty_producing = find_empty_producing(grammar)
    n = n.union([make_doppelganger(x) for x in n_empty_producing])
    new_grammar.n = list(n)

    if grammar.s in n_empty_producing:
        new_grammar.s = make_doppelganger(grammar.s)
        rule = Rule()
        rule.left = new_grammar.s
        rule.right = [EMPTY]
        new_grammar.p.append(rule)
    else:
        new_grammar.s = grammar.s

    for p in grammar.p:
        if p.is_empty():
            new_grammar.p.append(p)
        else:
            m = 0
            flag = True
            for symbol in p.right:
                if symbol in n_empty_producing and flag:
                    m += 1
                else:
                    flag = False
            if m > 0:
                for i in range(m):
                    rule = Rule()
                    rule.left = p.left
                    rule.right.append(make_doppelganger(p.right[i]))
                    rule.right.extend(p.right[i+1:])
                    new_grammar.p.append(rule)
            if len(p.right) - m > 0:
                rule = Rule()
                rule.left = p.left
                rule.right = p.right[m:]
                new_grammar.p.append(rule)

    for p in new_grammar.p[:]:
        if p.left in n_empty_producing and not p.is_empty():
            rule = Rule()
            rule.left = make_doppelganger(p.left)
            rule.right = p.right[:]
            new_grammar.p.append(rule)

    return exclude_unreachable(new_grammar)


def g_inv(alpha):
    return ''.join(alpha)


def ii_3(alpha, terminals, old_n):
    t = None
    n = list(set(old_n).intersection(set(alpha)))
    rest = []

    if alpha[0] in terminals and n:
        t = alpha[0]
        for _n in n:
            for i in range(len(alpha)):
                if alpha[i] == _n:
                    rest.append(alpha[i+1:])

    return t, n, rest


def algorithm_8_2(grammar):
    new_grammar = Grammar()
    tmp_grammar = algorithm_8_1(grammar)
    new_grammar.t = tmp_grammar.t
    right_exclude = list()
    n_exclude = list()

    for p in tmp_grammar.p:
        if p.is_empty():
            right_exclude.append(p.left)

    for p in tmp_grammar.p:
        right = p.right[:]
        for exclude in right_exclude:
            try:
                right.remove(exclude)
            except ValueError:
                pass
        if len(right) == 0:
            n_exclude.append(p.left)

    new_grammar.p = [_p for _p in tmp_grammar.p if _p.left not in n_exclude]
    for p in new_grammar.p:
        for n in n_exclude:
            try:
                p.right.remove(n)
            except ValueError:
                pass

    new_grammar.s = [tmp_grammar.s]

    new_grammar.n = [new_grammar.s]

    old_rules = tmp_grammar.p[:]
    new_grammar.p = []

    for n in new_grammar.n:
        for p in old_rules:
            first = n[0]
            left = p.left
            if first == left:
                rule = Rule()
                rule.left = n
                rule.right = [g_inv(p.right + n[1:])]
                new_grammar.p.append(rule)
                if p.right != [EMPTY]:
                    new_grammar.n.append(p.right + n[1:])

    old_n = tmp_grammar.n[:]

    for n in new_grammar.n:
        t, not_t, rest = ii_3(n, new_grammar.t, old_n)
        if t and not_t and rest:
            rule = Rule()
            rule.left = n
            rule.right = [t]
            new_grammar.p.append(rule)
            for i in range(len(not_t)):
                for p in tmp_grammar.p:
                    if p.left == not_t[i] and not p.is_empty():
                        rule = Rule()
                        rule.left = n
                        rule.right = [t] + [g_inv(p.right) + g_inv(rest[i])]
                        new_grammar.p.append(rule)
                        new_n = p.right + rest[i]
                        if new_n not in new_grammar.n:
                            new_grammar.n.append(new_n)

    return new_grammar


if __name__ == "__main__":
    g = Grammar()
    g.from_file('INPUT.TXT')
    new_g = algorithm_8_2(g)
    new_g.to_file('OUTPUT.TXT')
