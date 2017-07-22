# -*- coding: utf-8 -*-

import parsley

grammar = parsley.makeGrammar("""
string = '"' <('\\\\' '"' | ~'"' anything )*>:val '"' -> '"{}"'.format(val)

positive_int = <digit+>:ds -> int(ds)
negative_int '-' positive_int:n -> -n
integer =  positive_int | negative_int

float = integer:h '.' positive_int:t -> float("{}.{}".format(h,t))
number = float | integer

list = ('[' ws ']' -> []) |
       ('[' ws string:s ws ']' -> [s]) |
       ('[' (ws string:s ws -> s):h ((',' ws string:s -> s)*):t ws ']' -> [h] + t)

map = ('{' ws '}' -> {}) | '{' ws (kv_pair:kv ws -> kv)+:keys '}' -> {k:v for k,v in keys}
key = <(letterOrDigit | '_')+>
kv_pair = key:k ws '=' ws string:v -> (k,v)

default_decl = 'default' ws '=' ws default:d -> ("default",d)
default = number | string | list | map

description_decl = 'description' ws '=' ws description:d -> ("description",d)
description = string

type_decl = 'type' ws '=' ws type:t -> ("type",t)
type = '"' ('string' | 'list' | 'map'):t '"' -> t

variable_body = (ws (type_decl:t ws -> t):t (description_decl:ds ws -> ds):ds (default_decl:df ws -> df):df -> [t,ds,df] ) | # t df ds
                (ws (type_decl:t ws -> t):t (default_decl:df ws -> df):df (description_decl:ds ws -> ds):ds -> [t,ds,df] ) | # t ds df
                (ws (description_decl:ds ws -> ds):ds (type_decl:t ws -> t):t (default_decl:df ws -> df):df -> [t,ds,df] ) | # ds t df
                (ws (description_decl:ds ws -> ds):ds (default_decl:df ws -> df):df (type_decl:t ws -> t):t -> [t,ds,df] ) | # ds df t
                (ws (default_decl:df ws -> df):df (description_decl:ds ws -> ds):ds (type_decl:t ws -> t):t -> [t,ds,df] ) | # df ds t
                (ws (default_decl:df ws -> df):df (type_decl:t ws -> t):t (description_decl:ds ws -> ds):ds -> [t,ds,df] ) | # df t ds
                (ws (type_decl:t ws -> t):t (description_decl:ds ws -> ds):ds -> [t,ds,None] ) |
                (ws (type_decl:t ws -> t):t (default_decl:df ws -> df):df -> [t,None,df] ) |
                (ws (description_decl:ds ws -> ds):ds (type_decl:t ws -> t):t -> [t,ds,None] ) |
                (ws (description_decl:ds ws -> ds):ds (default_decl:df ws -> df):df -> [None,ds,df] ) |
                (ws (default_decl:df ws -> df):df (type_decl:t ws -> t):t -> [t,None,df] ) |
                (ws (default_decl:df ws -> df):df (description_decl:ds ws -> ds):ds -> [None,ds,df] ) |
                (ws (type_decl:t ws -> t):t -> [t,None,None] ) |
                (ws (description_decl:ds ws -> ds):ds -> [None,ds,None] ) |
                (ws (default_decl:df ws -> df):df -> [None,None,df] ) |
                ws -> [None,None,None]

variable = 'variable' ws string:name ws '{' variable_body:vb '}' -> [("name",name)] + vb #(name,{x[0]:x[1] for x in vb if x is not None})
vars_file = ws (variable:v ws -> v)*:vs -> [{x[0]:x[1] for x in v if x is not None} for v in vs]
""",{})
