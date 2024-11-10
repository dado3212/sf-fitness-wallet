import os, hashlib, json, subprocess, shutil
from secret import MEMBER_ID, TEAM_IDENTIFIER, NAME, P12_FILE_PATH, P12_PASSWORD, PASS_IDENTIFIER

DIRECTORY = 'pass'

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

# Create a temporary directory (deleting if it exists)
if os.path.exists(DIRECTORY):
    shutil.rmtree(DIRECTORY)
os.mkdir(DIRECTORY)

# Copy in the image assets
for filename in os.listdir('images'):
    source_path = os.path.join('images', filename)
    destination_path = os.path.join(DIRECTORY, filename)
    shutil.copy2(source_path, destination_path)
    
# Using the Pass template and the secret variables (see README) create
# the main pass.json file
with open('pass.template.json', 'r') as f:
    pass_json = json.load(f)
    pass_json['passTypeIdentifier'] = PASS_IDENTIFIER
    pass_json['serialNumber'] = MEMBER_ID
    pass_json['teamIdentifier'] = TEAM_IDENTIFIER
    pass_json['barcodes'] = [{
        "message": MEMBER_ID,
        "format": "PKBarcodeFormatQR",
        "messageEncoding": "iso-8859-1",
        "altText": MEMBER_ID
    }]
    pass_json['storeCard']['secondaryFields'][0]['value'] = NAME
    pass_json['storeCard']['auxiliaryFields'][0]['value'] = MEMBER_ID
    
    with open(DIRECTORY + '/pass.json', 'w') as pass_file:
        json.dump(pass_json, pass_file, indent=4)

# Generate a manifest.json with SHA1 hashes for each file in the directory.
manifest = {}
for root, dirs, files in os.walk(DIRECTORY):
    for filename in files:
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
    
# Sign the file

# Extract the certificate from the .p12 file
subprocess.run([
    "openssl", "pkcs12", "-in", 'certificates/' + P12_FILE_PATH, "-passin", f"pass:{P12_PASSWORD}",
    "-nokeys", "-out", "cert.pem", "-legacy"
], check=True)

# Extract the private key from the .p12 file
subprocess.run([
    "openssl", "pkcs12", "-in", 'certificates/' + P12_FILE_PATH, "-passin", f"pass:{P12_PASSWORD}",
    "-nocerts", "-out", "key.pem", "-nodes", "-legacy"
], check=True)

# Sign the manifest.json using the certificate and private key
subprocess.run([
    "openssl", "smime", "-sign", "-in", manifest_path, "-out", os.path.join(DIRECTORY, 'signature'),
    "-outform", "DER", "-nodetach", "-binary", "-signer", "cert.pem", "-inkey", "key.pem", "-certfile", "certificates/wwdr.pem"
], check=True)

# Remove temporary signing files
os.remove('cert.pem')
os.remove('key.pem')

# Zip it up
shutil.make_archive('Fitness SF', 'zip', DIRECTORY)
os.rename('Fitness SF.zip', 'Fitness SF.pkpass')

# Delete the temporary directory
shutil.rmtree(DIRECTORY)