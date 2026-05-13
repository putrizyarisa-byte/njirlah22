# Contributing to NJIRLAH-SS

We welcome contributions! Here's how you can help:

---

## 📋 How to Contribute

### 1. Reporting Issues
- Use GitHub Issues
- Include:
  - Dataset number
  - Record ID (if specific)
  - Description of problem
  - Suggested fix (if any)

### 2. Adding Records
1. Fork the repository
2. Create new records in `raw/` following template
3. Run validation:
   ```bash
   python scripts/validator.py
   ```
4. Submit PR with description of changes

### 3. Improving Quality
- Fix grammatical errors
- Add references/citations
- Improve answer structure
- Add visual aids where helpful

---

## 🔧 Development Setup

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run tests
pytest tests/
```

---

## 📝 Guidelines

### Content Standards
- **Accuracy:** Verified from reputable sources
- **Clarity:** Well-structured, logical flow
- **Depth:** Sufficient detail for domain
- **Originality:** No plagiarism

### Format Requirements
- JSONL format
- All required fields present
- Quality score ≥ 0.90
- No duplicates

### Benchmark Alignment
- Follow benchmark-specific guidelines
- Include required task types
- Maintain difficulty distribution

---

## 🎯 Review Process

1. **Automated Checks:**
   - JSON validation
   - Quality score
   - Duplicate detection

2. **Manual Review:**
   - Domain expert review
   - Benchmark alignment
   - Answer quality

3. **Merge Criteria:**
   - ✅ Passes all automated checks
   - ✅ Approved by 2 reviewers
   - ✅ No breaking changes

---

## 🏆 Recognition

Contributors will be:
- Added to CONTRIBUTORS.md
- Acknowledged in release notes
- Invited to NJIRLAH AI community events

---

## 🤝 Code of Conduct

Be respectful, collaborative, and constructive.

---

**Questions?** Open an issue or email contribute@njirlah.ai
