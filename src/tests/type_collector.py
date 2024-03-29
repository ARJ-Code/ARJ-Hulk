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
            type A(x, y) inherits B {
                w = x;
                hello() { print('hello'); }
                qwe(a: Number): Number => a + a;
            }

            type B inherits A {
                y: Number = 2;
            }

            function raudel(a: A) => 2;
            
            let a: A = new A() in {
                a.hello();
                print(a.qwe(2));
            }
        """
    
    # assert hulk_compile_str(type_test)

    let_test =\
        """
            let a = 2 in 2;
        """
    
    # assert hulk_compile_str(let_test)

    if_test =\
        """
            let a: Number = if (2 >= 3) 'a' elif (true) 2 else '2' in 2;
        """
    
    # assert hulk_compile_str(if_test)

    while_test =\
        """
            let a = while (2 - 3 > 0) {
                2 + 2;
                'hola' @@ 'jky';
                2 @ true; 
                let b: Number = 2 in 3 + 2;
            } in 'hello'
        """
    
    # assert hulk_compile_str(while_test)

    variable_test =\
        """{
            let a: String = let a = 2, b = 3 in a + b in 2;
            let a = true, b = false in a | b;
            let a = 'sacaste', b = 2 in a @@ b;
            }
        """
    
    # assert hulk_compile_str(variable_test)

    assignement_test =\
        """
            let a: String = 'hello' in a := 1;
        """
    
    assert hulk_compile_str(assignement_test)
    