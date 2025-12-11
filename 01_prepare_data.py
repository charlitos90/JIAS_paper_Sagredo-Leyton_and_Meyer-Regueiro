"""
PAPER B: CONDOM USE CORRELATES
================================

This analysis focuses on correlates of condom use frequency in the ENSSEX 2024 
Chile survey, using condom use as the PRIMARY OUTCOME variable.

KEY VARIABLES:
1. OUTCOME: Condom Use Frequency (P73)
   - Always (P73=1)
   - Sometimes (P73=2)
   - Never (P73=3)
   
2. PREDICTORS:
   - Age (edad_grupo, edad_grupo_lbl)
   - HIV knowledge score (0-6 corrected scoring from P212 items)
   - Number of partners last year (P71)
   - STI diagnosis history (any_sti, hiv_diagnosis)
   - HIV testing behavior (P208: tested in last 12 months)
   - Reasons for testing (P210)
   - Reasons for NOT testing (P211)
   - PrEP awareness (P213)

ANALYSIS PLAN:
Step 1: Data preparation and variable construction
Step 2: Descriptive statistics for condom use by subgroups
Step 3: Bivariate associations (correlations, group comparisons)
Step 4: Logistic regression models predicting condom use
Step 5: Age-stratified analyses
Step 6: Visualizations

OUTPUT LOCATION: Analysis/PaperB/Results/
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import chi2_contingency, spearmanr, kruskal, mannwhitneyu
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

# ============================================================================
# CONFIGURATION
# ============================================================================

IN_FN = '/Users/carlosmeyer2/IAS/ENSSEX_age_groups.xlsx'
IN_CSV = '/Users/carlosmeyer2/IAS/Analysis/Datasets/20241205_ENSSEX_data.csv'
OUT_DIR = '/Users/carlosmeyer2/IAS/Analysis/PaperB/Results/'

print('='*80)
print('PAPER B: CORRELATES OF CONDOM USE')
print('='*80)
print()

# ============================================================================
# STEP 1: LOAD AND PREPARE DATA
# ============================================================================
print('STEP 1: Loading data...')
print('-'*80)

try:
    df = pd.read_excel(IN_FN, engine='openpyxl')
    print(f"Loaded from Excel: {len(df)} participants")
    data_source = "ENSSEX_age_groups.xlsx"
except Exception as e:
    print(f"Could not load Excel: {e}")
    print("Loading from CSV...")
    df = pd.read_csv(IN_CSV, sep=' ', low_memory=False)
    print(f"Loaded from CSV: {len(df)} participants")
    data_source = "20241205_ENSSEX_data.csv"
    
    # Create age groups if loading from CSV
    def assign_age_group(age):
        try:
            age = float(age)
            if pd.isna(age): return pd.NA
        except: return pd.NA
        if age >= 18 and age < 30: return 1
        if age >= 30 and age < 40: return 2
        if age >= 40 and age < 50: return 3
        if age >= 50 and age < 60: return 4
        if age >= 60 and age < 70: return 5
        if age >= 70 and age < 80: return 6
        if age >= 80: return 7
        return pd.NA
    
    df['edad_grupo'] = df['p4'].apply(assign_age_group)

print()

# ============================================================================
# STEP 2: CONSTRUCT HIV KNOWLEDGE SCORE (CORRECTED METHOD)
# ============================================================================
print('STEP 2: Constructing HIV knowledge score...')
print('-'*80)

# P212 items with correct answers
# Items 1,2,3,6 = TRUE (correct answer is code 1)
# Items 4,5 = FALSE (correct answer is code 2)
hiv_items = {
    'i_1_p212': 1,  # TRUE
    'i_2_p212': 1,  # TRUE
    'i_3_p212': 1,  # TRUE
    'i_4_p212': 2,  # FALSE
    'i_5_p212': 2,  # FALSE
    'i_6_p212': 1   # TRUE
}

# Calculate knowledge score
df['hiv_knowledge_score'] = 0
for item, correct_answer in hiv_items.items():
    if item in df.columns:
        # Score 1 if correct, 0 otherwise (including missing)
        df['hiv_knowledge_score'] += (df[item] == correct_answer).astype(int)

print(f"HIV knowledge score created (range 0-6)")
print(f"  Mean: {df['hiv_knowledge_score'].mean():.2f}")
print(f"  Median: {df['hiv_knowledge_score'].median():.1f}")
print(f"  Valid cases: {df['hiv_knowledge_score'].notna().sum()}")
print()

# ============================================================================
# STEP 3: CONSTRUCT CONDOM USE VARIABLES (PRIMARY OUTCOME)
# ============================================================================
print('STEP 3: Constructing condom use variables...')
print('-'*80)

# P73: Condom use frequency in last year
# 1=Always, 2=Sometimes, 3=Never, 9=Missing
df['condom_use_freq'] = df['p73'].copy()
df.loc[df['p73'].isin([9, 99]), 'condom_use_freq'] = np.nan

# Binary outcome: Always use condoms (vs sometimes/never)
df['always_condom'] = (df['p73'] == 1).astype(float)
df.loc[df['p73'].isin([9, 99]), 'always_condom'] = np.nan

# Binary outcome: Ever use condoms (always or sometimes vs never)
df['ever_condom'] = (df['p73'].isin([1, 2])).astype(float)
df.loc[df['p73'].isin([9, 99]), 'ever_condom'] = np.nan

# Categorical labels
df['condom_use_lbl'] = df['condom_use_freq'].map({
    1: 'Always',
    2: 'Sometimes', 
    3: 'Never'
})

print(f"Condom use frequency distribution:")
print(df['condom_use_lbl'].value_counts(dropna=False))
print()
print(f"Always use condoms: {df['always_condom'].sum():.0f} ({df['always_condom'].mean()*100:.1f}%)")
print(f"Ever use condoms: {df['ever_condom'].sum():.0f} ({df['ever_condom'].mean()*100:.1f}%)")
print()

# ============================================================================
# STEP 4: CONSTRUCT PARTNER VARIABLES
# ============================================================================
print('STEP 4: Constructing partner variables...')
print('-'*80)

# P71: Partners in last year
df['partners_last_year'] = df['p71'].copy()
df.loc[df['p71'] == 999, 'partners_last_year'] = np.nan
df.loc[df['p71'] > 100, 'partners_last_year'] = np.nan  # Cap extremes

# Binary: Multiple partners (≥2 vs 0-1)
df['multiple_partners'] = (df['partners_last_year'] >= 2).astype(float)
df.loc[df['partners_last_year'].isna(), 'multiple_partners'] = np.nan

print(f"Partners last year:")
print(f"  Mean: {df['partners_last_year'].mean():.2f}")
print(f"  Median: {df['partners_last_year'].median():.1f}")
print(f"  Valid cases: {df['partners_last_year'].notna().sum()}")
print(f"  Multiple partners (≥2): {df['multiple_partners'].sum():.0f} ({df['multiple_partners'].mean()*100:.1f}%)")
print()

# ============================================================================
# STEP 5: CONSTRUCT STI DIAGNOSIS VARIABLES
# ============================================================================
print('STEP 5: Constructing STI diagnosis variables...')
print('-'*80)

# Check for STI variables
sti_vars = [c for c in df.columns if c.startswith('p202_')]
print(f"Found {len(sti_vars)} STI diagnosis variables: {sti_vars[:5]}...")

# Any STI diagnosis
if 'its_alguna_vez' in df.columns:
    df['any_sti'] = (df['its_alguna_vez'] == 1).astype(float)
else:
    # Create from individual STI variables
    df['any_sti'] = 0
    for var in sti_vars:
        if var in df.columns:
            df['any_sti'] = ((df['any_sti'] == 1) | (df[var] == 1)).astype(float)

# HIV diagnosis specifically
if 'p202_vih' in df.columns:
    df['hiv_diagnosis'] = (df['p202_vih'] == 1).astype(float)
else:
    df['hiv_diagnosis'] = np.nan

print(f"Any STI diagnosis: {df['any_sti'].sum():.0f} ({df['any_sti'].mean()*100:.2f}%)")
if 'hiv_diagnosis' in df.columns and df['hiv_diagnosis'].notna().any():
    print(f"HIV diagnosis: {df['hiv_diagnosis'].sum():.0f} ({df['hiv_diagnosis'].mean()*100:.2f}%)")
print()

# ============================================================================
# STEP 6: CONSTRUCT HIV TESTING VARIABLES
# ============================================================================
print('STEP 6: Constructing HIV testing variables...')
print('-'*80)

# P208: Tested for HIV in last 12 months
if 'p208' in df.columns:
    df['tested_hiv_12mo'] = (df['p208'] == 1).astype(float)
    df.loc[df['p208'].isin([9, 99]), 'tested_hiv_12mo'] = np.nan
    print(f"Tested for HIV in last 12 months: {df['tested_hiv_12mo'].sum():.0f} ({df['tested_hiv_12mo'].mean()*100:.1f}%)")
else:
    df['tested_hiv_12mo'] = np.nan
    print("P208 (HIV testing) not found in dataset")

# P210: Reasons for testing (among those who tested)
if 'p210' in df.columns:
    df['test_reason'] = df['p210'].copy()
    df.loc[df['p210'].isin([9, 99]), 'test_reason'] = np.nan
    print(f"Test reasons available: {df['test_reason'].notna().sum()} cases")
else:
    df['test_reason'] = np.nan
    print("P210 (test reasons) not found")

# P211: Reasons for NOT testing (among those who didn't test)
if 'p211' in df.columns:
    df['no_test_reason'] = df['p211'].copy()
    df.loc[df['p211'].isin([9, 99]), 'no_test_reason'] = np.nan
    print(f"No-test reasons available: {df['no_test_reason'].notna().sum()} cases")
else:
    df['no_test_reason'] = np.nan
    print("P211 (no-test reasons) not found")

# P213: PrEP awareness
if 'p213' in df.columns:
    df['knows_prep'] = (df['p213'] == 1).astype(float)
    df.loc[df['p213'].isin([9, 99]), 'knows_prep'] = np.nan
    print(f"PrEP awareness: {df['knows_prep'].sum():.0f} ({df['knows_prep'].mean()*100:.1f}%)")
else:
    df['knows_prep'] = np.nan
    print("P213 (PrEP awareness) not found")

print()

# ============================================================================
# STEP 7: CREATE AGE GROUP LABELS
# ============================================================================
print('STEP 7: Creating age group labels...')
print('-'*80)

age_labels = {
    1: '18-29',
    2: '30-39',
    3: '40-49',
    4: '50-59',
    5: '60-69',
    6: '70-79',
    7: '80+'
}

if 'edad_grupo_lbl' not in df.columns:
    df['edad_grupo_lbl'] = df['edad_grupo'].map(age_labels)

print("Age group distribution:")
print(df['edad_grupo_lbl'].value_counts().sort_index())
print()

# ============================================================================
# STEP 8: FILTER FOR ANALYSIS SAMPLE
# ============================================================================
print('STEP 8: Creating analysis sample...')
print('-'*80)

# Inclusion criteria:
# 1. Has condom use data (P73)
# 2. Has age group
# 3. Has at least one sexual partner in last year (P71 > 0)

initial_n = len(df)
print(f"Initial sample: {initial_n}")

# Filter for sexually active in last year
df_analysis = df[df['partners_last_year'] > 0].copy()
print(f"  After requiring ≥1 partner last year: {len(df_analysis)} ({len(df_analysis)/initial_n*100:.1f}%)")

# Filter for valid condom use data
df_analysis = df_analysis[df_analysis['condom_use_freq'].notna()].copy()
print(f"  After requiring valid condom use data: {len(df_analysis)} ({len(df_analysis)/initial_n*100:.1f}%)")

# Filter for valid age
df_analysis = df_analysis[df_analysis['edad_grupo'].notna()].copy()
print(f"  After requiring valid age: {len(df_analysis)} ({len(df_analysis)/initial_n*100:.1f}%)")

print()
print(f"Final analysis sample: {len(df_analysis)} participants")
print()

# ============================================================================
# STEP 9: SAVE PREPARED DATASET
# ============================================================================
print('STEP 9: Saving prepared dataset...')
print('-'*80)

# Select variables for analysis
analysis_vars = [
    'folio',
    'p4',  # Raw age
    'edad_grupo',
    'edad_grupo_lbl',
    'hiv_knowledge_score',
    'knows_prep',
    'tested_hiv_12mo',
    'test_reason',
    'no_test_reason',
    'condom_use_freq',
    'condom_use_lbl',
    'always_condom',
    'ever_condom',
    'partners_last_year',
    'multiple_partners',
    'any_sti',
    'hiv_diagnosis',
    'p3',  # Gender
]

# Keep only variables that exist
analysis_vars = [v for v in analysis_vars if v in df_analysis.columns]

df_out = df_analysis[analysis_vars].copy()

# Save
out_file = OUT_DIR + 'paperB_analytical_dataset.xlsx'
df_out.to_excel(out_file, index=False, engine='openpyxl')
print(f"Saved: {out_file}")
print(f"  Variables: {len(df_out.columns)}")
print(f"  Observations: {len(df_out)}")
print()

# ============================================================================
# STEP 10: DESCRIPTIVE STATISTICS
# ============================================================================
print('STEP 10: Descriptive statistics...')
print('-'*80)

print("CONDOM USE BY AGE GROUP:")
print(pd.crosstab(df_analysis['edad_grupo_lbl'], 
                   df_analysis['condom_use_lbl'],
                   margins=True, normalize='index') * 100)
print()

print("CONDOM USE BY NUMBER OF PARTNERS:")
partner_groups = pd.cut(df_analysis['partners_last_year'], 
                        bins=[0, 1, 2, 5, 100],
                        labels=['1 partner', '2 partners', '3-5 partners', '6+ partners'])
print(pd.crosstab(partner_groups, 
                   df_analysis['condom_use_lbl'],
                   margins=True, normalize='index') * 100)
print()

print("CONDOM USE BY HIV TESTING STATUS:")
if df_analysis['tested_hiv_12mo'].notna().any():
    print(pd.crosstab(df_analysis['tested_hiv_12mo'], 
                       df_analysis['condom_use_lbl'],
                       margins=True, normalize='index') * 100)
print()

print("CONDOM USE BY STI DIAGNOSIS:")
if df_analysis['any_sti'].notna().any():
    print(pd.crosstab(df_analysis['any_sti'], 
                       df_analysis['condom_use_lbl'],
                       margins=True, normalize='index') * 100)
print()

print('='*80)
print('DATA PREPARATION COMPLETE')
print('='*80)
print()
print(f"Analysis dataset: {len(df_analysis)} participants")
print(f"Variables constructed: {len(analysis_vars)}")
print(f"Output saved to: {OUT_DIR}")
print()
print("Next steps:")
print("  1. Run 02_bivariate_associations.py")
print("  2. Run 03_regression_models.py")
print("  3. Run 04_visualizations.py")
