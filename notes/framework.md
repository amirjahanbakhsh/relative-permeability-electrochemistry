# Framework Notes

Notes about modeling framework, numerical methods, and architecture.

# Framework: Relative Permeability in Porous Electrochemical Systems

## 1. Problem Definition

Porous electrochemical electrodes (e.g., gas diffusion electrodes in CO₂ electrolysis) operate under multiphase conditions where gas (CO₂) and liquid (electrolyte) phases coexist and compete for transport pathways.

High liquid saturation (flooding) reduces gas transport to reaction sites, leading to performance degradation. While existing models resolve saturation fields, they do not establish a general relationship between phase distribution and electrochemical performance.

### Objective

Develop a physics-based framework that links:
- Phase saturation (S)
- Transport capacity
- Electrochemical performance (current density)

using relative permeability concepts from porous media flow.

---

## 2. Key Idea

Instead of treating saturation as a secondary output, we define it as a governing variable controlling transport.

### Core Concept

Gas transport is controlled by saturation-dependent mobility:

    krg(S) = (1 - S)^n

This directly affects:
- Effective diffusivity
- Reactant availability
- Reaction rate

### Key Relationship

    j = f(S)

where:
- j = current density
- S = liquid saturation

### Interpretation

Performance collapse occurs when gas phase mobility decreases due to increasing liquid saturation.

---

## 3. Governing Equations

### 3.1 Transport Equation (1D, steady-state)

CO₂ transport through porous medium:

    d/dx [ D_eff(S) * dC/dx ] = -R

where:
- C = CO₂ concentration
- D_eff(S) = effective diffusivity
- R = reaction rate

---

### 3.2 Effective Diffusivity

Defined using relative permeability:

    D_eff(S) = D * krg(S)

where:
- D = bulk diffusivity
- krg(S) = relative permeability of gas phase

---

### 3.3 Relative Permeability (Corey-type)

    krg(S) = (1 - S)^n
    krl(S) = S^m

where:
- S = liquid saturation (0 ≤ S ≤ 1)
- n, m = empirical exponents (typically 2–4)

---

### 3.4 Reaction Term

Reaction depends on local CO₂ availability:

    R = k_r * C * krg(S)

where:
- k_r = reaction rate constant

---

### 3.5 Performance Metric

Total current density:

    j ∝ ∫ R dx

Normalized:

    j / j_max

---

## 4. Assumptions

To isolate transport effects, the model is simplified:

### Geometry
- 1D through-plane domain

### Physics
- Steady-state
- Isothermal conditions
- No convection (diffusion-dominated)
- No explicit pressure solution

### Multiphase Treatment
- Saturation (S) is prescribed or parameterised
- No dynamic phase transport (first paper)

### Electrochemistry
- Simplified kinetics (linear in concentration)
- No detailed Butler–Volmer or charge transport

---

## 5. Expected Behaviour

### Limiting Cases

- S = 0 (dry):
    - krg = 1
    - Maximum transport
    - j = j_max

- S → 1 (fully flooded):
    - krg → 0
    - No gas transport
    - j → 0

---

### Key Hypothesis

Performance vs saturation is nonlinear:

- Weak impact at low S
- Sharp drop beyond critical saturation S_crit

---

## 6. Outputs of Interest

### Primary Output

- j vs S curve

### Secondary Outputs

- Concentration profile C(x)
- Reaction distribution R(x)
- Sensitivity to n (pore structure effect)

---

## 7. Novelty

This framework introduces:

1. Saturation as a governing variable
2. Relative permeability as transport descriptor
3. Direct link between phase mobility and performance
4. Concept of critical saturation threshold

---

## 8. Scope of First Study

This is a conceptual and physics-focused model intended to:

- Establish governing relationships
- Demonstrate transport-limited behaviour
- Provide a generalisable framework

Not intended to:

- Fully reproduce experimental systems
- Capture detailed electrochemistry
- Model full multiphase dynamics

---

## 9. Future Extensions

- Dynamic saturation transport (Buckley–Leverett type)
- Coupling with pressure field
- 2D/3D simulations (OpenFOAM)
- Application to hydrogen electrolysis
- Integration with microkinetics
