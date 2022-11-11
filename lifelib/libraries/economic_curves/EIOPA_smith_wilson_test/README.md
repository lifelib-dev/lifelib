<h1 align="center" style="border-botom: none">
  <b>
  🐍 Risk free curve test 🐍
 </b>
</h1>

</br>

The risk free curve is one of the principal inputs into an economic scenario generator. This test recalculates the risk free curve using the parameters that are claimed to be used.

## This example
In this example, we look at the EIOPA risk free rate publication from August 2022. In particular, this example focuses on the EUR curve.
The publication can be found [EIOPA RFR website](https://www.eiopa.europa.eu/tools-and-data/risk-free-interest-rate-term-structures_en).

The observed maturities `M_Obs` and the calibrated vector `Qb` can be found in the Excel sheet *EIOPA_RFR_20220831_Qb_SW.xlsx*.
The target maturities (`T_Obs`), the additional parameters (`UFR` and `alpha`) and the given curve can be found in the Excel *EIOPA_RFR_20220831_Term_Structures.xlsx*, sheet *RFR_spot_no_VA*.

## Smith&Wilson algorithm

The implementation of the SW algorithm is a slight modification to the original OSM implementation. The original implementation can be found in different languages on the OSM's GitHub repository:
-  [Python](https://github.com/qnity/insurance_python/tree/main/smith%26wilson).
-  [Matlab](https://github.com/qnity/insurance_matlab/tree/main/smith%26wilson).
-  [JavaScript](https://github.com/qnity/insurance_javascript/tree/main/smith-wilson).
