%{
#include "y.tab.h"
#include <string.h>
%}

%%

[a-zA-Z]    { yylval.s = strdup(yytext); return LETTRE; }
"+"         { return PLUS; }
"."         { return CONCAT; }
"*"         { return ETOILE; }
"("         { return PAR_O; }
")"         { return PAR_F; }
"\n"        { return FIN; }
[ \t]       ; /* ignore les espaces */
.           { printf("Erreur lexique\n"); }

%%

int yywrap() {
    return 1;
}