import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, ArrowStyle
from matplotlib.path import Path

# Define the start, middle, and end points for the arrow with a 90-degree kink
start = (0, 1)
middle = (0, 0)
end = (1, 0)

style = "Simple, tail_width=0.5, head_width=4, head_length=8"
kw = dict(arrowstyle=style, color="k")
# Create the FancyArrowPatch object with the specified path
arrow = FancyArrowPatch(
    path=Path([start, middle, end]),
    arrowstyle=ArrowStyle.CurveB(head_length=4.0, head_width=4.0),
    connectionstyle="angle3,angleA=90,angleB=0",
)

# Plot the arrow
fig, ax = plt.subplots()
ax.add_patch(arrow)
ax.set_xlim(-1, 2)
ax.set_ylim(-1, 2)
ax.set_aspect("equal")
plt.show()
