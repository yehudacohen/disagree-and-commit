# 👋 START HERE

Welcome to the AWS Executive Panel Discussion POC!

---

## 🎯 What Is This?

An agentic program that simulates a panel discussion between three AWS executives:
- **Jeff Barr** (pragmatic builder)
- **Swami Sivasubramanian** (eternal optimist)  
- **Werner Vogels** (brutally direct technologist)

They debate your problem through 4 rounds, each bringing their unique personality and expertise.

---

## ⚡ Quick Start (3 Commands)

```bash
# 1. Setup
./setup.sh && source venv/bin/activate

# 2. Test
python test_credentials.py

# 3. Run
python panel_discussion.py "Should we use serverless or containers?"
```

**That's it!** Watch the debate unfold in your terminal.

---

## 📚 Where to Go Next

### First Time Here?
→ **[QUICK_START.md](QUICK_START.md)** - 5-minute setup guide

### Want to Understand How It Works?
→ **[ROUNDS_EXPLAINED.md](ROUNDS_EXPLAINED.md)** - Detailed explanation of each round

### Need Help?
→ **[TROUBLESHOOTING.md](TROUBLESHOOTING.md)** - Common issues and solutions

### Looking for Everything?
→ **[INDEX.md](INDEX.md)** - Complete documentation index

### Ready to Use It?
→ **[PROJECT_COMPLETE.md](PROJECT_COMPLETE.md)** - Full project summary

---

## 🎭 The 4 Rounds

1. **Initial Opinions** - Each panelist shares their approach
2. **Disagreements** - They challenge each other's ideas
3. **Personal Callouts** - Personalities shine through
4. **Disagree and Commit** - They commit to one solution

---

## 💡 Try These Problems

```bash
# Architecture
python panel_discussion.py "Should we use serverless or containers?"

# Migration
python panel_discussion.py "How do we migrate to microservices?"

# AI Strategy
python panel_discussion.py "How should we integrate AI agents?"

# Database
python panel_discussion.py "SQL or NoSQL for our new app?"
```

---

## ✅ Requirements

- Python 3.8+
- AWS account with Bedrock access
- Claude Sonnet 4.5 enabled
- AWS profile named `scratchspace`

---

## 🚀 You're Ready!

Run this now:
```bash
./setup.sh
source venv/bin/activate
python test_credentials.py
python panel_discussion.py "Your problem here"
```

Enjoy the debate! 🎉
