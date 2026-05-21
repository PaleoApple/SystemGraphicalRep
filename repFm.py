import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.patheffects as path_effects
import numpy as np

class ProteinSchematic:
    def __init__(self):
        self.fig, self.ax = plt.subplots(figsize=(6, 2), facecolor='none')
        self.ax.set_xlim(-10, 260)
        self.ax.set_ylim(-10, 10)
        self.ax.patch.set_facecolor('none')
        self.ax.axis('off')

    def _draw_wiggle(self, start_x, num_res, color, is_highlighted, alpha):
        x = np.linspace(start_x, start_x + num_res, num_res * 2)
        y = 0.8 * np.sin(2 * np.pi * x / 6)
        
        effects = [path_effects.withStroke(linewidth=8, foreground="gold", alpha=0.6)] if is_highlighted else []
        
        self.ax.plot(x, y, color=color, lw=2.5, solid_capstyle='round', 
                     zorder=2, alpha=alpha, path_effects=effects)
        return x[-1]

    def _draw_globular_domain(self, x_start, width, height, color, label, is_highlighted, alpha):
        effects = [path_effects.withStroke(linewidth=10, foreground="gold", alpha=0.6)] if is_highlighted else []

        box = mpatches.FancyBboxPatch(
            (x_start, -height/2), width, height,
            boxstyle="round,pad=2,rounding_size=3",
            facecolor=color, edgecolor='black', lw=1.5, zorder=3, alpha=alpha
        )
#        box.set_path_effects(effects)
        self.ax.add_patch(box)
        
        self.ax.text(x_start + width/2, 0, label, color='white', 
                     weight='bold', ha='center', va='center', fontsize=22, alpha=alpha)

    def render(self, highlight=None, save_name=None):
        # Convert single string to list for uniform handling
        if isinstance(highlight, str):
            highlight = [highlight]
        elif highlight is None:
            highlight = []

        # Determine if everything should be bright (standard view)
        show_all = len(highlight) == 0

        # Highlighting logic for each segment
        h1 = 'idr1' in highlight
        h2 = 'idr2' in highlight
        h3 = 'headpiece' in highlight

        # Opacity: 1.0 if it's highlighted OR if nothing is highlighted
        a1 = 1.0 if (h1 or show_all) else 0.05
        a2 = 1.0 if (h2 or show_all) else 0.05
        a3 = 1.0 if (h3 or show_all) else 0.05

        # Draw components
        end1 = self._draw_wiggle(0, 147, 'royalblue', h1, a1)
        end2 = self._draw_wiggle(end1, 43, 'crimson', h2, a2)
        self._draw_globular_domain(end2 + 1, 30, 4, '#555555', "HP", h3, a3)

        if save_name:
            plt.savefig(save_name, transparent=True, dpi=300, bbox_inches='tight')
        
        plt.show()

# --- Execution ---
viz = ProteinSchematic()

# This will now highlight BOTH the red wiggle and the HP domain
viz.render(highlight=['idr2', 'headpiece'], save_name='c_term_focus.png')
