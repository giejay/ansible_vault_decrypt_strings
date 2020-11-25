#!/usr/bin/env python
import sys

from ansible.parsing.vault import VaultLib, VaultSecret, PromptVaultSecret
from ruamel.yaml import YAML, scalarstring
from ruamel.yaml.scalarstring import LiteralScalarString

if len(sys.argv) < 3:
    print("Supply <input_yaml> <output_yaml> Optional(<password_file>)")
    sys.exit(1)

if len(sys.argv) == 4:
    try:
        with open(sys.argv[3], "rb") as pw_file:
            pw = pw_file.read()
            vault_pw = VaultSecret(pw)
            vault_pw.load()
    except FileNotFoundError:
        print("Password file not found")
        sys.exit(1)
else:
    vault_pw = PromptVaultSecret(prompt_formats=["password: "])
    vault_pw.load()

vl = VaultLib(secrets=[
    (None, vault_pw)
])

def to_yaml(representer, node):
    return representer.represent_scalar('!vault', node, style='|')

yaml = YAML()
yaml.indent(mapping=2, sequence=4, offset=2)
yaml.representer.add_representer(LiteralScalarString, to_yaml)

with open(sys.argv[1], 'r') as orig:
    y = yaml.load(orig)

for value in y:
    y[value] = vl.encrypt(y[value], vault_pw).decode('utf-8')

scalarstring.walk_tree(y)

with open(sys.argv[2], 'w') as dest:
    yaml.dump(y, dest)
