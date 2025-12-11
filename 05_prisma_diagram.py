"""
PAPERB: PRISMA FLOW DIAGRAM
============================

Creates a PRISMA-style flow diagram showing participant selection
from initial ENSSEX sample to final analysis sample.
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import numpy as np

# Set up figure
fig, ax = plt.subplots(figsize=(12, 14))
ax.set_xlim(0, 10)
ax.set_ylim(0, 16)
ax.axis('off')

# Define colors
box_color = '#E8F4F8'
exclude_color = '#FFE5E5'
final_color = '#D4EDDA'
text_color = '#2C3E50'
arrow_color = '#34495E'

# Box styling
box_style = "round,pad=0.1"
box_props = dict(boxstyle=box_style, facecolor=box_color, edgecolor='#2C3E50', linewidth=2)
exclude_props = dict(boxstyle=box_style, facecolor=exclude_color, edgecolor='#C0392B', linewidth=2)
final_props = dict(boxstyle=box_style, facecolor=final_color, edgecolor='#27AE60', linewidth=3)

# Arrow properties
arrow_props = dict(arrowstyle='->', lw=2.5, color=arrow_color)

# =============================================================================
# ENROLLMENT
# =============================================================================

y_pos = 15

# Initial enrollment box
enrollment_text = "ENSSEX National Survey 2024\nTotal participants enrolled\nn = 20,392"
ax.text(5, y_pos, enrollment_text, ha='center', va='center', fontsize=13, 
        fontweight='bold', bbox=box_props, color=text_color)

# Arrow down
ax.annotate('', xy=(5, y_pos-1), xytext=(5, y_pos-0.5),
            arrowprops=arrow_props)

# =============================================================================
# SCREENING 1: SEXUAL ACTIVITY
# =============================================================================

y_pos = 13

# Sexually active assessment box
screening1_text = "Assessed for sexual activity\nin last 12 months"
ax.text(5, y_pos, screening1_text, ha='center', va='center', fontsize=12,
        bbox=box_props, color=text_color)

# Arrow down
ax.annotate('', xy=(5, y_pos-1), xytext=(5, y_pos-0.5),
            arrowprops=arrow_props)

# Exclusion box 1
exclude1_text = "Excluded: No sexual partners\nin last year (P71 = 0 or missing)\nn = 7,517"
ax.text(8.5, y_pos, exclude1_text, ha='center', va='center', fontsize=11,
        bbox=exclude_props, color='#C0392B')

# Arrow to exclusion
ax.annotate('', xy=(8.5, y_pos), xytext=(6, y_pos),
            arrowprops=dict(arrowstyle='->', lw=1.5, color='#C0392B'))

# =============================================================================
# SCREENING 2: CONDOM USE DATA
# =============================================================================

y_pos = 11

# After sexual activity filter
remaining1_text = "Sexually active participants\nn = 12,875"
ax.text(5, y_pos, remaining1_text, ha='center', va='center', fontsize=12,
        bbox=box_props, color=text_color)

# Arrow down
ax.annotate('', xy=(5, y_pos-1), xytext=(5, y_pos-0.5),
            arrowprops=arrow_props)

# Exclusion box 2
exclude2_text = "Excluded: Missing or invalid\ncondom use data (P73)\nn = 110"
ax.text(8.5, y_pos, exclude2_text, ha='center', va='center', fontsize=11,
        bbox=exclude_props, color='#C0392B')

# Arrow to exclusion
ax.annotate('', xy=(8.5, y_pos), xytext=(6, y_pos),
            arrowprops=dict(arrowstyle='->', lw=1.5, color='#C0392B'))

# =============================================================================
# SCREENING 3: AGE DATA
# =============================================================================

y_pos = 9

# After condom use filter
remaining2_text = "Valid condom use data\nn = 12,765"
ax.text(5, y_pos, remaining2_text, ha='center', va='center', fontsize=12,
        bbox=box_props, color=text_color)

# Arrow down
ax.annotate('', xy=(5, y_pos-1), xytext=(5, y_pos-0.5),
            arrowprops=arrow_props)

# Exclusion box 3
exclude3_text = "Excluded: Missing age data\nn = 0"
ax.text(8.5, y_pos, exclude3_text, ha='center', va='center', fontsize=11,
        bbox=exclude_props, color='#C0392B')

# Arrow to exclusion
ax.annotate('', xy=(8.5, y_pos), xytext=(6, y_pos),
            arrowprops=dict(arrowstyle='->', lw=1.5, color='#C0392B'))

# =============================================================================
# FINAL SAMPLE FOR ANALYSIS
# =============================================================================

y_pos = 7

# Final analytical sample
final_text = "FINAL ANALYTICAL SAMPLE\nn = 12,765\n(62.6% of total enrolled)"
ax.text(5, y_pos, final_text, ha='center', va='center', fontsize=13,
        fontweight='bold', bbox=final_props, color='#27AE60')

# Arrow down
ax.annotate('', xy=(5, y_pos-1), xytext=(5, y_pos-0.5),
            arrowprops=dict(arrowstyle='->', lw=3, color='#27AE60'))

# =============================================================================
# SAMPLE CHARACTERISTICS
# =============================================================================

y_pos = 5

# Sample characteristics box
characteristics_text = """SAMPLE CHARACTERISTICS

Demographics:
• Age: 18-89 years (median: 40 years)
• Age groups: 18-29 (26%), 30-39 (23%), 40-49 (18%),
  50-59 (16%), 60-69 (11%), 70-79 (5%), 80+ (1%)

Condom Use:
• Always: 2,236 (17.5%)
• Sometimes: 2,620 (20.5%)
• Never: 7,909 (62.0%)

Sexual Partners (last year):
• Mean: 1.50 partners (SD = 1.47)
• Multiple partners (≥2): 2,234 (17.4%)

HIV Knowledge & Testing:
• Mean knowledge score: 4.31/6 (SD = 1.45)
• Tested HIV (12mo): 4,004 (31.4%)
• PrEP awareness: 1,971 (15.4%)

STI Diagnosis:
• Any STI: 885 (6.9%)"""

ax.text(5, y_pos-2.5, characteristics_text, ha='center', va='top', fontsize=10,
        bbox=dict(boxstyle='round,pad=0.3', facecolor='#F8F9FA', 
                  edgecolor='#6C757D', linewidth=1.5),
        color=text_color, linespacing=1.5, family='monospace')

# =============================================================================
# EXCLUSIONS SUMMARY
# =============================================================================

y_pos = 0.8

# Total exclusions summary
exclusion_summary = """TOTAL EXCLUSIONS: 7,627 (37.4%)
• No sexual activity: 7,517 (36.9%)
• Missing condom data: 110 (0.5%)
• Missing age: 0 (0.0%)"""

ax.text(5, y_pos, exclusion_summary, ha='center', va='center', fontsize=10,
        bbox=dict(boxstyle='round,pad=0.2', facecolor='#FFF3CD', 
                  edgecolor='#856404', linewidth=1.5),
        color='#856404', fontweight='bold', linespacing=1.5)

# =============================================================================
# TITLE
# =============================================================================

fig.suptitle('PRISMA Flow Diagram: Participant Selection for PaperB\nCondom Use Correlates Analysis', 
             fontsize=16, fontweight='bold', y=0.98, color=text_color)

# Add PRISMA note
ax.text(5, -0.5, 'Based on PRISMA 2020 guidelines for reporting systematic reviews', 
        ha='center', va='center', fontsize=9, style='italic', color='#7F8C8D')

plt.tight_layout()
plt.savefig('/Users/carlosmeyer2/IAS/Analysis/PaperB/Results/prisma_flowchart.png', 
            dpi=300, bbox_inches='tight', facecolor='white')
print("PRISMA diagram saved: /Users/carlosmeyer2/IAS/Analysis/PaperB/Results/prisma_flowchart.png")

# =============================================================================
# CREATE DETAILED VERSION WITH NUMBERS
# =============================================================================

fig2, ax2 = plt.subplots(figsize=(10, 12))
ax2.set_xlim(0, 10)
ax2.set_ylim(0, 14)
ax2.axis('off')

y = 13

# Enrollment
ax2.text(5, y, "Total ENSSEX participants\nn = 20,392", ha='center', va='center', 
         fontsize=12, fontweight='bold', bbox=box_props)
ax2.annotate('', xy=(5, y-0.8), xytext=(5, y-0.4), arrowprops=arrow_props)

y -= 1.5

# Screen 1
ax2.text(5, y, "Sexually active in last year\n(P71 > 0)\nn = 12,875 (63.1%)", 
         ha='center', va='center', fontsize=11, bbox=box_props)
ax2.text(8.5, y, "Excluded\nn = 7,517\n(36.9%)", ha='center', va='center', 
         fontsize=10, bbox=exclude_props, color='#C0392B')
ax2.annotate('', xy=(8.5, y), xytext=(6, y), 
             arrowprops=dict(arrowstyle='->', lw=1.5, color='#C0392B'))
ax2.annotate('', xy=(5, y-0.8), xytext=(5, y-0.4), arrowprops=arrow_props)

y -= 1.5

# Screen 2
ax2.text(5, y, "Valid condom use data\n(P73 = 1, 2, or 3)\nn = 12,765 (62.6%)", 
         ha='center', va='center', fontsize=11, bbox=box_props)
ax2.text(8.5, y, "Excluded\nn = 110\n(0.5%)", ha='center', va='center', 
         fontsize=10, bbox=exclude_props, color='#C0392B')
ax2.annotate('', xy=(8.5, y), xytext=(6, y), 
             arrowprops=dict(arrowstyle='->', lw=1.5, color='#C0392B'))
ax2.annotate('', xy=(5, y-0.8), xytext=(5, y-0.4), arrowprops=arrow_props)

y -= 1.5

# Screen 3
ax2.text(5, y, "Valid age data\nn = 12,765 (62.6%)", 
         ha='center', va='center', fontsize=11, bbox=box_props)
ax2.text(8.5, y, "Excluded\nn = 0\n(0.0%)", ha='center', va='center', 
         fontsize=10, bbox=exclude_props, color='#C0392B')
ax2.annotate('', xy=(8.5, y), xytext=(6, y), 
             arrowprops=dict(arrowstyle='->', lw=1.5, color='#C0392B'))
ax2.annotate('', xy=(5, y-0.8), xytext=(5, y-0.4), 
             arrowprops=dict(arrowstyle='->', lw=3, color='#27AE60'))

y -= 1.5

# Final
ax2.text(5, y, "FINAL ANALYTICAL SAMPLE\nn = 12,765\n62.6% retention", 
         ha='center', va='center', fontsize=13, fontweight='bold', bbox=final_props,
         color='#27AE60')

y -= 2

# Breakdown by analysis
breakdown_text = """AVAILABLE DATA FOR ANALYSES:

• Bivariate associations: n = 12,765 (100%)
• Regression Model 1-2: n = 12,765 (100%)
• Regression Model 3 (+ STI): n = 12,513 (98.0%)
• Regression Model 4 (+ PrEP): n = 11,806 (92.5%)
• Age-stratified models: n = 12,765 (by age group)"""

ax2.text(5, y, breakdown_text, ha='center', va='center', fontsize=10,
         bbox=dict(boxstyle='round,pad=0.3', facecolor='#E8F8F5', 
                   edgecolor='#27AE60', linewidth=1.5),
         linespacing=1.6, family='monospace')

fig2.suptitle('PaperB Participant Flow: Simplified View', 
              fontsize=15, fontweight='bold', y=0.97)

plt.tight_layout()
plt.savefig('/Users/carlosmeyer2/IAS/Analysis/PaperB/Results/prisma_flowchart_simple.png', 
            dpi=300, bbox_inches='tight', facecolor='white')
print("Simple PRISMA diagram saved: /Users/carlosmeyer2/IAS/Analysis/PaperB/Results/prisma_flowchart_simple.png")

print("\nPRISMA diagrams created successfully!")
print("  - Detailed version: prisma_flowchart.png")
print("  - Simple version: prisma_flowchart_simple.png")
