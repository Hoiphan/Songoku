
//If statement
ifstatement: IF LPRENT expr RPRENT block elseifstament elsestament;
expr: ;
block: LBRACE statement RBRACE
elseifstament: elseifstamentprime | ;
elseifstamentprime: ELSE IF LPRENT expr RPRENT block;
elsestament: elseifstamentprime | ;
elseifstamentprime: ELSE block;


//For statement
// Loop with initialize, condition and Update

forloop: FOR initialize SEMI condition SEMI update block;

initialize: ID (':='|'=') expr ;
condition: expr;
update: ID ('+=' | '-=' | '*=' | '/=' | '=') expr;

// Loop with Range
forrange: for iterator  ':=' RANGE ID block;
interator: para | para COMA para;
para: '_' | ID;


