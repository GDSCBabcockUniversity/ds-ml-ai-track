import pandas as pd

def get_columns(df):
    return list(df.columns)

import pandas as pd

def summarize_data(df, columns):
    data_types = df[columns].dtypes.to_dict()

    unique_values = {}

    for column in columns:
        if df[column].dtype == 'object' or df[column].dtype.name == 'category':
            # Categorical: Return up to 20 unique values
            unique_values[column] = df[column].dropna().unique().tolist()[:20]
        elif 'datetime' in str(df[column].dtype):
            # Dates: Return the format of one value and the date range
            date_sample = df[column].dropna().iloc[0]
            inferred_format = pd.to_datetime([date_sample]).strftime('%Y-%m-%d')[0]
            min_date = df[column].min().strftime('%Y-%m-%d') if not df[column].isna().all() else None
            max_date = df[column].max().strftime('%Y-%m-%d') if not df[column].isna().all() else None
            unique_values[column] = {
                "inferred_format": inferred_format,
                "date_range": f"{min_date} to {max_date}" if min_date and max_date else None
            }
        elif pd.api.types.is_numeric_dtype(df[column]):
            # Numerical: Return the range of values
            min_value = df[column].min()
            max_value = df[column].max()
            unique_values[column] = {
                "value_range": f"{min_value} to {max_value}"
            }

    summary = (
        f"Columns: {columns}\n"
        f"Data Types: {data_types}\n"
        f"Unique Values for Categorical/Date Columns and Ranges for Numerical Columns:\n{unique_values}"
    )
    
    return summary
