from hulk.hulk import hulk_compile_str


def test():
    p1 =\
        """
        print(3+3);

        for (i in [2,3,4,4]){
            3+4;
            if (true) print("hello"); 
        }

        while (a==b)
            if (true){
                for (i in range(2,3)) 2+2;
            }
        """

    assert hulk_compile_str(p1)

    p2 =\
        """
        let a=[2,3,4,5];

        let w=2 in while(true){
            print(3);
        }
        """

    assert hulk_compile_str(p2)

    p3 =\
        """
        /* klsdvmkm +/**-//9++ 

        lkdnkn;2333@@@334667; */

        hello:=34+4;
        """

    assert hulk_compile_str(p3)

    p4 =\
        """
        let a='2333';

        let s=let w=9 in w*2 in 23;
        """

    assert hulk_compile_str(p4)

    p5 =\
        """
        if(true)
            for (i in [22]){
                print(3);
            }
        """

    assert not hulk_compile_str(p5)

    p6 =\
        """
        if (true ){
            hello:=3;
        } elif(false){
            2+3;
        } else 3+3;
        """

    assert hulk_compile_str(p6)

    p7 =\
        """
        type A inherits B {
            w=w;

            hello() { print('hello');}
            qwe(a:Number):Number => a+a;
        }
        """

    assert hulk_compile_str(p7)

    p8 =\
        """
        type E(w:Number) inherits B(w) {
            consoleWriteLine(s) => print(s);
        }

        """

    assert hulk_compile_str(p8)

    p9 =\
        """
        type E {
            consoleWriteLine(s) => print(s);

            type A {
                w=3;
            }
        }

        """

    assert not hulk_compile_str(p9)

    p10 =\
        """
        let a=[e^2 || e in range(3)];
        """

    assert hulk_compile_str(p10)

    p11 =\
        """
        protocol A extends B{
            hash():Number;
        }
        """

    assert hulk_compile_str(p11)
