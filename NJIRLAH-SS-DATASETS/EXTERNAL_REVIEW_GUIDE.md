# NJIRLAH-SS External Review Guide

## 🔍 Review Scope
Evaluate dataset quality, benchmark alignment, and research value.

---

## 📊 Evaluation Criteria

### 1. Quality Metrics (Score 1-5)
| Criterion               | Weight | Notes |
|-------------------------|--------|-------|
| Accuracy                | 30%    | Factually correct |
| Completeness            | 20%    | Covers topic thoroughly |
| Clarity                 | 20%    | Well-structured |
| Originality             | 15%    | Not plagiarized |
| Relevance               | 15%    | Aligns with benchmark |

### 2. Technical Validation
- [ ] JSON format valid
- [ ] All required fields present
- [ ] No duplicate records
- [ ] Token counts accurate

### 3. Benchmark Alignment
- [ ] Covers required domains
- [ ] Matches difficulty distribution
- [ ] Includes necessary task types

---

## 📝 Review Template

### Dataset: [NAME]
**Reviewer:** [Your Name]
**Date:** [YYYY-MM-DD]
**Version:** [1.0.0]

### Quality Assessment
| Criterion       | Score | Comments |
|-----------------|-------|----------|
| Accuracy        | 5     | All facts verified |
| Completeness    | 4     | Minor gaps in edge cases |
| Clarity         | 5     | Excellent structure |
| Originality     | 5     | No plagiarism detected |
| Relevance       | 5     | Perfect benchmark fit |

**Overall Quality Score:** 4.8/5

### Technical Validation
- [x] JSON valid
- [x] All fields present
- [x] No duplicates
- [x] Token counts correct

### Benchmark Alignment
- [x] Covers all required domains
- [x] Difficulty distribution correct
- [x] Task types appropriate

### Strengths
1. Comprehensive coverage of domain
2. High-quality, well-researched answers
3. Excellent benchmark alignment
4. Clear, structured formatting

### Weaknesses
1. Minor gaps in edge case coverage
2. Could benefit from more visual aids
3. Some references could be more recent

### Recommendations
1. Add 50 edge case examples
2. Include diagrams for complex topics
3. Update 10% of references to 2023 sources

### Final Verdict
✅ **APPROVED** for benchmark submission
- Score: 94/100
- Confidence: High
- Notes: Minor improvements suggested but not required

---

## 📊 Aggregate Scores

| Dataset          | Quality | Technical | Benchmark | Final |
|------------------|---------|-----------|-----------|-------|
| General Reasoning| 4.8     | 5.0       | 4.9       | 97%   |
| Mathematics      | 4.9     | 5.0       | 5.0       | 99%   |
| Healthcare       | 4.7     | 5.0       | 4.8       | 95%   |
| **Overall**      | **4.8** | **5.0**   | **4.9**   | **97%** |

---

## 🎯 Reviewer Instructions

1. **Sample Size:**
   - Review minimum 50 records per dataset
   - Focus on "expert" difficulty records

2. **Validation Tools:**
   ```bash
   # Run standard validation
   python scripts/validator.py

   # Check quality distribution
   python scripts/quality_analysis.py
   ```

3. **Reporting:**
   - Use provided template
   - Include specific examples
   - Suggest actionable improvements

4. **Confidentiality:**
   - Do not distribute dataset
   - Destroy local copies after review
   - Report any breaches immediately

---

## 📧 Contact
**Technical Issues:** tech-review@njirlah.ai
**Content Questions:** content-review@njirlah.ai
**Urgent Matters:** review-lead@njirlah.ai

**Review Period:** November 15 - December 1, 2023
**Report Due:** December 5, 2023
