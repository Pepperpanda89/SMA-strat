"""
╔══════════════════════════════════════════════════════════════════╗
║   S&P 500 Simple Moving Average (SMA) Strategy Backtester       ║
║   Interactive GUI — select a stock, configure SMA, backtest     ║
╚══════════════════════════════════════════════════════════════════╝

Requirements: pip install yfinance pandas numpy matplotlib seaborn scipy
Run:          python sma_backtest.py
"""

import warnings
warnings.filterwarnings("ignore")

import tkinter as tk
from tkinter import ttk, messagebox
import threading
import numpy as np
import pandas as pd
import yfinance as yf
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.patches import FancyBboxPatch
import matplotlib.dates as mdates
from datetime import datetime, timedelta
import os


# ═══════════════════════════════════════════════════════════════
# S&P 500 STOCK UNIVERSE — ticker: full company name
# ═══════════════════════════════════════════════════════════════

SP500 = {
    "Technology": {
        "AAPL": "Apple", "MSFT": "Microsoft", "NVDA": "NVIDIA", "AVGO": "Broadcom",
        "ORCL": "Oracle", "CRM": "Salesforce", "CSCO": "Cisco", "ACN": "Accenture",
        "ADBE": "Adobe", "AMD": "AMD", "IBM": "IBM", "INTC": "Intel",
        "INTU": "Intuit", "TXN": "Texas Instruments", "QCOM": "Qualcomm",
        "AMAT": "Applied Materials", "NOW": "ServiceNow", "ADI": "Analog Devices",
        "LRCX": "Lam Research", "MU": "Micron", "KLAC": "KLA Corp",
        "SNPS": "Synopsys", "CDNS": "Cadence Design", "MCHP": "Microchip Tech",
        "FTNT": "Fortinet", "MSI": "Motorola Solutions", "ANSS": "ANSYS",
        "KEYS": "Keysight", "MPWR": "Monolithic Power", "TER": "Teradyne",
        "ZBRA": "Zebra Technologies", "TRMB": "Trimble", "PTC": "PTC",
        "EPAM": "EPAM Systems", "JNPR": "Juniper Networks", "AKAM": "Akamai",
        "FFIV": "F5 Networks", "SWKS": "Skyworks", "QRVO": "Qorvo",
        "WDC": "Western Digital", "GEN": "Gen Digital", "NTAP": "NetApp",
        "CTSH": "Cognizant", "IT": "Gartner", "FSLR": "First Solar",
        "ON": "ON Semiconductor", "NXPI": "NXP Semi", "MRVL": "Marvell",
        "HPQ": "HP Inc", "HPE": "HP Enterprise", "STX": "Seagate",
    },
    "Financials": {
        "BRK-B": "Berkshire Hathaway", "JPM": "JPMorgan Chase", "V": "Visa",
        "MA": "Mastercard", "BAC": "Bank of America", "WFC": "Wells Fargo",
        "GS": "Goldman Sachs", "MS": "Morgan Stanley", "SPGI": "S&P Global",
        "BLK": "BlackRock", "C": "Citigroup", "AXP": "American Express",
        "PGR": "Progressive", "CB": "Chubb", "SCHW": "Charles Schwab",
        "MMC": "Marsh McLennan", "ICE": "Intercontinental Exchange",
        "CME": "CME Group", "AON": "Aon", "MCO": "Moody's",
        "MET": "MetLife", "AIG": "AIG", "AFL": "Aflac",
        "PRU": "Prudential", "TRV": "Travelers", "AJG": "Arthur J Gallagher",
        "MSCI": "MSCI", "COF": "Capital One", "USB": "US Bancorp",
        "PNC": "PNC Financial", "TFC": "Truist", "BK": "Bank of New York",
        "ALL": "Allstate", "FITB": "Fifth Third", "STT": "State Street",
        "HBAN": "Huntington Banc", "RF": "Regions Financial",
        "CFG": "Citizens Financial", "KEY": "KeyCorp", "NTRS": "Northern Trust",
        "CINF": "Cincinnati Financial", "RJF": "Raymond James",
        "CBOE": "Cboe Global", "NDAQ": "Nasdaq Inc", "IVZ": "Invesco",
        "BEN": "Franklin Templeton", "GL": "Globe Life", "L": "Loews",
        "ZION": "Zions Bancorp", "CMA": "Comerica",
    },
    "Healthcare": {
        "UNH": "UnitedHealth", "LLY": "Eli Lilly", "JNJ": "Johnson & Johnson",
        "MRK": "Merck", "ABBV": "AbbVie", "TMO": "Thermo Fisher",
        "ABT": "Abbott Labs", "DHR": "Danaher", "PFE": "Pfizer",
        "AMGN": "Amgen", "BMY": "Bristol-Myers", "ELV": "Elevance Health",
        "ISRG": "Intuitive Surgical", "MDT": "Medtronic", "SYK": "Stryker",
        "GILD": "Gilead Sciences", "CI": "Cigna", "REGN": "Regeneron",
        "VRTX": "Vertex Pharma", "BDX": "Becton Dickinson", "ZTS": "Zoetis",
        "BSX": "Boston Scientific", "HUM": "Humana", "HCA": "HCA Healthcare",
        "IDXX": "IDEXX Labs", "IQV": "IQVIA", "EW": "Edwards Lifesciences",
        "A": "Agilent", "MTD": "Mettler-Toledo", "DXCM": "DexCom",
        "RMD": "ResMed", "BAX": "Baxter", "ALGN": "Align Technology",
        "WST": "West Pharma", "COO": "CooperCompanies", "HOLX": "Hologic",
        "TFX": "Teleflex", "XRAY": "Dentsply Sirona", "HSIC": "Henry Schein",
        "DGX": "Quest Diagnostics", "LH": "Labcorp", "BIO": "Bio-Rad",
        "CRL": "Charles River Labs", "OGN": "Organon", "VTRS": "Viatris",
        "DVA": "DaVita", "INCY": "Incyte", "MOH": "Molina Healthcare",
    },
    "Consumer Discretionary": {
        "AMZN": "Amazon", "TSLA": "Tesla", "HD": "Home Depot",
        "MCD": "McDonald's", "NKE": "Nike", "LOW": "Lowe's",
        "SBUX": "Starbucks", "TJX": "TJX Companies", "BKNG": "Booking Holdings",
        "CMG": "Chipotle", "ORLY": "O'Reilly Auto", "AZO": "AutoZone",
        "ROST": "Ross Stores", "MAR": "Marriott", "HLT": "Hilton",
        "DHI": "D.R. Horton", "LEN": "Lennar", "GM": "General Motors",
        "F": "Ford", "YUM": "Yum! Brands", "DPZ": "Domino's Pizza",
        "POOL": "Pool Corp", "APTV": "Aptiv", "GRMN": "Garmin",
        "BBY": "Best Buy", "EBAY": "eBay", "ETSY": "Etsy",
        "ULTA": "Ulta Beauty", "KMX": "CarMax", "GPC": "Genuine Parts",
        "LKQ": "LKQ Corp", "BWA": "BorgWarner", "CZR": "Caesars",
        "WYNN": "Wynn Resorts", "MGM": "MGM Resorts", "LVS": "Las Vegas Sands",
        "NVR": "NVR Inc", "PHM": "PulteGroup", "TPR": "Tapestry",
        "RL": "Ralph Lauren", "HAS": "Hasbro", "MHK": "Mohawk Industries",
        "NCLH": "Norwegian Cruise", "CCL": "Carnival", "RCL": "Royal Caribbean",
        "WHR": "Whirlpool", "VFC": "VF Corp",
    },
    "Consumer Staples": {
        "PG": "Procter & Gamble", "PEP": "PepsiCo", "KO": "Coca-Cola",
        "COST": "Costco", "WMT": "Walmart", "PM": "Philip Morris",
        "MDLZ": "Mondelez", "MO": "Altria", "CL": "Colgate-Palmolive",
        "KMB": "Kimberly-Clark", "GIS": "General Mills", "HSY": "Hershey",
        "KHC": "Kraft Heinz", "SJM": "J.M. Smucker", "K": "Kellanova",
        "CAG": "Conagra", "MKC": "McCormick", "HRL": "Hormel Foods",
        "CPB": "Campbell Soup", "TSN": "Tyson Foods", "ADM": "Archer-Daniels",
        "STZ": "Constellation Brands", "TAP": "Molson Coors",
        "CHD": "Church & Dwight", "CLX": "Clorox", "EL": "Estee Lauder",
        "MNST": "Monster Beverage", "WBA": "Walgreens", "KR": "Kroger",
        "SYY": "Sysco",
    },
    "Energy": {
        "XOM": "ExxonMobil", "CVX": "Chevron", "COP": "ConocoPhillips",
        "SLB": "Schlumberger", "EOG": "EOG Resources", "MPC": "Marathon Petroleum",
        "PSX": "Phillips 66", "VLO": "Valero Energy", "OXY": "Occidental",
        "WMB": "Williams Cos", "DVN": "Devon Energy", "HES": "Hess Corp",
        "HAL": "Halliburton", "FANG": "Diamondback Energy", "KMI": "Kinder Morgan",
        "BKR": "Baker Hughes", "TRGP": "Targa Resources", "OKE": "ONEOK",
        "CTRA": "Coterra Energy", "MRO": "Marathon Oil", "APA": "APA Corp",
        "EQT": "EQT Corp",
    },
    "Industrials": {
        "CAT": "Caterpillar", "RTX": "RTX Corp", "UNP": "Union Pacific",
        "HON": "Honeywell", "DE": "Deere & Co", "BA": "Boeing",
        "UPS": "UPS", "GE": "GE Aerospace", "LMT": "Lockheed Martin",
        "ADP": "ADP", "MMM": "3M", "ITW": "Illinois Tool Works",
        "EMR": "Emerson Electric", "ETN": "Eaton", "PH": "Parker Hannifin",
        "NSC": "Norfolk Southern", "CSX": "CSX Corp", "GD": "General Dynamics",
        "TT": "Trane Technologies", "WM": "Waste Management",
        "RSG": "Republic Services", "CTAS": "Cintas", "FAST": "Fastenal",
        "PCAR": "PACCAR", "CARR": "Carrier Global", "OTIS": "Otis Worldwide",
        "ROK": "Rockwell Automation", "DOV": "Dover Corp", "AME": "AMETEK",
        "XYL": "Xylem", "GWW": "W.W. Grainger", "IR": "Ingersoll Rand",
        "IEX": "IDEX Corp", "NDSN": "Nordson", "SNA": "Snap-on",
        "TXT": "Textron", "LDOS": "Leidos", "HII": "Huntington Ingalls",
        "MAS": "Masco", "DAL": "Delta Air Lines", "UAL": "United Airlines",
        "LUV": "Southwest Airlines", "AAL": "American Airlines",
        "AXON": "Axon Enterprise", "VRSK": "Verisk Analytics",
        "WAB": "Westinghouse Air", "CPRT": "Copart", "EFX": "Equifax",
    },
    "Communication Services": {
        "GOOGL": "Alphabet (Google)", "META": "Meta Platforms",
        "NFLX": "Netflix", "DIS": "Walt Disney", "CMCSA": "Comcast",
        "T": "AT&T", "VZ": "Verizon", "TMUS": "T-Mobile",
        "CHTR": "Charter Communications", "EA": "Electronic Arts",
        "TTWO": "Take-Two Interactive", "MTCH": "Match Group",
        "LYV": "Live Nation", "WBD": "Warner Bros Discovery",
        "OMC": "Omnicom", "IPG": "Interpublic Group",
        "FOXA": "Fox Corp A", "FOX": "Fox Corp B",
        "NWS": "News Corp A", "NWSA": "News Corp B",
    },
    "Utilities": {
        "NEE": "NextEra Energy", "SO": "Southern Company", "DUK": "Duke Energy",
        "CEG": "Constellation Energy", "SRE": "Sempra", "AEP": "American Electric",
        "D": "Dominion Energy", "EXC": "Exelon", "XEL": "Xcel Energy",
        "ED": "Consolidated Edison", "WEC": "WEC Energy", "ES": "Eversource",
        "AWK": "American Water Works", "DTE": "DTE Energy", "PPL": "PPL Corp",
        "FE": "FirstEnergy", "ETR": "Entergy", "CMS": "CMS Energy",
        "AEE": "Ameren", "CNP": "CenterPoint", "ATO": "Atmos Energy",
        "EVRG": "Evergy", "NI": "NiSource", "PNW": "Pinnacle West",
        "LNT": "Alliant Energy", "NRG": "NRG Energy", "PEG": "PSEG",
        "AES": "AES Corp",
    },
    "Real Estate": {
        "PLD": "Prologis", "AMT": "American Tower", "CCI": "Crown Castle",
        "EQIX": "Equinix", "PSA": "Public Storage", "SPG": "Simon Property",
        "O": "Realty Income", "DLR": "Digital Realty", "WELL": "Welltower",
        "VICI": "VICI Properties", "ARE": "Alexandria Real Estate",
        "AVB": "AvalonBay", "EQR": "Equity Residential", "VTR": "Ventas",
        "MAA": "Mid-America Apartment", "UDR": "UDR Inc", "ESS": "Essex Property",
        "HST": "Host Hotels", "CPT": "Camden Property", "KIM": "Kimco Realty",
        "REG": "Regency Centers", "FRT": "Federal Realty", "BXP": "BXP Inc",
        "SLG": "SL Green", "VNO": "Vornado Realty", "MPW": "Medical Properties",
        "SBAC": "SBA Communications", "WY": "Weyerhaeuser",
        "IRM": "Iron Mountain", "CBRE": "CBRE Group",
    },
    "Materials": {
        "LIN": "Linde", "APD": "Air Products", "SHW": "Sherwin-Williams",
        "FCX": "Freeport-McMoRan", "ECL": "Ecolab", "NEM": "Newmont",
        "NUE": "Nucor", "DOW": "Dow Inc", "DD": "DuPont",
        "PPG": "PPG Industries", "VMC": "Vulcan Materials", "MLM": "Martin Marietta",
        "CTVA": "Corteva", "CF": "CF Industries", "MOS": "Mosaic",
        "ALB": "Albemarle", "EMN": "Eastman Chemical", "CE": "Celanese",
        "IFF": "IFF", "FMC": "FMC Corp", "PKG": "Packaging Corp",
        "IP": "International Paper", "WRK": "WestRock", "SEE": "Sealed Air",
        "AVY": "Avery Dennison", "BLL": "Ball Corp", "AMCR": "Amcor",
    },
}


# ═══════════════════════════════════════════════════════════════
# SMA BACKTEST ENGINE
# ═══════════════════════════════════════════════════════════════

def run_sma_backtest(df, short_window, long_window, initial_capital=10000):
    """
    Run a simple moving average crossover backtest.
    
    Strategy:
      - BUY  when short SMA crosses ABOVE long SMA (golden cross)
      - SELL when short SMA crosses BELOW long SMA (death cross)
    
    Returns a DataFrame with signals, positions, and portfolio value.
    """
    data = df.copy()
    data["SMA_Short"] = data["Close"].rolling(window=short_window, min_periods=1).mean()
    data["SMA_Long"] = data["Close"].rolling(window=long_window, min_periods=1).mean()

    # Signal: 1 = long, 0 = out of market
    data["Signal"] = 0
    data.loc[data.index[long_window:], "Signal"] = np.where(
        data["SMA_Short"].iloc[long_window:] > data["SMA_Long"].iloc[long_window:], 1, 0
    )

    # Position changes: +1 = buy, -1 = sell
    data["Position"] = data["Signal"].diff()

    # Portfolio simulation
    shares = 0
    cash = initial_capital
    portfolio_values = []
    buy_hold_values = []
    initial_price = data["Close"].iloc[0]
    buy_hold_shares = initial_capital / initial_price

    trades = []

    for i, row in data.iterrows():
        # Buy signal
        if row["Position"] == 1 and cash > 0:
            shares = cash / row["Close"]
            trades.append({"Date": i, "Type": "BUY", "Price": row["Close"],
                           "Shares": shares, "Value": cash})
            cash = 0

        # Sell signal
        elif row["Position"] == -1 and shares > 0:
            cash = shares * row["Close"]
            trades.append({"Date": i, "Type": "SELL", "Price": row["Close"],
                           "Shares": shares, "Value": cash})
            shares = 0

        # Portfolio value
        port_val = cash + shares * row["Close"]
        portfolio_values.append(port_val)
        buy_hold_values.append(buy_hold_shares * row["Close"])

    data["Portfolio"] = portfolio_values
    data["BuyHold"] = buy_hold_values

    trades_df = pd.DataFrame(trades)
    return data, trades_df


def compute_metrics(data, trades_df, initial_capital=10000):
    """Compute performance metrics for the backtest."""
    final_val = data["Portfolio"].iloc[-1]
    bh_final = data["BuyHold"].iloc[-1]

    days = (data.index[-1] - data.index[0]).days
    years = days / 365.25

    strat_return = (final_val / initial_capital - 1) * 100
    bh_return = (bh_final / initial_capital - 1) * 100

    strat_cagr = ((final_val / initial_capital) ** (1 / years) - 1) * 100 if years > 0 else 0
    bh_cagr = ((bh_final / initial_capital) ** (1 / years) - 1) * 100 if years > 0 else 0

    # Daily returns for Sharpe / max drawdown
    data["Daily_Return"] = data["Portfolio"].pct_change()
    data["BH_Daily_Return"] = data["BuyHold"].pct_change()

    sharpe = (data["Daily_Return"].mean() / data["Daily_Return"].std() * np.sqrt(252)
              if data["Daily_Return"].std() > 0 else 0)
    bh_sharpe = (data["BH_Daily_Return"].mean() / data["BH_Daily_Return"].std() * np.sqrt(252)
                 if data["BH_Daily_Return"].std() > 0 else 0)

    # Max drawdown
    cum_max = data["Portfolio"].cummax()
    drawdown = (data["Portfolio"] - cum_max) / cum_max
    max_dd = drawdown.min() * 100

    bh_cum_max = data["BuyHold"].cummax()
    bh_drawdown = (data["BuyHold"] - bh_cum_max) / bh_cum_max
    bh_max_dd = bh_drawdown.min() * 100

    num_trades = len(trades_df)

    # Win rate (round-trip trades)
    if len(trades_df) >= 2:
        sells = trades_df[trades_df["Type"] == "SELL"]
        buys = trades_df[trades_df["Type"] == "BUY"]
        min_pairs = min(len(buys), len(sells))
        if min_pairs > 0:
            wins = 0
            for j in range(min_pairs):
                if sells.iloc[j]["Price"] > buys.iloc[j]["Price"]:
                    wins += 1
            win_rate = wins / min_pairs * 100
        else:
            win_rate = 0
    else:
        win_rate = 0

    return {
        "Strategy Return": f"{strat_return:+.2f}%",
        "Buy & Hold Return": f"{bh_return:+.2f}%",
        "Strategy CAGR": f"{strat_cagr:+.2f}%",
        "Buy & Hold CAGR": f"{bh_cagr:+.2f}%",
        "Strategy Sharpe": f"{sharpe:.2f}",
        "Buy & Hold Sharpe": f"{bh_sharpe:.2f}",
        "Strategy Max Drawdown": f"{max_dd:.2f}%",
        "Buy & Hold Max Drawdown": f"{bh_max_dd:.2f}%",
        "Total Trades": str(num_trades),
        "Win Rate": f"{win_rate:.1f}%",
        "Final Portfolio Value": f"${final_val:,.2f}",
        "Buy & Hold Final Value": f"${bh_final:,.2f}",
        "Period": f"{data.index[0].strftime('%Y-%m-%d')} to {data.index[-1].strftime('%Y-%m-%d')}",
        "Duration": f"{days} days ({years:.1f} years)",
    }


# ═══════════════════════════════════════════════════════════════
# GUI APPLICATION
# ═══════════════════════════════════════════════════════════════

class SMABacktestApp:
    def __init__(self, root):
        self.root = root
        self.root.title("S&P 500 SMA Strategy Backtester")
        self.root.geometry("1500x900")
        self.root.minsize(1300, 800)

        self.selected_ticker = tk.StringVar(value="")
        self.data = None
        self.trades_df = None

        self._build_ui()

    def _build_ui(self):
        # ── Left panel: selection & config ──
        left = ttk.Frame(self.root, width=380)
        left.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)
        left.pack_propagate(False)

        ttk.Label(left, text="SMA Strategy Backtester",
                  font=("Helvetica", 14, "bold")).pack(pady=(10, 2))
        ttk.Label(left, text="Simple Moving Average Crossover",
                  font=("Helvetica", 9), foreground="gray").pack(pady=(0, 8))

        # ── Search box ──
        search_frame = ttk.Frame(left)
        search_frame.pack(fill=tk.X, padx=5, pady=5)
        ttk.Label(search_frame, text="Search:").pack(side=tk.LEFT)
        self.search_var = tk.StringVar()
        self.search_var.trace_add("write", self._filter_stocks)
        ttk.Entry(search_frame, textvariable=self.search_var).pack(
            side=tk.LEFT, fill=tk.X, expand=True, padx=5)

        # ── Stock list with radio buttons ──
        stock_frame = ttk.LabelFrame(left, text="Select a Stock")
        stock_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        self.canvas = tk.Canvas(stock_frame, highlightthickness=0)
        scrollbar = ttk.Scrollbar(stock_frame, orient=tk.VERTICAL,
                                  command=self.canvas.yview)
        self.stock_inner = ttk.Frame(self.canvas)

        self.stock_inner.bind("<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.create_window((0, 0), window=self.stock_inner, anchor=tk.NW)
        self.canvas.configure(yscrollcommand=scrollbar.set)

        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        def _on_mousewheel(event):
            self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        self.canvas.bind_all("<MouseWheel>", _on_mousewheel)

        # Populate stock radio buttons
        self.all_widgets = []
        for sector, stocks in SP500.items():
            lbl = ttk.Label(self.stock_inner, text=sector,
                            font=("Helvetica", 10, "bold"))
            lbl.pack(anchor=tk.W, padx=5, pady=(8, 2))
            self.all_widgets.append((lbl, None, None, sector))

            for ticker, name in sorted(stocks.items(), key=lambda x: x[1]):
                frame = ttk.Frame(self.stock_inner)
                frame.pack(fill=tk.X, padx=10)
                display = f"{name} ({ticker})"
                rb = ttk.Radiobutton(frame, text=display,
                                     variable=self.selected_ticker, value=ticker)
                rb.pack(anchor=tk.W)
                self.all_widgets.append((frame, ticker, name, sector))

        # ── Strategy Configuration ──
        config_frame = ttk.LabelFrame(left, text="Strategy Configuration")
        config_frame.pack(fill=tk.X, padx=5, pady=5)

        # Short SMA
        row1 = ttk.Frame(config_frame)
        row1.pack(fill=tk.X, padx=5, pady=3)
        ttk.Label(row1, text="Short SMA (days):").pack(side=tk.LEFT)
        self.short_sma_var = tk.StringVar(value="20")
        ttk.Combobox(row1, textvariable=self.short_sma_var,
                     values=["5", "10", "15", "20", "30", "50"],
                     width=6, state="readonly").pack(side=tk.RIGHT)

        # Long SMA
        row2 = ttk.Frame(config_frame)
        row2.pack(fill=tk.X, padx=5, pady=3)
        ttk.Label(row2, text="Long SMA (days):").pack(side=tk.LEFT)
        self.long_sma_var = tk.StringVar(value="50")
        ttk.Combobox(row2, textvariable=self.long_sma_var,
                     values=["20", "50", "100", "150", "200"],
                     width=6, state="readonly").pack(side=tk.RIGHT)

        # Years of data
        row3 = ttk.Frame(config_frame)
        row3.pack(fill=tk.X, padx=5, pady=3)
        ttk.Label(row3, text="Years of data:").pack(side=tk.LEFT)
        self.years_var = tk.StringVar(value="3")
        ttk.Combobox(row3, textvariable=self.years_var,
                     values=["1", "2", "3", "5", "10"],
                     width=6, state="readonly").pack(side=tk.RIGHT)

        # Initial capital
        row4 = ttk.Frame(config_frame)
        row4.pack(fill=tk.X, padx=5, pady=3)
        ttk.Label(row4, text="Initial capital ($):").pack(side=tk.LEFT)
        self.capital_var = tk.StringVar(value="10000")
        ttk.Entry(row4, textvariable=self.capital_var, width=10).pack(side=tk.RIGHT)

        # ── Strategy explanation ──
        ttk.Label(left, text="Strategy: Buy when short SMA crosses\n"
                  "above long SMA. Sell when it crosses below.",
                  font=("Helvetica", 8), foreground="gray",
                  justify=tk.LEFT).pack(padx=5, pady=2, anchor=tk.W)

        # Run button
        self.run_btn = ttk.Button(left, text="Run Backtest",
                                  command=self._run_backtest)
        self.run_btn.pack(fill=tk.X, padx=5, pady=5)

        # Save button
        self.save_btn = ttk.Button(left, text="Save Charts & Report",
                                   command=self._save_output, state=tk.DISABLED)
        self.save_btn.pack(fill=tk.X, padx=5, pady=(0, 5))

        # Status
        self.status_var = tk.StringVar(value="Select a stock and configure SMA, then click Run.")
        ttk.Label(left, textvariable=self.status_var, wraplength=350,
                  foreground="gray").pack(padx=5, pady=5)

        # ── Right panel: charts + analysis ──
        right = ttk.Frame(self.root)
        right.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=5)

        self.notebook = ttk.Notebook(right)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        # Tab 1: Price chart with SMA lines + signals
        self.tab_price = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_price, text="Price & Signals")

        # Tab 2: Portfolio performance
        self.tab_portfolio = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_portfolio, text="Portfolio Value")

        # Tab 3: Performance metrics
        self.tab_metrics = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_metrics, text="Performance Metrics")

        self.metrics_text = tk.Text(self.tab_metrics, wrap=tk.WORD,
                                    font=("Consolas", 11))
        metrics_scroll = ttk.Scrollbar(self.tab_metrics,
                                       command=self.metrics_text.yview)
        self.metrics_text.configure(yscrollcommand=metrics_scroll.set)
        metrics_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.metrics_text.pack(fill=tk.BOTH, expand=True)

        # Tab 4: Trade log
        self.tab_trades = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_trades, text="Trade Log")

        self.trades_text = tk.Text(self.tab_trades, wrap=tk.WORD,
                                   font=("Consolas", 10))
        trades_scroll = ttk.Scrollbar(self.tab_trades,
                                      command=self.trades_text.yview)
        self.trades_text.configure(yscrollcommand=trades_scroll.set)
        trades_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.trades_text.pack(fill=tk.BOTH, expand=True)

    # ── Helpers ──

    def _filter_stocks(self, *args):
        query = self.search_var.get().lower().strip()
        visible_sectors = set()

        for widget_tuple in self.all_widgets:
            w, ticker, name, sector = widget_tuple
            if ticker is None:
                continue
            if not query:
                w.pack(fill=tk.X, padx=10)
                visible_sectors.add(sector)
            elif query in ticker.lower() or query in name.lower() or query in sector.lower():
                w.pack(fill=tk.X, padx=10)
                visible_sectors.add(sector)
            else:
                w.pack_forget()

        for widget_tuple in self.all_widgets:
            w, ticker, name, sector = widget_tuple
            if ticker is None:  # sector label
                if sector in visible_sectors or not query:
                    w.pack(anchor=tk.W, padx=5, pady=(8, 2))
                else:
                    w.pack_forget()

    def _run_backtest(self):
        ticker = self.selected_ticker.get()
        if not ticker:
            messagebox.showwarning("No Stock", "Please select a stock first.")
            return

        short_w = int(self.short_sma_var.get())
        long_w = int(self.long_sma_var.get())

        if short_w >= long_w:
            messagebox.showwarning("Invalid SMA",
                                   "Short SMA must be less than Long SMA.")
            return

        try:
            capital = float(self.capital_var.get())
            if capital <= 0:
                raise ValueError
        except ValueError:
            messagebox.showwarning("Invalid Capital",
                                   "Please enter a valid positive number for capital.")
            return

        self.run_btn.configure(state=tk.DISABLED)
        self.status_var.set(f"Downloading {ticker} data...")

        thread = threading.Thread(target=self._backtest_worker,
                                  args=(ticker, short_w, long_w, capital),
                                  daemon=True)
        thread.start()

    def _backtest_worker(self, ticker, short_w, long_w, capital):
        try:
            years = int(self.years_var.get())
            end = datetime.now()
            start = end - timedelta(days=years * 365)

            df = yf.download(ticker, start=start.strftime("%Y-%m-%d"),
                             end=end.strftime("%Y-%m-%d"), progress=False)

            if df.empty:
                self.root.after(0, lambda: messagebox.showerror(
                    "Error", f"No data returned for {ticker}."))
                self.root.after(0, lambda: self.run_btn.configure(state=tk.NORMAL))
                return

            # Flatten MultiIndex columns if present
            if isinstance(df.columns, pd.MultiIndex):
                df.columns = df.columns.get_level_values(0)

            self.root.after(0, lambda: self.status_var.set("Running backtest..."))

            data, trades_df = run_sma_backtest(df, short_w, long_w, capital)
            metrics = compute_metrics(data, trades_df, capital)

            self.data = data
            self.trades_df = trades_df

            # Get company name
            company = ""
            for sector, stocks in SP500.items():
                if ticker in stocks:
                    company = stocks[ticker]
                    break

            self.root.after(0, lambda: self._display_results(
                data, trades_df, metrics, ticker, company, short_w, long_w, capital))

        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror(
                "Error", f"Backtest failed:\n{e}"))
            self.root.after(0, lambda: self.run_btn.configure(state=tk.NORMAL))

    def _display_results(self, data, trades_df, metrics, ticker, company,
                         short_w, long_w, capital):
        self._plot_price_chart(data, ticker, company, short_w, long_w)
        self._plot_portfolio_chart(data, ticker, company, capital)
        self._show_metrics(metrics, ticker, company, short_w, long_w)
        self._show_trades(trades_df, ticker, company)

        self.run_btn.configure(state=tk.NORMAL)
        self.save_btn.configure(state=tk.NORMAL)
        self.status_var.set(f"Backtest complete for {company} ({ticker}).")

    def _plot_price_chart(self, data, ticker, company, short_w, long_w):
        for w in self.tab_price.winfo_children():
            w.destroy()

        fig, ax = plt.subplots(figsize=(12, 6))
        fig.patch.set_facecolor("#fafafa")
        ax.set_facecolor("#fafafa")

        ax.plot(data.index, data["Close"], label="Close Price",
                color="#333333", linewidth=1.0, alpha=0.8)
        ax.plot(data.index, data["SMA_Short"], label=f"SMA {short_w}",
                color="#2196F3", linewidth=1.2)
        ax.plot(data.index, data["SMA_Long"], label=f"SMA {long_w}",
                color="#FF9800", linewidth=1.2)

        # Buy signals
        buys = data[data["Position"] == 1]
        ax.scatter(buys.index, buys["Close"], marker="^", color="#4CAF50",
                   s=100, zorder=5, label="Buy Signal", edgecolors="white", linewidth=0.5)

        # Sell signals
        sells = data[data["Position"] == -1]
        ax.scatter(sells.index, sells["Close"], marker="v", color="#F44336",
                   s=100, zorder=5, label="Sell Signal", edgecolors="white", linewidth=0.5)

        ax.set_title(f"{company} ({ticker}) — SMA {short_w}/{long_w} Crossover",
                     fontsize=13, fontweight="bold", pad=12)
        ax.set_ylabel("Price ($)", fontsize=10)
        ax.legend(loc="upper left", fontsize=8, framealpha=0.9)
        ax.grid(True, alpha=0.3)
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m"))
        fig.autofmt_xdate()
        fig.tight_layout()

        canvas = FigureCanvasTkAgg(fig, master=self.tab_price)
        canvas.draw()
        toolbar = NavigationToolbar2Tk(canvas, self.tab_price)
        toolbar.update()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        plt.close(fig)

    def _plot_portfolio_chart(self, data, ticker, company, capital):
        for w in self.tab_portfolio.winfo_children():
            w.destroy()

        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 7),
                                        height_ratios=[3, 1])
        fig.patch.set_facecolor("#fafafa")
        ax1.set_facecolor("#fafafa")
        ax2.set_facecolor("#fafafa")

        # Portfolio vs Buy & Hold
        ax1.plot(data.index, data["Portfolio"], label="SMA Strategy",
                 color="#2196F3", linewidth=1.5)
        ax1.plot(data.index, data["BuyHold"], label="Buy & Hold",
                 color="#888888", linewidth=1.2, linestyle="--")
        ax1.axhline(y=capital, color="#999999", linewidth=0.8,
                    linestyle=":", alpha=0.5)
        ax1.fill_between(data.index, data["Portfolio"], data["BuyHold"],
                         where=data["Portfolio"] >= data["BuyHold"],
                         alpha=0.1, color="#4CAF50")
        ax1.fill_between(data.index, data["Portfolio"], data["BuyHold"],
                         where=data["Portfolio"] < data["BuyHold"],
                         alpha=0.1, color="#F44336")

        ax1.set_title(f"{company} ({ticker}) — Portfolio Value",
                      fontsize=13, fontweight="bold", pad=12)
        ax1.set_ylabel("Portfolio Value ($)", fontsize=10)
        ax1.legend(loc="upper left", fontsize=9, framealpha=0.9)
        ax1.grid(True, alpha=0.3)

        # Drawdown
        cum_max = data["Portfolio"].cummax()
        drawdown = (data["Portfolio"] - cum_max) / cum_max * 100
        ax2.fill_between(data.index, drawdown, 0, color="#F44336", alpha=0.3)
        ax2.plot(data.index, drawdown, color="#F44336", linewidth=0.8)
        ax2.set_ylabel("Drawdown (%)", fontsize=10)
        ax2.set_title("Strategy Drawdown", fontsize=10, pad=6)
        ax2.grid(True, alpha=0.3)
        ax2.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m"))

        fig.autofmt_xdate()
        fig.tight_layout()

        canvas = FigureCanvasTkAgg(fig, master=self.tab_portfolio)
        canvas.draw()
        toolbar = NavigationToolbar2Tk(canvas, self.tab_portfolio)
        toolbar.update()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        plt.close(fig)

    def _show_metrics(self, metrics, ticker, company, short_w, long_w):
        self.metrics_text.configure(state=tk.NORMAL)
        self.metrics_text.delete("1.0", tk.END)

        header = (
            f"{'═' * 60}\n"
            f"  BACKTEST RESULTS: {company} ({ticker})\n"
            f"  Strategy: SMA {short_w} / {long_w} Crossover\n"
            f"{'═' * 60}\n\n"
        )
        self.metrics_text.insert(tk.END, header)

        self.metrics_text.insert(tk.END, "  PERIOD\n")
        self.metrics_text.insert(tk.END, f"  {'─' * 50}\n")
        self.metrics_text.insert(tk.END, f"  Period:              {metrics['Period']}\n")
        self.metrics_text.insert(tk.END, f"  Duration:            {metrics['Duration']}\n\n")

        self.metrics_text.insert(tk.END, "  RETURNS\n")
        self.metrics_text.insert(tk.END, f"  {'─' * 50}\n")
        self.metrics_text.insert(tk.END, f"  Strategy Return:     {metrics['Strategy Return']}\n")
        self.metrics_text.insert(tk.END, f"  Buy & Hold Return:   {metrics['Buy & Hold Return']}\n")
        self.metrics_text.insert(tk.END, f"  Strategy CAGR:       {metrics['Strategy CAGR']}\n")
        self.metrics_text.insert(tk.END, f"  Buy & Hold CAGR:     {metrics['Buy & Hold CAGR']}\n\n")

        self.metrics_text.insert(tk.END, "  RISK\n")
        self.metrics_text.insert(tk.END, f"  {'─' * 50}\n")
        self.metrics_text.insert(tk.END, f"  Strategy Sharpe:     {metrics['Strategy Sharpe']}\n")
        self.metrics_text.insert(tk.END, f"  Buy & Hold Sharpe:   {metrics['Buy & Hold Sharpe']}\n")
        self.metrics_text.insert(tk.END, f"  Strategy Max DD:     {metrics['Strategy Max Drawdown']}\n")
        self.metrics_text.insert(tk.END, f"  Buy & Hold Max DD:   {metrics['Buy & Hold Max Drawdown']}\n\n")

        self.metrics_text.insert(tk.END, "  TRADING\n")
        self.metrics_text.insert(tk.END, f"  {'─' * 50}\n")
        self.metrics_text.insert(tk.END, f"  Total Trades:        {metrics['Total Trades']}\n")
        self.metrics_text.insert(tk.END, f"  Win Rate:            {metrics['Win Rate']}\n\n")

        self.metrics_text.insert(tk.END, "  FINAL VALUES\n")
        self.metrics_text.insert(tk.END, f"  {'─' * 50}\n")
        self.metrics_text.insert(tk.END, f"  Strategy:            {metrics['Final Portfolio Value']}\n")
        self.metrics_text.insert(tk.END, f"  Buy & Hold:          {metrics['Buy & Hold Final Value']}\n")

        self.metrics_text.insert(tk.END, f"\n{'═' * 60}\n")
        self.metrics_text.insert(tk.END,
            "\n  NOTE: This is a historical backtest. Past performance\n"
            "  does not guarantee future results. Transaction costs\n"
            "  and slippage are not included.\n")

        self.metrics_text.configure(state=tk.DISABLED)

    def _show_trades(self, trades_df, ticker, company):
        self.trades_text.configure(state=tk.NORMAL)
        self.trades_text.delete("1.0", tk.END)

        header = (
            f"{'═' * 70}\n"
            f"  TRADE LOG: {company} ({ticker})\n"
            f"{'═' * 70}\n\n"
        )
        self.trades_text.insert(tk.END, header)

        if trades_df.empty:
            self.trades_text.insert(tk.END, "  No trades generated.\n")
        else:
            header_line = f"  {'#':>3}  {'Date':<12} {'Type':<6} {'Price':>10} {'Shares':>12} {'Value':>12}\n"
            self.trades_text.insert(tk.END, header_line)
            self.trades_text.insert(tk.END, f"  {'─' * 62}\n")

            for i, row in trades_df.iterrows():
                date_str = row['Date'].strftime('%Y-%m-%d')
                line = (f"  {i + 1:>3}  {date_str:<12} {row['Type']:<6} "
                        f"${row['Price']:>9.2f} {row['Shares']:>11.4f} "
                        f"${row['Value']:>11.2f}\n")
                self.trades_text.insert(tk.END, line)

        self.trades_text.configure(state=tk.DISABLED)

    def _save_output(self):
        if self.data is None:
            return

        ticker = self.selected_ticker.get()
        desktop = os.path.join(os.path.expanduser("~"), "Desktop")
        if not os.path.isdir(desktop):
            desktop = os.path.join(os.path.expanduser("~"), "OneDrive", "Skrivbord")
        if not os.path.isdir(desktop):
            desktop = os.path.expanduser("~")

        folder = os.path.join(desktop, f"SMA_Backtest_{ticker}")
        os.makedirs(folder, exist_ok=True)

        # Save data CSV
        csv_path = os.path.join(folder, f"{ticker}_backtest_data.csv")
        export = self.data[["Close", "SMA_Short", "SMA_Long", "Signal",
                            "Position", "Portfolio", "BuyHold"]].copy()
        export.to_csv(csv_path)

        # Save trades CSV
        if not self.trades_df.empty:
            trades_path = os.path.join(folder, f"{ticker}_trades.csv")
            self.trades_df.to_csv(trades_path, index=False)

        # Save metrics text
        metrics_path = os.path.join(folder, f"{ticker}_metrics.txt")
        with open(metrics_path, "w") as f:
            f.write(self.metrics_text.get("1.0", tk.END))

        messagebox.showinfo("Saved", f"Files saved to:\n{folder}")


# ═══════════════════════════════════════════════════════════════
# ENTRY POINT
# ═══════════════════════════════════════════════════════════════

if __name__ == "__main__":
    root = tk.Tk()
    app = SMABacktestApp(root)
    root.mainloop()
