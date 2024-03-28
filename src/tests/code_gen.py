from hulk.hulk import hulk_compile_str

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
                move(origin, destination){
                    let from = "se movio desde", to = "hacia" in {
                        from @@ origin @@ to @@ destination;
                    }; 
                }
                lay_down(place) {
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
