`hushbugger` is an alternative to a debugger. Instead of helping you find bugs and remove them, it will do its best to make bugs invisible.

# Example

Imagine you have the following code (as featured in the [Hypothesis docs](https://hypothesis.readthedocs.io/en/latest/quickstart.html)):

```py
def encode(input_string):
    count = 1
    prev = ''
    lst = []
    for character in input_string:
        if character != prev:
            if prev:
                entry = (prev, count)
                lst.append(entry)
            count = 1
            prev = character
        else:
            count += 1
    else:
        entry = (character, count)
        lst.append(entry)
    return lst
```

It has a fatal flaw: it crashes if you give it an empty string:

```
>>> encode('')
Traceback (most recent call last):
  ...
UnboundLocalError: local variable 'character' referenced before assignment
```

To hide the bug, simply apply the `hush` decorator:

```py
from hushbugger import hush

@hush
def encode(input_string):
    count = 1
    prev = ''
    lst = []
    for character in input_string:
        if character != prev:
            if prev:
                entry = (prev, count)
                lst.append(entry)
            count = 1
            prev = character
        else:
            count += 1
    else:
        entry = (character, count)
        lst.append(entry)
    return lst
```

Now it works!

```
>>> encode('')
[]
```

# How it works

If the function raises an exception, its bytecode is disassembled and inspected to look for return statements. If a constant value is returned (e.g. `return True`), that value is used. If a variable is returned (e.g. `return x`), and that variable had a value at the time of the exception, that value is used.

If no usable return statements are found, a `Dummy` object is returned. It responds to almost any operation you throw at it (calling it, adding it, iterating over it, etcetera), so hopefully it gets discarded before visibly breaking anything. Its `repr` is also disguised, as if it belonged to a random module.

```py
@hush
def double(x):
    return 2 * x
```

```
>>> double([1, 2, 3])
[1, 2, 3, 1, 2, 3]
>>> ret = double({})
>>> ret
<errno.Coalescer object at 0x7f96708cb438>
>>> len(list(ret.invert()))
51
```

# Installing

```
pip install hushbugger
```
