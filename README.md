# <img src="/images/logo@3x.png?raw=true" height="30px" alt="SF Fitness Logo"/> SF Fitness - Apple Wallet

A script for generating scannable Apple Wallet Passes for SF Fitness with auto-location suggestions when you're nearby. Compatible with Apple Watches too.

<p align="center">
<img width="296" alt="Screenshot 2024-11-10 at 2 10 37 PM" src="https://github.com/user-attachments/assets/695c92a6-79ca-4697-982b-244f15ed8815">
</p>

## Build Steps

Unfortunately to build this you'll need a paid Apple Developer account, which costs $99/year. I think it's unreasonable that Apple doesn't let you create Apple Wallet passes for free, but that's the world we currently live in.

### Getting a Certificate

1. Go to Apple Developer Account and sign in - [https://developer.apple.com/account](https://developer.apple.com/account).
2. Go to the "Identifiers" section under "Certificates, Identifiers and Profiles" - [https://developer.apple.com/account/resources/identifiers/list](https://developer.apple.com/account/resources/identifiers/list)  
![1](https://github.com/user-attachments/assets/7394185a-24e4-4591-be10-8e104cb33193)
4. Click the "+" icon to add a new "Pass Type IDs" identifier, and choose a name (I used `pass.com.hackingdartmouth`).  
![2](https://github.com/user-attachments/assets/ba0540d1-845a-418d-9a4c-2e77b1041cfa)
5. Click in on the newly created pass and choose "Create Certificate".  
![3](https://github.com/user-attachments/assets/dbc09f9b-e0bd-4950-acdd-3569d1b8e3b6)
6. You will need a CSR request which you can create following [https://developer.apple.com/help/account/create-certificates/create-a-certificate-signing-request](https://developer.apple.com/help/account/create-certificates/create-a-certificate-signing-request). After uploading that, download the generated certificate.  
![5](https://github.com/user-attachments/assets/9aafda6b-95ba-46f8-967d-e29a8fc4b831)
7. Export the certificate as a .p12 file, and save it as `certificate.p12` in the "certificates" folder of this directory.  
![6](https://github.com/user-attachments/assets/b48ec269-eaa3-4237-9497-bb18a28dec66)

### secret.py file

Create a `secret.py` file with the following format:
```
TEAM_IDENTIFIER = '<Apple ID Team Identifier>'
NAME = 'Your Name'
P12_FILE_PATH = 'certificate.p12'
P12_PASSWORD = '<password>'
PASS_IDENTIFIER = '<Apple Pass Type Identifier>'
MEMBER_ID = '<SF Fitness Member ID>'
```

* `TEAM_IDENTIFIER` is something like 7XFU7D52S4. If you don't know yours it appears under your name in the [Apple Developer pages](https://developer.apple.com/account/resources/identifiers/list).
* `P12_PASSWORD` is if you exported the `certificate.p12` file with a password. If you didn't, set this to the empty string, `''`.
* `PASS_IDENTIFIER` is what you chose in Step 4, in my case `pass.com.hackingdartmouth`.
* `MEMBER_ID` is your SF Fitness Member ID. You can get it by scanning the QR code in the app, though I think it tends to be the first 9 digits of your phone #.

Then just run `python3 build.py` and voila! It creates "Fitness SF.pkpass", which you can text/email to yourself. Opening it on your iPhone will allow you to add it to your wallet.
