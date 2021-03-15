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

config_trafaret = t.Dict(
    {
        t.Key("app"): app_trafaret
    }
)
