from intention.contracts import Table

def ordered_serialization_columns(table:Table):
    source=table.metadata.get("source") if isinstance(table.metadata,dict) else None
    normalized=isinstance(source,dict) and source.get("dataset_id")=="wikitables_www2018"
    if normalized:
        columns=table.metadata.get("columns")
        if not isinstance(columns,list) or any(not isinstance(item,dict) or set(item)!={"column_id","ordinal","header_text"} for item in columns):raise ValueError("normalized WikiTables serialization requires canonical semantic-column metadata")
        if [item["ordinal"] for item in columns]!=list(range(len(columns))) or any(item["header_text"] is not None and not isinstance(item["header_text"],str) for item in columns):raise ValueError("malformed canonical semantic-column metadata")
        internal=[item["column_id"] for item in columns]
        if any(list(row)!=internal for row in table.rows):raise ValueError("normalized rows do not align with canonical column metadata")
        return tuple((item["column_id"],item["header_text"]) for item in columns)
    return tuple((column,column) for column in (list(table.rows[0]) if table.rows else []))
