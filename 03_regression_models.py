"""
PAPER B: REGRESSION MODELS PREDICTING CONDOM USE
=================================================

Logistic regression models with condom use as outcome.
Tests associations with age, HIV knowledge, partners, STI, and testing behavior.
"""

import pandas as pd
import numpy as np
import statsmodels.api as sm
from statsmodels.formula.api import logit
import warnings
warnings.filterwarnings('ignore')

# ============================================================================
# LOAD DATA
# ============================================================================

IN_FILE = '/Users/carlosmeyer2/IAS/Analysis/PaperB/Results/paperB_analytical_dataset.xlsx'
OUT_DIR = '/Users/carlosmeyer2/IAS/Analysis/PaperB/Results/'

print('='*80)
print('PAPER B: REGRESSION MODELS - CONDOM USE PREDICTORS')
print('='*80)
print()

df = pd.read_excel(IN_FILE, engine='openpyxl')
print(f"Loaded {len(df)} participants")
print()

# ============================================================================
# MODEL 1: AGE AND HIV KNOWLEDGE → ALWAYS CONDOM USE
# ============================================================================

print('='*80)
print('MODEL 1: Age + HIV Knowledge → Always Condom Use')
print('='*80)
print()

# Prepare data
model1_data = df[['always_condom', 'edad_grupo', 'hiv_knowledge_score']].dropna()
print(f"Sample size: {len(model1_data)}")

# Fit model
formula1 = 'always_condom ~ edad_grupo + hiv_knowledge_score'
model1 = logit(formula1, data=model1_data).fit(disp=False)

print(model1.summary())
print()

# Extract results
model1_results = pd.DataFrame({
    'Variable': model1.params.index,
    'OR': np.exp(model1.params),
    'CI_lower': np.exp(model1.conf_int()[0]),
    'CI_upper': np.exp(model1.conf_int()[1]),
    'P_value': model1.pvalues,
    'Coef': model1.params
})
print("Odds Ratios:")
print(model1_results)
print()

# ============================================================================
# MODEL 2: ADD NUMBER OF PARTNERS
# ============================================================================

print('='*80)
print('MODEL 2: Age + Knowledge + Number of Partners → Always Condom Use')
print('='*80)
print()

model2_data = df[['always_condom', 'edad_grupo', 'hiv_knowledge_score', 
                   'partners_last_year']].dropna()
print(f"Sample size: {len(model2_data)}")

formula2 = 'always_condom ~ edad_grupo + hiv_knowledge_score + partners_last_year'
model2 = logit(formula2, data=model2_data).fit(disp=False)

print(model2.summary())
print()

model2_results = pd.DataFrame({
    'Variable': model2.params.index,
    'OR': np.exp(model2.params),
    'CI_lower': np.exp(model2.conf_int()[0]),
    'CI_upper': np.exp(model2.conf_int()[1]),
    'P_value': model2.pvalues,
    'Coef': model2.params
})
print("Odds Ratios:")
print(model2_results)
print()

# ============================================================================
# MODEL 3: ADD STI DIAGNOSIS AND HIV TESTING
# ============================================================================

print('='*80)
print('MODEL 3: Full Model with STI and Testing Variables')
print('='*80)
print()

model3_data = df[['always_condom', 'edad_grupo', 'hiv_knowledge_score', 
                   'partners_last_year', 'any_sti', 'tested_hiv_12mo']].dropna()
print(f"Sample size: {len(model3_data)}")

formula3 = '''always_condom ~ edad_grupo + hiv_knowledge_score + 
              partners_last_year + any_sti + tested_hiv_12mo'''
model3 = logit(formula3, data=model3_data).fit(disp=False)

print(model3.summary())
print()

model3_results = pd.DataFrame({
    'Variable': model3.params.index,
    'OR': np.exp(model3.params),
    'CI_lower': np.exp(model3.conf_int()[0]),
    'CI_upper': np.exp(model3.conf_int()[1]),
    'P_value': model3.pvalues,
    'Coef': model3.params
})
print("Odds Ratios:")
print(model3_results)
print()

# ============================================================================
# MODEL 4: ADD PREP AWARENESS
# ============================================================================

print('='*80)
print('MODEL 4: Full Model + PrEP Awareness')
print('='*80)
print()

model4_data = df[['always_condom', 'edad_grupo', 'hiv_knowledge_score', 
                   'partners_last_year', 'any_sti', 'tested_hiv_12mo',
                   'knows_prep']].dropna()
print(f"Sample size: {len(model4_data)}")

formula4 = '''always_condom ~ edad_grupo + hiv_knowledge_score + 
              partners_last_year + any_sti + tested_hiv_12mo + knows_prep'''
model4 = logit(formula4, data=model4_data).fit(disp=False)

print(model4.summary())
print()

model4_results = pd.DataFrame({
    'Variable': model4.params.index,
    'OR': np.exp(model4.params),
    'CI_lower': np.exp(model4.conf_int()[0]),
    'CI_upper': np.exp(model4.conf_int()[1]),
    'P_value': model4.pvalues,
    'Coef': model4.params
})
print("Odds Ratios:")
print(model4_results)
print()

# ============================================================================
# MODEL 5: AGE INTERACTION WITH HIV KNOWLEDGE
# ============================================================================

print('='*80)
print('MODEL 5: Age × HIV Knowledge Interaction')
print('='*80)
print()

model5_data = df[['always_condom', 'edad_grupo', 'hiv_knowledge_score', 
                   'partners_last_year']].dropna()
print(f"Sample size: {len(model5_data)}")

formula5 = '''always_condom ~ edad_grupo + hiv_knowledge_score + 
              partners_last_year + edad_grupo:hiv_knowledge_score'''
model5 = logit(formula5, data=model5_data).fit(disp=False)

print(model5.summary())
print()

model5_results = pd.DataFrame({
    'Variable': model5.params.index,
    'OR': np.exp(model5.params),
    'CI_lower': np.exp(model5.conf_int()[0]),
    'CI_upper': np.exp(model5.conf_int()[1]),
    'P_value': model5.pvalues,
    'Coef': model5.params
})
print("Odds Ratios:")
print(model5_results)
print()

# Test interaction significance
lr_test = -2 * (model2.llf - model5.llf)
from scipy.stats import chi2
p_interaction = 1 - chi2.cdf(lr_test, 1)
print(f"Likelihood ratio test for interaction:")
print(f"  χ² = {lr_test:.2f}, p = {p_interaction:.4f}")
print()

# ============================================================================
# AGE-STRATIFIED MODELS
# ============================================================================

print('='*80)
print('AGE-STRATIFIED MODELS')
print('='*80)
print()

age_stratified_results = []

age_groups = df['edad_grupo_lbl'].unique()
age_groups = sorted([a for a in age_groups if pd.notna(a)])

for age in age_groups:
    age_data = df[df['edad_grupo_lbl'] == age][['always_condom', 
                                                  'hiv_knowledge_score',
                                                  'partners_last_year']].dropna()
    
    if len(age_data) >= 30:  # Minimum sample size
        formula_age = 'always_condom ~ hiv_knowledge_score + partners_last_year'
        model_age = logit(formula_age, data=age_data).fit(disp=False)
        
        # Extract knowledge OR
        knowledge_or = np.exp(model_age.params['hiv_knowledge_score'])
        knowledge_ci_lower = np.exp(model_age.conf_int().loc['hiv_knowledge_score', 0])
        knowledge_ci_upper = np.exp(model_age.conf_int().loc['hiv_knowledge_score', 1])
        knowledge_p = model_age.pvalues['hiv_knowledge_score']
        
        # Extract partners OR
        partners_or = np.exp(model_age.params['partners_last_year'])
        partners_ci_lower = np.exp(model_age.conf_int().loc['partners_last_year', 0])
        partners_ci_upper = np.exp(model_age.conf_int().loc['partners_last_year', 1])
        partners_p = model_age.pvalues['partners_last_year']
        
        age_stratified_results.append({
            'Age_Group': age,
            'N': len(age_data),
            'Knowledge_OR': knowledge_or,
            'Knowledge_CI_lower': knowledge_ci_lower,
            'Knowledge_CI_upper': knowledge_ci_upper,
            'Knowledge_P': knowledge_p,
            'Partners_OR': partners_or,
            'Partners_CI_lower': partners_ci_lower,
            'Partners_CI_upper': partners_ci_upper,
            'Partners_P': partners_p
        })
        
        print(f"\n{age} (N={len(age_data)}):")
        print(f"  HIV Knowledge: OR={knowledge_or:.3f} (95% CI: {knowledge_ci_lower:.3f}-{knowledge_ci_upper:.3f}), p={knowledge_p:.4f}")
        print(f"  Partners: OR={partners_or:.3f} (95% CI: {partners_ci_lower:.3f}-{partners_ci_upper:.3f}), p={partners_p:.4f}")

age_strat_df = pd.DataFrame(age_stratified_results)
print()

# ============================================================================
# SAVE ALL RESULTS
# ============================================================================

print('='*80)
print('SAVING RESULTS')
print('='*80)
print()

with pd.ExcelWriter(OUT_DIR + 'paperB_regression_models.xlsx', 
                    engine='openpyxl') as writer:
    
    model1_results.to_excel(writer, sheet_name='Model1_Age_Knowledge', index=False)
    print("  Saved: Model 1 (Age + Knowledge)")
    
    model2_results.to_excel(writer, sheet_name='Model2_Add_Partners', index=False)
    print("  Saved: Model 2 (Add Partners)")
    
    model3_results.to_excel(writer, sheet_name='Model3_Add_STI_Testing', index=False)
    print("  Saved: Model 3 (Add STI + Testing)")
    
    model4_results.to_excel(writer, sheet_name='Model4_Add_PrEP', index=False)
    print("  Saved: Model 4 (Add PrEP)")
    
    model5_results.to_excel(writer, sheet_name='Model5_Interaction', index=False)
    print("  Saved: Model 5 (Age × Knowledge)")
    
    age_strat_df.to_excel(writer, sheet_name='Age_Stratified', index=False)
    print("  Saved: Age-stratified models")
    
    # Model comparison summary
    model_comparison = pd.DataFrame({
        'Model': ['Model 1', 'Model 2', 'Model 3', 'Model 4', 'Model 5'],
        'Variables': [
            'Age + Knowledge',
            'Age + Knowledge + Partners',
            'Age + Knowledge + Partners + STI + Testing',
            'Age + Knowledge + Partners + STI + Testing + PrEP',
            'Age + Knowledge + Partners + Age×Knowledge'
        ],
        'N': [len(model1_data), len(model2_data), len(model3_data), 
              len(model4_data), len(model5_data)],
        'Log_Likelihood': [model1.llf, model2.llf, model3.llf, model4.llf, model5.llf],
        'AIC': [model1.aic, model2.aic, model3.aic, model4.aic, model5.aic],
        'BIC': [model1.bic, model2.bic, model3.bic, model4.bic, model5.bic],
        'Pseudo_R2': [model1.prsquared, model2.prsquared, model3.prsquared, 
                      model4.prsquared, model5.prsquared]
    })
    model_comparison.to_excel(writer, sheet_name='Model_Comparison', index=False)
    print("  Saved: Model comparison")

print()
print('='*80)
print('REGRESSION MODELS COMPLETE')
print('='*80)
print()
print(f"Results saved to: {OUT_DIR}paperB_regression_models.xlsx")
print()
print("KEY FINDINGS:")
print(f"  - HIV knowledge effect on condom use: OR = {model4_results[model4_results['Variable']=='hiv_knowledge_score']['OR'].values[0]:.3f}")
print(f"  - Partners effect: OR = {model4_results[model4_results['Variable']=='partners_last_year']['OR'].values[0]:.3f}")
print(f"  - Age effect: OR = {model4_results[model4_results['Variable']=='edad_grupo']['OR'].values[0]:.3f}")
if 'tested_hiv_12mo' in model4_results['Variable'].values:
    print(f"  - Testing effect: OR = {model4_results[model4_results['Variable']=='tested_hiv_12mo']['OR'].values[0]:.3f}")
if 'knows_prep' in model4_results['Variable'].values:
    print(f"  - PrEP awareness: OR = {model4_results[model4_results['Variable']=='knows_prep']['OR'].values[0]:.3f}")
