# Franklin Grégoire
# 14/02/2025

import pyomo.environ as pyo

# Create a Pyomo model
model = pyo.ConcreteModel()

# Define model parameters
V = 200000 # Volume of a boat in m^3
LHV_NH3 = 18.5e6 # Lower heating value of NH3 in J/kg
rho_NH3 = 600 # Density of NH3 in kg/m^3
LHV_CH4 = 50e6 # Lower heating value of CH4 in J/kg
rho_CH4 = 500 # Density of CH4 in kg/m^3
losses_NH3 = 0.4 # Losses of NH3 in the process
losses_CH4 = 0.35 # Losses of CH4 in the process
H2CH4 = 0.25 # H2 per ton of CH4
H2NH3 = 0.18 # H2 per ton of NH3
CO2CH4 = 2.75 # ton of CO2 needed per ton of CH4

# Define model variables
model.bCH4 = pyo.Var(within = pyo.NonNegativeReals)
model.bNH3 = pyo.Var(within = pyo.NonNegativeReals)

# Define the objective functions
model.obj = pyo.Objective(expr = V*rho_CH4*H2CH4*model.bCH4+V*rho_NH3*H2NH3*model.bNH3, sense = pyo.maximize)

# Define the constraints
model.con1 = pyo.Constraint(expr = model.bCH4+ model.bNH3 <= 100) 
model.con2 = pyo.Constraint(expr = V*rho_CH4*model.bCH4*CO2CH4 <= 14e6) 
model.con3 = pyo.Constraint(expr = V*rho_CH4*model.bCH4*LHV_CH4/(1-losses_CH4) + V*rho_NH3*LHV_NH3*model.bNH3/(1-losses_NH3)<= 140e12)

# Specify the path towards your solver (gurobi) file
solver = pyo.SolverFactory("gurobi")
sol = solver.solve(model)

# Print here the number of CH4 boats and NH3 boats
print(model.bCH4.value)
print(model.bNH3.value)
