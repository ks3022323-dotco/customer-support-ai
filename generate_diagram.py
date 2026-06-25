# generate_diagram.py
# Generates the LangGraph workflow diagram as PNG

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

fig, ax = plt.subplots(1, 1, figsize=(14, 20))
ax.set_xlim(0, 10)
ax.set_ylim(0, 22)
ax.axis('off')
ax.set_facecolor('#f8f9fa')
fig.patch.set_facecolor('#f8f9fa')

def draw_box(ax, x, y, w, h, text, color='#4A90D9', text_color='white', fontsize=9):
    box = mpatches.FancyBboxPatch((x - w/2, y - h/2), w, h,
                                   boxstyle="round,pad=0.15",
                                   facecolor=color, edgecolor='#2c3e50', linewidth=2)
    ax.add_patch(box)
    ax.text(x, y, text, ha='center', va='center', fontsize=fontsize,
            color=text_color, fontweight='bold', multialignment='center')

def draw_arrow(ax, x1, y1, x2, y2, color='#2c3e50'):
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle="->", color=color, lw=2))

# ── Title ─────────────────────────────────────
ax.text(5, 21.3, 'ABC Technologies', ha='center', fontsize=16,
        fontweight='bold', color='#2c3e50')
ax.text(5, 20.8, 'AI-Powered Customer Support — LangGraph Workflow',
        ha='center', fontsize=12, color='#555')

# ── Nodes ─────────────────────────────────────
draw_box(ax, 5, 20.0, 4, 0.7, 'Customer Query Input', '#2c3e50')
draw_box(ax, 5, 18.8, 4, 0.7, 'Intent Classification Node\n(Task 3)', '#2980b9')
draw_box(ax, 5, 17.5, 4, 0.7, 'RAG Knowledge Retrieval\n(Task 6)', '#8e44ad')

# Department agents
draw_box(ax, 1.2, 15.5, 2.0, 0.8, 'Sales\nAgent', '#27ae60')
draw_box(ax, 3.5, 15.5, 2.0, 0.8, 'Technical\nAgent', '#e67e22')
draw_box(ax, 6.0, 15.5, 2.0, 0.8, 'Billing\nAgent', '#c0392b')
draw_box(ax, 8.5, 15.5, 2.0, 0.8, 'Account\nAgent', '#16a085')

# Memory
draw_box(ax, 5, 14.0, 4, 0.7, 'Memory Recall Node\n(SQLite — Task 7)', '#7f8c8d')

# Human approval
draw_box(ax, 5, 12.5, 4, 0.8, '🔴 Human Supervisor Approval\n(HITL — Task 8)', '#e74c3c')

# Supervisor
draw_box(ax, 5, 11.0, 4, 0.7, 'Supervisor Review Node\n(Task 9)', '#2980b9')

# Final response
draw_box(ax, 5, 9.5, 4, 0.7, 'Generate Final Response\n(Task 10)', '#27ae60')

# SQLite storage
draw_box(ax, 5, 8.0, 4, 0.7, 'SQLite Memory Storage\n(memory.db)', '#95a5a6')

# END
draw_box(ax, 5, 6.5, 4, 0.7, '✅ END — Response to Customer', '#2c3e50')

# ── Arrows ────────────────────────────────────
draw_arrow(ax, 5, 19.65, 5, 19.15)
draw_arrow(ax, 5, 18.45, 5, 17.85)

# RAG to agents
for x in [1.2, 3.5, 6.0, 8.5]:
    draw_arrow(ax, 5, 17.15, x, 15.9)

# Agents to human approval
for x in [1.2, 3.5, 6.0, 8.5]:
    draw_arrow(ax, x, 15.1, 5, 12.9)

# Memory path from intent classification
ax.annotate("", xy=(5, 14.35), xytext=(5, 18.45),
            arrowprops=dict(arrowstyle="->", color='#7f8c8d', lw=1.5,
                           connectionstyle="arc3,rad=0.5"))
ax.text(7.8, 16.3, 'Memory\nPath', fontsize=8, color='#7f8c8d',
        style='italic', ha='center')

draw_arrow(ax, 5, 12.1, 5, 11.35)
draw_arrow(ax, 5, 10.65, 5, 9.85)
draw_arrow(ax, 5, 9.15, 5, 8.35)
draw_arrow(ax, 5, 7.65, 5, 6.85)

# ── Labels ────────────────────────────────────
ax.text(6.2, 16.6, 'Route by\nIntent', fontsize=8,
        color='#2980b9', style='italic')
ax.text(6.2, 13.2, 'Needs\nApproval?', fontsize=8,
        color='#e74c3c', style='italic')

# ── Legend ────────────────────────────────────
legend_items = [
    mpatches.Patch(color='#2980b9', label='Classification / Supervisor'),
    mpatches.Patch(color='#8e44ad', label='RAG Pipeline'),
    mpatches.Patch(color='#27ae60', label='Sales / Final Response'),
    mpatches.Patch(color='#e67e22', label='Technical Support'),
    mpatches.Patch(color='#c0392b', label='Billing Support'),
    mpatches.Patch(color='#16a085', label='Account Support'),
    mpatches.Patch(color='#e74c3c', label='Human-in-the-Loop'),
    mpatches.Patch(color='#7f8c8d', label='Memory / SQLite'),
    mpatches.Patch(color='#2c3e50', label='Start / End'),
]
ax.legend(handles=legend_items, loc='lower left',
          fontsize=8, title='Node Types', title_fontsize=9)

plt.tight_layout()
plt.savefig('diagrams/langgraph_workflow.png', dpi=150, bbox_inches='tight')
print("✅ Diagram saved to diagrams/langgraph_workflow.png")
plt.show()