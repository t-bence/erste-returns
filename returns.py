import polars as pl


def compute_returns(holdings: pl.DataFrame, rates: pl.DataFrame):
    return (
        holdings.join(rates, on=pl.col("Date bought"))
        .with_columns(
            pl.when(pl.col("Currency") == "HUF")
            .then(pl.lit(1.0))
            .when(pl.col("Currency") == "EUR")
            .then(pl.col("EUR rate"))
            .otherwise(pl.lit(None))
            .alias("Purchase currency rate")
        )
        .with_columns(
            (
                pl.col("Unit cost")
                * (pl.col("Current currency rate") - pl.col("Purchase currency rate"))
            ).alias("EURHUF gain")
        )
        .with_columns(
            (
                (pl.col("Current price") - pl.col("Unit cost"))
                * pl.col("Current currency rate")
            ).alias("Underlying gain")
        )
        .sort(pl.col("Date bought"))
    )
