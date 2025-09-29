"""
configure_pyvista_notebook
Idempotent, safe setup for PyVista 'client' mode in Jupyter/Binder.

Usage:
    import configure_pyvista_notebook  # auto-runs setup()
or:
    from configure_pyvista_notebook import setup
    setup()
"""

from __future__ import annotations
import os

# Cache so repeated imports don't re-run side effects
_ALREADY_RAN = False


def _silence_vtk():
    # Turn off VTK stderr chatter (X/EGL/OSMesa probes, etc.)
    try:
        from vtkmodules.vtkCommonCore import vtkLogger

        # VERBOSITY_OFF = 0; keep attribute-based access to avoid import surprises
        vtkLogger.SetStderrVerbosity(0)
    except Exception:
        pass

    try:
        import vtk

        vtk.vtkObject.GlobalWarningDisplayOff()
    except Exception:
        pass


def _unset_offscreen_env():
    # Ensure we don't trigger native/off-screen probing paths
    for var in ("PYVISTA_OFF_SCREEN", "PYVISTA_USE_IPYVTK"):  # second is just in case
        os.environ.pop(var, None)


def _set_client_backend():
    import pyvista as pv

    # Only change if not already explicitly set by user
    try:
        pv.set_jupyter_backend("client")
    except Exception:
        # Fallback: some old envs need a lazy import of trame pieces; ignore if unavailable
        pass


def setup(silent: bool = True, backend: str = "client"):
    """Configure PyVista for Jupyter/Binder.

    Args:
        silent: hide VTK warnings on stderr and disable warning popups
        backend: jupyter backend to use ("client" recommended here)
    """
    global _ALREADY_RAN
    if _ALREADY_RAN:
        return

    if silent:
        _silence_vtk()
    _unset_offscreen_env()

    if backend == "client":
        _set_client_backend()

    _ALREADY_RAN = True


# auto-run on import
setup()
