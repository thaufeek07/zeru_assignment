### Wallet Analysis

This document summarizes key insights and patterns derived from analyzing user wallets on the Compound V2 protocol. The analysis was conducted after computing credit scores for each wallet based on their historical transactions involving supply, borrow, repay, withdraw, and liquidation activities.

## Dataset Overview

The raw data consisted of Compound V2 transaction logs for wallets interacting with the protocol. These transactions included five main types:

supply
borrow
repay
withdraw
liquidate

Each wallet's behavior was summarized by counting the frequency of these actions, then normalized using MinMaxScaler to bring all activity levels to a common scale between 0 and 1.

## Scoring Summary

The final credit score was computed using the formula:

credit_score = supply + repay - borrow - withdraw - liquidate
This formula rewards positive actions (supply, repay) and penalizes risky or negative actions (borrow, withdraw, liquidate). After computing raw scores, we applied normalization and classified wallets into the following risk categories:

High Risk: Credit Score ≤ 30
Medium Risk: Credit Score between 30 and 70
Low Risk: Credit Score ≥ 70

## Key Observations

Low Risk Wallets: These wallets frequently supplied and repaid assets, with minimal borrowing or liquidation events. They showed consistent, responsible usage of the protocol and indicate strong creditworthiness.

Medium Risk Wallets: These users had a mix of positive and negative actions. Their scores suggest balanced activity, possibly due to moderate borrowing or occasional liquidations.

High Risk Wallets: These wallets either borrowed frequently, were involved in multiple liquidations, or showed erratic behavior. Some of these wallets had little to no repayment activity, which dragged down their scores significantly.

## Bot Detection

In addition to score-based risk assessment, we implemented a basic bot detection heuristic. Wallets with:

Very high frequency of identical repeated transactions and unusual patterns like rapid-fire supply/withdraw loops were flagged as potential bots. While not definitive, these heuristics helped surface non-human patterns that could indicate wash trading or artificial volume.

## Notable Trends

A small number of wallets dominated the "high activity" segment, often showing both high supply and high borrow rates. These may represent institutional users or advanced yield farmers.

Many high-risk wallets had little to no repay activity, a red flag in terms of creditworthiness.

Some low-scoring wallets had only one or two transactions, making their credit score less reliable. These were mostly filtered out in bot/noise detection.

## Conclusion

The credit scoring and wallet analysis approach successfully categorized user risk levels and flagged suspicious behavior. This provides a foundational method to understand user profiles on Compound V2, which can be used for future risk-based filtering, user segmentation, or access control in DeFi applications.