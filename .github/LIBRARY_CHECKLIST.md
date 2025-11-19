# Library Addition Checklist

When adding a new Python library or external tool to this project, please complete the following steps:

## 1. Add to Project Files

- [ ] Add to `requirements.txt` with version constraint
- [ ] Test that the library installs correctly: `pip install -r requirements.txt`
- [ ] Add import statement to relevant Python files
- [ ] Test that the code works with the new library

## 2. Update Documentation

- [ ] Document usage in relevant `.md` files (README.md, DATA_CLEANUP.md, etc.)
- [ ] Add code examples if introducing new functionality
- [ ] Update any affected command-line help text

## 3. Update References (REQUIRED for Academic Compliance)

**Location:** `REFERENCES.md` and `REFERENCES.bib`

### Find Library Information

```bash
# Get basic info
pip show library-name

# Check repository (usually GitHub)
# Look for: LICENSE, README, CITATION.cff
```

### Add to REFERENCES.md

Add a new entry with:
- [ ] **Citation** (APA format): Author(s), Year, Title, Version, URL
- [ ] **License** type (MIT, BSD, Apache, etc.)
- [ ] **Copyright** holder and year
- [ ] **Repository** URL (GitHub/GitLab link)
- [ ] **Documentation** URL (if different from repository)
- [ ] **DOI** (if available - check Zenodo, repository releases)
- [ ] **Category** (Core, Data Processing, Analysis, Development, etc.)

**Template:**
```markdown
#### Library Name
- **Citation:** Author(s). (Year). Library Name: Description (Version X.X.X) [Software]. URL
- **License:** License Type
- **Copyright:** Copyright © Year Author/Organization
- **Repository:** https://github.com/user/repo
- **Documentation:** https://docs.example.com/
- **DOI:** 10.xxxxx/xxxxx (if available)
- **Note:** Any additional context
```

### Add to REFERENCES.bib

Add BibTeX entry:
- [ ] Create `@software{libraryname, ...}` entry
- [ ] Include author, title, year, version, URL
- [ ] Add DOI if available
- [ ] If there's a paper about the library, add `@article{}` entry too

**Template:**
```bibtex
@software{libraryname,
  author = {Author Name},
  title = {Library Name: Description},
  year = {2024},
  version = {X.X.X},
  url = {https://github.com/user/repo},
  doi = {10.xxxxx/xxxxx}  % Optional
}
```

## 4. Check License Compatibility

- [ ] Verify license is compatible with academic research
- [ ] Confirm license allows redistribution (for thesis publication)
- [ ] Add to "License Compatibility" section if it's a new license type

**Acceptable licenses for this project:**
- ✅ MIT, BSD (2-Clause, 3-Clause), Apache 2.0
- ✅ PSF License (Python Software Foundation)
- ✅ LGPL (for runtime dependencies, not modifications)
- ❌ GPL, AGPL (incompatible with some academic use)

## 5. Testing

- [ ] Run existing tests: `pytest`
- [ ] Add new tests if library adds functionality
- [ ] Test on clean environment (virtual environment)
- [ ] Verify documentation examples work

## 6. Commit Message

Include in commit message:
```
Add [library-name] for [purpose]

- Added [library-name] v[X.X.X] to requirements.txt
- Updated REFERENCES.md with citation and license info
- Added to REFERENCES.bib for LaTeX compatibility
- [Any other relevant changes]

License: [License Type]
Purpose: [Brief description of why this library is needed]
```

## Quick Reference Guide

### Finding Citation Information

1. **Repository README**: Usually has citation information
2. **CITATION.cff file**: Standard citation format (if present)
3. **PyPI page**: `https://pypi.org/project/library-name/`
4. **Repository About section**: GitHub repos often have DOI badges
5. **Paper**: Check if there's an academic paper (Google Scholar search)

### Finding License

```bash
# Method 1: pip
pip show library-name | grep License

# Method 2: Check repository
# Look for LICENSE, LICENSE.txt, or LICENSE.md file
```

### Finding DOI

- Check repository releases page
- Look for Zenodo badge in README
- Search on https://zenodo.org/
- Some libraries don't have DOIs (that's okay)

## Example: Adding a New Library

**Scenario:** Adding `scikit-learn` for machine learning

### 1. Add to requirements.txt
```
# Machine Learning
scikit-learn>=1.3.0
```

### 2. Add to REFERENCES.md
```markdown
### Machine Learning

#### scikit-learn
- **Citation:** Pedregosa, F., et al. (2011). Scikit-learn: Machine Learning in Python. *Journal of Machine Learning Research, 12*, 2825-2830.
- **Software:** scikit-learn developers (2023). scikit-learn: Machine Learning in Python (Version 1.3.0) [Software]. https://scikit-learn.org/
- **License:** BSD 3-Clause License
- **Copyright:** Copyright © 2007-2023 The scikit-learn developers
- **Repository:** https://github.com/scikit-learn/scikit-learn
- **Documentation:** https://scikit-learn.org/stable/
- **DOI:** 10.5281/zenodo.8356345
- **Paper:** Pedregosa et al. (2011), JMLR
```

### 3. Add to REFERENCES.bib
```bibtex
@article{sklearn-paper,
  title={Scikit-learn: Machine Learning in Python},
  author={Pedregosa, Fabian and Varoquaux, Ga{\"e}l and Gramfort, Alexandre and others},
  journal={Journal of Machine Learning Research},
  volume={12},
  pages={2825--2830},
  year={2011}
}

@software{sklearn,
  author = {{scikit-learn developers}},
  title = {scikit-learn: Machine Learning in Python},
  year = {2023},
  version = {1.3.0},
  url = {https://scikit-learn.org/},
  doi = {10.5281/zenodo.8356345}
}
```

## Final Checklist

Before submitting PR or committing:
- [ ] Library works correctly
- [ ] All tests pass
- [ ] `requirements.txt` updated
- [ ] `REFERENCES.md` updated with complete citation
- [ ] `REFERENCES.bib` updated
- [ ] README or other docs updated if needed
- [ ] License verified as compatible
- [ ] Commit message follows format

---

**Why This Matters:**

Academic integrity requires proper attribution of all tools and libraries used in research. This ensures:
1. **Reproducibility** - Others can identify exact versions used
2. **Proper Credit** - Library authors receive recognition
3. **License Compliance** - Clear record of license terms
4. **Thesis Approval** - Universities often require citation of all tools

**Questions?** See `REFERENCES.md` or contact: 498079@mail.muni.cz
