# yaml2env
A single file python script to convert the whole or a specific branch of a YAML file to the ENV format.

# Usage
yaml2env.py [-h] [--parents | --no-parents] [--children | --no-children] filename path

By default, children is set to false and parents is set to true. These default settings flatten a branch from the root to the node.

<b>filename</b> : 

The YAML file to parse.

<b>path</b> :

The path to a node in the YAML file. The diffent levels are separated by a '#' and the first one could be omitted.

'foo#bar#baz' is equivalent to '#foo#bar#baz and represents
<pre>
.
├── foo
│   ├── bar
│   │   ├── baz
</pre>

## CLI examples

```
yaml2env.py file.yaml 'foo#bar'
```

Returns entries of each levels root, 'foo' and 'bar' without including deeper levels like 'baz'.


```
yaml2env.py --children file.yaml ''
```

Flatten the whole file.


```
yaml2env.py --no-parents --children file.yaml 'foo#bar'
```

Returns all entries of 'bar' and its children.


## Errors
- If an incorrect path is given, the script will stop with an error message.
- If duplicate names are found, the script will warn you, keep one of the values encountered and continue.
- If invalid ENV names are found, the script will warn you, discard the entrie and continue.
