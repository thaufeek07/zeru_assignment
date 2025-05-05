# Methodology

This document outlines the steps taken to analyze and score Compound V2 wallets using the provided raw transaction data. The aim was to evaluate wallet activity and assign a risk category and bot label based on behavior.

## 1. Data Collection and Preprocessing

The dataset included multiple JSON files representing different types of Compound transactions. To reduce processing time, I selected the three largest files from the data/ directory, as these typically contained the most relevant transaction types (e.g., borrow, repay, liquidate).

Each file was parsed into Python dictionaries. Transactions without a valid to_address or from_address were excluded to ensure only usable data was included. Only relevant fields like wallet address and transaction value were retained.

## 2. Transaction Categorization

Each wallet address was mapped to its associated transaction types and values. Transaction types considered include:  

Supply  
Borrow  
Repay  
Withdraw  
Liquidate  

Using a defaultdict, I aggregated the values for each wallet across these categories, which served as the basis for scoring.

## 3. Wallet Scoring

For each wallet, a raw score was calculated using the following weighted formula:

score = supply + repay - borrow - withdraw - liquidate  
This scoring system rewards positive behaviors (such as supplying or repaying) and penalizes negative or risky actions (like borrowing or getting liquidated).

Raw scores varied widely in scale, so I applied MinMaxScaler from sklearn.preprocessing to normalize scores between 0 and 100.

## 4. Risk Categorization

Wallets were then categorized into risk levels based on their normalized scores:  

High Risk: Score below 30  
Medium Risk: Score between 30 and 70  
Low Risk: Score above 70  

These thresholds provide a basic risk segmentation to help identify potentially malicious or unstable actors.

## 5. Bot Detection

To detect bots, I implemented a simple heuristic: if a wallet performed the same transaction amount more than 10 times, it was flagged as a likely bot. This approach assumes that bots are more likely to repeat identical actions, which may not be common in organic wallet behavior.

## 6. Output Files and Visualization

After scoring and categorizing, the top 1000 wallets (by normalized score) were saved in a file named top_1000_wallets.csv. Each entry includes:  

Wallet Address  
Normalized Score  
Risk Label  
Bot Flag  

I also generated a bar chart to visualize the top 20 wallets by score, offering a quick snapshot of the highest-performing users.

