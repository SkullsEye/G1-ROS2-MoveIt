import xml.etree.ElementTree as ET
import os

# Paths
input_path = "src/g1_description/urdf/g1.urdf"
output_path = "src/g1_description/urdf/g1_safe.urdf"

print(f"Parsing {input_path}...")
tree = ET.parse(input_path)
root = tree.getroot()

count = 0

# Iterate over all links in the robot
for link in root.findall('link'):
    link_name = link.get('name')
    
    # Check every collision tag in this link
    for collision in link.findall('collision'):
        geometry = collision.find('geometry')
        if geometry is not None:
            # If a mesh exists, remove it and add a simple sphere
            mesh = geometry.find('mesh')
            if mesh is not None:
                geometry.remove(mesh)
                
                # Add replacement sphere
                sphere = ET.SubElement(geometry, 'sphere')
                sphere.set('radius', '0.05') # 5cm sphere
                
                count += 1
                print(f"  Fixed collision for link: {link_name}")

print(f"\nTotal links fixed: {count}")
tree.write(output_path)
print(f"Saved crash-proof URDF to: {output_path}")
