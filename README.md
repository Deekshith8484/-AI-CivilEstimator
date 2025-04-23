# -AI-CivilEstimator
CivilEstimator-KA is an AI-based estimation engine built using Karnataka SOR data. It takes construction item descriptions and dimensional inputs (L × B × D) and returns full BOQ-style cost breakdowns, including unit rate, total cost, and optional profit margins.
# 🏗️ AI Civil Estimator (Karnataka SOR)

**AI Civil Estimator** is an intelligent, BOQ-style construction estimation engine that uses **Karnataka Public Works Department (KPWD)** Schedule of Rates (SOR) data to calculate detailed project costs. Built using a combination of **AI**, **vector search**, and **real government data**, this tool allows engineers, contractors, and project estimators to generate precise cost estimates based on actual input dimensions.

---

### 🎯 Features

- 🧠 **AI-powered natural language understanding**
  - Accepts queries like “RCC M20 slab 12m x 0.9m x 0.9m”
- 🔍 **Smart retrieval from Karnataka SOR**
  - Uses semantic search or vector similarity to find item codes
- 🧮 **Dimension-based quantity calculations**
  - Supports Length × Breadth × Depth or Area logic
- 💰 **Auto-calculated BOQ output with profit**
  - Final estimate with configurable profit margin
- 📤 **Export-ready output**
  - Compatible with Excel or printable BOQ sheets

---

### 🧪 Sample Input

```plaintext
Item: RCC M20 for slab
Length: 12m
Breadth: 0.9m
Depth: 0.9m
Profit Margin: 15%
