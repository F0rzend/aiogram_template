import ssl


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
