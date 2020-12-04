##### upgrade #####
DROP TABLE IF EXISTS "timedbasemodel";
##### downgrade #####
CREATE TABLE IF NOT EXISTS "timedbasemodel" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP
);;
