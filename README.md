# Gaia

A work-in-progress golfing language inspired by [CJam](https://sourceforge.net/projects/cjam/), [Jelly](https://github.com/DennisMitchell/jelly), [Ohm](https://github.com/nickbclifford/Ohm), and [SOGL](https://github.com/dzaima/SOGL).

Gaia is still incomplete. Currently the parser is mostly complete, so it's usable but still has a limited set of operators and built-in functions.

Documentation is currently unavailable. I will begin to write up proper docs when the language is more complete.

## Basic Syntax

Gaia is stack-based, so all operators and functions are written in postfix notation. There are three data types in Gaia: number, string, list. All operators do something different for each data type. For example, the operator `$`

 - converts a number to a list of digits;
 - converts a string to a list of characters; or
 - joins a list into a string, with no separator.
 
Not every operator supports all types or combinations of types.
