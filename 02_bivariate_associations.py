"""
PAPER B: BIVARIATE ASSOCIATIONS WITH CONDOM USE
================================================

Analyzes relationships between condom use and:
- Age
- HIV knowledge
- Number of partners
- STI diagnosis
- HIV testing behavior
- PrEP awareness
"""

import pandas as pd
import numpy as np
from scipy.stats import spearmanr, chi2_contingency, kruskal, mannwhitneyu
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

# ============================================================================
# LOAD DATA
# ============================================================================

IN_FILE = '/Users/carlosmeyer2/IAS/Analysis/PaperB/Results/paperB_analytical_dataset.xlsx'
OUT_DIR = '/Users/carlosmeyer2/IAS/Analysis/PaperB/Results/'

print('='*80)
print('PAPER B: BIVARIATE ASSOCIATIONS WITH CONDOM USE')
print('='*80)
print()

df = pd.read_excel(IN_FILE, engine='openpyxl')
print(f"Loaded {len(df)} participants")
print()

# ============================================================================
# CORRELATIONS: CONTINUOUS VARIABLES WITH CONDOM USE
# ============================================================================

print('='*80)
print('SPEARMAN CORRELATIONS WITH CONDOM USE')
print('='*80)
print()

correlations = []

# Variables to correlate with condom use frequency (1=Always, 2=Sometimes, 3=Never)
# Note: Higher frequency codes = LESS condom use, so negative correlations = more use
continuous_vars = {
    'edad_grupo': 'Age group',
    'p4': 'Age (years)',
    'hiv_knowledge_score': 'HIV knowledge score',
    'partners_last_year': 'Partners last year',
}

for var, label in continuous_vars.items():
    if var in df.columns and df[var].notna().any():
        valid = df[[var, 'condom_use_freq']].dropna()
        if len(valid) > 0:
            rho, p = spearmanr(valid[var], valid['condom_use_freq'])
            correlations.append({
                'Variable': label,
                'Spearman_rho': rho,
                'P_value': p,
                'N': len(valid),
                'Interpretation': 'More use' if rho < 0 else 'Less use'
            })
            print(f"{label}:")
            print(f"  ρ = {rho:.3f}, p = {p:.4f}, N = {len(valid)}")
            print(f"  {('↑ variable → ↓ condom use' if rho > 0 else '↑ variable → ↑ condom use')}")
            print()

corr_df = pd.DataFrame(correlations)
print()

# ============================================================================
# CHI-SQUARE: CATEGORICAL PREDICTORS OF CONDOM USE
# ============================================================================

print('='*80)
print('CHI-SQUARE TESTS: CATEGORICAL PREDICTORS')
print('='*80)
print()

chi2_results = []

# Binary predictors
binary_predictors = {
    'multiple_partners': 'Multiple partners (≥2)',
    'any_sti': 'Any STI diagnosis',
    'tested_hiv_12mo': 'Tested HIV (12mo)',
    'knows_prep': 'PrEP awareness',
}

for var, label in binary_predictors.items():
    if var in df.columns and df[var].notna().any():
        # Create contingency table
        ct = pd.crosstab(df[var], df['condom_use_lbl'])
        if ct.shape[0] > 1 and ct.shape[1] > 1:
            chi2, p, dof, expected = chi2_contingency(ct)
            
            # Calculate percentages
            ct_pct = pd.crosstab(df[var], df['condom_use_lbl'], normalize='index') * 100
            
            chi2_results.append({
                'Predictor': label,
                'Chi2': chi2,
                'df': dof,
                'P_value': p,
                'N': ct.sum().sum()
            })
            
            print(f"{label}:")
            print(f"  χ² = {chi2:.2f}, df = {dof}, p = {p:.4f}")
            print(f"  Contingency table (row %):")
            print(ct_pct.round(1))
            print()

chi2_df = pd.DataFrame(chi2_results)
print()

# ============================================================================
# GROUP COMPARISONS: CONDOM USE BY AGE
# ============================================================================

print('='*80)
print('CONDOM USE BY AGE GROUP (KRUSKAL-WALLIS)')
print('='*80)
print()

# Compare condom frequency across age groups
age_groups = []
for age in df['edad_grupo_lbl'].dropna().unique():
    group_data = df[df['edad_grupo_lbl'] == age]['condom_use_freq'].dropna()
    if len(group_data) > 0:
        age_groups.append(group_data.values)

if len(age_groups) > 1:
    h_stat, p_val = kruskal(*age_groups)
    print(f"Kruskal-Wallis H = {h_stat:.2f}, p = {p_val:.4f}")
    print()
    
    # Descriptive by age
    print("Condom use by age group (median, IQR):")
    age_desc = df.groupby('edad_grupo_lbl')['condom_use_freq'].agg(['median', 
                                                                      lambda x: x.quantile(0.25),
                                                                      lambda x: x.quantile(0.75),
                                                                      'count'])
    age_desc.columns = ['Median', 'Q1', 'Q3', 'N']
    age_desc['Median_label'] = age_desc['Median'].map({1: 'Always', 2: 'Sometimes', 3: 'Never'})
    print(age_desc)
    print()

# ============================================================================
# GROUP COMPARISONS: PREDICTORS BY CONDOM USE STATUS
# ============================================================================

print('='*80)
print('PREDICTORS BY CONDOM USE (ALWAYS vs NOT ALWAYS)')
print('='*80)
print()

# Compare predictors between always users and others
always_users = df[df['always_condom'] == 1]
not_always = df[df['always_condom'] == 0]

print(f"Always users: N = {len(always_users)}")
print(f"Not always: N = {len(not_always)}")
print()

comparison_results = []

for var, label in continuous_vars.items():
    if var in df.columns:
        always_vals = always_users[var].dropna()
        not_always_vals = not_always[var].dropna()
        
        if len(always_vals) > 0 and len(not_always_vals) > 0:
            u_stat, p = mannwhitneyu(always_vals, not_always_vals, alternative='two-sided')
            
            comparison_results.append({
                'Variable': label,
                'Always_median': always_vals.median(),
                'NotAlways_median': not_always_vals.median(),
                'Always_mean': always_vals.mean(),
                'NotAlways_mean': not_always_vals.mean(),
                'U_statistic': u_stat,
                'P_value': p
            })
            
            print(f"{label}:")
            print(f"  Always users: median = {always_vals.median():.2f}, mean = {always_vals.mean():.2f}")
            print(f"  Not always: median = {not_always_vals.median():.2f}, mean = {not_always_vals.mean():.2f}")
            print(f"  Mann-Whitney U = {u_stat:.0f}, p = {p:.4f}")
            print()

comp_df = pd.DataFrame(comparison_results)
print()

# ============================================================================
# CORRELATION MATRIX: KEY VARIABLES
# ============================================================================

print('='*80)
print('CORRELATION MATRIX (SPEARMAN)')
print('='*80)
print()

matrix_vars = ['edad_grupo', 'hiv_knowledge_score', 'partners_last_year', 
               'condom_use_freq', 'always_condom']
matrix_vars = [v for v in matrix_vars if v in df.columns]

corr_matrix = df[matrix_vars].corr(method='spearman')
print(corr_matrix.round(3))
print()

# ============================================================================
# SPECIAL ANALYSIS: TESTING REASONS AND CONDOM USE
# ============================================================================

if 'test_reason' in df.columns and df['test_reason'].notna().any():
    print('='*80)
    print('HIV TESTING REASONS BY CONDOM USE')
    print('='*80)
    print()
    
    # Cross-tabulate test reason with condom use
    test_reason_ct = pd.crosstab(df['test_reason'], 
                                  df['condom_use_lbl'],
                                  normalize='index') * 100
    
    print("Test reasons by condom use (row %):")
    print(test_reason_ct.round(1))
    print()

# ============================================================================
# SAVE RESULTS
# ============================================================================

print('='*80)
print('SAVING RESULTS')
print('='*80)
print()

with pd.ExcelWriter(OUT_DIR + 'paperB_bivariate_associations.xlsx', 
                    engine='openpyxl') as writer:
    
    # Correlations
    corr_df.to_excel(writer, sheet_name='Correlations', index=False)
    print(f"  Saved: Correlations ({len(corr_df)} associations)")
    
    # Chi-square tests
    chi2_df.to_excel(writer, sheet_name='Chi_Square_Tests', index=False)
    print(f"  Saved: Chi-square tests ({len(chi2_df)} tests)")
    
    # Group comparisons
    comp_df.to_excel(writer, sheet_name='Group_Comparisons', index=False)
    print(f"  Saved: Group comparisons ({len(comp_df)} comparisons)")
    
    # Correlation matrix
    corr_matrix.to_excel(writer, sheet_name='Correlation_Matrix')
    print(f"  Saved: Correlation matrix")
    
    # Age group descriptives
    if 'age_desc' in locals():
        age_desc.to_excel(writer, sheet_name='Condom_Use_by_Age')
        print(f"  Saved: Condom use by age")
    
    # Condom use distribution by subgroups
    summary_stats = []
    
    # Overall
    summary_stats.append({
        'Group': 'Overall',
        'N': len(df),
        'Always_%': df['always_condom'].mean() * 100,
        'Sometimes_%': ((df['condom_use_freq'] == 2).sum() / len(df)) * 100,
        'Never_%': ((df['condom_use_freq'] == 3).sum() / len(df)) * 100
    })
    
    # By age group
    for age in df['edad_grupo_lbl'].dropna().unique():
        age_data = df[df['edad_grupo_lbl'] == age]
        summary_stats.append({
            'Group': f'Age: {age}',
            'N': len(age_data),
            'Always_%': age_data['always_condom'].mean() * 100,
            'Sometimes_%': ((age_data['condom_use_freq'] == 2).sum() / len(age_data)) * 100,
            'Never_%': ((age_data['condom_use_freq'] == 3).sum() / len(age_data)) * 100
        })
    
    # By partners
    summary_stats.append({
        'Group': '1 partner',
        'N': (df['partners_last_year'] == 1).sum(),
        'Always_%': df[df['partners_last_year'] == 1]['always_condom'].mean() * 100,
        'Sometimes_%': ((df[df['partners_last_year'] == 1]['condom_use_freq'] == 2).sum() / 
                       (df['partners_last_year'] == 1).sum()) * 100,
        'Never_%': ((df[df['partners_last_year'] == 1]['condom_use_freq'] == 3).sum() / 
                   (df['partners_last_year'] == 1).sum()) * 100
    })
    
    summary_stats.append({
        'Group': '2+ partners',
        'N': (df['partners_last_year'] >= 2).sum(),
        'Always_%': df[df['partners_last_year'] >= 2]['always_condom'].mean() * 100,
        'Sometimes_%': ((df[df['partners_last_year'] >= 2]['condom_use_freq'] == 2).sum() / 
                       (df['partners_last_year'] >= 2).sum()) * 100,
        'Never_%': ((df[df['partners_last_year'] >= 2]['condom_use_freq'] == 3).sum() / 
                   (df['partners_last_year'] >= 2).sum()) * 100
    })
    
    summary_df = pd.DataFrame(summary_stats)
    summary_df.to_excel(writer, sheet_name='Summary_Statistics', index=False)
    print(f"  Saved: Summary statistics")

print()
print('='*80)
print('BIVARIATE ASSOCIATIONS COMPLETE')
print('='*80)
print()
print(f"Results saved to: {OUT_DIR}paperB_bivariate_associations.xlsx")
