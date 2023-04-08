parent(jan, marek).
parent(jan, konrad).
parent(kuba, krystian).
parent(kuba, michal).
parent(julia, krystian).
parent(julia, michal).
parent(marek, maciej).
parent(marek, damian).
parent(kacper, damian).
parent(kacper, konrad).
parent(krystian, piotrek).
parent(michal, sebastian).
parent(damian, sebastian).

%przyklad A
siblings(X, Y) :-
    parent(X, Z),
    parent(Y, Z),
    X \= Y.

%przyklad B
cousins(X, Y) :-
    parent(X, P),
    parent(Y, Q),
    siblings(P, Q),
    X \= Y.

%przyklad C
coParentInLaw(X,Y) :-
    parent(Z,X),
    parent(W,Y),
    parent(V,Z),
    parent(V,W),
    X \= Y,
    W \= Z.

%przyklad D
stepmother(X,Y) :-
	parent(X,Z),
	parent(W,Z),
	parent(W,Y),
	\+ parent(X,Y),
	X \= Y.

%przyklad E
halfSiblings(X,Y) :-
	parent(X,V),
	parent(X,W),
	parent(Y,W),
	parent(Y,Z),
	\+ parent(X,Z),
	\+ parent(Y,V),
	X \= Y,
	V \= W,
	V \= Z.

%przyklad F
brotherInLaw(X,Y) :-
	parent(Z,X),
	parent(Z,W),
	parent(W,V),
	parent(Y,V),
	X \= Y,
	X \= W,
	Y \= W.

%przyklad G (rodzenstwo zdefiniowane wyzej)
uncle(X,Y) :-
	parent(X,Z),
	parent(Z,W),
	parent(Y,W),
	X \= Y,
	Y \= Z.

