"""
Smoke tests — verify that all public interfaces import cleanly and instantiate.

These tests do not check physics correctness; they confirm the package structure
is intact and the basic object graph can be built without errors.
"""

import numpy as np
import pytest

from green_machine_mini import (
    BoostedBSM,
    DistributedLogicalQubit,
    GreenMachineInterconnect,
    ModuleType,
    QuantumHardwareModule,
)
from green_machine_mini.interconnect.mzi import MZI
from green_machine_mini.interconnect.time_bins import TimeBinRegister
from green_machine_mini.protocols.boosted_bsm import BellState, BSMOutcome
from green_machine_mini.qec.distributed_w_code import ModuleStatus


class TestMZI:
    def test_default_instantiation(self) -> None:
        mzi = MZI()
        assert mzi.theta == pytest.approx(np.pi / 4)
        assert mzi.phi == pytest.approx(0.0)

    def test_matrix_shape_and_dtype(self) -> None:
        mzi = MZI(theta=np.pi / 4, phi=0.0)
        u = mzi.matrix()
        assert u.shape == (2, 2)
        assert np.issubdtype(u.dtype, np.complexfloating)

    def test_unitarity(self) -> None:
        for theta in [0.0, np.pi / 6, np.pi / 4, np.pi / 3, np.pi / 2]:
            mzi = MZI(theta=theta, phi=0.5)
            assert mzi.is_unitary(), f"MZI not unitary at theta={theta}"


class TestTimeBinRegister:
    def test_instantiation(self) -> None:
        reg = TimeBinRegister(n_bins=8)
        assert reg.n_bins == 8
        assert len(reg.free_bins()) == 8
        assert len(reg.occupied_bins()) == 0

    def test_allocate(self) -> None:
        reg = TimeBinRegister(n_bins=4)
        slot = reg.allocate(bin_index=2, module_name="test_module")
        assert slot.occupied
        assert slot.module_name == "test_module"
        assert len(reg.free_bins()) == 3

    def test_double_allocate_raises(self) -> None:
        reg = TimeBinRegister(n_bins=4)
        reg.allocate(bin_index=1, module_name="alpha")
        with pytest.raises(ValueError):
            reg.allocate(bin_index=1, module_name="beta")

    def test_out_of_range_raises(self) -> None:
        reg = TimeBinRegister(n_bins=4)
        with pytest.raises(IndexError):
            reg.allocate(bin_index=99, module_name="ghost")


class TestQuantumHardwareModule:
    def test_instantiation(self) -> None:
        mod = QuantumHardwareModule(name="test_ion", module_type=ModuleType.TRAPPED_ION)
        assert mod.name == "test_ion"
        assert mod.module_type == ModuleType.TRAPPED_ION
        assert mod.connected_time_bin is None

    def test_emit_without_registration_raises(self) -> None:
        mod = QuantumHardwareModule(name="orphan")
        with pytest.raises(RuntimeError):
            mod.emit_photon()

    def test_emit_after_registration(self) -> None:
        mod = QuantumHardwareModule(name="ion_a", module_type=ModuleType.TRAPPED_ION)
        mod._assign_time_bin(3)
        emission = mod.emit_photon()
        assert emission.module_name == "ion_a"
        assert emission.time_bin == 3
        assert emission.success is True


class TestGreenMachineInterconnect:
    def test_instantiation(self) -> None:
        ic = GreenMachineInterconnect(n_time_bins=8)
        assert ic.n_time_bins == 8
        assert ic.registered_modules() == []

    def test_requires_at_least_two_bins(self) -> None:
        with pytest.raises(ValueError):
            GreenMachineInterconnect(n_time_bins=1)

    def test_register_module(self) -> None:
        ic = GreenMachineInterconnect(n_time_bins=8)
        mod = QuantumHardwareModule(name="alpha", module_type=ModuleType.NV_CENTER)
        ic.register_module(mod, time_bin_index=0)
        assert len(ic.registered_modules()) == 1
        assert mod.connected_time_bin == 0

    def test_duplicate_module_name_raises(self) -> None:
        ic = GreenMachineInterconnect(n_time_bins=8)
        mod1 = QuantumHardwareModule(name="dup")
        mod2 = QuantumHardwareModule(name="dup")
        ic.register_module(mod1, time_bin_index=0)
        with pytest.raises(ValueError):
            ic.register_module(mod2, time_bin_index=1)

    def test_summary_runs(self) -> None:
        ic = GreenMachineInterconnect(n_time_bins=8)
        ic.register_module(QuantumHardwareModule("a", ModuleType.TRAPPED_ION), 0)
        ic.register_module(QuantumHardwareModule("b", ModuleType.NV_CENTER), 1)
        summary = ic.summary()
        assert "trapped_ion" in summary
        assert "nv_center" in summary


class TestBoostedBSM:
    def test_standard_bsm_success_probability(self) -> None:
        bsm = BoostedBSM(n_ancilla_modes=0)
        assert bsm.success_probability == pytest.approx(0.50)

    def test_boosted_bsm_success_probability(self) -> None:
        bsm = BoostedBSM(n_ancilla_modes=4)
        assert bsm.success_probability == pytest.approx(0.75)

    def test_default_is_boosted(self) -> None:
        bsm = BoostedBSM()
        assert bsm.n_ancilla_modes == 4
        assert bsm.success_probability == pytest.approx(0.75)

    def test_attempt_measurement_returns_outcome(self) -> None:
        bsm = BoostedBSM(n_ancilla_modes=4)
        outcome = bsm.attempt_measurement("alpha", "beta")
        assert isinstance(outcome, BSMOutcome)
        assert outcome.success is True
        assert outcome.n_ancilla_modes == 4

    def test_negative_ancilla_raises(self) -> None:
        with pytest.raises(ValueError):
            BoostedBSM(n_ancilla_modes=-1)


class TestDistributedLogicalQubit:
    def test_instantiation(self) -> None:
        lq = DistributedLogicalQubit(["a", "b", "c"], label="L0")
        assert lq.n_modules == 3
        assert set(lq.active_modules) == {"a", "b", "c"}

    def test_requires_at_least_two_modules(self) -> None:
        with pytest.raises(ValueError):
            DistributedLogicalQubit(["solo"])

    def test_mark_failed(self) -> None:
        lq = DistributedLogicalQubit(["a", "b", "c"])
        lq.mark_failed("b")
        assert "b" in lq.failed_modules
        assert "b" not in lq.active_modules
        assert len(lq.active_modules) == 2

    def test_mark_unknown_module_raises(self) -> None:
        lq = DistributedLogicalQubit(["a", "b"])
        with pytest.raises(KeyError):
            lq.mark_failed("ghost")

    def test_status_report_runs(self) -> None:
        lq = DistributedLogicalQubit(["a", "b", "c"])
        report = lq.status_report()
        assert "L0" in report
