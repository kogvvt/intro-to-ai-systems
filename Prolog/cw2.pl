osoba(krystian).
osoba(ignacy).
osoba(ola).

mezczyzna(krystian).
mezczyzna(ignacy).
rodzic(krystian,ola).

% 1 - kobieta(X)
kobieta(X) :-
    osoba(X),
    \+mezczyzna(X).

% 2 - ojciec(X,Y)
ojciec(X,Y) :-
    osoba(X),
    osoba(Y),
    rodzic(X,Y),
    mezczyzna(X).

% 3 - matka(X,Y)
matka(X,Y) :-
    osoba(X),
    osoba(Y),
    rodzic(X,Y),
    kobieta(X).

% 4 corka(X,Y)
corka(X,Y) :-
    osoba(X),
    osoba(Y),
    rodzic(X,Y),
    kobieta(Y).

% 5 brat_rodzony(X,Y)
brat_rodzony(X,Y) :-
    osoba(X),
    osoba(Y),
    ojciec(X,Z),
    ojciec(Y,Z), 
    matka(X,W),
    matka(Y,W), 
    mezczyzna(X).

% 6 brat_przyrodni(X,Y)
brat_przyrodni(X,Y) :-
    osoba(X),
    osoba(Y),
    ((
        ojciec(X,Z),
        ojciec(Y,Z), 
        matka(X,W),
        matka(X,V),
        W \= V );
    (
        matka(X,W),
        matka(X,V),
        ojciec(X,Z),
        ojciec(Y,Z), 
        W \= V )).

% 7 kuzyn(X,Y)
kuzyn(X,Y) :-
    rodzic(Z, X),
    rodzic(W, Y),
    rodzic(V, Z),
    rodzic(V, Z),
    mezczyzna(X),
    X \= Y,
    W \= Z.

% 8 dziadek_od_strony_ojca(X,Y)
dziadek_od_strony_ojca(X,Y) :-
	ojciec(Z,Y),
	ojciec(X,Z).

% 9 dziadek_od_strony_matki(X,Y)
dziadek_od_strony_matki(X,Y) :-
	matka(Z,Y),
	ojciec(X,Z).

% 10 dziadek(X,Y) 
dziadek(X,Y) :-
	dziadek_od_strony_ojca(X,Y);
	dziadek_od_strony_matki(X,Y).

% 11 babcia(X,Y) 
babcia(X,Y) :-
	(
        ojciec(Z,Y),
	    matka(X,Z)
    );
	(
        matka(Z,Y),
	    matka(X,Z)
    ).

% 12 wnuczka(X,Y) 
wnuczka(X,Y) :-
	babcia(X,Y),
	kobieta(Y).

% 13 przodek_do2pokolenia_wstecz(X,Y)
przodek_do2pokolenia_wstecz(X,Y) :-
	rodzic(Y,X);
	dziadek(Y,X);
	babcia(Y,X).

% 14 przodek_do3pokolenia_wstecz(X,Y)
przodek_do3pokolenia_wstecz(X,Y) :-
	przodek_do2pokolenia_wstecz(X,Y);
	dziadek(Z,X),
    rodzic(Y,Z);
	babcia(Z,X),
    rodzic(Y,Z).