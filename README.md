# ImageCrypt
## Steganographic tool to encrypt files and hide them in .jpeg pictures
![image](https://github.com/user-attachments/assets/ebc345e9-72e4-42a6-9e04-4463004b095e)
## Usage
### Merging files
1. Enter paths to your .jpeg and file you want to hide on the left side of the launcher.
2. If you have Fernet key, you can fill the __"Key file"__ field too. Otherwise, program will generate random encryption key.
3. Press __"Merge files"__ button. Files will be in the directory you've started program from. %filename%.jpeg-old.jpeg is a clear version of your image. %filename%.jpeg is the image with encrypted data inside.
### Extracting data
1. Enter paths to a merged .jpeg and the file with the key it was encrypted with.
2. Press __"Extract files"__ button. Decrypted file will be in the directory you've started program from.
## Installation
## Universal method
### Go to [the releases tab](https://github.com/gh0stKn1ght/ImageCrypt/releases) and download latest release for your OS
## Run from source
### Linux
1. Run command:
```
sudo apt install pip && pip install pyside6 cryptography && curl https://raw.githubusercontent.com/gh0stKn1ght/ImageCrypt/refs/heads/main/launcher.py
```
2. Start by:
```
python launcher.py
```
### Windows
1. Download and install pip
2. Run command
```
pip install pyside6 cryptography && curl https://raw.githubusercontent.com/gh0stKn1ght/ImageCrypt/refs/heads/main/launcher.py
```
3. Start by:
```
python launcher.py
```
