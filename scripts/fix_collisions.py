import re

# Paths
input_file = "src/g1_description/urdf/g1.urdf"
output_file = "src/g1_description/urdf/g1_safe.urdf"

with open(input_file, "r") as f:
    content = f.read()

# Regex to find collision mesh tags and replace them with a simple sphere
# This looks for <collision>...<mesh filename="..."/>...</collision> blocks
# and replaces the mesh geometry with a simple sphere.
pattern = r'(<collision>[\s\S]*?<geometry>)\s*<mesh filename="package://[^"]+"/>\s*(</geometry>[\s\S]*?</collision>)'
replacement = r'\1\n        <sphere radius="0.02"/>\n      \2'

# Apply replacement
new_content = re.sub(pattern, replacement, content)

# Save new file
with open(output_file, "w") as f:
    f.write(new_content)

print(f"Successfully created {output_file} with simplified collisions.")
