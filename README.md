# ZERU – Internship Assignment

This project involves developing a risk scoring mechanism for wallets interacting with Compound V2 using historical transaction data. The goal is to rank wallets based on their reliability and behavior, and categorize them into risk segments for potential creditworthiness evaluation.

## Files Included

- `score_wallets.py` – The main Python script that performs:
  - Data ingestion and preprocessing
  - Risk scoring based on defined logic
  - Risk category assignment
  - Output generation of top 1000 wallets

- `top_1000_wallets.csv` – Final output file with:
  - `wallet_address`, `score`, and `risk_category` columns

- `methodology.md` – Detailed explanation of the scoring logic and rationale used in this analysis

- `wallet_analysis.md` – Key takeaways from the data, wallet behavior trends, and breakdown of risk categories


## How to Run

1. Make sure you have Python 3.8+ installed.
2. Install required libraries:
   ```bash
   pip install pandas numpy
3. Run the script:
python score_wallets.py
The final CSV file (top_1000_wallets.csv) will be generated in the root directory.

## Scoring Summary

The scoring mechanism accounts for multiple wallet behaviors including:

Interaction frequency with Compound V2
Borrowing and repayment discipline
Liquidation history
Collateral vs borrow ratios
Time-weighted activity consistency
For a full explanation, see methodology.md.

## Insights & Observations

Wallet behavior shows distinct patterns with respect to reliability and risk. See wallet_analysis.md for a full breakdown of:

Risk category distributions
Interesting wallet traits
Edge cases

## Author

Assignment completed by Mohamed Thaufeek
Submitted for AI Engineer Intern Role – Zeru
