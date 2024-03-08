from datetime import datetime, timedelta
from cryptography import x509
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.x509.oid import NameOID
from cryptography.hazmat.backends import default_backend

# Example usage
serial_number = 6900024000093  # Replace this with your serial number

def generate_certificate(serial_number):
    # Generate a new RSA key pair
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )

    # Define the subject of the certificate
    subject = x509.Name([
        x509.NameAttribute(NameOID.COUNTRY_NAME, u"US"),
        x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, u"California"),
        x509.NameAttribute(NameOID.LOCALITY_NAME, u"Mountain View"),
        x509.NameAttribute(NameOID.ORGANIZATION_NAME, u"MyOrg"),
        x509.NameAttribute(NameOID.COMMON_NAME, u"example.com"),
    ])

    # Set the certificate validity period
    now = datetime.utcnow()
    not_valid_before = now
    not_valid_after = now + timedelta(days=365)

    # Create a self-signed certificate
    certificate = x509.CertificateBuilder().subject_name(
        subject
    ).issuer_name(
        subject
    ).public_key(
        private_key.public_key()
    ).serial_number(
        serial_number
    ).not_valid_before(
        not_valid_before
    ).not_valid_after(
        not_valid_after
    ).sign(private_key, default_backend())

    return certificate

# Example usage
#$serial_number = 1234567890  # Replace this with your desired serial number
certificate = generate_certificate(serial_number)

# Output the generated certificate to a file
with open("generated_certificate.crt", "wb") as cert_file:
    cert_file.write(certificate.public_bytes(serialization.Encoding.PEM))