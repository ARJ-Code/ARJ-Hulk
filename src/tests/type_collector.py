from hulk.hulk import hulk_compile_str

def test():
    type_test =\
        """
            type A(x: Number, y: String) inherits B {
                w: Number = x;
                hello(): Number { print('hello'); }
                qwe(a: Number): Number => a + a;
            }

            type B {
                a = 2;
            }

            protocol D {
                hello(a: A, b: [A, 2]): A;
            }

            protocol C extends D {
                qwe(a: Number): Number;
            }
            
            let a: A = new A() in {
                a.hello();
                print(a.qwe(2));
            }
        """
    
    # assert hulk_compile_str(type_test)

    type_test =\
        """
            type A(x, y) {
                w = x;
                hello() { print('hello'); }
                qwe(a: Number): Number => a + a;
            }

            type B {
                y: Number = 2;
            }
            
            let a: A = new A() in {
                a.hello();
                print(a.qwe(2));
            }
        """
    
    assert hulk_compile_str(type_test)