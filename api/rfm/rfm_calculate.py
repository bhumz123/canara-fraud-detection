import pandas as pd
import geohash2

# existing_df= pd.read_csv('Existing_data.csv')
# final_df = pd.DataFrame()
# existing_df['trans_date_trans_time'] = pd.to_datetime(existing_df['trans_date_trans_time'])
# existing_df['cc_num'] = existing_df['cc_num'].astype('object')
# existing_df['trans_month'] = existing_df['trans_month'].astype('int32')
# print("exisiting shape: ", existing_df.shape)

# def add_to_existing_df(df):
#     final_df = pd.concat([existing_df, df])
#     c_result=customer_spending_behavior(existing_df.iloc[:,:-1], df['cc_num'], df)
#     m_result=merchant_risk_window(existing_df, c_result,df['merchant'])
#     category_result=category_risk_window(existing_df, m_result, df['category'])
#     e_df=encode_category(category_result)
#     e_df['distance']=calc_distance(e_df['cust_locn'],e_df['merchant_locn'])
#     print(e_df.columns)
#     print(e_df.shape)
#     return fin


def calculate_distance(geohash1, geohash3):
        # Decode geohash strings into latitude and longitude
        import math
        lat1, lon1 = geohash2.decode(geohash1)
        lat2, lon2 = geohash2.decode(geohash3)
        # Calculate distance using Haversine formula
        radius = 6371  # Earth's radius in kilometers
        lat1 = float(lat1)
        lat2 = float(lat2)
        lon1 = float(lon1)
        lon2 = float(lon2)
        # print(lat1,lon1,lat2,lon2)
        dlat = math.radians(lat2 - lat1)
        dlon = math.radians(lon2 - lon1)
        a = math.sin(dlat / 2) * math.sin(dlat / 2) + math.cos(math.radians(lat1)) * math.cos(
            math.radians(lat2)) * math.sin(dlon / 2) * math.sin(dlon / 2)
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        distance = radius * c
        return distance


def get_customer_spending_behaviour_features(customer_transactions, windows_size_in_days=[1, 7, 30]):
    # Let us first order transactions chronologically
    customer_transactions = customer_transactions.sort_values("trans_date_trans_time")
    # The transaction date and time is set as the index, which will allow the use of the rolling function
    customer_transactions.index = customer_transactions.trans_date_trans_time
    # For each window size
    for window_size in windows_size_in_days:
        # Compute the sum of the transaction amounts and the number of transactions for the given window size
        SUM_AMOUNT_TX_WINDOW = customer_transactions['amt'].rolling(window_size).sum()
        NB_TX_WINDOW = customer_transactions['amt'].rolling(window_size).count()
        # Compute the average transaction amount for the given window size
        # NB_TX_WINDOW is always >0 since current transaction is always included
        AVG_AMOUNT_TX_WINDOW = SUM_AMOUNT_TX_WINDOW / NB_TX_WINDOW
        # Save feature values
        customer_transactions[f'Frequency_{window_size}DAY_WINDOW'] = NB_TX_WINDOW
        customer_transactions[f'Monetary_{window_size}DAY_WINDOW'] = SUM_AMOUNT_TX_WINDOW

    customer_transactions.fillna(0, inplace=True)
    return customer_transactions.iloc[-1,:]

def merchant_risk_window(terminal_transactions, incoming_row, merchant, delay_period=7, window_days=[1, 7, 30],feature="merchant"):
    # Filter transactions for the specific merchant
    merchant_transactions = terminal_transactions[terminal_transactions[feature] == incoming_row[feature]]
    # Sort transactions chronologically
    merchant_transactions = merchant_transactions.sort_values("trans_date_trans_time")
    # Compute the cumulative fraud count within the delay period
    FRAUD_DELAY = merchant_transactions['is_fraud'].rolling(delay_period, min_periods=0).sum()
    TX_DELAY = merchant_transactions['is_fraud'].rolling(delay_period, min_periods=0).count()
    # Iterate over the window sizes
    for window_size in window_days:
        # Compute the fraud count and transaction count within the delay period + window size
        FRAUD_DELAY_WINDOW = merchant_transactions['is_fraud'].rolling(delay_period + window_size, min_periods=0).sum()
        TX_DELAY_WINDOW = merchant_transactions['is_fraud'].rolling(delay_period + window_size, min_periods=0).count()
        # Compute the fraud count and transaction count within the window only
        FRAUD_WINDOW = FRAUD_DELAY_WINDOW - FRAUD_DELAY
        TX_WINDOW = TX_DELAY_WINDOW - TX_DELAY
        # Compute the risk score as the ratio of fraud count to transaction count within the window
        RISK_WINDOW = FRAUD_WINDOW / TX_WINDOW
        # Save the feature values for the incoming row
        incoming_row[feature + '_Trnscn_count' + str(window_size) + 'Day'] = TX_WINDOW.iloc[-1]
        incoming_row[feature + '_Risk_Score' + str(window_size) + 'Day'] = RISK_WINDOW.iloc[-1]
    # Replace NA values with 0 (for cases where NB_TX_WINDOW is 0)
    return incoming_row

def category_risk_window(terminal_transactions, incoming_row,catgory,delay_period=7, window_days=[1, 7, 30], feature="category"):
    # Filter transactions for the specific merchant
    category_transactions = terminal_transactions[terminal_transactions[feature] == incoming_row[feature]]
    # Sort transactions chronologically
    category_transactions = category_transactions.sort_values('trans_date_trans_time')
    # Compute the cumulative fraud count within the delay period
    FRAUD_DELAY = category_transactions['is_fraud'].rolling(delay_period,min_periods=0).sum()
    TX_DELAY = category_transactions['is_fraud'].rolling(delay_period,min_periods=0).count()

    # Iterate over the window sizes
    for window_size in window_days:
        # Compute the fraud count and transaction count within the delay period + window size
        FRAUD_DELAY_WINDOW = category_transactions['is_fraud'].rolling(delay_period + window_size,min_periods=0).sum()
        TX_DELAY_WINDOW = category_transactions['is_fraud'].rolling(delay_period + window_size,min_periods=0).count()
        # Compute the fraud count and transaction count within the window only
        FRAUD_WINDOW = FRAUD_DELAY_WINDOW - FRAUD_DELAY
        TX_WINDOW = TX_DELAY_WINDOW - TX_DELAY
        # Compute the risk score as the ratio of fraud count to transaction count within the window
        RISK_WINDOW = FRAUD_WINDOW / TX_WINDOW
        # Save the feature values for the incoming row
        incoming_row[feature+'_Trnscn_count'+str(window_size)+'Day'] =  TX_WINDOW.iloc[-1]
        incoming_row[feature+'_Risk_Score'+str(window_size)+'Day'] = RISK_WINDOW.iloc[-1]

    # Replace NA values with 0 (for cases where NB_TX_WINDOW is 0)
    incoming_row.fillna(0, inplace=True)
    incoming_row.pop('is_fraud')
    return incoming_row
