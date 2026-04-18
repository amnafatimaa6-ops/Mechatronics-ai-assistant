def physics_fallback(query):

    q = query.lower()

    # =========================
    # 🧠 MECHATRONICS CORE KNOWLEDGE ENGINE
    # =========================

    if "mechatronics" in q:

        return """
MECHATRONICS SYSTEMS OVERVIEW

Mechatronics is a multidisciplinary engineering field that integrates:

• Mechanical Engineering → motion, structures, dynamics  
• Electrical Engineering → circuits, sensors, power systems  
• Control Engineering → feedback systems, stability, PID control  
• Computer Engineering → embedded systems, automation, AI control  

CORE IDEA:
It is the design of intelligent machines that can sense, process, and act.

KEY COMPONENTS:
• Sensors (temperature, position, speed)
• Actuators (motors, hydraulics, pneumatics)
• Controllers (microcontrollers, PLCs)
• Software (control algorithms)

REAL-WORLD SYSTEMS:
• Industrial robots
• Self-driving cars
• CNC machines
• Smart manufacturing systems
• Drones and automation systems

ENGINEERING PURPOSE:
To create systems that reduce human intervention while increasing precision, speed, and efficiency.
"""

    # =========================
    # ⚙️ MOTOR / GENERAL ENGINEERING MODE
    # =========================

    if any(x in q for x in ["motor", "heating", "torque", "vibration"]):

        return """
ENGINEERING ANALYSIS

Common causes in electromechanical systems:

1. Electrical overload (high current draw)
2. Thermal buildup (poor cooling or ventilation)
3. Mechanical friction (bearing wear or misalignment)
4. Voltage instability
5. Load mismatch (motor undersized for task)

ENGINEERING FIX:
• Reduce load demand
• Improve cooling system
• Check bearing condition
• Verify rated voltage/current
• Inspect mechanical alignment
"""

    # =========================
    # ⚙️ DEFAULT ENGINEERING KNOWLEDGE
    # =========================

    return """
MECHATRONICS ENGINEERING SYSTEM

This system integrates mechanical, electrical, and control principles.

It is used in:
• Robotics
• Automation systems
• Industrial machinery
• Smart devices

Core principle:
Sensors → Controller → Actuator loop
"""
