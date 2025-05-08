import pandas as pd
import os
import json
from collections import defaultdict
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt

#set the path to your data folder
data_folder = 'data'

#check if the folder exists and contains files
if not os.path.exists(data_folder):
    print(f"Data folder '{data_folder}' does not exist.")
    exit()
else:
    files = sorted(os.listdir(data_folder), key=lambda x: os.path.getsize(os.path.join(data_folder, x)), reverse=True)[:3]
    if not files:
        print(f"No files found in the data folder '{data_folder}'.")
        exit()

#initialize a list to store the dataframes
data_frames = []

#load the files and append them to the list
for file in files:
    print(f"Loading file: {file}")
    file_path = os.path.join(data_folder, file)

    try:
        if file.endswith(".json"):
            with open(file_path, 'r') as f:
                data = json.load(f)

            #print the type of the data to help diagnose the issue
            print(f"Data type of {file}: {type(data)}")

            #if the data is a dictionary, check its structure
            if isinstance(data, dict):
                #print the keys of the dictionary to understand its structure
                print(f"Keys in the dictionary: {list(data.keys())}")

                #combine data from keys like 'deposits', 'withdraws', etc.
                combined_transactions = []
                for key in ["deposits", "withdraws", "borrows", "repays", "liquidates"]:
                    if key in data:
                        for txn in data[key]:
                            txn["transaction_type"] = key  #add a column to indicate the transaction type
                            combined_transactions.append(txn)

                if combined_transactions:
                    df = pd.DataFrame(combined_transactions)
                else:
                    print(f"No transactions found in {file}.")
                    continue
            else:
                print(f"Data in {file} is not a dictionary or list. First few elements: {data[:3]}")
                continue
        elif file.endswith(".csv"):
            df = pd.read_csv(file_path)
        else:
            print(f"Unsupported file format: {file}")
            continue

        print(f"Loaded file with shape: {df.shape}")
        data_frames.append(df)

    except Exception as e:
        print(f"Failed to load {file} due to: {e}")

#check if any dataframes were loaded
if data_frames:
    #combine all loaded data into a single dataframe
    combined_data = pd.concat(data_frames, ignore_index=True)
    print(f"\nCombined data shape: {combined_data.shape}")
    print("\nColumns:", combined_data.columns)
    print("\nSample of the data:\n", combined_data.head(3))
else:
    print("No dataframes were loaded. Please check the data structure.")
    exit()

#initialize a dictionary to track wallet transaction totals
wallet_stats = defaultdict(lambda: {
    "total_deposit": 0,
    "total_withdraw": 0,
    "total_borrow": 0,
    "total_repay": 0,
    "total_liquidate": 0
})

#process each transaction record in the dataframe
for _, row in combined_data.iterrows():
    try:
        wallet_id = row["account"].get("id", None) if isinstance(row["account"], dict) else None
        txn_amount = row.get("amountUSD", None)
        txn_type = row.get("transaction_type", None)

        if txn_amount is None or txn_type is None or wallet_id is None:
            continue

        try:
            txn_amount = float(txn_amount)
        except ValueError:
            print(f"Error: Invalid amount USD value for wallet {wallet_id} in {txn_type}")
            continue

        key = f"total_{txn_type[:-1]}"  #removing the trailing 's' from txn type
        wallet_stats[wallet_id][key] += txn_amount

    except Exception as e:
        print(f"Error processing transaction: {e}")

#convert wallet transaction statistics into a DataFrame
wallet_df = pd.DataFrame.from_dict(wallet_stats, orient='index').reset_index()
wallet_df = wallet_df.rename(columns={"index": "wallet_address"})

print("\nWallet statistics:\n", wallet_df.head())

#calculate a simple score for each wallet based on transaction types
wallet_df["score"] = (
    wallet_df["total_deposit"] * 0.2 +
    wallet_df["total_repay"] * 0.3 - 
    wallet_df["total_borrow"] * 0.3 - 
    wallet_df["total_liquidate"] * 0.2
)

#sort wallets based on their score
wallet_df = wallet_df.sort_values(by="score", ascending=False).reset_index(drop=True)

#display the top 10 wallets by score
print("\nTop 10 wallets by score:")
print(wallet_df.head(10))

#normalize the transaction totals using Min-Max scaling
scaler = MinMaxScaler()
normalized_wallet_df = wallet_df.copy()
features_to_normalize = ["total_deposit", "total_withdraw", "total_borrow", "total_repay", "total_liquidate"]
normalized_wallet_df[features_to_normalize] = scaler.fit_transform(normalized_wallet_df[features_to_normalize])

#recalculate the score based on the normalized values
normalized_wallet_df["score"] = (
    normalized_wallet_df["total_deposit"] * 0.2 +
    normalized_wallet_df["total_repay"] * 0.3 - 
    normalized_wallet_df["total_borrow"] * 0.3 - 
    normalized_wallet_df["total_liquidate"] * 0.2
)

#add the wallet addresses back to the normalized dataframe
normalized_wallet_df["wallet_address"] = wallet_df["wallet_address"]

#sort the wallets again based on the normalized score
normalized_wallet_df = normalized_wallet_df.sort_values(by="score", ascending=False).reset_index(drop=True)

#function to assign a risk category based on the score
def categorize_risk(score):
    if score > 0.7:
        return "Low Risk"
    elif score > 0.4:
        return "Medium Risk"
    else:
        return "High Risk"

#apply the risk categorization
normalized_wallet_df["risk_category"] = normalized_wallet_df["score"].apply(categorize_risk)

#display the top 10 wallets with their normalized scores and risk categories
print("\nTop 10 wallets with normalized scores and risk categories:")
print(normalized_wallet_df[["wallet_address", "score", "risk_category"]].head(10))

#detect bot-like behavior: looking for repetitive patterns
def detect_bot_behavior(data):
    #count the number of identical transactions for each wallet
    repeated_patterns = data.groupby(['wallet_address', 'amountUSD']).size().reset_index(name='count')
    suspicious_wallets = repeated_patterns[repeated_patterns['count'] > 10]['wallet_address'].unique()
    return suspicious_wallets

#add this detection to your main workflow
if 'wallet_address' in combined_data.columns and 'amountUSD' in combined_data.columns:
    suspicious_wallets = detect_bot_behavior(combined_data)
    print(f"Suspicious wallets identified: {len(suspicious_wallets)}")
else:
    print("Required columns for bot detection are missing.")
    suspicious_wallets = []

#add bot detection information to the normalized wallet dataframe
normalized_wallet_df["is_bot"] = normalized_wallet_df["wallet_address"].isin(suspicious_wallets)

#create another column for wallets categorized as "bot-like"
normalized_wallet_df["bot_risk"] = normalized_wallet_df["is_bot"].apply(lambda x: "Bot" if x else "Human")

#save the top 1,000 wallets to a CSV file
top_1000_wallets = normalized_wallet_df.head(1000)
top_1000_wallets.to_csv("top_1000_wallets.csv", index=False)
print("\nTop 1,000 wallets saved to 'top_1000_wallets.csv'")

#print the top 5 wallets
top_5_wallets = normalized_wallet_df.head(5)
print("\nTop 5 wallets:\n")
print(top_5_wallets.to_string(index=False))

#print the bottom 5 wallets
print("\nBottom 5 wallets:\n")
bottom_5_wallets = normalized_wallet_df.tail(5)
print(bottom_5_wallets.to_string(index=False))

#plot the wallet statistics
plt.figure(figsize=(12, 6))

#get the top 10 wallets
top_wallets = normalized_wallet_df.head(10)

#plot the bar chart
plt.bar(range(len(top_wallets)), top_wallets["score"], color='skyblue')

#set the x-axis ticks and labels
plt.xticks(range(len(top_wallets)), top_wallets["wallet_address"], rotation=45, ha='right', fontsize=8)

#label the chart
plt.xlabel('Wallet Address')
plt.ylabel('Normalized Score')
plt.title('Top 10 Wallets by Normalized Score')

#adjust layout to prevent label overlap
plt.tight_layout()

#display the chart
plt.show()