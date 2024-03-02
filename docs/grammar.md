# Gramática

### Símbolos no terminales:

- $P$ programa (distinguido)
- $I$ instrucción
- $E$ expresión
- $E_B$ expresión booleana
- $E_A$ expresión aritmética
- $E_S$ expresión string
- $E_L$ expresión let
- $E_C$ expresión call (llamar a una función)
- $E_F$ expresión _for_
- $E_W$ expresión _while_
- $E_{IF}$ expresión _if_
- $B$ bloque de expresiones
- $A$ asignación
- $F$ función

### Distinguido y expresiones

- $P\rightarrow I_S$
- $B\rightarrow \{I_S\}$
- $I_S\rightarrow II_S|I$
- $I\rightarrow E;|E|F$
- $E\rightarrow E_A|E_B|E_S$

### Expresión booleana

- $E_B\rightarrow T_B || E_B|T_B$
- $T_B\rightarrow F_B \&\& T_B|F_B$
- $F_B\rightarrow !G_B|G_B$
- $G_B\rightarrow id|\text{true}|\text{false}|(E_B)|E_C|E_L|E_F|E_W|E_{IF}|B|A$

### Expresión aritmética

- $E_A\rightarrow T_A+E_A|T_A-E_A|-T_A|+T_A|T_A$
- $T_A\rightarrow F_A\cdot T_A|F_A/T_A|F_A$
- $F_A\rightarrow F_A \wedge G_A|G_A$
- $G_A\rightarrow num|id|(E_A)|E_C|E_L|E_F|E_W|E_{IF}|B|A$

### Expresión string

- $E_S\rightarrow T_S @ E_S$
- $E_S\rightarrow T_S @@ E_S$
- $T_S\rightarrow id|(E_S)|E_C|E_L|E_F|E_W|E_{IF}|B|A$

### Expresión let

- $E_L\rightarrow \text{let } A_L B_L$
- $A_L\rightarrow S_L, A_L| S_L$
- $S_L\rightarrow id=E$
- $B_L\rightarrow \text{in }E|\epsilon$

### Expresión asignación

- $E_C\rightarrow id(A_1)$
- $A_1\rightarrow A_2|\epsilon$
- $A_2\rightarrow A_2,E|E$

### Expresión _if_

- $E_{IF}\rightarrow \text{if } (E_B) E B_1 B_2$
- $B_1\rightarrow \text{elif } E B_1|\epsilon$
- $B_2\rightarrow \text{else } E|\epsilon$

### Bucles

- $E_W\rightarrow \text{while } (E_B) E$
- $E_F\rightarrow \text{for } id\text{ in range}(E,E,E) E$

### Expresión call

- $E_C\rightarrow id(D_1)$
- $D_1\rightarrow \epsilon | D_2$
- $D_2\rightarrow E,D_2|E$

### Funciones

- $F\rightarrow \text{function } (C_1) C_2$
- $C_2\rightarrow => E|B$
- $C_1\rightarrow C_3|\epsilon$
- $C_3\rightarrow id,C_3|id$