# Algorithmic Trading Repository

This repository contains various algorithmic trading strategies, technical indicators, and tools for backtesting and live trading using Interactive Brokers API, MetaTrader5, and other platforms.

## 📋 Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

## 🚀 Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/Faiz9771/Algotrading_Basics.git
cd Algotrading_Basics
```

### 2. Create a Virtual Environment

**Important:** Always use a virtual environment to avoid conflicts with system packages.

#### On macOS/Linux:
```bash
python3 -m venv venv
source venv/bin/activate
```

#### On Windows:
```bash
python -m venv venv
venv\Scripts\activate
```

After activation, you should see `(venv)` in your terminal prompt.

### 3. Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Additional Setup (Optional)

Some packages may require additional setup:

- **TA-Lib**: May require system libraries. Visit [TA-Lib installation guide](https://github.com/TA-Lib/ta-lib-python) for platform-specific instructions.
- **MetaTrader5**: Requires MetaTrader 5 platform to be installed.
- **Interactive Brokers API**: Requires TWS or IB Gateway to be running.

## 📁 Project Structure

```
Algotrading_Basics/
├── Backtest_KPIs/          # Backtesting key performance indicators
├── Interactive_Brokers/     # IB API implementations
│   ├── Basics_IBAPI/        # Basic IB API examples
│   ├── Backtesting/         # Backtesting strategies
│   ├── KPIs_IBAPI/          # Performance metrics
│   ├── OOP/                 # Object-oriented examples
│   └── TA_IBAPI/            # Technical indicators
├── MT5/                     # MetaTrader 5 scripts
├── Strategies/              # Trading strategies
├── TA/                      # Technical analysis indicators
├── Values_Investing/        # Value investing strategies
├── Web Scraping/            # Web scraping utilities
├── requirements.txt         # Python dependencies
└── README.md               # This file
```

## 💻 Usage Examples

### Running a Strategy

```bash
python Strategies/Backtesting_Strategy_1.py
```

### Using Interactive Brokers API

Make sure TWS or IB Gateway is running, then:

```bash
python Interactive_Brokers/Basics_IBAPI/ibapi_basic_app.py
```

### Technical Analysis

```bash
python TA/MACD.py
```

## 🔧 Virtual Environment Management

### Deactivating the Virtual Environment

When you're done working:

```bash
deactivate
```

### Reactivating the Virtual Environment

To resume work:

```bash
source venv/bin/activate  # macOS/Linux
# or
venv\Scripts\activate     # Windows
```

### Updating Dependencies

If `requirements.txt` is updated:

```bash
pip install --upgrade -r requirements.txt
```

## 📝 Notes

- The `quant/` directory (if present) is a virtual environment and is ignored by git
- Always activate your virtual environment before running scripts
- API keys and sensitive information should be stored in `.env` files (not committed to git)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is open source and available under the MIT License.

## 👤 Author

**Faiz Memon**
- Email: fcoc444@gmail.com
- GitHub: [@Faiz9771](https://github.com/Faiz9771)

## ⚠️ Disclaimer

This software is for educational purposes only. Trading involves risk, and past performance does not guarantee future results. Always test strategies thoroughly before using real money.

