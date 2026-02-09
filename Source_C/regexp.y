%{
#include <stdio.h>
#include <string.h>
#include <stdlib.h>

int yylex();
void yyerror(const char *s);

int cpt = 0; // Compteur pour les noms d'automates 
char* last_a1 = NULL;
char* last_a2 = NULL;
%}

%union {
    char *s;
}

%token <s> LETTRE
%token PLUS CONCAT ETOILE PAR_O PAR_F FIN

%type <s> exp

/* Priorités classiques */
%left PLUS
%left CONCAT
%right ETOILE

%%

input:
    { printf("from automate import *\n\n"); }
    liste
    ;

liste:
    ligne
    | liste ligne
    ;

ligne:
    exp FIN { 
        char* res = malloc(16);
        sprintf(res, "a%d", cpt++);
        printf("%s = tout_faire(%s)\n\n", res, $1);
        
        // Stocke les deux derniers pour le egal final
        if (last_a1 == NULL) last_a1 = res;
        else {
            last_a2 = res;
            printf("if egal(%s, %s):\n", last_a1, last_a2);
            printf("    print(\"EGAL\")\n");
            printf("else:\n");
            printf("    print(\"NON EGAL\")\n");
        }
    }
    | FIN
    ;

exp:
    LETTRE { 
        $$ = malloc(16);
        sprintf($$, "a%d", cpt++);
        printf("%s = automate(\"%s\")\n", $$, $1); 
    }
    | exp PLUS exp { 
        $$ = malloc(16);
        sprintf($$, "a%d", cpt++);
        printf("%s = union(%s, %s)\n", $$, $1, $3); 
    }
    | exp CONCAT exp { 
        $$ = malloc(16);
        sprintf($$, "a%d", cpt++);
        printf("%s = concatenation(%s, %s)\n", $$, $1, $3); 
    }
    | exp ETOILE { 
        $$ = malloc(16);
        sprintf($$, "a%d", cpt++);
        printf("%s = etoile(%s)\n", $$, $1); 
    }
    | PAR_O exp PAR_F { $$ = $2; }
    ;

%%

void yyerror(const char *s) {
    // On laisse vide ou un message simple 
}

int main() {
    yyparse();
    return 0;
}