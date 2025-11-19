# References and Citations

This document provides academic references for all third-party libraries, tools, and sources used in this project. This file should be updated whenever new dependencies are added.

**Last Updated:** 2025-01-19

---

## Table of Contents

1. [Core Dependencies](#core-dependencies)
2. [Data Processing Libraries](#data-processing-libraries)
3. [Analysis and Visualization](#analysis-and-visualization)
4. [Development Tools](#development-tools)
5. [Python Language](#python-language)
6. [Citation Formats](#citation-formats)
7. [Updating This File](#updating-this-file)

---

## Core Dependencies

### HTTP and Web Scraping

#### Requests
- **Citation:** Reitz, K. (2023). Requests: HTTP for Humans (Version 2.31.0) [Software]. Python Software Foundation. https://requests.readthedocs.io/
- **License:** Apache License 2.0
- **Copyright:** Copyright 2019 Kenneth Reitz
- **Repository:** https://github.com/psf/requests
- **Documentation:** https://requests.readthedocs.io/

#### HTTPX
- **Citation:** Encode (2023). HTTPX: A next-generation HTTP client for Python (Version 0.25.0) [Software]. https://www.python-httpx.org/
- **License:** BSD 3-Clause License
- **Copyright:** Copyright © 2019-present, Encode OSS Ltd.
- **Repository:** https://github.com/encode/httpx
- **Documentation:** https://www.python-httpx.org/

#### Beautiful Soup 4
- **Citation:** Richardson, L. (2023). Beautiful Soup: A Python library for pulling data out of HTML and XML files (Version 4.12.0) [Software]. https://www.crummy.com/software/BeautifulSoup/
- **License:** MIT License
- **Copyright:** Copyright © 2004-2023 Leonard Richardson
- **Repository:** https://bazaar.launchpad.net/~leonardr/beautifulsoup/bs4/files
- **Documentation:** https://www.crummy.com/software/BeautifulSoup/bs4/doc/

#### lxml
- **Citation:** Behnel, S., et al. (2023). lxml: XML and HTML with Python (Version 4.9.0) [Software]. https://lxml.de/
- **License:** BSD 3-Clause License
- **Copyright:** Copyright © 2004-2023 Infrae
- **Repository:** https://github.com/lxml/lxml
- **Documentation:** https://lxml.de/

#### urllib3
- **Citation:** urllib3 contributors (2023). urllib3: HTTP client for Python (Version 2.0.0) [Software]. https://urllib3.readthedocs.io/
- **License:** MIT License
- **Copyright:** Copyright © 2008-2023 Andrey Petrov and contributors
- **Repository:** https://github.com/urllib3/urllib3
- **Documentation:** https://urllib3.readthedocs.io/

---

## Data Processing Libraries

### PDF Processing

#### PDFPlumber
- **Citation:** Singer, J. (2023). pdfplumber: Plumb a PDF for detailed information about each char, rectangle, line, et cetera (Version 0.9.0) [Software]. https://github.com/jsvine/pdfplumber
- **License:** MIT License
- **Copyright:** Copyright © 2023 Jeremy Singer-Vine
- **Repository:** https://github.com/jsvine/pdfplumber
- **Documentation:** https://github.com/jsvine/pdfplumber

#### PDFMiner.six
- **Citation:** Shinyama, Y., & Goulu (2023). PDFMiner.six: Community maintained fork of pdfminer [Software]. https://github.com/pdfminer/pdfminer.six
- **License:** MIT License
- **Copyright:** Copyright © 2004-2023 Yusuke Shinyama & contributors
- **Repository:** https://github.com/pdfminer/pdfminer.six
- **Note:** Dependency of pdfplumber

### Configuration and Data Handling

#### PyYAML
- **Citation:** PyYAML contributors (2023). PyYAML: YAML parser and emitter for Python (Version 6.0.1) [Software]. https://pyyaml.org/
- **License:** MIT License
- **Copyright:** Copyright © 2017-2023 Ingy döt Net, Copyright © 2006-2016 Kirill Simonov
- **Repository:** https://github.com/yaml/pyyaml
- **Documentation:** https://pyyaml.org/wiki/PyYAMLDocumentation

#### pandas
- **Citation:** McKinney, W., & pandas development team (2023). pandas: Powerful data structures for data analysis, time series, and statistics (Version 2.1.0) [Software]. Zenodo. https://doi.org/10.5281/zenodo.3509134
- **License:** BSD 3-Clause License
- **Copyright:** Copyright © 2008-2023, AQR Capital Management, LLC, Lambda Foundry, Inc. and PyData Development Team
- **Repository:** https://github.com/pandas-dev/pandas
- **Documentation:** https://pandas.pydata.org/
- **DOI:** 10.5281/zenodo.3509134

#### JSONLines
- **Citation:** Delano, D. (2023). jsonlines: A Python library for reading and writing JSON lines (Version 4.0.0) [Software]. https://github.com/wbolster/jsonlines
- **License:** BSD 3-Clause License
- **Copyright:** Copyright © 2023 wouter bolsterlee
- **Repository:** https://github.com/wbolster/jsonlines

### Utilities

#### tqdm
- **Citation:** da Costa-Luis, C., et al. (2023). tqdm: A Fast, Extensible Progress Bar for Python and CLI (Version 4.66.0) [Software]. Zenodo. https://doi.org/10.5281/zenodo.595120
- **License:** MIT License, Mozilla Public License 2.0
- **Copyright:** Copyright © 2013-2023 noamraph, Casper da Costa-Luis
- **Repository:** https://github.com/tqdm/tqdm
- **Documentation:** https://tqdm.github.io/
- **DOI:** 10.5281/zenodo.595120

#### tabulate
- **Citation:** Loginov, S. (2023). tabulate: Pretty-print tabular data in Python (Version 0.9.0) [Software]. https://github.com/astanin/python-tabulate
- **License:** MIT License
- **Copyright:** Copyright © 2011-2023 Sergey Astanin
- **Repository:** https://github.com/astanin/python-tabulate

#### python-dateutil
- **Citation:** Niemelä, T., & Regebro, L. (2023). python-dateutil: Extensions to the standard Python datetime module (Version 2.8.0) [Software]. https://github.com/dateutil/dateutil
- **License:** Apache License 2.0, BSD 3-Clause License (dual license)
- **Copyright:** Copyright © 2017 dateutil contributors
- **Repository:** https://github.com/dateutil/dateutil
- **Documentation:** https://dateutil.readthedocs.io/

#### chardet
- **Citation:** Pilgrim, M., & chardet contributors (2023). chardet: Universal encoding detector for Python (Version 5.2.0) [Software]. https://github.com/chardet/chardet
- **License:** LGPL 2.1
- **Copyright:** Copyright © 1998 Netscape Communications Corporation
- **Repository:** https://github.com/chardet/chardet

#### python-magic
- **Citation:** python-magic contributors (2023). python-magic: A python wrapper for libmagic (Version 0.4.27) [Software]. https://github.com/ahupp/python-magic
- **License:** MIT License
- **Copyright:** Copyright © 2001-2023 Adam Hupp
- **Repository:** https://github.com/ahupp/python-magic

#### xxHash
- **Citation:** Collet, Y. (2023). xxHash: Extremely fast hash algorithm (Version 3.4.0) [Software]. https://github.com/Cyan4973/xxHash
- **License:** BSD 2-Clause License
- **Copyright:** Copyright © 2012-2023 Yann Collet
- **Repository:** https://github.com/Cyan4973/xxHash
- **Python binding:** https://github.com/ifduyue/python-xxhash

#### coloredlogs
- **Citation:** Peeters, P. (2023). coloredlogs: Colored terminal output for Python's logging module (Version 15.0.1) [Software]. https://github.com/xolox/python-coloredlogs
- **License:** MIT License
- **Copyright:** Copyright © 2023 Peter Odding
- **Repository:** https://github.com/xolox/python-coloredlogs
- **Documentation:** https://coloredlogs.readthedocs.io/

---

## Analysis and Visualization

### Jupyter and Interactive Computing

#### Jupyter
- **Citation:** Pérez, F., & Granger, B. E. (2007). IPython: A system for interactive scientific computing. *Computing in Science & Engineering, 9*(3), 21-29. https://doi.org/10.1109/MCSE.2007.53
- **Software:** Project Jupyter (2023). Jupyter (Version 1.0.0) [Software]. https://jupyter.org/
- **License:** BSD 3-Clause License
- **Copyright:** Copyright © 2001-2023 IPython Development Team, Copyright © 2015-2023 Jupyter Development Team
- **Repository:** https://github.com/jupyter/jupyter
- **Documentation:** https://jupyter.org/documentation
- **DOI (paper):** 10.1109/MCSE.2007.53

#### JupyterLab / Notebook
- **Citation:** Kluyver, T., Ragan-Kelley, B., Pérez, F., Granger, B., Bussonnier, M., Frederic, J., ... & Willing, C. (2016). Jupyter Notebooks – a publishing format for reproducible computational workflows. In *Positioning and Power in Academic Publishing: Players, Agents and Agendas* (pp. 87-90). IOS Press. https://doi.org/10.3233/978-1-61499-649-1-87
- **License:** BSD 3-Clause License
- **Repository:** https://github.com/jupyter/notebook
- **DOI:** 10.3233/978-1-61499-649-1-87

#### IPython/IPyKernel
- **Citation:** Pérez, F., & Granger, B. E. (2007). IPython: A system for interactive scientific computing. *Computing in Science & Engineering, 9*(3), 21-29.
- **License:** BSD 3-Clause License
- **Repository:** https://github.com/ipython/ipykernel
- **DOI:** 10.1109/MCSE.2007.53

### Visualization Libraries

#### Matplotlib
- **Citation:** Hunter, J. D. (2007). Matplotlib: A 2D graphics environment. *Computing in Science & Engineering, 9*(3), 90-95. https://doi.org/10.1109/MCSE.2007.55
- **Software:** Matplotlib Development Team (2023). Matplotlib (Version 3.8.0) [Software]. https://matplotlib.org/
- **License:** Python Software Foundation License (BSD-compatible)
- **Copyright:** Copyright © 2002-2023 John Hunter, Darren Dale, Eric Firing, Michael Droettboom and the Matplotlib development team
- **Repository:** https://github.com/matplotlib/matplotlib
- **Documentation:** https://matplotlib.org/stable/index.html
- **DOI:** 10.1109/MCSE.2007.55

#### Seaborn
- **Citation:** Waskom, M. L. (2021). seaborn: statistical data visualization. *Journal of Open Source Software, 6*(60), 3021. https://doi.org/10.21105/joss.03021
- **License:** BSD 3-Clause License
- **Copyright:** Copyright © 2012-2023 Michael Waskom
- **Repository:** https://github.com/mwaskom/seaborn
- **Documentation:** https://seaborn.pydata.org/
- **DOI:** 10.21105/joss.03021

### Network Analysis

#### NetworkX
- **Citation:** Hagberg, A. A., Schult, D. A., & Swart, P. J. (2008). Exploring network structure, dynamics, and function using NetworkX. In *Proceedings of the 7th Python in Science Conference* (SciPy2008), (pp. 11-15). Pasadena, CA USA.
- **Software:** NetworkX Developers (2023). NetworkX: Network Analysis in Python (Version 3.2.0) [Software]. https://networkx.org/
- **License:** BSD 3-Clause License
- **Copyright:** Copyright © 2004-2023 NetworkX Developers
- **Repository:** https://github.com/networkx/networkx
- **Documentation:** https://networkx.org/documentation/stable/
- **Paper:** https://conference.scipy.org/proceedings/SciPy2008/paper_2/

---

## Natural Language Processing and Machine Learning

### Named Entity Recognition

#### GLiNER
- **Citation:** Zaratiana, U., Tomeh, N., Holat, P., & Charnois, T. (2024). GLiNER: Generalist Model for Named Entity Recognition using Bidirectional Transformer. In *Proceedings of the 2024 Conference of the North American Chapter of the Association for Computational Linguistics: Human Language Technologies (Volume 1: Long Papers)* (pp. 5364-5376). Association for Computational Linguistics. https://doi.org/10.18653/v1/2024.naacl-long.300
- **Software:** Zaratiana, U. (2024). GLiNER (Version 0.2.0) [Software]. https://github.com/urchade/GLiNER
- **License:** Apache License 2.0
- **Repository:** https://github.com/urchade/GLiNER
- **Models:** https://huggingface.co/urchade
- **Documentation:** https://github.com/urchade/GLiNER
- **ArXiv:** https://arxiv.org/abs/2311.08526
- **DOI:** 10.18653/v1/2024.naacl-long.300
- **Note:** Used for zero-shot extraction of organizations and persons from Czech NGO texts without requiring training data.

#### PyTorch
- **Citation:** Paszke, A., Gross, S., Massa, F., Lerer, A., Bradbury, J., Chanan, G., ... & Chintala, S. (2019). PyTorch: An imperative style, high-performance deep learning library. In *Advances in Neural Information Processing Systems* 32 (pp. 8024-8035). https://arxiv.org/abs/1912.01703
- **Software:** PyTorch Team (2024). PyTorch (Version 2.0+) [Software]. https://pytorch.org/
- **License:** BSD 3-Clause License
- **Copyright:** Copyright © 2016-2024 Facebook, Inc. (Meta Platforms)
- **Repository:** https://github.com/pytorch/pytorch
- **Documentation:** https://pytorch.org/docs/
- **Note:** Deep learning framework used by GLiNER for transformer-based entity recognition.

#### Transformers (Hugging Face)
- **Citation:** Wolf, T., Debut, L., Sanh, V., Chaumond, J., Delangue, C., Moi, A., ... & Rush, A. M. (2020). Transformers: State-of-the-art natural language processing. In *Proceedings of the 2020 Conference on Empirical Methods in Natural Language Processing: System Demonstrations* (pp. 38-45). Association for Computational Linguistics. https://doi.org/10.18653/v1/2020.emnlp-demos.6
- **Software:** Hugging Face (2024). Transformers (Version 4.38+) [Software]. https://github.com/huggingface/transformers
- **License:** Apache License 2.0
- **Copyright:** Copyright © 2018-2024 The Hugging Face team
- **Repository:** https://github.com/huggingface/transformers
- **Documentation:** https://huggingface.co/docs/transformers/
- **DOI:** 10.18653/v1/2020.emnlp-demos.6
- **Note:** Provides pre-trained multilingual transformer models (DeBERTa) used by GLiNER.

---

## Development Tools

### Testing

#### pytest
- **Citation:** Krekel, H., Oliveira, B., Pfannschmidt, R., Bruynooghe, F., Laugher, B., & Bruhin, F. (2023). pytest (Version 7.4.0) [Software]. https://pytest.org/
- **License:** MIT License
- **Copyright:** Copyright © 2004-2023 Holger Krekel and others
- **Repository:** https://github.com/pytest-dev/pytest
- **Documentation:** https://docs.pytest.org/

#### pytest-cov
- **Citation:** pytest-cov contributors (2023). pytest-cov: Coverage plugin for pytest (Version 4.1.0) [Software]. https://github.com/pytest-dev/pytest-cov
- **License:** MIT License
- **Repository:** https://github.com/pytest-dev/pytest-cov

#### responses
- **Citation:** Dropbox, Inc. (2023). responses: A utility library for mocking out the requests Python library (Version 0.24.0) [Software]. https://github.com/getsentry/responses
- **License:** Apache License 2.0
- **Copyright:** Copyright © 2015 David Cramer, Dropbox, Inc.
- **Repository:** https://github.com/getsentry/responses

### Code Quality

#### Black
- **Citation:** Langa, Ł. (2023). Black: The uncompromising Python code formatter (Version 23.11.0) [Software]. https://black.readthedocs.io/
- **License:** MIT License
- **Copyright:** Copyright © 2018-2023 Łukasz Langa and contributors
- **Repository:** https://github.com/psf/black
- **Documentation:** https://black.readthedocs.io/

#### Flake8
- **Citation:** Cordasco, I., Layman, J., & Stevens, K. (2023). Flake8: Your Tool For Style Guide Enforcement (Version 6.1.0) [Software]. https://flake8.pycqa.org/
- **License:** MIT License
- **Copyright:** Copyright © 2011-2013 Tarek Ziade, Copyright © 2012-2023 Ian Cordasco
- **Repository:** https://github.com/PyCQA/flake8
- **Documentation:** https://flake8.pycqa.org/

#### mypy
- **Citation:** Lehtosalo, J., et al. (2023). mypy: Optional static typing for Python (Version 1.7.0) [Software]. http://www.mypy-lang.org/
- **License:** MIT License
- **Copyright:** Copyright © 2015-2023 Jukka Lehtosalo and contributors
- **Repository:** https://github.com/python/mypy
- **Documentation:** https://mypy.readthedocs.io/

---

## Python Language

### Python
- **Citation:** Van Rossum, G., & Drake, F. L. (2009). *Python 3 Reference Manual*. Scotts Valley, CA: CreateSpace.
- **Software:** Python Software Foundation (2023). Python (Version 3.11) [Software]. https://www.python.org/
- **License:** Python Software Foundation License (PSFL)
- **Copyright:** Copyright © 2001-2023 Python Software Foundation
- **Website:** https://www.python.org/
- **Documentation:** https://docs.python.org/3/

---

## Research Data and Methodology

### COMPON Project
- **Citation:** COMPON Project (2024). *Comparing Policy Network Analysis Approaches: A Methodological Comparison*. Masaryk University. [Note: Update with specific citation once published]
- **Note:** This project's methodology is based on the COMPON project's approach to NGO network analysis.

### Web Scraping Ethics
- **Source:** Krotov, V., Johnson, L., & Silva, L. (2020). Legality and ethics of web scraping. *Communications of the Association for Information Systems, 47*(1), 539-563. https://doi.org/10.17705/1CAIS.04724
- **DOI:** 10.17705/1CAIS.04724

---

## Citation Formats

### APA 7th Edition (General Format)

**For Python libraries:**
```
Author/Organization. (Year). Software Title (Version X.X.X) [Computer software].
URL or https://doi.org/xxxxx
```

**Example:**
```
Richardson, L. (2023). Beautiful Soup (Version 4.12.0) [Computer software].
https://www.crummy.com/software/BeautifulSoup/
```

### BibTeX Format

A complete BibTeX file is available in `REFERENCES.bib` for use with LaTeX documents.

### IEEE Format

**Example:**
```
L. Richardson, "Beautiful Soup," version 4.12.0, 2023. [Online].
Available: https://www.crummy.com/software/BeautifulSoup/
```

---

## Updating This File

**When adding a new library or dependency, please update this file with:**

1. **Library name and version**
2. **Citation in APA format** (Author/Organization, Year, Title, Version, URL)
3. **License type** (MIT, Apache 2.0, BSD, etc.)
4. **Copyright holder and year**
5. **Repository URL** (GitHub, GitLab, etc.)
6. **Documentation URL** (if different from repository)
7. **DOI** (if available, especially for academic papers)
8. **Category** (Core, Data Processing, Analysis, Development, etc.)

### How to Find This Information

1. **Repository:** Usually on GitHub/GitLab - check the repository URL
2. **License:** Check the `LICENSE` file in the repository or PyPI page
3. **Copyright:** Usually in the `LICENSE` file or package `__init__.py`
4. **Citation:** Check the repository's `CITATION.cff` file or documentation
5. **DOI:** Check the repository's README or releases page (often via Zenodo)
6. **Documentation:** Listed in the repository's README or PyPI page

### Template for New Entries

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

### Checking PyPI for Information

```bash
pip show library-name
```

This displays version, license, homepage, and other metadata.

---

## License Compatibility

All libraries used in this project have been selected for their compatibility with academic research and open-source distribution:

- **Permissive Licenses:** MIT, BSD 2-Clause, BSD 3-Clause, Apache 2.0, PSF License
- **Copyleft:** LGPL 2.1 (chardet - used only for runtime, not modified)

All licenses are compatible with academic research, publication, and thesis submission.

---

## Acknowledgments

This project builds upon the excellent work of the open-source community. We are grateful to all the developers and maintainers of the libraries listed above.

Special acknowledgment to:
- **Python Software Foundation** for the Python language and ecosystem
- **Project Jupyter** for interactive computing tools
- **NetworkX team** for network analysis capabilities
- **Beautiful Soup developers** for web scraping tools
- **All contributors** to the scientific Python ecosystem

---

**For questions about citations or license compliance, please contact:**
- Email: 498079@mail.muni.cz
- Repository: https://github.com/Leriot/leriot-web-scraper-for-thesis

---

**Version History:**
- v1.0 (2025-11-19): Initial comprehensive reference list
