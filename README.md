# Decrypt values in yaml files that were encrypted with `ansible-vault encrypt_string`

## Add encrypted strings to your yaml file

Eg
```
something:
  test: $ANSIBLE_VAULT;1.1;AES256
          37363230323630386166393535343530313135646639616461666531303638346265393430613834
          3266363635316239356165616364366631363436316166390a313465323762376432306237366564
          66303132633533613463303965636535653965326133613133313030383232346435613063306335
          3562303938626232380a666333336164383931383236373437646665336166623862616130363764
          3239

```

## Decrypt the fields in your yaml file

`python decrypt.py vault.yaml decrypted.yaml`

## Encrypt it again

`python3 encrypt.py decrypted.yml vault.yml`

## Add it to your bash profile for convenience

```
encryptfile(){
python3 decrypted.yml vault.yml optionalpathtopwfile
}

decryptfile(){
python3 vault.yml decrypted.yml optionalpathtopwfile
}
```
