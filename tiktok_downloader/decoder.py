# Menghadeh Convert dari Js ke Py
# Decryptor For Snaptik/Tikmate Obfuscate

from typing import Union
from ast import literal_eval
from re import findall
alpha = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ+/"


def search(d: Union[str, list], q: str):
    try:
        return d.index(q)
    except Exception:
        return -1


def main(d, e, f):
    g = list(alpha)
    h = g[0:e]
    i = g[0:f]

    def freduce(a, b, c):
        if search(h, b) != -1:
            a += search(h, b) * (e ** c)
            return a
    j = reduces(freduce, list(d)[::-1], 0)
    k = ""
    while j > 0:
        k = i[j % f] + k
        j = int((j - (j % f)) / f)
    return int(k) or 0

def from_string(text: str):
    return decoder(*literal_eval(
            findall(
                r'\(\".*?,.*?,.*?,.*?,.*?.*?\)',
                text
            )[0]
        ))

def reduces(function, iterable, initializer=None) -> int:
    """
    [!] modified reduce function like js
    :https://www.geeksforgeeks.org/reduce-in-python/
    """
    it = iter(iterable)
    if initializer is None:
        value = next(it)
    else:
        value = function(initializer, next(it), 0)
    for index, element in enumerate(it, 1):
        value = function(value, element, index)
    return value


def decoder(h, u, n, t, e, r):
    r = ""
    i = 0
    while i < h.__len__():
        s = ""
        while h[i] != n[e]:
            s += h[i]
            i += 1
        for j in range(n.__len__()):
            s = s.replace(n[j], j.__str__())
        r += chr(main(s, e, 10) - t)
        i += 1
    return r
