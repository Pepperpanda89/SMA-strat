# SMA Crossover Strategy Backtester

An interactive desktop app for backtesting a **Simple Moving Average (SMA) crossover** trading strategy on any S&P 500 stock, and comparing it against plain buy-and-hold.

Pick a stock, choose your moving-average windows, and the app downloads historical prices, simulates the trades and shows you how the strategy would have performed.

## Features

- **~500 S&P 500 stocks** organised by sector, with live search by ticker, company or sector
- **Configurable strategy**: short and long SMA windows, years of history and starting capital
- **Four result tabs**
  - *Price & Signals*: closing price with both SMAs and every buy/sell marked
  - *Portfolio Value*: strategy equity curve vs. buy-and-hold
  - *Performance Metrics*: side-by-side comparison with buy-and-hold
  - *Trade Log*: every trade with date, price, shares and value
- **Export**: save the full data, trade log and metrics report to a folder with one click

## The strategy

| Signal | Condition | Action |
|---|---|---|
| Golden cross | Short SMA crosses **above** long SMA | Buy with all available cash |
| Death cross | Short SMA crosses **below** long SMA | Sell the whole position |

When out of the market the portfolio sits in cash. Every run is benchmarked against buying the stock on day one and holding it.

## Metrics reported

Total return, CAGR, annualised Sharpe ratio, maximum drawdown, number of trades, win rate and final portfolio value, for both the strategy and buy-and-hold.

## Getting started

Requires Python 3.9+.

```bash
git clone https://github.com/Pepperpanda89/SMA-strat.git
cd SMA-strat
pip install -r requirements.txt
python sma_backtest.py
```

Price data is downloaded from Yahoo Finance via [`yfinance`](https://github.com/ranaroussi/yfinance), so an internet connection is needed.

## Limitations

This is an educational tool, not investment advice. The backtest ignores trading fees, slippage, taxes and dividends, and uses today's S&P 500 members (survivorship bias). Past performance does not predict future results.

## Built with

Python · tkinter · pandas · NumPy · matplotlib · yfinance

## License

[MIT](LICENSE)
