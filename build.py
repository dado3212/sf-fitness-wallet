import os, hashlib, json, subprocess, shutil
from secret import MEMBER_ID, TEAM_IDENTIFIER, NAME, P12_FILE_PATH, P12_PASSWORD, PASS_IDENTIFIER

DIRECTORY = 'Fitness SF.pass'

# Calculate the SHA1 hash of a file.
def calculate_sha1(filepath):
    sha1 = hashlib.sha1()
    with open(filepath, 'rb') as f:
        while True:
            data = f.read(65536)  # Read in 64k chunks
            if not data:
                break
            sha1.update(data)
    return sha1.hexdigest()

# Clear the old files if they exist
# os.remove('Fitness SF.pass/')

# Load up the base pass JSON file
with open('pass-base.json', 'r') as f:
    loaded = json.load(f)
    loaded['passTypeIdentifier'] = PASS_IDENTIFIER
    loaded['serialNumber'] = MEMBER_ID
    loaded['teamIdentifier'] = TEAM_IDENTIFIER
    loaded['barcodes'] = [{
        "message": MEMBER_ID,
        "format": "PKBarcodeFormatQR",
        "messageEncoding": "iso-8859-1",
        "altText": MEMBER_ID
    }]
    loaded['storeCard']['secondaryFields'][0]['value'] = NAME
    loaded['storeCard']['auxiliaryFields'][0]['value'] = MEMBER_ID
    
    with open('FItness SF.pass/pass.json', 'w') as x:
        json.dump(loaded, x, indent=4)

"""Generate a manifest.json with SHA1 hashes for each file in the directory."""
manifest = {}
for root, dirs, files in os.walk(DIRECTORY):
    for filename in files:
        # Skip manifest + signature files
        if filename in ['manifest.json', 'signature']:
            continue

        # Get the relative path to the file
        filepath = os.path.join(root, filename)
        relpath = os.path.relpath(filepath, DIRECTORY)
        
        # Calculate SHA1 hash of the file
        sha1_hash = calculate_sha1(filepath)
        
        # Add the file's relative path and its SHA1 hash to the manifest
        manifest[relpath.replace(os.sep, '/')] = sha1_hash

# Save manifest.json
manifest_path = os.path.join(DIRECTORY, 'manifest.json')
with open(manifest_path, 'w') as manifest_file:
    json.dump(manifest, manifest_file, indent=4)
    
"""Sign it.""" 
# Build the OpenSSL command
openssl_command = [
    "openssl", "pkcs12", "-in", P12_FILE_PATH, "-passin", f"pass:{P12_PASSWORD}",
    "-nokeys", "-out", "cert.pem", "-legacy"
]

# Extract the certificate from the .p12 file
subprocess.run(openssl_command, check=True)

openssl_command = [
    "openssl", "pkcs12", "-in", P12_FILE_PATH, "-passin", f"pass:{P12_PASSWORD}",
    "-nocerts", "-out", "key.pem", "-nodes", "-legacy"
]

# Extract the private key from the .p12 file
subprocess.run(openssl_command, check=True)

# Sign the manifest.json using the certificate and private key
openssl_sign_command = [
    "openssl", "smime", "-sign", "-in", manifest_path, "-out", os.path.join(DIRECTORY, 'signature'),
    "-outform", "DER", "-nodetach", "-binary", "-signer", "cert.pem", "-inkey", "key.pem", "-certfile", "wwdr.pem"
]

# Run the OpenSSL command to create the detached signature
subprocess.run(openssl_sign_command, check=True)

os.remove('cert.pem')
os.remove('key.pem')

# Zip it up
shutil.make_archive('Fitness SF', 'zip', DIRECTORY)
os.rename('Fitness SF.zip', 'Fitness SF.pkpass')