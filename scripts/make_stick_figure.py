import xml.etree.ElementTree as ET

# Paths
input_path = "src/g1_description/urdf/g1.urdf"
output_path = "src/g1_description/urdf/g1_stick.urdf"

print(f"Parsing {input_path}...")
tree = ET.parse(input_path)
root = tree.getroot()

count = 0

def replace_geometry(geom_tag):
    # If a mesh exists, remove it
    mesh = geom_tag.find('mesh')
    if mesh is not None:
        geom_tag.remove(mesh)
        # Add replacement cylinder
        cyl = ET.SubElement(geom_tag, 'cylinder')
        cyl.set('radius', '0.04')
        cyl.set('length', '0.1')
        return True
    return False

# Iterate over all links
for link in root.findall('link'):
    link_name = link.get('name')
    modified = False
    
    # 1. Fix Visuals
    for visual in link.findall('visual'):
        geometry = visual.find('geometry')
        if geometry is not None:
            if replace_geometry(geometry):
                modified = True

    # 2. Fix Collisions
    for collision in link.findall('collision'):
        geometry = collision.find('geometry')
        if geometry is not None:
            if replace_geometry(geometry):
                modified = True
                
    if modified:
        count += 1
        print(f"  Simplified link: {link_name}")

print(f"\nTotal links converted to stick-figure: {count}")
tree.write(output_path)
print(f"Saved super-safe URDF to: {output_path}")
