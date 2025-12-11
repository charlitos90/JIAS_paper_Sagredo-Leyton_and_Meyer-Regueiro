================================================================================
PAPER B: CORRELATES OF CONDOM USE IN CHILEAN ADULTS
================================================================================

PROJECT OVERVIEW
================================================================================

This analysis examines correlates of condom use frequency using data from the 
ENSSEX 2024 National Sexual Health Survey in Chile. Unlike PaperA (which focused 
on HIV knowledge → STI outcomes), PaperB uses condom use as the PRIMARY OUTCOME 
variable to understand what factors predict consistent condom use.

RESEARCH QUESTIONS
================================================================================

1. What is the relationship between age and condom use frequency?
2. Does HIV knowledge predict condom use behavior?
3. How does number of sexual partners relate to condom use?
4. Are STI diagnosis and HIV testing associated with condom use?
5. Does PrEP awareness correlate with condom use patterns?
6. Do these relationships vary by age group?

KEY FINDINGS SNAPSHOT
================================================================================

✓ Strong age gradient: 32% always use (18-29) → 2% always use (80+)
✓ Number of partners is strongest predictor: OR = 1.10 per partner
✓ HIV knowledge has modest effect: OR = 1.08 per point increase
✓ PrEP awareness associated with more use: OR = 1.22
✓ No association with STI diagnosis (missed intervention opportunity)
✓ Knowledge effect strongest in youth (18-29) and middle-aged (50-59)

FOLDER STRUCTURE
================================================================================

PaperB/
│
├── Scripts/
│   ├── 01_prepare_data.py          # Data loading & variable construction
│   ├── 02_bivariate_associations.py # Correlations & chi-square tests
│   ├── 03_regression_models.py      # Logistic regression models
│   └── 04_visualizations.py         # Publication figures
│
├── Results/
│   ├── paperB_analytical_dataset.xlsx        # Analysis data (12,765 × 17)
│   ├── paperB_bivariate_associations.xlsx    # Statistical tests
│   ├── paperB_regression_models.xlsx         # 5 logistic models
│   ├── figure1_condom_use_patterns.png       # 4-panel overview
│   ├── figure2_regression_forest_plot.png    # Model 4 ORs
│   ├── figure3_age_stratified_effects.png    # Effects by age
│   ├── figure4_testing_prep_condom_use.png   # Testing associations
│   ├── figure5_manuscript_simple.png         # 2-panel simplified
│   └── RESULTS_SUMMARY.txt                   # Comprehensive findings
│
└── Documentation/
    └── README.txt                             # This file

ANALYSIS PIPELINE
================================================================================

STEP 1: Data Preparation (01_prepare_data.py)
----------------------------------------------
Input: ENSSEX_age_groups.xlsx (20,392 participants)

Processing:
  - Construct HIV knowledge score (0-6, corrected scoring)
  - Create condom use variables (always, ever, frequency)
  - Clean partner variables (P71, cap extremes)
  - Construct STI diagnosis variables
  - Extract HIV testing variables (P208, P210, P211)
  - Extract PrEP awareness (P213)
  - Create age group labels

Filtering:
  - Include: ≥1 sexual partner last year
  - Include: Valid condom use data (P73)
  - Include: Valid age group
  
Output: 12,765 participants (62.6% retention)
        17 variables

STEP 2: Bivariate Associations (02_bivariate_associations.py)
--------------------------------------------------------------
Analyses:
  1. Spearman correlations (continuous predictors)
     - Age, knowledge, partners vs condom frequency
  
  2. Chi-square tests (categorical predictors)
     - Multiple partners, STI, testing, PrEP vs condom use
  
  3. Kruskal-Wallis test
     - Condom frequency across age groups
  
  4. Mann-Whitney U tests
     - Predictors: Always users vs not always
  
  5. Correlation matrix
     - 5 key variables

Output: paperB_bivariate_associations.xlsx (6 sheets)

STEP 3: Regression Models (03_regression_models.py)
----------------------------------------------------
Models:
  1. Age + Knowledge → Always condom use
  2. Add number of partners
  3. Add STI diagnosis + HIV testing
  4. Add PrEP awareness (FINAL MODEL)
  5. Age × Knowledge interaction test
  
Age-Stratified Models:
  - Knowledge + Partners → Condom use
  - Separate models for each age group (7 groups)
  - Compare effect sizes across ages

Output: paperB_regression_models.xlsx (7 sheets)

STEP 4: Visualizations (04_visualizations.py)
----------------------------------------------
Figures:
  1. 4-panel patterns (age, partners, trend, knowledge)
  2. Forest plot (Model 4 odds ratios)
  3. Age-stratified effects (knowledge & partners)
  4. Testing & PrEP associations
  5. Simplified 2-panel for manuscript

Output: 5 PNG files (300 DPI, publication-ready)

VARIABLES CONSTRUCTED
================================================================================

OUTCOME VARIABLE:
  - condom_use_freq: 1=Always, 2=Sometimes, 3=Never (P73)
  - always_condom: Binary (1=Always, 0=Sometimes/Never)
  - ever_condom: Binary (1=Always/Sometimes, 0=Never)
  - condom_use_lbl: Text labels for frequency

PREDICTOR VARIABLES:
  - edad_grupo: Age group (1-7)
  - edad_grupo_lbl: Age labels (18-29 through 80+)
  - hiv_knowledge_score: 0-6 score (corrected method)
  - partners_last_year: Number of partners (P71, capped)
  - multiple_partners: Binary (≥2 vs 0-1)
  - any_sti: Any STI diagnosis (composite)
  - hiv_diagnosis: HIV specifically
  - tested_hiv_12mo: Tested in last 12 months (P208)
  - test_reason: Why tested (P210)
  - no_test_reason: Why not tested (P211)
  - knows_prep: PrEP awareness (P213)

DATA SOURCES
================================================================================

Primary: ENSSEX_age_groups.xlsx
  - ENSSEX 2024 National Sexual Health Survey
  - Representative sample of Chilean adults
  - 20,392 participants, ages 18-89
  - Space-separated values

Alternative: 20241205_ENSSEX_data.csv
  - Same data in CSV format
  - Used if Excel file unavailable

Key Variables from Survey:
  - P4: Age
  - P71: Sexual partners last year
  - P73: Condom use frequency ← PRIMARY OUTCOME
  - P202_*: STI diagnoses
  - P208: HIV tested (12mo)
  - P210: Reasons for testing
  - P211: Reasons for not testing
  - P212: HIV knowledge items (i_1_p212 through i_6_p212)
  - P213: PrEP awareness

SAMPLE CHARACTERISTICS
================================================================================

Total: 12,765 participants (sexually active in last year)

Age Distribution:
  18-29: 3,311 (25.9%)
  30-39: 2,988 (23.4%)
  40-49: 2,313 (18.1%)
  50-59: 2,080 (16.3%)
  60-69: 1,372 (10.7%)
  70-79: 589 (4.6%)
  80+: 112 (0.9%)

Condom Use:
  Always: 2,236 (17.5%)
  Sometimes: 2,620 (20.5%)
  Never: 7,909 (62.0%)

Partners (Last Year):
  Mean: 1.50 (SD = 1.47)
  Median: 1.0
  Multiple (≥2): 2,234 (17.4%)

HIV Knowledge:
  Mean: 4.31/6 (SD = 1.45)
  Median: 5.0/6

STI & Testing:
  STI diagnosed: 885 (6.9%)
  Tested HIV (12mo): 4,004 (31.4%)
  PrEP aware: 1,971 (15.4%)

STATISTICAL METHODS
================================================================================

Bivariate Analyses:
  - Spearman rank correlation (continuous variables)
  - Chi-square test of independence (categorical variables)
  - Kruskal-Wallis test (condom use across age groups)
  - Mann-Whitney U test (always vs not always users)

Multivariable Analyses:
  - Logistic regression (outcome: always condom use)
  - Odds ratios with 95% confidence intervals
  - Pseudo R² (McFadden) for model fit
  - Likelihood ratio tests for interactions

Age-Stratified Analyses:
  - Separate logistic models per age group
  - Test for effect modification

Significance Level: α = 0.05 (two-tailed)

Software: Python 3.12
  - pandas 2.3.3 (data manipulation)
  - scipy 1.14.1 (statistical tests)
  - statsmodels 0.14.4 (regression models)
  - matplotlib 3.10.7 (visualizations)
  - seaborn 0.13.2 (advanced plotting)

MAIN RESULTS
================================================================================

BIVARIATE ASSOCIATIONS:

Correlations with Condom Frequency (ρ, p-value):
  - Age group: 0.408, p < 0.001 (older → less use)
  - Age (years): 0.422, p < 0.001
  - HIV knowledge: -0.020, p = 0.026 (more knowledge → more use)
  - Partners: -0.304, p < 0.001 (more partners → more use)

Chi-Square Tests (χ², p-value):
  - Multiple partners: 1176.71, p < 0.001 ✓✓✓
  - HIV testing: 30.86, p < 0.001 ✓✓✓
  - PrEP awareness: 80.40, p < 0.001 ✓✓✓
  - STI diagnosis: 1.78, p = 0.411 (NS)

MULTIVARIABLE REGRESSION (Model 4):

Adjusted Odds Ratios (95% CI, p-value):
  - Age group: 0.56 (0.54-0.58), p < 0.001
    → Each age group ↑ = 44% lower odds of always using
  
  - HIV knowledge: 1.08 (1.03-1.12), p < 0.001
    → Each point ↑ = 8% higher odds of always using
  
  - Partners: 1.10 (1.07-1.13), p < 0.001
    → Each partner ↑ = 10% higher odds of always using
  
  - STI diagnosis: 0.99 (0.78-1.24), p = 0.947 (NS)
  
  - HIV testing: 0.92 (0.80-1.03), p = 0.136 (NS)
  
  - PrEP awareness: 1.22 (1.05-1.34), p = 0.006
    → PrEP aware = 22% higher odds of always using

Model Fit: Pseudo R² = 0.097, N = 11,806

AGE-STRATIFIED RESULTS:

HIV Knowledge Effect by Age:
  - 18-29: OR = 1.11*, strongest effect in youth
  - 30-39: OR = 1.00 (NS)
  - 40-49: OR = 1.01 (NS)
  - 50-59: OR = 1.14*, reemergence in middle-age
  - 60+: Not significant in older groups

Partners Effect by Age:
  - Significant in ages 18-59 (OR = 1.05-1.19)
  - Not significant in ages 60+
  - Strongest in 40-49 group (OR = 1.19)

INTERPRETATION
================================================================================

1. AGE DOMINATES CONDOM USE BEHAVIOR
   - Largest effect size (OR = 0.56 per age group)
   - 16-fold difference: 32% (youth) vs 2% (elderly)
   - Reflects: pregnancy concerns, relationship types, cohort effects

2. PARTNERS DRIVE RISK PERCEPTION
   - Clear dose-response relationship
   - Casual/multiple partners → perceived risk → condom use
   - Effect disappears in ages 60+ (different relationship dynamics)

3. KNOWLEDGE EFFECT IS MODEST
   - OR = 1.08 means knowledge alone insufficient
   - Strongest in youth (OR = 1.11) where prevention messages resonate
   - Reemergent in 50-59 (OR = 1.14) - possible renewed concern
   - Absent in 60+ - suggests different barriers

4. PREP AWARENESS AS ENGAGEMENT MARKER
   - OR = 1.22 suggests broader sexual health knowledge
   - NOT risk compensation (no decrease in condom use)
   - May indicate: health literacy, access to information, proactive behavior

5. MISSED OPPORTUNITIES
   - STI diagnosis doesn't change behavior (OR = 0.99, NS)
   - HIV testing only marginally associated (OR = 0.92, NS)
   - Both represent missed counseling opportunities

HOW TO RUN THE ANALYSIS
================================================================================

Prerequisites:
  - Python 3.12 or higher
  - Virtual environment with required packages:
    * pandas, numpy, scipy, statsmodels
    * matplotlib, seaborn, openpyxl

Step-by-step:

1. Activate virtual environment:
   ```
   cd /Users/carlosmeyer2/IAS
   source IAS.venv/bin/activate
   ```

2. Run scripts in order:
   ```
   cd Analysis/PaperB/Scripts
   
   python 01_prepare_data.py
   python 02_bivariate_associations.py
   python 03_regression_models.py
   python 04_visualizations.py
   ```

3. Results will be saved to: Analysis/PaperB/Results/

Expected Runtime: ~2-3 minutes total

COMPARISON WITH PAPERA
================================================================================

PaperA: HIV Knowledge → STI Outcomes
  - Outcome: Any STI diagnosis
  - Finding: Knowledge paradox (more knowledge → MORE STIs)
  - Explanation: Reverse causation + testing bias

PaperB: Correlates → Condom Use
  - Outcome: Always condom use
  - Finding: Knowledge → MORE condom use (OR = 1.08)
  - Explanation: Direct behavioral effect (though modest)

Integration:
  - Knowledge increases BOTH testing AND condom use
  - Testing increases detection → apparent paradox in PaperA
  - Condom use increase is real but small (8%)
  - Multiple partners confound both relationships
  - Together: complete picture of knowledge → behavior → outcomes

LIMITATIONS
================================================================================

1. Cross-sectional design (no causality)
2. Self-reported behavior (social desirability bias)
3. Limited condom use measurement (doesn't distinguish partner types)
4. Missing data (37% excluded)
5. Unmeasured confounders (relationship status, access, etc.)
6. Low variance explained (R² = 0.097)

FUTURE DIRECTIONS
================================================================================

1. Longitudinal analysis to establish temporal sequence
2. Qualitative research on age-specific barriers
3. Intervention studies targeting:
   - Age-tailored condom promotion
   - Partner communication skills
   - Post-STI diagnosis counseling
4. Integration with PaperA for pathway analysis:
   Knowledge → Condom use → STI risk

CITATION
================================================================================

Data Source:
ENSSEX 2024 - National Sexual Health Survey
Ministry of Health (MINSAL), Chile
N = 20,392 participants

Analysis:
Paper B: Correlates of Condom Use in Chilean Adults
IAS Research Team, December 2025

CONTACT
================================================================================

For questions about this analysis:
- Review RESULTS_SUMMARY.txt for detailed findings
- Check individual script headers for methodology
- Consult ENSSEX_Questions_Reference.txt for variable definitions

================================================================================
Last Updated: December 10, 2025
================================================================================
