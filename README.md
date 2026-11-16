<p align="center">
  <img src="assets/banner.svg" alt="Bala Nambi, quant developer in training: ML for trading, execution systems, cloud data pipelines" width="100%">
</p>

<p align="center">
  <a href="https://www.linkedin.com/in/balanambi/"><img src="https://img.shields.io/badge/LinkedIn-balanambi-0A66C2?style=flat-square&logo=linkedin&logoColor=white" alt="LinkedIn"></a>
  <img src="https://img.shields.io/badge/42-Paris-111827?style=flat-square&logo=42&logoColor=white" alt="42 Paris">
  <img src="https://img.shields.io/badge/Goal-quant%20developer%20·%202027-0f766e?style=flat-square" alt="Goal: quant developer by 2027">
</p>

### About

I build the full loop of a systematic trading idea: capture the data, state the hypothesis before
looking at results, test it honestly after costs, and run it on infrastructure I set up myself.

- **Now:** student at 42 Paris (AI track: Python, C), moving into **C++ and Rust** for low-latency work.
- **Research style:** pre-registered hypotheses, frozen contracts, sealed test sets, results reported even when they say "no edge".
- **Before 42:** systems analyst at Allianz (AGCS), then a decade in business development and web project management; MBA.
- **Community:** community manager at 42 AI.

### Featured work

<table>
<tr>
<td width="50%" valign="top">

<b><a href="https://github.com/balasbrn/llm-veto-distillation">llm-veto-distillation</a></b><br>
Can a 3 ms model copy an LLM's trade veto, and is the veto worth copying? Students reach κ ≈ 0.4–0.5 against a Gemini teacher, and the project keeps "copies the teacher" apart from "makes money".<br>
<sub>Python · scikit-learn · Vertex AI · triple-barrier labels</sub>

</td>
<td width="50%" valign="top">

<b><a href="https://github.com/balasbrn/ATR_breakout_strategy">ATR_breakout_strategy</a></b><br>
One volatility-breakout idea tested across US stocks, NSE, crypto and FX/gold, with a frozen, versioned contract: gross edge first, then after costs.<br>
<sub>Python · pre-registration · transaction costs · multi-market</sub>

</td>
</tr>
<tr>
<td width="50%" valign="top">

<b><a href="https://github.com/balasbrn/llm-compression-lab-notes">llm-compression-lab-notes</a></b><br>
Pruning, distillation and serving benchmarks on Llama 3.2 3B: ~20% fewer parameters with throughput and latency gains. NVIDIA DLI assessment 100/100.<br>
<sub>NAS pruning · knowledge distillation · inference benchmarking</sub>

</td>
<td width="50%" valign="top">

<b><a href="https://github.com/balasbrn/google-cloud-ace-study">google-cloud-ace-study</a></b><br>
Public study log for the Google Cloud Associate Cloud Engineer exam: decision tables, commands, AWS comparisons and tracked weak spots.<br>
<sub>GCP · IAM · GCS · Compute Engine</sub>

</td>
</tr>
</table>

<details>
<summary><b>In the lab</b>: private research systems, being prepared for public release</summary>
<br>

| Project | What it does | Stack |
|---|---|---|
| Unified Quant Platform | Multi-broker data ingestion (IBKR, cTrader, Zerodha, Bybit) into a leak-checked data lake, pluggable signal modules and paper-only shadow tracking | Python, Polars, DuckDB, BigQuery |
| Execution research workspace | cTrader cBots and IBKR paper trading, with baselines kept separate from experiments | C#, Python, IBKR |
| Stock shadow bot | Single-stock paper bot on a 15-minute Cloud Run schedule, with IBKR execution, econometric features and log telemetry | Python, Cloud Run, IBKR |
| OHLCV research assistant | Validated bar data, deterministic signals, optional FinBERT sentiment, vectorised backtests | Python, pandas, PyTorch |
| Trade storyboard | Per-stock trade-study dashboard for exploring high-frequency study events | React, Vite, TypeScript |
| C library from scratch ([libft](https://github.com/balasbrn/library-functions-in-C)) | 42 core project: libc, memory, string and linked-list functions | C |

</details>

### Stack

<p>
  <img src="https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/C-A8B9CC?style=flat-square&logo=c&logoColor=black" alt="C">
  <img src="https://img.shields.io/badge/C%23-512BD4?style=flat-square&logo=dotnet&logoColor=white" alt="C#">
  <img src="https://img.shields.io/badge/TypeScript-3178C6?style=flat-square&logo=typescript&logoColor=white" alt="TypeScript">
  <img src="https://img.shields.io/badge/C%2B%2B-learning-00599C?style=flat-square&logo=cplusplus&logoColor=white" alt="C++ (learning)">
  <img src="https://img.shields.io/badge/Rust-learning-000000?style=flat-square&logo=rust&logoColor=white" alt="Rust (learning)">
  <br>
  <img src="https://img.shields.io/badge/pandas-150458?style=flat-square&logo=pandas&logoColor=white" alt="pandas">
  <img src="https://img.shields.io/badge/Polars-CD792C?style=flat-square&logo=polars&logoColor=white" alt="Polars">
  <img src="https://img.shields.io/badge/DuckDB-FFF000?style=flat-square&logo=duckdb&logoColor=black" alt="DuckDB">
  <img src="https://img.shields.io/badge/scikit--learn-F7931E?style=flat-square&logo=scikitlearn&logoColor=white" alt="scikit-learn">
  <img src="https://img.shields.io/badge/PyTorch-EE4C2C?style=flat-square&logo=pytorch&logoColor=white" alt="PyTorch">
  <br>
  <img src="https://img.shields.io/badge/Google%20Cloud-4285F4?style=flat-square&logo=googlecloud&logoColor=white" alt="Google Cloud">
  <img src="https://img.shields.io/badge/Vertex%20AI-4285F4?style=flat-square&logo=googlecloud&logoColor=white" alt="Vertex AI">
  <img src="https://img.shields.io/badge/Oracle%20Cloud-F80000?style=flat-square&logo=oracle&logoColor=white" alt="Oracle Cloud">
  <img src="https://img.shields.io/badge/Linux-FCC624?style=flat-square&logo=linux&logoColor=black" alt="Linux">
  <img src="https://img.shields.io/badge/Docker-2496ED?style=flat-square&logo=docker&logoColor=white" alt="Docker">
  <img src="https://img.shields.io/badge/GitHub%20Actions-2088FF?style=flat-square&logo=githubactions&logoColor=white" alt="GitHub Actions">
  <br>
  <img src="https://img.shields.io/badge/cTrader-1f2937?style=flat-square" alt="cTrader">
  <img src="https://img.shields.io/badge/Interactive%20Brokers-D71920?style=flat-square" alt="Interactive Brokers">
  <img src="https://img.shields.io/badge/Kraken%20tick%20data-5741D9?style=flat-square" alt="Kraken tick data">
</p>

### Certifications

| | Certification | Status |
|---|---|---|
| <img src="https://img.shields.io/badge/-NVIDIA-76B900?style=flat-square&logo=nvidia&logoColor=white" alt="NVIDIA"> | **The Art of Compressing LLMs**: pruning, distillation and quantization (DLI Certificate of Competency) | Nov 2026 · 100/100 · [verify](https://learn.nvidia.com/certificates?id=5GdXy5BkQyKAFXkroo0lyw) |
| <img src="https://img.shields.io/badge/-Google%20Cloud-4285F4?style=flat-square&logo=googlecloud&logoColor=white" alt="Google Cloud"> | **Associate Cloud Engineer** | In progress · [study log](https://github.com/balasbrn/google-cloud-ace-study) |

### Activity

<p>
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="assets/generated/stats-dark.svg">
    <img src="assets/generated/stats-light.svg" alt="Contribution stats for the last 12 months" width="49%">
  </picture>
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="assets/generated/languages-dark.svg">
    <img src="assets/generated/languages-light.svg" alt="Most used languages by code size" width="49%">
  </picture>
</p>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/generated/activity-dark.svg">
  <img src="assets/generated/activity-light.svg" alt="Contribution calendar for the last 12 months" width="100%">
</picture>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/generated/snake-dark.svg">
  <img src="assets/generated/snake-light.svg" alt="Snake eating the contribution graph" width="100%">
</picture>

<sub>Cards are rendered daily by a GitHub Action in this repo (<code>scripts/build_cards.py</code>) and served from it, with no third-party stats service.</sub>
