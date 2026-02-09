CC = gcc
LEX = flex
YACC = yacc

all: regexp_parser

# Compilation du parser C
regexp_parser: lex.yy.c y.tab.c
	$(CC) y.tab.c lex.yy.c -o regexp_parser

lex.yy.c: regexp.l y.tab.h
	$(LEX) regexp.l

y.tab.c y.tab.h: regexp.y
	$(YACC) -d regexp.y

# Nettoyage
clean:
	rm -f lex.yy.c y.tab.c y.tab.h regexp_parser ../Source_Python/main.py

# Pour lancer le test final d'un coup
test: regexp_parser
	./regexp_parser < test.1 > ../Source_Python/main.py
	python3 ../Source_Python/main.py