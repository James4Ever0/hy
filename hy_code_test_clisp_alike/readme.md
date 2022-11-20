# try-except wrapped code blocks

## option to analyze symbols to deal with function reloading

if function is defined in hy code, then better wrap it in some reloading decorator.

if function is within python code, how to reload? we only have symbols, the only way to reload that function is right at the function call, locate the code, extract definition and then execute the code with wrapped shits. this kind of reloading must require some source code analysis, provide different options for hy code and py code.

if hy definition is already there with reloading decorator, is it necessary to locate and reload that function?

## re-execute that line of code

use `hy.repr` to extract the code definition and execute that.

## skip that line of code

return None as value, do nothing.

## return selected value as replacement

check if it is a symbol, string, expression or anything to return instead. make sure the value is returned!

## raise exception

execute the corresponding `(raise)` expression