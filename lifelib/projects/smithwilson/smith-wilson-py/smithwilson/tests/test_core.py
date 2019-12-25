
import unittest
import smithwilson as sw
import numpy as np

class TestSmithWilson(unittest.TestCase):

    def test_ufr_discount_factor(self):
        """Test creation of UFR discount factor vector"""

        # Input
        ufr = 0.029
        t = np.array([0.25, 1.0, 5.0, 49.5, 125.0])

        # Expected Output
        expected = np.array([0.992878614, 0.971817298, 0.866808430, 0.242906395, 0.028059385])

        # Actual Output
        actual = sw.ufr_discount_factor(ufr=ufr, t=t)

        # Assert
        self.assertEqual(type(actual), type(expected), "Returned types not matching")
        self.assertTupleEqual(actual.shape, expected.shape, "Shapes not matching")
        np.testing.assert_almost_equal(actual, expected, decimal=8, err_msg="UFR discount factors not matching")


    def test_calculate_prices(self):
        """Test calculation of zero-coupon bond price vector"""

        # Input
        r = np.array([0.02, 0.025, -0.033, 0.01, 0.0008])
        t = np.array([0.25, 1.0, 5.0, 49.5, 125.0])

        # Expected Output
        expected = np.array([0.995061577, 0.975609756, 1.182681027, 0.611071456, 0.904873593])

        # Actual Output
        actual = sw.calculate_prices(rates=r, t=t)

        # Assert
        self.assertEqual(type(actual), type(expected), "Returned types not matching")
        self.assertTupleEqual(actual.shape, expected.shape, "Shapes not matching")
        np.testing.assert_almost_equal(actual, expected, decimal=8, err_msg="Prices not matching")


    def test_wilson_function_symmetric(self):
        """Test creation of a symmetric Wilson-function matrix (t1 = t2)"""

        # Input
        t = np.array([0.25, 1.0, 5.0, 49.5, 125.0]).reshape((-1, 1))
        ufr = 0.029
        alpha = 0.2

        # Expected Output
        expected = np.array([[0.00238438, 0.00872884, 0.02719467, 0.01205822, 0.00139298],
                             [0.00872884, 0.03320614, 0.10608305, 0.04720974, 0.00545372],
                             [0.02719467, 0.10608305, 0.42652097, 0.2105409 , 0.02432211],
                             [0.01205822, 0.04720974, 0.2105409 , 0.55463306, 0.06747646],
                             [0.00139298, 0.00545372, 0.02432211, 0.06747646, 0.01928956]])

        # Actual Output
        actual = sw.wilson_function(t1=t, t2=t, ufr=ufr, alpha=alpha)

        # Assert
        self.assertEqual(type(actual), type(expected), "Returned types not matching")
        self.assertTupleEqual(actual.shape, expected.shape, "Shapes not matching")
        np.testing.assert_almost_equal(actual, expected, decimal=8, err_msg="Wilson functions not matching")


    def test_wilson_function_asymmetric_t1_lt_t2(self):
        """Test creation of a symmetric Wilson-function matrix (t1 != t2) with length of t1 > length of t2"""

        # Input
        t_obs = np.array([0.25, 1.0, 5.0, 49.5, 125.0]).reshape((-1, 1))
        t_target = np.array([0.25, 0.5, 1.0, 2.0, 2.5, 3.5, 5.0, 10.0, 20.0, 49.5, 125.0]).reshape((-1, 1))
        ufr = 0.029
        alpha = 0.2

        # Expected Output
        expected = np.array([[0.00238438, 0.00872884, 0.02719467, 0.01205822, 0.00139298],
                             [0.00463874, 0.01723526, 0.0539627 , 0.0239447 , 0.00276612],
                             [0.00872884, 0.03320614, 0.10608305, 0.04720974, 0.00545372],
                             [0.015444  , 0.05969492, 0.20375322, 0.0917584 , 0.01060004],
                             [0.01817438, 0.07046799, 0.24880429, 0.11307011, 0.013062  ],
                             [0.02260267, 0.08794588, 0.33012767, 0.15383656, 0.01777143],
                             [0.02719467, 0.10608305, 0.42652097, 0.2105409 , 0.02432211],
                             [0.03225016, 0.12614043, 0.54769846, 0.36498556, 0.04216522],
                             [0.02751232, 0.10770227, 0.47881259, 0.54833094, 0.06336226],
                             [0.01205822, 0.04720974, 0.2105409 , 0.55463306, 0.06747646],
                             [0.00139298, 0.00545372, 0.02432211, 0.06747646, 0.01928956]])

        # Actual Output
        actual = sw.wilson_function(t1=t_target, t2=t_obs, ufr=ufr, alpha=alpha)

        # Assert
        self.assertEqual(type(actual), type(expected), "Returned types not matching")
        self.assertTupleEqual(actual.shape, expected.shape, "Shapes not matching")
        np.testing.assert_almost_equal(actual, expected, decimal=8, err_msg="Wilson functions not matching")


    def test_wilson_function_asymmetric_t2_lt_t1(self):
        """Test creation of a symmetric Wilson-function matrix (t1 != t2) with length of t2 > length of t1"""

        # Input
        t_target = np.array([0.50, 1.5, 7.0, 22.5]).reshape((-1, 1))
        t_obs = np.array([0.25, 1.0, 2.0, 2.5, 5.0, 10.0, 20.0]).reshape((-1, 1))
        ufr = 0.032
        alpha = 0.15

        # Expected Output
        expected = np.array([[0.00263839, 0.00990704, 0.01791847, 0.02129457, 0.03324991, 0.04184617, 0.03736174],
                             [0.00714378, 0.02751832, 0.05096578, 0.06087744, 0.09600535, 0.12138299, 0.1085669 ],
                             [0.01939785, 0.07563626, 0.14568738, 0.17843321, 0.31674624, 0.45088288, 0.42190812],
                             [0.01768861, 0.06909389, 0.13384921, 0.16464728, 0.3035725 , 0.51271549, 0.69668792]])

        # Actual Output
        actual = sw.wilson_function(t1=t_target, t2=t_obs, ufr=ufr, alpha=alpha)

        # Assert
        self.assertEqual(type(actual), type(expected), "Returned types not matching")
        self.assertTupleEqual(actual.shape, expected.shape, "Shapes not matching")
        np.testing.assert_almost_equal(actual, expected, decimal=8, err_msg="Wilson functions not matching")


    def test_fit_parameters(self):
        """Test estimation of Smith-Wilson parameter vector ζ"""

        # Input
        r = np.array([0.02, 0.025, -0.033, 0.01, 0.0008]).reshape((-1, 1))
        t = np.array([0.25, 1.0, 5.0, 49.5, 125.0]).reshape((-1, 1))
        ufr = 0.029
        alpha = 0.2

        # Expected Output
        expected = np.array([-42.78076209, 23.4627511, -3.96498616, 8.92604195, -75.22418515]).reshape((-1, 1))

        # Actual Output
        actual = sw.fit_parameters(rates=r, t=t, ufr=ufr, alpha=alpha)

        # Assert
        self.assertEqual(type(actual), type(expected), "Returned types not matching")
        self.assertTupleEqual(actual.shape, expected.shape, "Shapes not matching")
        np.testing.assert_almost_equal(actual, expected, decimal=8, err_msg="Parameter not matching")


    def test_fit_smithwilson_rates_actual(self):
        """Test estimation of yield curve fitted with the Smith-Wilson algorithm.
           This example uses an actual example from EIOPA. Deviations must be less than 1bps (0.01%).
           Source: https://eiopa.europa.eu/Publications/Standards/EIOPA_RFR_20190531.zip
                   EIOPA_RFR_20190531_Term_Structures.xlsx; Tab: RFR_spot_no_VA; Switzerland
        """

        # Input
        r = np.array([-0.00803, -0.00814, -0.00778, -0.00725, -0.00652,
                      -0.00565, -0.0048, -0.00391, -0.00313, -0.00214,
                      -0.0014, -0.00067, -0.00008, 0.00051, 0.00108,
                      0.00157, 0.00197, 0.00228, 0.0025, 0.00264,
                      0.00271, 0.00274, 0.0028, 0.00291, 0.00309]).reshape((-1, 1))
        t = np.array([float(y + 1) for y in range(len(r))]).reshape((-1, 1)) # 1.0, 2.0, ..., 25.0
        ufr = 0.029
        alpha = 0.128562

        t_target = np.array([float(y + 1) for y in range(65)]).reshape((-1, 1))

        # Expected Output
        expected = np.array([-0.00803, -0.00814, -0.00778, -0.00725, -0.00652,
                             -0.00565, -0.0048, -0.00391, -0.00313, -0.00214,
                             -0.0014, -0.00067, -0.00008, 0.00051, 0.00108,
                             0.00157, 0.00197, 0.00228, 0.0025, 0.00264,
                             0.00271, 0.00274, 0.0028, 0.00291, 0.00309,
                             0.00337, 0.00372, 0.00412, 0.00455, 0.00501,
                             0.00548, 0.00596, 0.00644, 0.00692, 0.00739,
                             0.00786, 0.00831, 0.00876, 0.00919, 0.00961,
                             0.01002, 0.01042, 0.01081, 0.01118, 0.01154,
                             0.01189, 0.01223, 0.01255, 0.01287, 0.01318,
                             0.01347, 0.01376, 0.01403, 0.0143, 0.01456,
                             0.01481, 0.01505, 0.01528, 0.01551, 0.01573,
                             0.01594, 0.01615, 0.01635, 0.01655, 0.01673]).reshape((-1, 1))

        # Actual Output
        actual = sw.fit_smithwilson_rates(rates_obs=r, t_obs=t, t_target=t_target, ufr=ufr, alpha=alpha)

        # Assert - Precision of 4 decimal points equals deviatino of less than 1bps
        self.assertEqual(type(actual), type(expected), "Returned types not matching")
        self.assertTupleEqual(actual.shape, expected.shape, "Shapes not matching")
        np.testing.assert_almost_equal(actual, expected, decimal=4, err_msg="Fitted rates not matching")


    def test_fit_smithwilson_rates_random(self):
        """Test estimation of yield curve fitted with the Smith-Wilson algorithm
           This test uses random data points.
        """

        # Input
        r = np.array([0.02, 0.025, -0.033, 0.01, 0.0008]).reshape((-1, 1))
        t = np.array([0.25, 1.0, 5.0, 20.0, 25.0]).reshape((-1, 1))
        ufr = 0.029
        alpha = 0.12

        t_target = np.array([0.25, 0.5, 1.0, 2.0, 2.5, 3.5, 5.0, 10.0, 20.0, 49.5, 125.0]).reshape((-1, 1))

        # Expected Output
        expected = np.array([0.02, 0.02417656, 0.025, 0.00361999, -0.00733027,
                            -0.02345319, -0.033, -0.01256218, 0.01, 0.00715949, 0.02015626]).reshape((-1, 1))

        # Actual Output
        actual = sw.fit_smithwilson_rates(rates_obs=r, t_obs=t, t_target=t_target, ufr=ufr, alpha=alpha)

        # Assert
        self.assertEqual(type(actual), type(expected), "Returned types not matching")
        self.assertTupleEqual(actual.shape, expected.shape, "Shapes not matching")
        np.testing.assert_almost_equal(actual, expected, decimal=8, err_msg="Fitted rates not matching")