import ssl

from datetime import timedelta, datetime


def get_ssl_context(webhook_cert: str, webhook_pkey: str):
    ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
    ssl_context.load_cert_chain(
        webhook_cert,
        webhook_pkey,
    )
    return ssl_context


def get_ssh_certificate(webhook_cert: str):
    with open(webhook_cert, 'rb') as f:
        return f.read()


def generate_selfsigned_cert(
    hostname,
    cert_path='cert.pem',
    pkey_path='pkey.pem',
    ip_addresses=None,
    key=None,
    public_exponent=65537,
    key_size=2048,
    backend=None,
    serial_number=1000,
    expire_days=None,
):
    """Generates self signed certificate for a hostname, and optional IP addresses."""
    import ipaddress
    try:
        from cryptography import x509
        from cryptography.x509.oid import NameOID
        from cryptography.hazmat.primitives import hashes
        from cryptography.hazmat.backends import default_backend
        from cryptography.hazmat.primitives import serialization
        from cryptography.hazmat.primitives.asymmetric import rsa
    except ImportError:
        raise ImportError('You need to pip install cryptography for generating self-signed cert')

    # Generate our key
    if key is None:
        key = rsa.generate_private_key(
            public_exponent=public_exponent,
            key_size=key_size,
            backend=backend or default_backend(),
        )

    name = x509.Name([
        x509.NameAttribute(NameOID.COMMON_NAME, hostname)
    ])

    # best practice seem to be to include the hostname in the SAN, which *SHOULD* mean COMMON_NAME is ignored.
    alt_names = [x509.DNSName(hostname)]

    # allow addressing by IP, for when you don't have real DNS (common in most testing scenarios
    if ip_addresses:
        for addr in ip_addresses:
            # openssl wants DNSnames for ips...
            alt_names.append(x509.DNSName(addr))
            # ... whereas golang's crypto/tls is stricter, and needs IPAddresses
            # note: older versions of cryptography do not understand ip_address objects
            alt_names.append(x509.IPAddress(ipaddress.ip_address(addr)))

    san = x509.SubjectAlternativeName(alt_names)

    # path_len=0 means this cert can only sign itself, not other certs.
    basic_contraints = x509.BasicConstraints(ca=True, path_length=0)
    now = datetime.utcnow()
    cert = (
        x509.CertificateBuilder()
            .subject_name(name)
            .issuer_name(name)
            .public_key(key.public_key())
            .serial_number(serial_number)
            .not_valid_before(now)
            .not_valid_after(now + timedelta(days=expire_days or 3650))
            .add_extension(basic_contraints, False)
            .add_extension(san, False)
            .sign(key, hashes.SHA256(), default_backend())
    )
    cert_pem = cert.public_bytes(encoding=serialization.Encoding.PEM)
    key_pem = key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption(),
    )

    with open(cert_path, 'wb') as f:
        f.write(cert_pem)
    with open(pkey_path, 'wb') as f:
        f.write(key_pem)


def certificates_cli():
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--config", dest="config")
    parser.add_argument('-e', '--expire-days', type=int, default=3650, dest='expire_days', action='store')
    config_file = os.getenv("BOT_CONFIG_FILE")
    if not config_file:
        config_file = DEFAULT_CONFIG_PATH

    environment_variables = {"config": config_file}

    args = parser.parse_args()
    cli_arguments = {key: value for key, value in vars(args).items() if value}
    arguments = ChainMap(cli_arguments, environment_variables)

    config = parse_config(arguments["config"])
    cert_path = config['webhook']['certificates']['public']
    pkey_path = config['webhook']['certificates']['private']

    generate_selfsigned_cert(
        hostname=config['webhook']['host'],
        cert_path=cert_path,
        pkey_path=pkey_path,
        expire_days=arguments['expire_days']
    )


if __name__ == '__main__':
    import argparse
    import os
    from bot.settings import DEFAULT_CONFIG_PATH
    from bot.utils.parse_config import parse_config
    from collections import ChainMap
    certificates_cli()
    print('Success')
