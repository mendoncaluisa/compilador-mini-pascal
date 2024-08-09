## Compilador-mini-pascal
#### Aluna: Maria Luísa Mendonça Oliveira
#### Professor: Walace de Almeida Rodrigues
Compilador de mini pascal.
Trabalho realizado em python.

O compilador segua a gramatica a seguir
````
<program> ->
	program id ( <identifier_list> ) ;
	<declarations>
	<subprogram_declarations>
	<compound_statement>
	.

<identifier_list> ->
	id <resto_identifier_list>

<resto_identifier_list> ->
	, id <resto_identifier_list>
	| LAMBDA

<declarations> ->
	var <identifier_list> : <type> ; <declarations> 
	| LAMBDA

<type> ->
	<standard_type>
	| array [ num .. num ] of <standard_type>

<standard_type> ->
	integer
	| real

<subprogram_declarations> ->
	<subprogram_declartion> ; <subprogram_declarations> 
	| LAMBDA

<subprogram_declaration> ->
	<subprogram_head> <declarations> <compound_statement>

<subprogram_head> ->
	function id <arguments> : <standard_type> ;
	| procedure id <arguments> ;

<arguments> ->
	( <parameter_list> )
	| LAMBDA

<parameter_list> ->
	<identifier_list> : <type> <resto_parameter_list>

<resto_parameter_list> ->	
	; <identifier_list> : <type> <resto_parameter_list>
    | LAMBDA

<compound_statement> ->
	begin
	<optional_statements>
	end

<optional_statements> ->
	<statement_list>
	| LAMBDA

<statement_list> ->
	<statement> <resto_statement_list>

<resto_statement_list> ->
	 ; <statement> <resto_statement_list>
	 | LAMBDA

<statement> ->
	<variable> assignop <expression>
	| <procedure_statement>
	| <compound_statement>
	| <if_statement>
	| while <expression> do <statement>
	| <inputOutput>

<if_statement> ->
	if <expression> then <statement> <opc_else>

<opc_else> ->
    else <statement>
    | LAMBDA
	 
<variable> ->
	id <opc_index>

<opc_index> ->
    [ <expression> ]
    | LAMBDA

<procedure_statement> ->
	id <opc_parameters>

<opc_parameters> ->
    ( <expression_list> )
    | LAMBDA

<expression_list> ->
	<expression> <resto_expression_list>

<resto_expression_list>
	, <expression> <resto_expression_list>
	| LAMBDA

<expression> ->
	<simple_expression> <resto_expression>
	
<resto_expression> ->
	LAMBDA
	| relop <simple_expression> <resto_expression>

<simple_expression> ->
	<term> <resto_simple_expression>

<resto_simple_expression> ->
	LAMBDA
	| addop <term> <resto_simple_expression>

<term> ->
	<uno> <resto_term>

<resto_term> ->
    LAMBDA
    | mulop <uno> <resto_term>

<uno> ->
    <factor>
    | addop <factor>

<factor> ->
	id <resto_id>
	| num
	| ( <expression> )
	| not <factor>

<resto_id> ->
	LAMBDA
	| ( <expression_list> )


<input_output> ->
    writeln(<outputs>)
    | write(<outputs>)
    | read(id)
    | readln(id)

<outputs> ->
    <out> <restoOutputs>

<resto_outputs> ->
    , <out> <restoOutputs>
    | LAMBDA

<out> ->
    num
    | id
    | string
````
Características da gramática:

* String: apenas com aspas duplas " "
* Comentario: apenas em linha utilizando //
* Não aceita AND e OR
