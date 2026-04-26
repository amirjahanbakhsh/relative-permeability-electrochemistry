import sys
import unittest
import numpy as np

sys.path.append(r'.')

from model import solve, krg


class TestSolver(unittest.TestCase):
    def test_shapes_and_boundary(self):
        N = 21
        res = solve(D0=1.0, n=2.0, k_r=0.0, L=1.0, N=N, C_left=1.0, C_right=0.0,
                    saturation=lambda x: 0.0 * x)
        self.assertEqual(res['x'].shape[0], N)
        self.assertEqual(res['C'].shape[0], N)
        # Dirichlet BCs respected
        self.assertAlmostEqual(res['C'][0], 1.0, places=12)
        self.assertAlmostEqual(res['C'][-1], 0.0, places=12)

    def test_linear_profile_no_reaction(self):
        # With k_r=0 and uniform saturation=0 the solution should be linear
        N = 31
        res = solve(D0=1.0, n=2.0, k_r=0.0, L=1.0, N=N, C_left=1.0, C_right=0.0,
                    saturation=lambda x: np.zeros_like(x))
        C = res['C']
        # check second differences ~ 0
        second_diff = np.diff(C, n=2)
        self.assertTrue(np.allclose(second_diff, 0.0, atol=1e-8))

    def test_saturation_reduces_reaction_integral(self):
        # Compare integrated reaction for low vs high saturation
        N = 101
        k_r = 2.0
        lowS = lambda x: 0.0 * x
        highS = lambda x: 0.9 + 0.0 * x

        res_low = solve(D0=1.0, n=2.0, k_r=k_r, L=1.0, N=N, C_left=1.0, C_right=0.0, saturation=lowS)
        res_high = solve(D0=1.0, n=2.0, k_r=k_r, L=1.0, N=N, C_left=1.0, C_right=0.0, saturation=highS)

        x = res_low['x']
        dx = x[1] - x[0]
        R_low = k_r * res_low['C'] * krg(res_low['S'], n=2.0)
        R_high = k_r * res_high['C'] * krg(res_high['S'], n=2.0)
        J_low = np.sum(R_low) * dx
        J_high = np.sum(R_high) * dx

        self.assertGreater(J_low, J_high)


if __name__ == '__main__':
    unittest.main(verbosity=2)
