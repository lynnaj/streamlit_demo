import pandas as pd
from pandas import DataFrame
from pandas import DataFrame as df

def load_data() -> pd.DataFrame:
    """Load some sample data.

    Returns:
        pd.DataFrame: A DataFrame with the following columns: name(str), location(str), age(int)
    """
    s3_uri = "path_to_s3_file"
    try:
        df = pd.read_excel(s3_uri)
        # rename columns
        df.columns = ['start_date', 'end_date', 'product_code', 'usage_type', 'operation', 'unblended_cost', 'description', 'product_sku', 'pricing_rate_code', 'pricing_rate_id', 'reservation_subscription_id']

        # date formatting
        df['start_date'] = pd.to_datetime(df['start_date'])
        df['end_date'] = pd.to_datetime(df['end_date'])

    except Exception as e:
        print(f"Error: {e}")
    return df