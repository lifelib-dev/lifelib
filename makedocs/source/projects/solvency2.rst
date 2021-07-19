.. module:: solvency2

.. _project_solvency2:

Project **solvency2**
=====================

**solvency2** is a project for building a model to
calculate life risks of selected policies at various points in their policy periods
based on Solvency II standard formula.
This project serves as a reference for
building models that contain complex nested projections.

Overview
--------

The model included in this project is named ``solvency2``.
The model calculates the capital requirement for life underwriting risk
based on Solvency II standard formula by policy and duration.

The overall capital requirement for life underwriting risk,
expressed as :math:`SCR_{life}`, is calculated by aggregating life sub-risks,
using a correlation matrix.

Each life sub-risk, as defined in the reference below, is defined
as the difference in net asset value under the base (best estimate) scenario
and the deterministic scenario with a prescribed stress on the risk factor,
except for Lapse risk.
For Lapse risk, three ("up", "down", "mass") scenarios are considered.

The model contains a parametric space
:mod:`SCR_Life[t0, PolicyID, ScenID] <solvency2.model.SCR_life>`.
:func:`~solvency2.model.SCR_life.SCR_life` cells in each ``SCR_Life[t0, PolicyID, ScenID]``
holds the value of Life underwriting risk at time ``t0`` for ``PolicyID``
and ``ScenID`` (1 by default), calculated based on
the solvency capital requirement standard formula under Solvency II.


References:
    * `COMMISSION DELEGATED REGULATION (EU) 2015/35 of 10 October 2014 <https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A32015R0035>`_
    * `Solvency II Technical Specifications <https://wayback.archive-it.org/org-1495/20191229100044/https:/eiopa.europa.eu/regulation-supervision/insurance/solvency-ii/solvency-ii-technical-specifications>`_


Model Structure
---------------

Composition Structure
^^^^^^^^^^^^^^^^^^^^^

.. blockdiag::

   blockdiag {
     default_node_color="#D5E8D4";
     default_linecolor="#628E47";
     solvency2 [shape=roundedbox, linecolor="#7B99C5", color="#D4E8FC", width=96];
     solvency2 <- "SCR_life[t0, PolicyID, ScenID]" <- "Projection[Risk, Shock, Scope]" [hstyle=composition];
     "SCR_life[t0, PolicyID, ScenID]" [stacked, width=200];
     "Projection[Risk, Shock, Scope]" [stacked, width=200];
     solvency2 <- Economic [hstyle=composition];
     solvency2  <- Assumptions [hstyle=composition];
     solvency2 <- Policy [hstyle=composition];
     solvency2 <- LifeTable [hstyle=composition];
     solvency2 <- Input [hstyle=composition];
     solvency2 <- PV [hstyle=composition];
     solvency2 <- BaseProj [hstyle=composition];
     PV [style=dotted]
     BaseProj [style=dotted]
     solvency2 <- Override
     Override <- Mortality[hstyle=composition]
     Override <- Lapse[hstyle=composition]
     Override <- LapseMass[hstyle=composition]
     Override <- Expense[hstyle=composition]
   }

Inheritance Structure
^^^^^^^^^^^^^^^^^^^^^

.. blockdiag::

   blockdiag {
     default_node_color="#D5E8D4";
     default_linecolor="#628E47";
     "SCR_life[t0, PolicyID, ScenID]" [width=200]
     SCR_life <- "SCR_life[t0, PolicyID, ScenID]"[hstyle=generalization]
     PV <- Projection[hstyle=generalization]
     BaseProj <- Projection[hstyle=generalization]
     Override <- Mortality[hstyle=composition]
     Override <- Lapse[hstyle=composition]
     Override <- LapseMass[hstyle=composition]
     Override <- Expense[hstyle=composition]
     Projection <- "Projection[Risk, Shock, Scope]" [hstyle=generalization]
     "Projection[Risk, Shock, Scope]" [width=200];
     Mortality <- "Projection[Risk, Shock, Scope]" [hstyle=generalization, style=dotted]
     Lapse <- "Projection[Risk, Shock, Scope]" [hstyle=generalization, style=dotted]
     LapseMass <- "Projection[Risk, Shock, Scope]" [hstyle=generalization, style=dotted]
     Expense <- "Projection[Risk, Shock, Scope]" [hstyle=generalization, style=dotted]
     SCR_life, PV, BaseProj, Projection, Mortality, Lapse, LapseMass, Expense [style=dotted]
   }


Space Details
-------------

.. autosummary::
   :toctree: generated/
   :template: llmodule.rst

   ~model.Assumptions
   ~model.BaseProj
   ~model.Economic
   ~model.LifeTable
   ~model.Override.Expense
   ~model.Override.Lapse
   ~model.Override.LapseMass
   ~model.Override.Mortality
   ~model.SCR_life.Projection
   ~model.Policy
   ~model.PV
   ~model.SCR_life

