"""
app:
    bot:
        token: str
        connections_limit: int (Optional)
        proxy: str (Optional)
        validate_token: bool (Optional)
        parse_mode: str (Optional)
    modules: list of str
    superusers: list of str

api_server:
    host: str
    port: int

webhook:
    host: str
    port: int
    path: str  # Must include a token

webapp:
    host: str
    port: int
"""

import trafaret as t


app_trafaret = t.Dict(
            {
                t.Key("bot"): t.Dict(
                    {
                        t.Key("token"): t.String,
                        t.Key("connections_limit", optional=True): t.Int,
                        t.Key("proxy", optional=True): t.String,
                        t.Key("validate_token", optional=True): t.Bool,
                        t.Key("parse_mode", optional=True): t.String,
                    }
                ),
                t.Key("superusers"): t.List(t.Int),
            }
        )

api_server_trafaret = t.Dict({
    t.Key("host"): t.String,
    t.Key("port"): t.Int,
})

webhook_trafaret = t.Dict({
    t.Key("host"): t.String,
    t.Key("port"): t.Int,
    t.Key("path"): t.String,
})

webapp_trafaret = t.Dict({
    t.Key("host"): t.String,
    t.Key("port"): t.Int,
})

config_trafaret = t.Dict(
    {
        t.Key("app"): app_trafaret,
        t.Key("api_server"): api_server_trafaret,
        t.Key("webhook"): webhook_trafaret,
        t.Key("webapp"): webapp_trafaret,
    }
)
