# SF Fitness - Apple Wallet
A script for generating Apple Wallet Passes for SF Fitness

## Setup

Create a `secret.py` file with the following format:
```
MEMBER_ID = '<SF Fitness Member ID>'
TEAM_IDENTIFIER = '<Apple ID Team Identifier>'
NAME = 'Your Name'
P12_FILE_PATH = 'certificate.p12'
P12_PASSWORD = '<password>'
PASS_IDENTIFIER = '<Apple Pass Type Identifier>'
```

Run `build.py`.

pass.com.hackingdartmouth