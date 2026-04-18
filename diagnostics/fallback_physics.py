def physics_fallback(query):
    return """
DC motor heating is governed by:

1. Electrical losses (I²R heating)
2. Mechanical friction losses
3. Magnetic losses (eddy currents)
4. Thermal dissipation limits

Engineering Fix:
- reduce load torque
- improve heat dissipation
- ensure correct voltage/current rating
- inspect bearings
"""
