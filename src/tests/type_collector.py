from hulk.hulk import hulk_compile_str

def test():
    type_test =\
        """
            type A inherits B {
                w = 1;
                hello() { print('hello'); }
                qwe(a: Number): Number => a + a;
            }

            protocol C {
                qwe(a: Number): Number;
            }

            type D {
                w = 1;
                hello() { print('hello'); }
                qwe(a: Number): Number => a + a;
            }
            
            let a: A = new A() in {
                a.hello();
                print(a.qwe(2));
            }
        """
    
    assert hulk_compile_str(type_test)