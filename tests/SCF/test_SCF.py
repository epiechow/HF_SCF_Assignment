
import pytest
import SCF
import pickle


def test_calc_nuclear_repulsion_energy(mol_h2o):
    assert SCF.calc_nuclear_repulsion_energy(mol_h2o) == 8.00236706181077


def test_calc_initial_density(mol_h2o):
    Duv = SCF.calc_initial_density(mol_h2o)
    assert Duv.sum() == 0
    assert Duv.shape == (mol_h2o.nao, mol_h2o.nao)


def test_calc_hcore_matrix(mol_h2o):
    Tuv = pickle.load(open("tuv.pkl", "rb"))
    Vuv = pickle.load(open("vuv.pkl", "rb"))
    h_core = SCF.calc_hcore_matrix(Tuv, Vuv)
    assert h_core[0, 0] == -32.57739541261037
    assert h_core[3, 4] == 0
    assert h_core[4, 3] == 0


def test_calc_fock_matrix(mol_h2o):
    Tuv = pickle.load(open("tuv.pkl", "rb"))
    Vuv = pickle.load(open("vuv.pkl", "rb"))
    eri = pickle.load(open("eri.pkl", "rb"))
    h_core = SCF.calc_hcore_matrix(Tuv, Vuv)
    Duv = SCF.calc_initial_density(mol_h2o)
    Fuv = SCF.calc_fock_matrix(mol_h2o, h_core, eri, Duv)
    assert Fuv[0, 0] == -32.57739541261037
    assert Fuv[2, 5] == pytest.approx(-1.6751501447185015, 0.000000000000001)
    assert Fuv[5, 2] == pytest.approx(-1.6751501447185015, 0.000000000000001)


def test_solve_Roothan_equation(mol_h2o):
    Tuv = pickle.load(open("tuv.pkl", "rb"))
    Vuv = pickle.load(open("vuv.pkl", "rb"))
    eri = pickle.load(open("eri.pkl", "rb"))
    Suv = pickle.load(open("suv.pkl", "rb"))
    h_core = SCF.calc_hcore_matrix(Tuv, Vuv)
    Duv = SCF.calc_initial_density(mol_h2o)
    Fuv = SCF.calc_fock_matrix(mol_h2o, h_core, eri, Duv)
    mo_energies, mo_coeffs = SCF.solve_Roothan_equations(Fuv, Suv)
    assert mo_energies == pytest.approx([-32.5783029, -8.08153571, -7.55008599,
                                         -7.36396923,  -7.34714487,
                                         -4.00229867,
                                         -3.98111115])
    assert mo_coeffs[0, 0] == pytest.approx(-1.00154358e+00)
    assert abs(mo_coeffs[0, 1]) == pytest.approx(abs(2.33624458e-01))
    assert mo_coeffs[0, 2] == pytest.approx(-4.97111543e-16)
    assert mo_coeffs[0, 3] == pytest.approx(-8.56842145e-02)
    assert mo_coeffs[0, 4] == pytest.approx(-2.02299681e-29)
    assert abs(mo_coeffs[0, 5]) == pytest.approx(abs(4.82226067e-02))
    assert mo_coeffs[0, 6] == pytest.approx(-4.99600361e-16)


def test_form_density_matrix(mol_h2o):
    Tuv = pickle.load(open("tuv.pkl", "rb"))
    Vuv = pickle.load(open("vuv.pkl", "rb"))
    eri = pickle.load(open("eri.pkl", "rb"))
    Suv = pickle.load(open("suv.pkl", "rb"))
    h_core = SCF.calc_hcore_matrix(Tuv, Vuv)
    Duv = SCF.calc_initial_density(mol_h2o)
    Fuv = SCF.calc_fock_matrix(mol_h2o, h_core, eri, Duv)
    mo_energies, mo_coeffs = SCF.solve_Roothan_equations(Fuv, Suv)
    Duvnew = SCF.form_density_matrix(mol_h2o, mo_coeffs)
    assert Duvnew[0, 0] == pytest.approx(2.130023428655504, 0.0000000000000001)
    assert Duvnew[2, 5] == pytest.approx(-0.29226330209653156, 0.000000000001)
    assert Duvnew[5, 2] == pytest.approx(-0.29226330209653156, 0.000000000001)


def test_calc_total_energy(mol_h2o):
    Tuv = pickle.load(open("tuv.pkl", "rb"))
    Vuv = pickle.load(open("vuv.pkl", "rb"))
    eri = pickle.load(open("eri.pkl", "rb"))
    Suv = pickle.load(open("suv.pkl", "rb"))
    h_core = SCF.calc_hcore_matrix(Tuv, Vuv)
    Duv = SCF.calc_initial_density(mol_h2o)
    Fuv = SCF.calc_fock_matrix(mol_h2o, h_core, eri, Duv)
    mo_energies, mo_coeffs = SCF.solve_Roothan_equations(Fuv, Suv)
    Enuc = SCF.calc_nuclear_repulsion_energy(mol_h2o)
    Etot = SCF.calc_total_energy(Fuv, h_core, Duv, Enuc)

    assert Etot == pytest.approx(8.0023670618)
