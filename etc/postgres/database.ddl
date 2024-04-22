-- Create the public schema if it doesn't exist
CREATE SCHEMA IF NOT EXISTS public;

-- Create the sku table
CREATE TABLE IF NOT EXISTS public.sku
(
    uuid                   UUID PRIMARY KEY,
    marketplace_id         INTEGER,
    product_id             BIGINT,
    title                  TEXT,
    description            TEXT,
    brand                  INTEGER,
    seller_id              INTEGER,
    seller_name            TEXT,
    first_image_url        TEXT,
    category_id            INTEGER,
    category_lvl_1         TEXT,
    category_lvl_2         TEXT,
    category_lvl_3         TEXT,
    category_remaining     TEXT,
    features               JSON,
    rating_count           INTEGER,
    rating_value           DOUBLE PRECISION,
    price_before_discounts REAL,
    discount               DOUBLE PRECISION,
    price_after_discounts  REAL,
    bonuses                INTEGER,
    sales                  INTEGER,
    inserted_at            TIMESTAMP DEFAULT NOW(),
    updated_at             TIMESTAMP DEFAULT NOW(),
    currency               TEXT,
    barcode                BIGINT
);

-- Add indexes
CREATE INDEX IF NOT EXISTS sku_brand_index ON public.sku (brand);
CREATE UNIQUE INDEX IF NOT EXISTS sku_marketplace_id_sku_id_uindex ON public.sku (COALESCE(marketplace_id, ''), product_id) ;
CREATE UNIQUE INDEX IF NOT EXISTS sku_uuid_uindex ON public.sku (uuid);
