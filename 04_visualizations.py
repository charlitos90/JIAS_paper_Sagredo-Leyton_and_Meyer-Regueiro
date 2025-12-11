"""
PAPER B: VISUALIZATIONS - CONDOM USE CORRELATES
================================================

Creates publication-ready figures for condom use analysis.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

# Set publication style
plt.rcParams['figure.dpi'] = 300
plt.rcParams['font.size'] = 11
plt.rcParams['font.family'] = 'Arial'
sns.set_palette("Set2")

# ============================================================================
# LOAD DATA
# ============================================================================

IN_FILE = '/Users/carlosmeyer2/IAS/Analysis/PaperB/Results/paperB_analytical_dataset.xlsx'
IN_MODELS = '/Users/carlosmeyer2/IAS/Analysis/PaperB/Results/paperB_regression_models.xlsx'
OUT_DIR = '/Users/carlosmeyer2/IAS/Analysis/PaperB/Results/'

print('='*80)
print('PAPER B: VISUALIZATIONS - CONDOM USE')
print('='*80)
print()

df = pd.read_excel(IN_FILE, engine='openpyxl')
print(f"Loaded {len(df)} participants")
print()

# ============================================================================
# FIGURE 1: CONDOM USE PATTERNS BY AGE AND PARTNERS (4-PANEL)
# ============================================================================

print('Creating Figure 1: Condom use patterns...')

fig = plt.figure(figsize=(16, 10))

# Panel A: Condom use by age group (stacked bar)
ax1 = plt.subplot(2, 2, 1)
condom_by_age = pd.crosstab(df['edad_grupo_lbl'], 
                             df['condom_use_lbl'],
                             normalize='index') * 100
condom_by_age = condom_by_age[['Always', 'Sometimes', 'Never']]  # Order
condom_by_age.plot(kind='bar', stacked=True, ax=ax1, 
                   color=['#2E86AB', '#F4A259', '#C73E1D'],
                   edgecolor='black', linewidth=0.5)
ax1.set_xlabel('Age Group', fontsize=12, fontweight='bold')
ax1.set_ylabel('Percentage (%)', fontsize=12, fontweight='bold')
ax1.set_title('A. Condom Use Frequency by Age Group', 
              fontsize=13, fontweight='bold', loc='left')
ax1.legend(title='Condom Use', bbox_to_anchor=(1.05, 1), loc='upper left')
ax1.set_xticklabels(ax1.get_xticklabels(), rotation=45, ha='right')
ax1.set_ylim([0, 100])

# Panel B: Condom use by number of partners
ax2 = plt.subplot(2, 2, 2)
partner_bins = pd.cut(df['partners_last_year'], 
                      bins=[0, 1, 2, 5, 100],
                      labels=['1', '2', '3-5', '6+'])
condom_by_partners = pd.crosstab(partner_bins, 
                                  df['condom_use_lbl'],
                                  normalize='index') * 100
condom_by_partners = condom_by_partners[['Always', 'Sometimes', 'Never']]
condom_by_partners.plot(kind='bar', stacked=True, ax=ax2,
                        color=['#2E86AB', '#F4A259', '#C73E1D'],
                        edgecolor='black', linewidth=0.5)
ax2.set_xlabel('Number of Partners (Last Year)', fontsize=12, fontweight='bold')
ax2.set_ylabel('Percentage (%)', fontsize=12, fontweight='bold')
ax2.set_title('B. Condom Use by Number of Sexual Partners', 
              fontsize=13, fontweight='bold', loc='left')
ax2.legend(title='Condom Use', bbox_to_anchor=(1.05, 1), loc='upper left')
ax2.set_xticklabels(ax2.get_xticklabels(), rotation=0)
ax2.set_ylim([0, 100])

# Panel C: Always condom use by age (line plot with CI)
ax3 = plt.subplot(2, 2, 3)
always_by_age = df.groupby('edad_grupo_lbl')['always_condom'].agg(['mean', 'std', 'count'])
always_by_age['se'] = always_by_age['std'] / np.sqrt(always_by_age['count'])
always_by_age['ci_lower'] = (always_by_age['mean'] - 1.96 * always_by_age['se']) * 100
always_by_age['ci_upper'] = (always_by_age['mean'] + 1.96 * always_by_age['se']) * 100
always_by_age['mean_pct'] = always_by_age['mean'] * 100

age_order = ['18-29', '30-39', '40-49', '50-59', '60-69', '70-79', '80+']
always_by_age = always_by_age.reindex(age_order)

ax3.plot(range(len(always_by_age)), always_by_age['mean_pct'], 
         marker='o', linewidth=2.5, markersize=8, color='#2E86AB')
ax3.fill_between(range(len(always_by_age)), 
                  always_by_age['ci_lower'], 
                  always_by_age['ci_upper'],
                  alpha=0.3, color='#2E86AB')
ax3.set_xticks(range(len(always_by_age)))
ax3.set_xticklabels(always_by_age.index, rotation=45, ha='right')
ax3.set_xlabel('Age Group', fontsize=12, fontweight='bold')
ax3.set_ylabel('Always Use Condoms (%)', fontsize=12, fontweight='bold')
ax3.set_title('C. Proportion Always Using Condoms by Age', 
              fontsize=13, fontweight='bold', loc='left')
ax3.grid(True, alpha=0.3)

# Panel D: Condom use by HIV knowledge groups
ax4 = plt.subplot(2, 2, 4)
# Create knowledge groups based on distribution
df['knowledge_group'] = pd.cut(df['hiv_knowledge_score'], 
                                bins=[-0.1, 3, 4, 5, 6],
                                labels=['0-3 (Low)', '4 (Med-Low)', '5 (Med-High)', '6 (High)'])
condom_by_knowledge = pd.crosstab(df['knowledge_group'], 
                                   df['condom_use_lbl'],
                                   normalize='index') * 100
condom_by_knowledge = condom_by_knowledge[['Always', 'Sometimes', 'Never']]
condom_by_knowledge.plot(kind='bar', stacked=True, ax=ax4,
                         color=['#2E86AB', '#F4A259', '#C73E1D'],
                         edgecolor='black', linewidth=0.5)
ax4.set_xlabel('HIV Knowledge Score Quartile', fontsize=12, fontweight='bold')
ax4.set_ylabel('Percentage (%)', fontsize=12, fontweight='bold')
ax4.set_title('D. Condom Use by HIV Knowledge Level', 
              fontsize=13, fontweight='bold', loc='left')
ax4.legend(title='Condom Use', bbox_to_anchor=(1.05, 1), loc='upper left')
ax4.set_xticklabels(ax4.get_xticklabels(), rotation=45, ha='right')
ax4.set_ylim([0, 100])

plt.tight_layout()
plt.savefig(OUT_DIR + 'figure1_condom_use_patterns.png', 
            dpi=300, bbox_inches='tight')
print(f"  Saved: figure1_condom_use_patterns.png")
print()

# ============================================================================
# FIGURE 2: FOREST PLOT OF REGRESSION RESULTS
# ============================================================================

print('Creating Figure 2: Regression results forest plot...')

# Load Model 4 results (full model with PrEP)
model4 = pd.read_excel(IN_MODELS, sheet_name='Model4_Add_PrEP', engine='openpyxl')
model4 = model4[model4['Variable'] != 'Intercept'].copy()

# Rename variables for display
var_labels = {
    'edad_grupo': 'Age group',
    'hiv_knowledge_score': 'HIV knowledge score',
    'partners_last_year': 'Partners (last year)',
    'any_sti': 'Any STI diagnosis',
    'tested_hiv_12mo': 'Tested HIV (12mo)',
    'knows_prep': 'PrEP awareness'
}
model4['Variable_label'] = model4['Variable'].map(var_labels)

fig, ax = plt.subplots(figsize=(10, 6))

# Plot OR with CI
y_pos = range(len(model4))
ax.errorbar(model4['OR'], y_pos, 
            xerr=[model4['OR'] - model4['CI_lower'], 
                  model4['CI_upper'] - model4['OR']],
            fmt='o', markersize=10, linewidth=2, capsize=5,
            color='#2E86AB', ecolor='#2E86AB', capthick=2)

# Reference line at OR=1
ax.axvline(1, color='black', linestyle='--', linewidth=1, alpha=0.5)

# Styling
ax.set_yticks(y_pos)
ax.set_yticklabels(model4['Variable_label'])
ax.set_xlabel('Odds Ratio (95% CI)', fontsize=12, fontweight='bold')
ax.set_title('Logistic Regression: Predictors of Always Using Condoms', 
             fontsize=13, fontweight='bold')
ax.grid(True, alpha=0.3, axis='x')

# Add OR values as text
for i, (or_val, ci_low, ci_high, p_val) in enumerate(zip(model4['OR'], 
                                                          model4['CI_lower'],
                                                          model4['CI_upper'],
                                                          model4['P_value'])):
    sig = '***' if p_val < 0.001 else '**' if p_val < 0.01 else '*' if p_val < 0.05 else ''
    ax.text(model4['OR'].max() + 0.1, i, 
            f'{or_val:.2f} ({ci_low:.2f}-{ci_high:.2f}) {sig}',
            va='center', fontsize=10)

plt.tight_layout()
plt.savefig(OUT_DIR + 'figure2_regression_forest_plot.png', 
            dpi=300, bbox_inches='tight')
print(f"  Saved: figure2_regression_forest_plot.png")
print()

# ============================================================================
# FIGURE 3: AGE-STRATIFIED EFFECTS
# ============================================================================

print('Creating Figure 3: Age-stratified effects...')

# Load age-stratified results
age_strat = pd.read_excel(IN_MODELS, sheet_name='Age_Stratified', engine='openpyxl')

fig = plt.figure(figsize=(14, 6))

# Panel A: HIV knowledge effect by age
ax1 = plt.subplot(1, 2, 1)
ax1.errorbar(range(len(age_strat)), age_strat['Knowledge_OR'],
             yerr=[age_strat['Knowledge_OR'] - age_strat['Knowledge_CI_lower'],
                   age_strat['Knowledge_CI_upper'] - age_strat['Knowledge_OR']],
             fmt='o-', markersize=10, linewidth=2.5, capsize=5,
             color='#2E86AB', ecolor='#2E86AB', capthick=2)
ax1.axhline(1, color='black', linestyle='--', linewidth=1, alpha=0.5)
ax1.set_xticks(range(len(age_strat)))
ax1.set_xticklabels(age_strat['Age_Group'], rotation=45, ha='right')
ax1.set_xlabel('Age Group', fontsize=12, fontweight='bold')
ax1.set_ylabel('Odds Ratio (95% CI)', fontsize=12, fontweight='bold')
ax1.set_title('A. HIV Knowledge Effect on Condom Use by Age', 
              fontsize=13, fontweight='bold', loc='left')
ax1.grid(True, alpha=0.3)

# Panel B: Number of partners effect by age
ax2 = plt.subplot(1, 2, 2)
ax2.errorbar(range(len(age_strat)), age_strat['Partners_OR'],
             yerr=[age_strat['Partners_OR'] - age_strat['Partners_CI_lower'],
                   age_strat['Partners_CI_upper'] - age_strat['Partners_OR']],
             fmt='s-', markersize=10, linewidth=2.5, capsize=5,
             color='#C73E1D', ecolor='#C73E1D', capthick=2)
ax2.axhline(1, color='black', linestyle='--', linewidth=1, alpha=0.5)
ax2.set_xticks(range(len(age_strat)))
ax2.set_xticklabels(age_strat['Age_Group'], rotation=45, ha='right')
ax2.set_xlabel('Age Group', fontsize=12, fontweight='bold')
ax2.set_ylabel('Odds Ratio (95% CI)', fontsize=12, fontweight='bold')
ax2.set_title('B. Number of Partners Effect on Condom Use by Age', 
              fontsize=13, fontweight='bold', loc='left')
ax2.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig(OUT_DIR + 'figure3_age_stratified_effects.png', 
            dpi=300, bbox_inches='tight')
print(f"  Saved: figure3_age_stratified_effects.png")
print()

# ============================================================================
# FIGURE 4: TESTING AND CONDOM USE
# ============================================================================

print('Creating Figure 4: HIV testing and condom use...')

fig = plt.figure(figsize=(14, 6))

# Panel A: Condom use by testing status
ax1 = plt.subplot(1, 2, 1)
test_labels = {0: 'Not tested', 1: 'Tested'}
df['tested_label'] = df['tested_hiv_12mo'].map(test_labels)
condom_by_test = pd.crosstab(df['tested_label'], 
                              df['condom_use_lbl'],
                              normalize='index') * 100
condom_by_test = condom_by_test[['Always', 'Sometimes', 'Never']]
condom_by_test.plot(kind='bar', stacked=True, ax=ax1,
                    color=['#2E86AB', '#F4A259', '#C73E1D'],
                    edgecolor='black', linewidth=0.5)
ax1.set_xlabel('HIV Testing Status (Last 12 Months)', fontsize=12, fontweight='bold')
ax1.set_ylabel('Percentage (%)', fontsize=12, fontweight='bold')
ax1.set_title('A. Condom Use by HIV Testing Status', 
              fontsize=13, fontweight='bold', loc='left')
ax1.legend(title='Condom Use')
ax1.set_xticklabels(ax1.get_xticklabels(), rotation=0)
ax1.set_ylim([0, 100])

# Panel B: Condom use by PrEP awareness
ax2 = plt.subplot(1, 2, 2)
prep_labels = {0: 'Unaware', 1: 'Aware'}
df['prep_label'] = df['knows_prep'].map(prep_labels)
condom_by_prep = pd.crosstab(df['prep_label'], 
                              df['condom_use_lbl'],
                              normalize='index') * 100
condom_by_prep = condom_by_prep[['Always', 'Sometimes', 'Never']]
condom_by_prep.plot(kind='bar', stacked=True, ax=ax2,
                    color=['#2E86AB', '#F4A259', '#C73E1D'],
                    edgecolor='black', linewidth=0.5)
ax2.set_xlabel('PrEP Awareness', fontsize=12, fontweight='bold')
ax2.set_ylabel('Percentage (%)', fontsize=12, fontweight='bold')
ax2.set_title('B. Condom Use by PrEP Awareness', 
              fontsize=13, fontweight='bold', loc='left')
ax2.legend(title='Condom Use')
ax2.set_xticklabels(ax2.get_xticklabels(), rotation=0)
ax2.set_ylim([0, 100])

plt.tight_layout()
plt.savefig(OUT_DIR + 'figure4_testing_prep_condom_use.png', 
            dpi=300, bbox_inches='tight')
print(f"  Saved: figure4_testing_prep_condom_use.png")
print()

# ============================================================================
# FIGURE 5: SIMPLIFIED 2-PANEL FOR MANUSCRIPT
# ============================================================================

print('Creating Figure 5: Simplified manuscript figure...')

fig = plt.figure(figsize=(14, 6))

# Panel A: Age gradient in condom use
ax1 = plt.subplot(1, 2, 1)
ax1.plot(range(len(always_by_age)), always_by_age['mean_pct'], 
         marker='o', linewidth=3, markersize=10, color='#2E86AB',
         label='Always use')
ax1.fill_between(range(len(always_by_age)), 
                  always_by_age['ci_lower'], 
                  always_by_age['ci_upper'],
                  alpha=0.3, color='#2E86AB')

# Add never use line
never_by_age = df.groupby('edad_grupo_lbl').apply(
    lambda x: ((x['condom_use_freq'] == 3).sum() / len(x)) * 100
).reindex(age_order)
ax1.plot(range(len(never_by_age)), never_by_age, 
         marker='s', linewidth=3, markersize=10, color='#C73E1D',
         label='Never use')

ax1.set_xticks(range(len(always_by_age)))
ax1.set_xticklabels(always_by_age.index, rotation=45, ha='right')
ax1.set_xlabel('Age Group', fontsize=13, fontweight='bold')
ax1.set_ylabel('Percentage (%)', fontsize=13, fontweight='bold')
ax1.set_title('Condom Use Across Age Groups', 
              fontsize=14, fontweight='bold')
ax1.legend(fontsize=11)
ax1.grid(True, alpha=0.3)

# Panel B: Multiple partners and condom use
ax2 = plt.subplot(1, 2, 2)
multi_partner_data = []
for partners in ['1', '2', '3-5', '6+']:
    if partners == '1':
        mask = df['partners_last_year'] == 1
    elif partners == '2':
        mask = df['partners_last_year'] == 2
    elif partners == '3-5':
        mask = (df['partners_last_year'] >= 3) & (df['partners_last_year'] <= 5)
    else:
        mask = df['partners_last_year'] >= 6
    
    subset = df[mask]
    always_pct = (subset['always_condom'] == 1).sum() / len(subset) * 100
    never_pct = (subset['condom_use_freq'] == 3).sum() / len(subset) * 100
    multi_partner_data.append({'Partners': partners, 
                                'Always': always_pct, 
                                'Never': never_pct})

mp_df = pd.DataFrame(multi_partner_data)
x = range(len(mp_df))
width = 0.35
ax2.bar([i - width/2 for i in x], mp_df['Always'], width, 
        label='Always use', color='#2E86AB', edgecolor='black')
ax2.bar([i + width/2 for i in x], mp_df['Never'], width, 
        label='Never use', color='#C73E1D', edgecolor='black')

ax2.set_xticks(x)
ax2.set_xticklabels(mp_df['Partners'])
ax2.set_xlabel('Number of Sexual Partners (Last Year)', fontsize=13, fontweight='bold')
ax2.set_ylabel('Percentage (%)', fontsize=13, fontweight='bold')
ax2.set_title('Condom Use by Number of Partners', 
              fontsize=14, fontweight='bold')
ax2.legend(fontsize=11)
ax2.grid(True, alpha=0.3, axis='y')

plt.tight_layout()
plt.savefig(OUT_DIR + 'figure5_manuscript_simple.png', 
            dpi=300, bbox_inches='tight')
print(f"  Saved: figure5_manuscript_simple.png")
print()

print('='*80)
print('VISUALIZATIONS COMPLETE')
print('='*80)
print()
print(f"Created 5 figures in: {OUT_DIR}")
print("  - Figure 1: 4-panel condom use patterns")
print("  - Figure 2: Regression forest plot")
print("  - Figure 3: Age-stratified effects")
print("  - Figure 4: Testing and PrEP associations")
print("  - Figure 5: Simplified 2-panel for manuscript")
