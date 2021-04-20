"""
app:
    bot:
        token: str
        connections_limit: int (Optional)
        proxy: str (Optional)
        validate_token: bool (Optional)
        parse_mode: str (Optional)
    superusers: list of str

database:
    username: str
    password: str
    host: str
    port: int
    database: str
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

database_trafaret = t.Dict(
    {
        t.Key("username"): t.String,
        t.Key("password"): t.String,
        t.Key("host"): t.String,
        t.Key("port"): t.Int,
        t.Key("database"): t.String,
    }
)

config_trafaret = t.Dict(
    {
        t.Key("app"): app_trafaret,
        t.Key("database"): database_trafaret,
    }
)
