from hulk.hulk_parser import hulk_to_grammar, hulk_parse
from compiler_tools.lexer import Lexer
from hulk.hulk_grammar import hulk_grammar


def hulk_compile_str(program: str):
    hulk_lexer = Lexer()
    hulk_lexer.load('hulk')

    result = hulk_lexer.run(program)
    tokens = result.tokens

    result = hulk_parse([hulk_to_grammar(t) for t in result.tokens])
    hulk_grammar.evaluate(result.derivation_tree, tokens)

    return result.ok


def test():
    string_test =\
        """
            let a = "hello" @@ "world" in {
                print(a);
                print("hello" @ "world");
            }
        """

    assert hulk_compile_str(string_test)

    boolean_test =\
        """
            let a = true in {
                print(a);
                print(!a);
                print(a & false);
                print(a | false);
                1 != 2;
                if (1 != 2) {
                    print(3);
                }
                else {
                    print(5);
                };
                1 > 2;
                1 <= 2;
                1 >= 2;
            }
        """

    assert hulk_compile_str(boolean_test)

    arithmetic_test =\
        """
            let a = 2 + 3 * 4 in {
                print(a);
                +3;
                -3;
                3+3;
                3 / 3;
            }
        """

    assert hulk_compile_str(arithmetic_test)

    declaration_test =\
        """
            let a = 2, b = 4, c = 8 in {
                print(a * b - c);
                a := 5;
                print(a);
            }
        """

    assert hulk_compile_str(declaration_test)

    array_test =\
        """
            let a = [2, 3, 4, 5] in {
                print(a);
                print(a[2]);
                a[2] := 9;
                print(a);
            }
        """

    assert hulk_compile_str(array_test)

    explicit_array_test =\
        """
        let a=[e^2 || e in range(3)] in print(a);
        """

    assert hulk_compile_str(explicit_array_test)

    while_test =\
        """
            let a = [2, 3, 4, 5] in {
                let w = 2 in while (true) {
                    print(3);
                };
            }
        """

    assert hulk_compile_str(while_test)

    comment_test =\
        """
            /* klsdvmkm +/**-//9++ 
            lkdnkn;2333@@@334667; */
            hello := 34 + 4;
        """

    assert hulk_compile_str(comment_test)

    nested_let_test =\
        """
            let a = '2333' in {
                let s = let w = 9 in w * 2 in 23;
            }
        """

    assert hulk_compile_str(nested_let_test)

    for_test =\
        """
            for (i in [22, 33, 44]) {
                print(i);
            }
        """

    assert hulk_compile_str(for_test)

    if_test =\
        """
            if (true) {
                hello := 3;
            } elif (false) {
                2 + 3;
            } else {
                3 + 3;
            }
        """

    assert hulk_compile_str(if_test)

    type_test =\
        """
            type A inherits B {
                w = 1;
                hello():Object { print('hello'); }
                qwe(a: Number): Number => a + a;
            }   
            
            let a: A = new A() in {
                a.hello();
                print(a.qwe(2));
            }
        """

    assert hulk_compile_str(type_test)

    variable_test =\
        """
            type B(w: Number) {
                w = w;
            }
            type E(w: Number) inherits B(w) {
                hello():Object => print(w);
            }
            let a = 2 in {
                let b = 3 in {
                    let c = a + b in {
                        let d: E = new E(c) in {
                            d.hello();
                        };
                    };
                };
            }
        """

    assert hulk_compile_str(variable_test)

    protocol_test =\
        """
            protocol A extends B{
                hash():Number;
            }

            print('hello');
        """

    assert hulk_compile_str(protocol_test)

    type_inference_test =\
        """
        type Person {
            name = 'Alex';

            hello():Object => print('Hello'@@name);
        }

        let p = new Person() in {
            if (p is Person) p.hello();
            else {
                print('Isnt a person');
                let z = p as Person in {
                     z.hello();
                };
            };
        }
    """

    assert hulk_compile_str(type_inference_test)

    vector_type_test =\
        """ 
        function count(vector: [String]): Number 
            => let a = 0 in 
                for (char in vector) 
                    let b = a in a := b + 1;

        let a = ['h', 'e', 'l', 'l', 'o'] in {
            let b: [Number] = [[1, 2], [3, 4]] in print('hello');
            print(count(a));
        }
    """

    assert hulk_compile_str(vector_type_test)
