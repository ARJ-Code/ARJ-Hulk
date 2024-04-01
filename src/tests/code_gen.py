import subprocess
from compiler_tools.lexer import Lexer
from hulk.hulk_code_generator import hulk_code_generator
from hulk.hulk_parser import hulk_parse, hulk_to_grammar
from hulk.hulk_semantic_check import hulk_semantic_check
from .hulk_grammar import hulk_grammar


def hulk_compile_str(program: str) -> str:
    hulk_lexer = Lexer()
    hulk_lexer.load('hulk')

    result = hulk_lexer.run(program)
    tokens = result.tokens

    if not result.ok:
        print(
            f'Lexer error:\nrow {result.error.row+1} col {result.error.col+1}')
        return ''

    result = hulk_parse([hulk_to_grammar(t) for t in result.tokens])

    if not result.ok:
        print(
            f'Parser error:\nrow {tokens[result.error-1].row+1} col {tokens[result.error-1].col+1}')
        return ''

    ast = hulk_grammar.evaluate(result.derivation_tree, tokens)
    result = hulk_semantic_check(ast)

    if not result.ok:
        error = '\n'.join(result.errors)
        print(f'Semantic errors:\n{error}')
        return ''

    hulk_code_generator(ast, result.context)

    result = subprocess.run(["gcc", "-o", "cache/main", "cache/main.c", "-lm"])
    result = subprocess.run(["./cache/main"], capture_output=True, text=True)


    return result.stdout

def test():
    type_test =\
        """
            type Animal(name, age){
                name = name;
                age = age;

                name() => self.name;
                age() => self.age;
            }

            type Dog(race, name, age) inherits Animal(name, age){
                race = race;

                ladra(name, age){
                    let phrase = "esta ladrando" in {
                        name @@ age @@ phrase;
                    };
                }
            }

            type Cat(race, name, age) inherits Animal(name, age){
                race = race;

                maulla(){
                    let phrase = "esta maullando como un" in {
                        self.name() @@ self.age() @@ phrase @@ self.race;
                    };
                }
            }

            let test_dog = new Dog("sato", "balto", 7), test_cat = new Cat("siames", "Lucas", 4) in {
                print (test_cat.maulla());
                print (test_dog.ladra("alex", 22));
            }
        """

    assert hulk_compile_str(type_test) == 'Lucas 4.000000 esta maullando como un siames\nalex 22.000000 esta ladrando\n'

    protocol_test =\
        """
            protocol Movable{
                move(origin: String, destination: String): String;
            }

            protocol Layable extends Movable{
                lay_down(place: String): String;
            }

            type Animal (name, age){
                name = name;
                age = age;

                name() => self.name;
                age() => self.age;
                move(origin:String, destination:String):String{
                    let from = "se movio desde", to = "hacia" in {
                        from @@ origin @@ to @@ destination;
                    }; 
                }
                lay_down(place:String):String {
                    let at = "se acosto en" in {
                        at @@ place;
                    };
                }
            }

            function test_move (parameter: Layable){
                let ans = parameter.move("la sala", "el cuarto") in ans;
            }

            function test_lay_down (parameter: Layable){
                let ans = parameter.lay_down("su cama") in ans;
            }

            let test_protocol = new Animal("Jerry", 10) in {
                print(test_protocol.name() @@ test_move(test_protocol));
                print(test_protocol.name() @@ test_lay_down(test_protocol));
            }
            
        """

    assert hulk_compile_str(protocol_test) == 'Jerry se movio desde la sala hacia el cuarto\nJerry se acosto en su cama\n'

    iterable_test =\
        """
            type Positions(start, last){
                start = start;
                last = last;
                current = start-1;

                next(): Boolean => (self.current := self.current+1) <= self.last;
                current(): Number => self.current;
                reset(): Number => self.current := self.start-1;
            }

            let test = new Positions(1, 4) in 
                for (i in test) {
                    for (i in [i + 1 || i in (new Positions(i, i + 3))]){
                        print (i);
                    };
                    print(i);
                }
        """
    
    assert hulk_compile_str(iterable_test) ==   '2.000000\n' + \
                                                '3.000000\n' + \
                                                '4.000000\n' + \
                                                '5.000000\n' + \
                                                '1.000000\n' + \
                                                '3.000000\n' + \
                                                '4.000000\n' + \
                                                '5.000000\n' + \
                                                '6.000000\n' + \
                                                '2.000000\n' + \
                                                '4.000000\n' + \
                                                '5.000000\n' + \
                                                '6.000000\n' + \
                                                '7.000000\n' + \
                                                '3.000000\n' + \
                                                '5.000000\n' + \
                                                '6.000000\n' + \
                                                '7.000000\n' + \
                                                '8.000000\n' + \
                                                '4.000000\n'
    
    override_test =\
        """
            type Person(name) {
                name = name;

                hello() => print('Hello' @@ self.name @@ '!!!');
            }

            type Student(name: String, age: Number) inherits Person(name) {
                name = name;
                age = age;

                hello() => print('Hi' @@ self.name @@ self.print_age());

                print_age() => ', you have' @@ self.age @@ 'years old';
            }

            let s = new Student('Alex', 23) in s.hello();
        """
    
    assert hulk_compile_str(override_test) == 'Hi Alex , you have 23.000000 years old\n'

    is_test =\
        """
            type Bird {
                // ...
            }

            type Plane {
                // ...
            }

            type Superman {
                // ...
            }

            let x = new Superman() in
                print(
                    if (x is Bird) "It's bird!"
                    elif (x is Plane) "It's a plane!"
                    else "No, it's Superman!"
                );
        """
    
    assert hulk_compile_str(is_test) == 'No, it\'s Superman!\n'
    