#!/usr/bin/python
# -*- coding: utf8

import sys,re,string,math,copy;
from itertools import *;

class fdep(object):
    def __init__(self, x_chars, y_chars , b):
        # x --> y | b(= certainity degree for probabilstic fdep,range = [0,1])
        self.x = set([c.lower() for c in x_chars])
        self.y = set([c.lower() for c in y_chars])
        self.b = b
        
    def __eq__(self, other):
        tmp_self_y = self.y.union(self.x)
        tmp_other_y = other.y.union(other.x)
        return self.x == other.x and tmp_self_y == tmp_other_y and self.b == other.b

    def __ne__(self, other):
        return not self.__eq__(other)

    def __str__(self):
        return '%s-->%s | %d' % (
            ''.join([str(v) for v in self.x]),
            ''.join([str(v) for v in self.y]),
            self.b
        )

    def __repr__(self):
        return "fdep(%s)" % self.__str__()

#   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
def closure(a_set, f_deps):
    for dep in f_deps:
        if dep.x.issubset(a_set):
            a_set = a_set.union(dep.y)
    return a_set

def get_keys(sets, f_deps, full_set):
    c_keys = []
    f_plus = []
    s_keys = []
    for s in sets:
        tmp = closure(s, f_deps)
        f_plus.append(fdep(s, tmp , 1))
        if is_full_set(tmp, full_set):
            s_keys.append([ch for ch in s])
            if not is_ck_superset(s, c_keys):
                c_keys.append([ch for ch in s])
    return c_keys, s_keys, f_plus

def is_full_set(chars, full_set):
    return set([c for c in chars]) == full_set

def is_ck_superset(chars, ck_list):
    for key in ck_list:
        if chars.issuperset(set(key)):
            return True
    return False

def is_trivial(left_set, right_set):
    return right_set.issubset(left_set)

def is_superkey(left_chars, super_keys):
    return left_chars in [set(k) for k in super_keys]

def is_schema_bcnf(f_deps, s_keys, verbose=False):
    results = []
    for fd in f_deps:
        results.append(is_f_bcnf(fd, s_keys))
    for i, r in enumerate(results):
        if not r and verbose:
            print '%s violates BCNF' % f_deps[i]
    return sum(results) == len(f_deps)

def is_f_bcnf(f_dep, s_keys):
    return f_dep.x in s_keys

def is_schema_3nf(f_deps, s_keys, c_keys, verbose=False):
    results = []
    for fd in f_deps:
        results.append(
            not is_superkey(fd.x, s_keys) and
            not is_trivial(fd.x, fd.y) and
            not is_prime_attribute(fd.x, fd.y, c_keys)
        )
    for i, r in enumerate(results):
        if r and verbose:
            print '%s violates 3NF' % f_deps[i]
    return sum(results) == 0

def is_prime_attribute(x_set, a_set, cks):
    diff = a_set.difference(x_set)
    for ch in diff:
        for k in cks:
            if ch in k:
                return True
    return False


def get_attribute_sets(attribs):
    fd_set = [set(val) for val in attribs]

    # pairs
    for i in range(len(attribs)):
        for j in range(i + 1, len(attribs)):
            tmp = set([attribs[i], attribs[j]])
            if not tmp in fd_set:
                fd_set.append(tmp)

    # threes
    for i in range(len(attribs)):
        for j in range(i + 1, len(attribs)):
            for k in range(j + 1, len(attribs)):
                tmp = set([attribs[i], attribs[j], attribs[k]])
                if not tmp in fd_set:
                    fd_set.append(tmp)
                    
    # fours
    for i in range(len(attribs)):
        for j in range(i + 1, len(attribs)):
            for k in range(j + 1, len(attribs)):
                for l in range(k + 1, len(attribs)):
                    tmp = set([attribs[i], attribs[j], attribs[k], attribs[l]])
                    if not tmp in fd_set:
                        fd_set.append(tmp)
                        
    # fives
    for i in range(len(attribs)):
        for j in range(i + 1, len(attribs)):
            for k in range(j + 1, len(attribs)):
                for l in range(k + 1, len(attribs)):
                    for m in range(l + 1, len(attribs)):
                        tmp = set([attribs[i], attribs[j], attribs[k], attribs[l], attribs[m]])
                        if not tmp in fd_set:
                            fd_set.append(tmp)
                            
    # sixes
    for i in range(len(attribs)):
        for j in range(i + 1, len(attribs)):
            for k in range(j + 1, len(attribs)):
                for l in range(k + 1, len(attribs)):
                    for m in range(l + 1, len(attribs)):
                        for n in range(m + 1, len(attribs)):
                            tmp = set([attribs[i], attribs[j], attribs[k], attribs[l], attribs[m], attribs[n]])
                            if not tmp in fd_set:
                                fd_set.append(tmp)
                                
    return fd_set


#   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


def decompose_bcnf(a_set, f_deps):
    decomp = []
    a_decomp = copy.deepcopy(a_set)
    all_attribs = get_attribute_sets(list(a_decomp))
    cks, sks, f_plus = get_keys(all_attribs, f_deps, a_decomp)
    while f_deps:
        for i, fd in enumerate(f_deps):
            if not is_f_bcnf(fd, sks):
             break

        decomp.append(
            (set(list(fd.x) + list(fd.y)), fd)
        )
        # remove fd
        f_deps = [f_deps[j] for j in range(len(f_deps)) if j != i]
        diff = fd.y.difference(fd.x)
        a_decomp = a_decomp.difference(diff)
        f_deps = [fd2 for fd2 in f_deps if fd2.x.union(fd2.y).issubset(a_decomp)]
        continue

    if a_decomp:
        decomp.append(
            (set(list(a_decomp)), None)
        )
    return decomp

#def synthesis_3nf(a_set , f_depts):

#   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def main():
    #a = ['a', 'b', 'c', 'd', 'e', 'g', 'h']
    # a = ['a', 'b', 'c', 'd', 'e']
    a = ['a', 'b', 'c', 'd', 'e']
    full_set = frozenset(a)

    f_deps = [
        fdep('c', 'b', 1),
        fdep('c', 'a', 1),
        fdep('c', 'd' , 2),
        fdep('ac', 'd' , 3),
        fdep('ae', 'bcd', 3)
    ]

    all_attribs = get_attribute_sets(a)

    cks, sks, f_plus = get_keys(all_attribs, f_deps, full_set)
    for d in f_plus:
        out_str = str(d)
        if is_trivial(d.x, d.y):
            out_str += ' T'
        if is_superkey(d.x, sks):
            out_str += ' S'
        print '%s' % out_str

    # sort'em
    [k.sort() for k in cks]
    [k.sort() for k in sks]

    print 'Super Keys:'
    for k in sks:
        print '\t%s' % ''.join(k)
    print 'Candidate Keys:'
    for k in cks:
        print '\t%s' % ''.join(k)

    print 'In BCNF: %s' % is_schema_bcnf(f_deps, sks)
    print 'In 3NF: %s' % is_schema_3nf(f_deps, sks, cks)

    bcnf_result = decompose_bcnf(full_set, f_deps)
    for s, f in bcnf_result:
        print s, f

if __name__ == '__main__':
    main()
