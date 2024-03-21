from hulk.hulk import hulk_compile_str


def test():
    string_test =\
        """
            let a = "hello" @@ "world" in {
                print(a);
                print("hello" @ "world");
            };
        """

    assert hulk_compile_str(string_test)

    # boolean_test =\
    #     """
    #         let a = true in {
    #             print(a);
    #             print(!a);
    #             print(a && false);
    #             print(a || false);
    #             1 == 2;
    #             if (1 != 2) {
    #                 print(3);
    #             }
    #             elif (1 < 2) {
    #                 print(4);
    #             }
    #             else {
    #                 print(5);
    #             }
    #             1 > 2;
    #             1 <= 2;
    #             1 >= 2;
    #         }
    #     """
    
    # assert hulk_compile_str(boolean_test)

    # arithmetic_test =\
    #     """
    #         let a = 2 + 3 * 4 in {
    #             print(a);
    #             +3;
    #             -3;
    #             3+3;
    #             3 / 3;
    #         }
    #     """
    
    # assert hulk_compile_str(arithmetic_test)

    # declaration_test =\
    #     """
    #         let a = 2, b = 4, c = 8 in {
    #             print(a * b - c);
    #             a := 5;
    #             print(a);
    #         }
    #     """
    
    # assert hulk_compile_str(declaration_test)

    # array_test =\
    #     """
    #         let a = [2, 3, 4, 5] in {
    #             print(a);
    #             print(a[2]);
    #             a[2] := 9;
    #             print(a);
    #         }
    #     """
    
    # assert hulk_compile_str(array_test)

    # while_test =\
    #     """
    #         let a = [2, 3, 4, 5] in {
    #             let w = 2 in while (true) {
    #                 print(3);
    #             }
    #         }
    #     """
    
    # assert hulk_compile_str(while_test)

    # comment_test =\
    #     """
    #         /* klsdvmkm +/**-//9++ 
    #         lkdnkn;2333@@@334667; */
    #         hello := 34 + 4;
    #     """
    
    # assert hulk_compile_str(comment_test)

    # nested_let_test =\
    #     """
    #         let a = '2333' in {
    #             let s = let w = 9 in w * 2 in 23;
    #         }
    #     """
    
    # assert hulk_compile_str(nested_let_test)

    # for_test =\
    #     """
    #         for (i in [22, 33, 44]) {
    #             print(i);
    #         };
    #     """
    
    # assert not hulk_compile_str(for_test)

    if_test =\
        """
            if (true) {
                hello := 3;
            } elif (false) {
                2 + 3;
            } else 3 + 3;
        """
    
    assert hulk_compile_str(if_test)

    # type_test =\
    #     """
    #         type A inherits B {
    #             let w = 1;
    #             hello() { print('hello'); }
    #             qwe(a: Number): Number => a + a;
    #         }   
            
    #         let a: B = new A in {
    #             a.hello();
    #             print(a.qwe(2));
    #         }
    #     """
    
    # assert hulk_compile_str(type_test)


    p2 =\
        """
        let a=[2,3,4,5] in
            let w=2 in while(true){
                print(3);
            }
        """

    assert hulk_compile_str(p2)

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