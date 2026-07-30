# Data Card — Crypto / On-Chain: Etherscan / CoinGecko / DeFiLlama

**Provider & what it is.** Three free (freemium) sources that, together, let you study crypto markets and the blockchains underneath them — the kind of data that *did not exist a decade ago*, which is itself a flavor of research novelty (Ch 7.1). **Etherscan** is the dominant block explorer for the Ethereum blockchain; its API serves *on-chain* data — individual transactions, token transfers (ERC-20/ERC-721), account balances, contract events, and gas — keyed by wallet/contract **address** and block. This is the ground truth of what actually happened on-chain, timestamped to the block. **CoinGecko** is a market-data aggregator: prices, market capitalization, trading volume, and supply for thousands of coins and tokens across exchanges, plus historical OHLC series — the *price* layer. **DeFiLlama** tracks **TVL** (Total Value Locked) — the dollar value of assets deposited in decentralized-finance protocols — by protocol and chain, the standard measure of "how big is this DeFi thing." The reveal: on-chain data is *transparent and timestamped to the second*, which gives you cleaner event timing than almost any traditional finance dataset — but it is also pseudonymous, noisy, and full of wash trading and bots, so the cleaning is where the real work (and the measurement error) lives.

**Coverage.** Etherscan: the full Ethereum mainnet history (2015–present) and, via sister explorers (Polygonscan, BscScan, etc.) other EVM chains; transaction-level. CoinGecko: thousands of assets, daily history back to each coin's listing (and intraday for recent windows). DeFiLlama: hundreds of protocols across dozens of chains, daily TVL history since each protocol launched. All update continuously — pin a snapshot.

**Key identifiers.** The **address** — a 42-character hex string beginning `0x` (e.g., `0xA0b8...`), used for both wallets and contracts; addresses are *pseudonymous*, not identities. A **transaction hash** (`0x...`, 66 chars) uniquely identifies a transaction; a **block number** orders everything in time. CoinGecko uses its own **coin id** (a slug like `ethereum`, `usd-coin`) and contract addresses; DeFiLlama uses a **protocol slug** and chain name. To join price (CoinGecko) to on-chain activity (Etherscan), map the token's contract address to its CoinGecko id and align on timestamp.

**Access path.** Free tiers everywhere; keys via environment variables, never hard-coded (CONVENTIONS §5):

```python
import os, requests

# Etherscan — free API key from the environment
es_key = os.environ["ETHERSCAN_API_KEY"]
r = requests.get("https://api.etherscan.io/api",
                 params={"module": "account", "action": "tokentx",
                         "contractaddress": "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",  # token
                         "page": 1, "offset": 100, "sort": "asc",
                         "apikey": es_key}, timeout=60)

# CoinGecko — free tier needs no key; the Demo/Pro tier reads a key from the env
cg_headers = {"x-cg-demo-api-key": os.environ.get("COINGECKO_API_KEY", "")}
px = requests.get("https://api.coingecko.com/api/v3/coins/usd-coin/market_chart",
                  params={"vs_currency": "usd", "days": "90"},
                  headers=cg_headers, timeout=60).json()

# DeFiLlama — open, no key
tvl = requests.get("https://api.llama.fi/protocol/uniswap", timeout=60).json()
```

**License & note.** These are *API terms of service*, not open-data licenses, and they vary. Etherscan and CoinGecko free tiers permit non-commercial/research use with attribution and forbid resale of the raw feed; DeFiLlama is open with attribution `[CHECK exact license/attribution for each provider`. The underlying *blockchain* data is itself public, but the convenient API packaging is the provider's service — so cache for your own reproducibility, cite the provider and access date, and do not republish the raw API responses as "your dataset."

**Gotchas.**
- **Pseudonymity ≠ identity.** One person can control many addresses; one address can be a shared exchange wallet. Treating an address as a "user" is a strong assumption — name it (a measurement issue, Ch 1.3).
- **Wash trading and bots.** A large share of reported DEX volume can be self-trades and MEV/arbitrage bots, inflating "volume." If your outcome is volume (Devon's is), this is the central data-quality threat — discuss it.
- **Timestamps: block time vs. UTC.** On-chain events are ordered by block; map block → timestamp carefully and decide your event window in a single, stated time zone. Reorgs (rare) can reshuffle very recent blocks.
- **TVL is a price-times-quantity artifact.** DeFiLlama TVL moves when *token prices* move even if no deposits change, and methodologies differ across protocols (double-counting via wrapped/staked tokens). Read the protocol's TVL definition before using it as a "size" variable.
- **Rate limits and pagination.** Etherscan free is on the order of a few calls per second with a daily cap; CoinGecko free is a modest per-minute limit `[CHECK exact limits]`. You must paginate large pulls and back off on errors, or you get throttled.
- **Survivorship in token lists.** Dead/rugged tokens disappear from convenient lists — the same survivorship trap as the equity APIs.

**First 10 rows — schema sketch (illustrative; values invented, not real on-chain records).**

| block_number | timestamp_utc | tx_hash | from_addr | to_addr | token_symbol | value_token | usd_price | source |
|---|---|---|---|---|---|---|---|---|
| 18500001 | 2023-11-01T00:00:11Z | 0x9f1a... | 0xAa01... | 0xBb02... | USDC | 25000.00 | 0.9998 | etherscan |
| 18500002 | 2023-11-01T00:00:23Z | 0x7c3d... | 0xCc03... | 0xDd04... | USDC | 12000.00 | 0.9997 | etherscan |
| 18500004 | 2023-11-01T00:00:59Z | 0x4e5f... | 0xEe05... | 0xFf06... | DAI | 8000.00 | 1.0001 | etherscan |
| 18500009 | 2023-11-01T00:02:11Z | 0x1a2b... | 0x1107... | 0x2208... | USDC | 500000.00 | 0.9985 | etherscan |
| — | 2023-11-01T00:00:00Z | — | — | — | USDC | — | 0.9998 | coingecko |
| — | 2023-11-01T01:00:00Z | — | — | — | USDC | — | 0.9971 | coingecko |
| — | 2023-11-01T02:00:00Z | — | — | — | USDC | — | 0.9990 | coingecko |
| — | 2023-11-01 | — | — | — | — | — | — | defillama (uniswap TVL=4.21e9) |
| — | 2023-11-02 | — | — | — | — | — | — | defillama (uniswap TVL=4.08e9) |
| — | 2023-11-03 | — | — | — | — | — | — | defillama (uniswap TVL=4.15e9) |

(Note the brief dip below \$1.00 in the CoinGecko price column — the kind of depeg moment Devon's event study is built around.)

**Which chapter/lab/capstone uses it.** This is **Devon's** data. His Ch 7.1 worked example — *when an ERC-20 stablecoin loses its dollar peg by more than 5%, how does same-day DEX trading volume respond?* — is an **event study** (Ch 4.2) keyed on the on-chain depeg timestamp: outcome = log daily DEX volume, treatment = depeg-event indicator, window `[-30, +5]` days, unit = stablecoin × day, data = **Etherscan + CoinGecko** (Ch 7.1 cast table and §worked-example-A). The crypto/FinTech thread runs through **Weeks 6–7** (text and on-chain data as new-data novelty) and feeds a crypto **capstone**. You acquire and document it in **Ch 7.2 / Lab 7** with the reproducible-pull discipline: pin the snapshot, cache the raw API responses (essential here, since the live chain keeps growing), log every request, and disclose the wash-trading and pseudonymity caveats in your data card.
