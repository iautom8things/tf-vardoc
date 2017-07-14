# -*- coding: utf-8 -*-

import parsley

grammer = parsley.makeGrammar("""
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

# some quick sanity checks
assert grammer("234").integer() == 234
assert grammer("-234").integer() == -234
assert grammer("-234").negative_int() == -234
assert grammer("234").positive_int() == 234
assert grammer("234.235").number() == 234.235
assert grammer("-234.235").number() == -234.235
assert grammer('"-234.235"').string() == '"-234.235"'
assert grammer('"then \\" he said \\"lol\\" "').string() == '"then \\" he said \\"lol\\" "'
assert grammer('[]').list() == []
assert grammer('[ ]').list() == []
assert grammer('[ "foo" ]').list() == ['"foo"']
assert grammer('[ "foo", "baz", "bar" ]').list() #== ['"foo"','"baz"','"bar"']
assert grammer('[ "foo", "bar" ]').list() == ['"foo"','"bar"']
assert grammer('''[
  "foo",
  "bar"
]''').list() == ['"foo"','"bar"']
assert grammer('foo = "bar"').kv_pair() == ('foo','"bar"')
assert grammer('{}').map() == {}
assert grammer('{ }').map() == {}
assert grammer('{ key = "val" }').map() == {'key':'"val"'}
assert grammer('''{
  dingo = "foo"
  bingo = "bar"
}''').map() == {'bingo':'"bar"','dingo':'"foo"'}
assert grammer('type = "list"').type_decl() == ('type','list')
assert grammer('type = "map"').type_decl() == ('type','map')
assert grammer('type = "string"').type_decl() == ('type','string')
assert grammer('default = "string"').default_decl() == ('default','"string"')
assert grammer('default = 42').default_decl() == ('default', 42)
assert grammer('default = ["bingo"]').default_decl() == ('default',['"bingo"'])
assert grammer('default = []').default_decl() == ('default',[])
assert grammer('default = {}').default_decl() == ('default',{})
assert grammer('default = { key = "val"}').default_decl() == ('default',{'key':'"val"'})
assert grammer('description = "string"').description_decl() == ('description','"string"')
assert grammer('description = "string"').variable_body() == [None, ('description', '"string"'), None]
assert grammer('type = "string"').variable_body() == [('type', 'string'), None, None]
assert grammer('''variable "bingoname" {
}''').variable() == [('name', '"bingoname"'), None, None, None]
assert grammer('''variable "bingoname" {
  type = "string"
}''').variable() == [('name', '"bingoname"'), ('type', 'string'), None, None]
assert grammer('''variable "bingoname" {
  description = "string"
}''').variable() ==[('name', '"bingoname"'), None, ('description', '"string"'), None]
assert grammer('''variable "bingoname" {
  default = "string"
}''').variable() == [('name', '"bingoname"'), None, None, ('default', '"string"')]
assert grammer('''variable "t_ds_df" {
  type = "string"
  description = "string2"
  default = "string3"
}''').variable() == [('name', '"t_ds_df"'), ('type', 'string'), ('description', '"string2"'), ('default', '"string3"')]
assert grammer('''variable "bingoname" { }''').vars_file() == [{'name': '"bingoname"'}]
assert grammer('''variable "empty" {}''').vars_file() == [{'name': '"empty"'}]
assert grammer('''variable "one_nl" {
}''').vars_file() == [{'name': '"one_nl"'}]
assert grammer('''variable "ds_t_df" {
  description = "string2"
  type = "string"
  default = "string3"
}''').variable() 
assert grammer('''variable "ds_df_t" {
  description = "string2"
  default = "string3"
  type = "string"
}''').variable() == [('name', '"ds_df_t"'), ('type', 'string'), ('description', '"string2"'), ('default', '"string3"')]
assert grammer('''variable "df_ds_t" {
  default = "string3"
  description = "string2"
  type = "string"
}''').variable() == [('name', '"df_ds_t"'), ('type', 'string'), ('description', '"string2"'), ('default', '"string3"')]
assert grammer('''variable "df_t_ds" {
  default = "string3"
  type = "string"
  description = "string2"
}''').variable() == [('name', '"df_t_ds"'), ('type', 'string'), ('description', '"string2"'), ('default', '"string3"')]
assert grammer('''variable "t_df_ds" {
  type = "string"
  default = "string3"
  description = "string2"
}''').variable() == [('name', '"t_df_ds"'), ('type', 'string'), ('description', '"string2"'), ('default', '"string3"')]
assert grammer('''variable "t_df_ds" {
  type = "string"
  default = "string3"
  description = "string2"
}''').vars_file() == [{'default': '"string3"', 'type': 'string', 'name': '"t_df_ds"', 'description': '"string2"'}]
assert grammer('''variable "t_df_ds" {
  type = "string"
  default = "string3"
  description = "string2"
}
variable "t_df_ds" { }''').vars_file() == [{'default': '"string3"', 'type': 'string', 'name': '"t_df_ds"', 'description': '"string2"'}, {'name': '"t_df_ds"'}]
assert grammer('').vars_file() == []
assert grammer('''
''').vars_file() == []
