from neo4j import GraphDatabase

# URI examples: "neo4j://localhost", "neo4j+s://xxx.databases.neo4j.io"
URI = "neo4j+s://8ff23937.databases.neo4j.io"
AUTH = ("neo4j", "HYyQNQgQugZfq-L1uujmnhOQDv1Oji6Li3KaLNiAg9E")

with GraphDatabase.driver(URI, auth=AUTH) as driver:
    driver.verify_connectivity()

    records = driver.execute_query(
        """
        MATCH (from)-[r:SENDS|RECEIVES]->(to)
        RETURN 
            r.transaction_id as transaction_id,
            r.timestamp as timestamp,
            from.address as from,
            to.address as to,
            r.value as value,
            r.method_called as method_called,
            r.token_price as token_price,
            r.liquidity as liquidity,
            r.market_cap as market_cap
        """
    )
    # Convert records to list of dictionaries
    data = [dict(record) for record in records.records]
    print(data)
    # Create polars DataFrame with schema from RawTrans
    # df = pl.DataFrame(data)
    # df = cast_schema(df, RawTrans().schema)
