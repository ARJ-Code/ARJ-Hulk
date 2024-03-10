from regex.regex import Regex


def test():
    r1 = Regex('[233')
    assert not r1.ok

    r2 = Regex('a|b|c')

    assert r2.match('a')
    assert not r2.match('2')

    r3 = Regex('a*')
    assert r3.match('aaaaa')

    r4 = Regex('a+')
    assert not r4.match('')

    r5 = Regex('a?+')
    assert not r5.ok

    r6 = Regex('(a?)+')
    assert r6.ok

    r7 = Regex('a?')
    assert r7.match('')
    assert r7.match('a')

    r8 = Regex('q|.')
    assert r8.match('w')

    r9 = Regex('[^ba]*')
    assert not r9.match('aac')
    assert r9.match('cwd')

    r10 = Regex('/\*([^\*]|\*[^/])*(\*/|\*\*/)')
    assert r10.match('/*a*/')
    assert r10.match('/***/')
    assert r10.match('/*a**/')
    assert not r10.match('/**/a')
    assert r10.match('/*a/a*/')

    r11 = Regex('[a-z]')
    assert r11.match('a')
    assert not r11.match('A')

    r12 = Regex('[^a-z]')
    assert r12.match('A')

    r13=Regex('[^a-z]*')
    assert r13.match('EEE')
