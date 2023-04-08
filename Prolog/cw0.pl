lubi(jan, pawel).
lubi(julia, wiktoria).
lubi(gabriela, piotrek).
lubi(piotrek, gabriela).
lubi(pawel, krzysztof).
lubi(pawel, jan).
lubi(jan, bartek).
lubi(bartek, janek).
lubi(janek, bartek).
lubi(michal, lukasz).
lubi(lukasz, michal).
mezczyzna(jan).
mezczyzna(pawel).
mezczyzna(piotrek).
mezczyzna(krzysztof).
mezczyzna(bartek).
mezczyzna(michal).
mezczyzna(lukasz).
mezczyzna(janek).

kobieta(X) :- 
    \+ mezczyzna(X).

przyjazn(X, Y) :- 
    lubi(X,Y), lubi(Y,X).

niby_przyjazn(X,Y) :- 
    lubi(X,Y); lubi(Y,X).

nieprzyjazn(X,Y) :- 
    \+przyjazn(X,Y).

true_love(X,Y) :- 
    przyjazn(X,Y), 
    \+ (
       (niby_przyjazn(X, Z);
       niby_przyjazn(Y, Z)),
           Z \= X,
           Z \= Y).

love(X, Y) :-
    lubi(X, Y),
    \+ (lubi(X,Z), Z\=Y).
