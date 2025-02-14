# Franklin Grégoire
# 14/02/2025

""" MY VERSION OF THE CODE 

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

"""

# Solution

import pyomo.environ as pyo

# Create a Pyomo model
model = pyo.ConcreteModel()



# Define model parameters
model.H2inNH3 = pyo.Param(initialize=0.18)
model.H2inCH4 = pyo.Param(initialize=0.25)
model.CO2inCH4 = pyo.Param(initialize=2.75)
model.volumeBoat = pyo.Param(initialize=200000.)
model.densityNH3 = pyo.Param(initialize=0.6)
model.densityCH4 = pyo.Param(initialize=0.5)
model.LHV_NH3 = pyo.Param(initialize=18.5) #GJ/t
model.LHV_CH4 = pyo.Param(initialize=50.) #GJ/t
model.losses_NH3 = pyo.Param(initialize=0.4)
model.losses_CH4 = pyo.Param(initialize=0.35) 
model.maxBoats = pyo.Param(initialize=100.)
model.maxEnergy = pyo.Param(initialize=140*1E6*3.6) #MJ
model.maxCO2 = pyo.Param(initialize=14E6)


# Define model variables
model.boatsNH3 = pyo.Var(domain=pyo.NonNegativeReals)
model.boatsCH4 = pyo.Var(domain=pyo.NonNegativeReals)

# Define objective function
model.objective = pyo.Objective(expr=model.boatsCH4*model.volumeBoat*model.densityCH4*model.H2inCH4+model.boatsNH3*model.volumeBoat*model.densityNH3*model.H2inNH3, sense=pyo.maximize)

# Define constraints
def maxBoats(model):
    return model.boatsNH3+model.boatsCH4 <= model.maxBoats

model.maxBoatsConstr = pyo.Constraint(rule=maxBoats)

def maxEnergy(model):
    return model.boatsNH3*model.volumeBoat*model.densityNH3*model.LHV_NH3/(1.-model.losses_NH3) + model.boatsCH4*model.volumeBoat*model.densityCH4*model.LHV_CH4/(1-model.losses_CH4) <= model.maxEnergy

model.maxEnergyConstr = pyo.Constraint(rule=maxEnergy)

def maxCO2(model):
    return model.boatsCH4*model.volumeBoat*model.densityCH4*model.CO2inCH4 <= model.maxCO2

model.maxCO2Constr = pyo.Constraint(rule=maxCO2)

model.dual = pyo.Suffix(direction=pyo.Suffix.IMPORT)
model.rc = pyo.Suffix(direction=pyo.Suffix.IMPORT)

solver = pyo.SolverFactory("gurobi")
sol = solver.solve(model)


print(model.boatsCH4.value)
print(model.boatsNH3.value)
model.display()
model.dual.display()
model.rc.display()