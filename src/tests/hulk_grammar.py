from hulk.hulk import hulk_compile_str


def test():
    p1 =\
        """
        {
            for (i in [2,3,4,4]){
                3+4;
                if (true) print("hello") else 3+3; 
            };
        }
        """

    assert hulk_compile_str(p1)

    # p2 =\
    #     """
    #     let a=[2,3,4,5] in
    #         let w=2 in while(true){
    #             print(3);
    #         }
    #     """

    # assert hulk_compile_str(p2)

    # p3 =\
    #     """
    #     /* klsdvmkm +/**-//9++ 

    #     lkdnkn;2333@@@334667; */

    #     hello:=34+4;
    #     """

    # assert hulk_compile_str(p3)

    # p4 =\
    #     """
    #     let a='2333' in 
    #         let s=let w=9 in w*2 in 23;
    #     """

    # assert hulk_compile_str(p4)

    # p5 =\
    #     """
    #     if(true)
    #         for (i in [22]){
    #             print(3);
    #         }
    #     ;
    #     """

    # assert not hulk_compile_str(p5)

    # p6 =\
    #     """
    #     if (true ){
    #         hello:=3;
    #     } elif(false){
    #         2+3;
    #     } else 3+3;
    #     """

    # assert hulk_compile_str(p6)

    # p7 =\
    #     """
    #     type A inherits B {
    #         w=w;

    #         hello() { print('hello');}
    #         qwe(a:Number):Number => a+a;
    #     }

    #     print('hello');
    #     """

    # assert hulk_compile_str(p7)

    # p8 =\
    #     """
    #     type E(w:Number) inherits B(w) {
    #         consoleWriteLine(s) => print(s);
    #     }

    #     let b = new E(2) in {
    #         b.consoleWriteLine('hello');
    #     }
    #     """

    # assert hulk_compile_str(p8)

    # p9 =\
    #     """
    #     type E {
    #         consoleWriteLine(s) => print(s);

    #         type A {
    #             w=3;
    #         }
    #     }

    #     print('hello');
    #     """

    # assert not hulk_compile_str(p9)

    # p10 =\
    #     """
    #     let a=[e^2 || e in range(3)] in print(a);
    #     """

    # assert hulk_compile_str(p10)

    # p11 =\
    #     """
    #     protocol A extends B{
    #         hash():Number;
    #     }

    #     print('hello');
    #     """

    # assert hulk_compile_str(p11)

    p12 =\
        """
        let a = [1,2,3,4,5] in {
            print(a[3]);
        }
        """

    assert hulk_compile_str(p12)