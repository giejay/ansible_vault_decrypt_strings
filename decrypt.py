import sys

from ansible.parsing.vault import VaultLib, VaultSecret, PromptVaultSecret, AnsibleVaultError
from ruamel.yaml import YAML

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

class VaultSecret:
    yaml_tag = u'!vault'

    def __init__(self, secret):
        self.secret = secret

    @classmethod
    def from_yaml(cls, constructor, node):
        return VaultSecret(vl.decrypt(node.value)).secret.decode('utf-8')

yaml = YAML()
yaml.indent(mapping=2, sequence=4, offset=2)
yaml.register_class(VaultSecret)

try:
    with open(sys.argv[1], 'r') as orig:
        try:
            y = yaml.load(orig)
        except AnsibleVaultError as e:
            print("Failed to decrypt")
            print(e)
            sys.exit(1)
except FileExistsError:
    print(f"Failed to open {sys.argv[2]}")

with open(sys.argv[2], 'w') as dest:
    yaml.dump(y, dest)
