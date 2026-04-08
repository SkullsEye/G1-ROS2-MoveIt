import os
import xml.etree.ElementTree as ET

# Paths
urdf_path = "src/g1_description/urdf/g1_safe.urdf"
output_path = "src/g1_moveit_config/config/joint_limits.yaml"

print(f"Reading joints from {urdf_path}...")
tree = ET.parse(urdf_path)
root = tree.getroot()

# Header for the YAML file
yaml_content = "joint_limits:\n"

count = 0
for joint in root.findall("joint"):
    joint_type = joint.get("type")
    # We only care about moving joints (revolute or continuous)
    if joint_type in ["revolute", "continuous"]:
        name = joint.get("name")
        # Write default limits (velocity = 2.0 rad/s, accel = 3.0 rad/s^2)
        yaml_content += f"  {name}:\n"
        yaml_content += "    has_velocity_limits: true\n"
        yaml_content += "    max_velocity: 2.0\n"
        yaml_content += "    has_acceleration_limits: true\n"
        yaml_content += "    max_acceleration: 3.0\n"
        count += 1

with open(output_path, "w") as f:
    f.write(yaml_content)

print(f"Successfully generated limits for {count} joints at {output_path}")
