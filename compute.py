import argparse

import polars as pl

from holdings import read_holdings
from rates import read_rates
from returns import compute_returns


def main():
    # Create the parser
    parser = argparse.ArgumentParser(
        description="Compute returns on investments at Erste."
    )

    # Add a required argument
    parser.add_argument("holdings", type=str, help="Holdings CSV file")

    # Add an optional argument with a default value
    parser.add_argument(
        "--rates",
        type=str,
        default="EURHUF.html",
        help="An optional argument for rates (default: EURHUF.html)",
    )

    # Parse the arguments
    args = parser.parse_args()

    holdings = read_holdings(args.holdings)
    rates = read_rates(args.rates)

    pl.Config.set_tbl_rows(100)
    results = compute_returns(holdings, rates)
    # print(results)

    print("Yearly invested amount in Forints")
    print(
        results.with_columns(
            pl.col("Date bought").dt.year().alias("Year"),
            (pl.col("Total cost") * pl.col("Purchase currency rate")).alias(
                "Total cost in HUF"
            ),
        )
        .group_by("Year")
        .agg(pl.col("Total cost in HUF").sum().cast(pl.Int64))
        .filter(pl.col("Year") < 2024)
        .sort("Year")
    )


if __name__ == "__main__":
    main()
