# G1 ROS2 MoveIt

**ROS2 MoveIt configuration** for the Unitree G1 humanoid robot. Includes URDF description, MoveIt motion planning setup, joint limit configuration, and helper scripts for collision and configuration management.

## Features

- Complete G1 URDF robot description with visual meshes
- MoveIt2 configuration for motion planning
- Collision geometry management and fixing tools
- Joint limit generation from robot specifications
- Automated MoveIt config generation scripts

## Project Structure

```
src/
    g1_description/         # G1 URDF model and meshes
    g1_moveit_config/       # MoveIt planning configuration
    g1_package/             # Additional G1 ROS2 package
scripts/
    generate_moveit_config.py   # Auto-generate MoveIt config
    fix_collisions.py           # Fix collision geometry issues
    force_fix.py                # Force-fix problematic configurations
    generate_limits.py          # Generate joint limits from specs
    make_stick_figure.py        # Debug visualization
```

## Prerequisites

- Ubuntu 22.04
- ROS2 Humble
- MoveIt2
- colcon build system

## Installation

```bash
cd ~/ros2_ws/src
git clone https://github.com/SkullsEye/G1-ROS2-MoveIt.git
cd ~/ros2_ws
rosdep install --from-paths src --ignore-src -r -y
colcon build
source install/setup.bash
```

## Usage

```bash
# Generate MoveIt configuration
python scripts/generate_moveit_config.py

# Fix collision geometry
python scripts/fix_collisions.py

# Launch MoveIt with G1
ros2 launch g1_moveit_config demo.launch.py
```

## Author

**Umar Bin Muzzafar**
B.Tech in Artificial Intelligence and Robotics, Dayananda Sagar University, Bangalore

## License

MIT License. See [LICENSE](LICENSE) for details.
