#!/bin/python3

import argparse
import re
import sys
import yaml

valid_var_name = re.compile(r'^[a-zA-Z_]+[a-zA-Z_0-9]*$')

def scalars(node: dict) -> dict[str, any]:
    return {k:v for k, v in node.items() if isinstance(v, (str, int, float, bool))}

def children_nodes(node:dict) -> list[str]:
    return [k for k, v in node.items() if isinstance(v, dict)]

def walk(node, path, parents, children, depth=0):
    max_depth = len(path) - 1
    curr_path = ' > '.join(['root'] + path[1:depth+1])

    values = {}
    if parents or depth == max_depth or depth > max_depth and children:
        entries = scalars(node)
        valid_entries = {k:v for k,v in entries.items() if valid_var_name.match(k)}
        if len(valid_entries) != len(entries):
            invalid = set(entries.keys()) - set(valid_entries.keys())
            print(f"Invalid env var name found in {curr_path} : {list(invalid)}", file=sys.stderr)
        values.update({k.upper():v for k,v in valid_entries.items()})
        
    branches = children_nodes(node)
    if depth < max_depth:
        if path[depth+1] in branches:
            branches = [path[depth+1]]
        else:
            print(f"Path not found : {curr_path}", file=sys.stderr)
            exit(1)
    else:
        if depth == max_depth and not children:
            branches = []
            
    for name in branches:
        if name == "":
            continue
        sub_node = node[name]
        if not isinstance(sub_node, dict):
            print(f"Expected a branch but found a node in {curr_path} : {' > '.join(branches[:depth+1])}", file=sys.stderr)
            exit(1)
        new_entries = walk(sub_node, path if depth < max_depth else path + [name], parents, children, depth+1)        
        if len(dups := set(values.keys()) & set(new_entries.keys())) > 0:
            print(f"Duplicate keys in {curr_path} : {dups}", file=sys.stderr)
        values.update(new_entries)

    return values


parser = argparse.ArgumentParser(description="")
parser.add_argument('path', help="Path to the YAML node. Use # as separator")
parser.add_argument('--filename', required=False, default=0, help="a YAML file. Otherwise, stdin will be used.")
parser.add_argument('--parents', action=argparse.BooleanOptionalAction, default=True, help="Include parents' vars")
parser.add_argument('--children', action=argparse.BooleanOptionalAction, default=False, help="Include children's vars")
args = parser.parse_args()

with open(args.filename, mode='r') as f:
    try:
        node = yaml.safe_load(f)    
    except:
        print("Can't parse YAML source", file=sys.stderr)
        exit(1)

    path = args.path.strip().split('#')
    path = [p for i,p in enumerate(['']+path) if i==0 or p.strip() != "" ]

    vars = walk(node, path, args.parents, args.children)
    escaped_vars = {k:v if not isinstance(v, str) else "'{}'".format(v.replace("'", "\\'")) for k,v in vars.items()}
    print("\n".join([f'{k}={v}' for k,v in escaped_vars.items()]))    
        
