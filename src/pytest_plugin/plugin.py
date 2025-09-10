"""
Modern pytest plugin template with clean hook implementations.
"""
import pytest
from pytest import Item, Config, Session, TestReport, CallInfo
from pathlib import Path
from typing import Optional, List, Union, Any
import warnings


class PytestPluginTemplate:
    """
    A modern pytest plugin template with commonly used hooks.
    
    This plugin demonstrates best practices for:
    - Hook registration using @pytest.hookimpl
    - Proper configuration management
    - Lazy initialization
    - Clean separation of concerns
    """
    
    def __init__(self):
        pass
    
    # ========== CONFIGURATION HOOKS ==========
    
    @pytest.hookimpl
    def pytest_configure(self, config: Config) -> None:
        pass
    
    @pytest.hookimpl
    def pytest_unconfigure(self, config: Config) -> None:
        pass

    # ========== SESSION HOOKS ==========
    
    @pytest.hookimpl
    def pytest_sessionstart(self, session: Session) -> None:
        pass
    
    @pytest.hookimpl
    def pytest_sessionfinish(self, session: Session, exitstatus: int) -> None:
        pass
    
    # ========== COLLECTION HOOKS ==========
    
    @pytest.hookimpl
    def pytest_collection_modifyitems(self, config: Config, items: List[Item]) -> None:
        if not self.enabled:
            return
        # Add your item modification logic here
    
    @pytest.hookimpl
    def pytest_generate_tests(self, metafunc) -> None:
        pass
    
    # ========== TEST EXECUTION HOOKS ==========

    @pytest.hookimpl
    def pytest_runtest_protocol(self, item: Item, nextitem: Optional[Item]) -> None:
        pass

    @pytest.hookimpl
    def pytest_runtest_setup(self, item: Item) -> None:
        """Called before each test setup."""
        pass

    @pytest.hookimpl
    def pytest_runtest_call(self, item: Item) -> None:
        """Called before each test call."""
        pass

    @pytest.hookimpl
    def pytest_runtest_teardown(self, item: Item, nextitem: Optional[Item]) -> None:
        """Called after each test teardown."""
        pass

    @pytest.hookimpl
    def pytest_runtest_makereport(self, item: Item, call: CallInfo) -> None:
        """Called to create a TestReport for each test phase."""
        pass

    @pytest.hookimpl
    def pytest_runtest_logreport(self, report: TestReport) -> None:
        """Called when a test report is ready to be logged."""
        pass

    # ========== REPORTING HOOKS ==========
    
    @pytest.hookimpl
    def pytest_report_header(self, config: Config, start_path: Path) -> Union[str, List[str]]:
        """Add information to the test report header."""
        pass
    
    @pytest.hookimpl
    def pytest_terminal_summary(self, terminalreporter, exitstatus: int, config: Config) -> None:
        """Add a section to the terminal summary reporting."""
        if not self.enabled:
            return
        # Add your terminal summary logic here
    
    # ========== ERROR/WARNING HOOKS ==========
    
    @pytest.hookimpl
    def pytest_warning_recorded(self, warning_message: warnings.WarningMessage, when: str, nodeid: str, location: tuple) -> None:
        """Called when a warning is recorded."""
        pass
    
    @pytest.hookimpl
    def pytest_exception_interact(self, node, call: CallInfo, report: TestReport) -> None:
        """Called when an exception occurred and can be interacted with."""
        pass

    # ========== HELPER METHODS ==========
    
    # Write your helper methods here

# Plugin instance - rename this for your specific plugin
_plugin_instance = PytestPluginTemplate()


def pytest_addoption(parser) -> None:
    """Add command-line options for the plugin."""
    group = parser.getgroup("template_plugin", "Template Plugin Options")
    
    # Add your custom options here
    group.addoption(
        "--enable-template",
        action="store_true",
        default=False,
        help="Enable the template plugin functionality"
    )


def pytest_configure(config):
    """Register the plugin instance."""
    config.pluginmanager.register(_plugin_instance, "template-plugin")


def pytest_unconfigure(config):
    """Unregister the plugin instance."""
    plugin = config.pluginmanager.get_plugin("template-plugin")
    if plugin:
        config.pluginmanager.unregister(plugin)