"""
DIGM 131 - Assignment 2: Procedural Pattern Generator
======================================================

OBJECTIVE:
    Use loops and conditionals to generate a repeating pattern of 3D objects
    in Maya. You will practice nested loops, conditional logic, and
    mathematical positioning.

REQUIREMENTS:
    1. Use a nested loop (a loop inside a loop) to create a grid or pattern
       of objects.
    2. Include at least one conditional (if/elif/else) that changes an
       object's properties (type, size, color, or position offset) based
       on its row, column, or index.
    3. Generate at least 25 objects total (e.g., a 5x5 grid).
    4. Comment every major block of code explaining your logic.

GRADING CRITERIA:
    - [25%] Nested loop correctly generates a grid/pattern of objects.
    - [25%] Conditional logic visibly changes object properties based on
            position or index.
    - [20%] At least 25 objects are generated.
    - [15%] Code is well-commented with clear explanations.
    - [15%] Pattern is visually interesting and intentional.

TIPS:
    - A 5x5 grid gives you 25 objects. A 6x6 grid gives you 36.
    - Use the loop variables (row, col) to calculate X and Z positions.
    - The modulo operator (%) is great for alternating patterns:
          if col % 2 == 0:    # every other column
    - You can vary: primitive type, height, width, position offset, etc.

COMMENT HABITS (practice these throughout the course):
    - Add a comment before each logical section explaining its purpose.
    - Use inline comments sparingly and only when the code is not obvious.
    - Keep comments up to date -- if you change the code, update the comment.
"""

import maya.cmds as cmds

# Clear the scene so I start fresh every time I run the script
cmds.file(new=True, force=True)

def generate_pattern():
    """Generate a 5x5 grid of rectangular prisms, with red ones on the diagonal."""

    # --- Configuration variables ---
    num_rows = 5        # Number of rows in the grid
    num_cols = 5        # Number of columns in the grid
    spacing = 3.0       # Space between each object

    # --- Nested loop: iterate over every row and column ---
    for row in range(num_rows):
        for col in range(num_cols):

            # Calculate the X and Z position for this object
            x_pos = col * spacing
            z_pos = row * spacing

            # --- Create a rectangular prism (polyCube with custom size) ---
            # polyCube returns a list; index [0] is the shape's name
            cube = cmds.polyCube(width=1.5, height=2.5, depth=1.0)[0]

            # Move the cube to its grid position
            cmds.move(x_pos, 0, z_pos, cube)

            # --- Conditional: make diagonal prisms red ---
            # The diagonal is where the row index equals the column index
            if row == col:
                # Create a new red Lambert material
                red_material = cmds.shadingNode('lambert', asShader=True)
                cmds.setAttr(red_material + '.color', 1, 0, 0, type='double3')

                # Connect the material to a shading group, then assign it
                shading_group = cmds.sets(renderable=True, noSurfaceShader=True,
                                          empty=True)
                cmds.connectAttr(red_material + '.outColor',
                                 shading_group + '.surfaceShader', force=True)
                cmds.sets(cube, edit=True, forceElement=shading_group)

# ---------------------------------------------------------------------------
# Run the generator
# ---------------------------------------------------------------------------
generate_pattern()

# Frame everything in the viewport so I can see the full grid
cmds.viewFit(allObjects=True)

print("Pattern generated successfully!")
