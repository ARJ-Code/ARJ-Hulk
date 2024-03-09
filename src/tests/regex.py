from regex.regex import Regex


def test():
    r1 = Regex('[233')
    assert not r1.ok

    r2 = Regex('a|b|c')

    assert r2.match('a').ok
    assert not r2.match('2').ok

    r3 = Regex('a*')
    assert r3.match('aaaaa').ok

    r4 = Regex('a+')
    assert not r4.match('').ok

    r5 = Regex('a?+')
    assert not r5.ok

    r6 = Regex('(a?)+')
    assert r6.ok

    r7 = Regex('/\*([^/\*]|\*[^/])*\*/')
    assert r7.match('/*a*/').ok
    assert not r7.match('/***/').ok

    r8 = Regex('/\*[^(\*/)]*\*/')
    assert r8.match('/***/').ok
