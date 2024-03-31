# ARJ-HULK

## Compilador del lenguaje HULK

### Autores
- [Raudel Gomez](https://github.com/raudel25) C411.
- [Juan Carlos Espinosa](https://github.com/Jky45) C411.
- [Alex Sierra](https://github.com/alexsierra45) C411.

### Definición de la gramática usada para el Lexer

#### No Terminales:
        E, A, F, G, H, I, J, K = <E>, <A>, <F>, <G>, <H>, <I>, <J>, <K>

#### Terminales:
        char, ocor, ccor, opar, cpar, ?, plus, star, dot, pow = <ch>, <[>, <]>, <(>, <)>, <?>, <+>, <*>, <.>, <^>

#### Producciones:
        S -> E
        E -> A | E | A
        A -> F A | F
        F -> [ G ] I | H I
        I -> ? | + | * | ε
        H -> ch | ( E ) | .
        G -> ^ J | J
        J -> K J | K
        K -> ch | ch - ch

### Definición de la gramática usada para parsear HULK

#### No Terminales:
         program = <P>
         expression = <E>
         expression-block, block, expression-instruction-list = <EB>, <B>, <I1s>
         expression-string, expression-let, expression-if, expression-while = <Es>, <El>, <Ei>, <Ew> 
         expression-for, expression-destructive-assignment, expression-array = <EF>, <Eas>, <Ear> 
         expression-call, expression-boolean, espression-arithmetic, expression-type = <Ec>, <Eb>, <Ea>, <Et>
         expression-array-call, expression-dot-call = <Ac>, <Epc>
         string-term = <Ts>
         let-assignment, let-assignment-list = <Sl>, <As>
         elif, elif-list = <Eelif>, <Eelifs>
         array-data, array-explicit-data-list = <X1>, <X2>
         expression-call-parameters, parameter-list = <C1>, <C2>
         boolean-factor, boolean-term, boolean-clausule, boolean-atomum = <Fb>, <Tb>, <Cb>, <Gb>
         arithmetic-term, arithmetic-factor, arithmetic-atomum, arithmetic-unary = <Ta>, <Fa>, <Ga>, <Oa>
         to-type, type-discriminator = <T>, <Type>
         atomic = <W>
         instruction-list = <I2s>
         instruction, class-declaration, protocol-declaration, function-declaration = <I>, <C>, <Pr>, <F>
         class-declaration-phrase, class-inheritance, class-body, class's-instruction = <Hc>, <Hih>, <CB>, <IC>
         protocol-declaration-phrase, protocol-extension, protocol-body, protocol's-instruction = <PT>, <Prex>, <PB>, <PF>
         function-parameters, parameter-list, typed-parameter, funtion-body = <D1>, <D2>, <D3>, <FB>


#### Terminales:
        semi, colon, comma, dot, opar, cpar, ocur, ccur = <;>, <:>, <,>, <.>, <(>, <)>, <{>, <}>
        dest-equal, equal, plus, minus, star, div = <:=> <=>, <+>, <->, <*>, </>
        concat, spaced-concat = <@>, <@@>
        and, or, not, eq, neq, lt, gt, lte, gte = <&>, <|>, <!>, <==>, <!=>, < < >, < > >, < <= >, < >= >
        idx, num, bool, string = <id>, <num>, <bool>, <string>
        if, elif, else, while, for = <if>, <elif>, <else>, <while>, <for>
        classx, protocolx, let, defx, return, printx = <protocol>, <type>, <let>, <function>, < => >, <print>
        inherits, extends = <inherits>, <extends>
        is, as, new = <is>, <as>, <new>
        since-that, ocor, ccor = <||>, <[>, <]>

#### Producciones:

        P -> P1
        P1 -> I2s EB ; I2s | I2s EB I2s
        I2s -> I2s I | ε
        I -> C | F | Pr
        EB -> E | B
        B -> { I1s }
        I1s -> I1s E ; | E ;
        E -> Es | El | Eif | Ew | Ef | Eas | Ear
        Es -> Es @ Ts | Es @@ Ts | Ts
        Ts -> Eb
        Eb -> Eb | Fb | Tb
        Tb -> Tb & Fb | Fb
        Fb -> ! Cb | Cb
        Cb -> Gb == Gb | Gb != Gb | Gb < Gb | Gb > Gb | Gb >= Gb | Gb <= Gb | Gb
        Gb -> Ea
        Ea -> Ea + Ta | Ea - Ta | Ta
        Ta -> Ta * Fa | Ta / Fa | Fa
        Fa -> Ga ^ Fa | Ga
        Ga -> + Oa | - Oa | Oa
        Oa -> W
        Epc -> Epc . Ec | Ec . Ec | id . Ec
        W -> id | id . id | num | bool | str | ( E ) | Et | Ec | Epc | Ac
        T -> : Type | ε
        Type -> id  |  [  id  ]  |  [  id , num  ]
        Sl -> id  T  =  E
        Eas -> id  :=  E  |  Ac  :=  E  |  id  .  id  :=  E
        El -> let  As  in  EB
        As -> Sl  ,  As  |  Sl
        Eif -> if  (  Eb  )  EB  Eelifs  else  EB
        Eelifs -> Eelifs  Eelif  |  ε
        Eelif -> elif  (  Eb  )  EB
        Ew -> while  (  Eb  )  EB
        Ef -> for  (  id  in  E  )  EB
        Ec -> id  (  C1  )
        C1 -> C2  |  ε
        C2 -> E  ,  C2  |  E
        F -> function  id  (  D1  )  T  FB
        FB -> B  |  ->  E  ;
        D1 -> D2  |  ε
        D2 -> D3  ,  D2  |  D3
        D3 -> id  T
        Hc -> type  id  |  type  id  (  D2  )
        Hih -> inherits  id  |  inherits  id  (  C2  )  |  ε
        C -> Hc  Hih  {  CB  }
        CB -> CB  IC  |  ε
        IC -> id  T  =  E  ;  |  id  (  D1  )  T  FB
        Et -> W  is  id  |  W  as  id  |  new  Ec
        Ear -> [  X1  ]
        X1 -> E  ||  id  in  E  |  X2  |  ε
        X2 -> X2  ,  E  |  E
        Ac -> id  [  E  ]  |  Ec  [  E  ]  |  Ac  [  E  ]  |  Epc  [  E  ]
        PT -> protocol  id
        Prex -> extends  id  |  ε
        Pr -> PT  Prex  {  PB  }
        PB -> PB  PF  |  PF
        PF -> id  (  D1  )  T  ;


### Chequeo semántico

### Generación de Código











       
