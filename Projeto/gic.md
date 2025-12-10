
    Prog -> Frase

    Frase -> Frase Exp
        | Print
        | ε

    Exp -> Termo
        | Exp Termo SINAL

    Termo -> NUM
        | '(' Exp ')'
