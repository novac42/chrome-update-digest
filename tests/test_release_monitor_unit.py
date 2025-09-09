"""
Comprehensive unit tests for release monitoring with mocks.
"""

import json
import sys
import tempfile
from pathlib import Path
from unittest.mock import MagicMock, Mock, patch, mock_open
import pytest

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from utils.release_monitor_core import ReleaseMonitorCore
from mcp_tools.release_monitor import ReleaseMonitorTool


class TestReleaseMonitorCore:
    """Unit tests for ReleaseMonitorCore with mocks."""
    
    @pytest.fixture
    def temp_dir(self):
        """Create a temporary directory for testing."""
        with tempfile.TemporaryDirectory() as tmpdir:
            yield Path(tmpdir)
    
    @pytest.fixture
    def monitor(self, temp_dir):
        """Create a ReleaseMonitorCore instance with temporary directory."""
        return ReleaseMonitorCore(temp_dir)
    
    def test_scan_existing_versions_stable_channel(self, monitor, temp_dir):
        """Test scanning for stable channel versions (no channel suffix)."""
        # Create test files
        webplatform_dir = temp_dir / "upstream_docs" / "release_notes" / "webplatform"
        webplatform_dir.mkdir(parents=True)
        
        # Create stable versions (no channel suffix)
        (webplatform_dir / "chrome-136.md").touch()
        (webplatform_dir / "chrome-137.md").touch()
        (webplatform_dir / "chrome-138.md").touch()
        
        # Create beta versions (with channel suffix)
        (webplatform_dir / "chrome-139-beta.md").touch()
        (webplatform_dir / "chrome-140-beta.md").touch()
        
        # Create WebGPU versions
        (webplatform_dir / "webgpu-136.md").touch()
        (webplatform_dir / "webgpu-137.md").touch()
        
        # Test stable channel scanning
        versions = monitor.scan_existing_versions("stable")
        
        assert versions["webplatform"] == {136, 137, 138}
        assert 139 not in versions["webplatform"]  # Beta version should not be included
        assert 140 not in versions["webplatform"]  # Beta version should not be included
        assert versions["webgpu"] == {136, 137}
    
    def test_scan_existing_versions_beta_channel(self, monitor, temp_dir):
        """Test scanning for beta channel versions."""
        # Create test files
        webplatform_dir = temp_dir / "upstream_docs" / "release_notes" / "webplatform"
        webplatform_dir.mkdir(parents=True)
        
        # Create stable versions
        (webplatform_dir / "chrome-136.md").touch()
        (webplatform_dir / "chrome-137.md").touch()
        
        # Create beta versions
        (webplatform_dir / "chrome-139-beta.md").touch()
        (webplatform_dir / "chrome-140-beta.md").touch()
        
        # Test beta channel scanning
        versions = monitor.scan_existing_versions("beta")
        
        assert versions["webplatform"] == {139, 140}
        assert 136 not in versions["webplatform"]  # Stable version should not be included
        assert 137 not in versions["webplatform"]  # Stable version should not be included
    
    def test_detect_missing_stable_versions(self, monitor, temp_dir):
        """Test detection of missing stable versions when beta exists."""
        # Create test files
        webplatform_dir = temp_dir / "upstream_docs" / "release_notes" / "webplatform"
        webplatform_dir.mkdir(parents=True)
        
        # Create stable versions
        (webplatform_dir / "chrome-136.md").touch()
        (webplatform_dir / "chrome-137.md").touch()
        
        # Create beta versions (139 has beta but no stable, 140 has beta but no stable)
        (webplatform_dir / "chrome-139-beta.md").touch()
        (webplatform_dir / "chrome-140-beta.md").touch()
        
        # Also create a stable version that has both stable and beta
        (webplatform_dir / "chrome-138.md").touch()
        (webplatform_dir / "chrome-138-beta.md").touch()
        
        # Test missing stable detection
        missing = monitor.detect_missing_stable_versions()
        
        assert 139 in missing  # Has beta but no stable
        assert 140 in missing  # Has beta but no stable
        assert 138 not in missing  # Has both stable and beta
        assert 136 not in missing  # Only has stable (no beta)
    
    @patch('utils.release_monitor_core.requests.get')
    def test_detect_latest_webplatform_version(self, mock_get, monitor):
        """Test detecting latest Chrome version from web."""
        # Mock responses for version probing
        mock_responses = []
        
        # Versions 136-138 exist
        for version in [136, 137, 138]:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_responses.append(mock_response)
        
        # Version 139 doesn't exist (404)
        mock_404 = Mock()
        mock_404.status_code = 404
        mock_responses.append(mock_404)
        
        mock_get.side_effect = mock_responses
        
        with patch.object(monitor, 'scan_existing_versions', return_value={"webplatform": {135}}):
            latest = monitor.detect_latest_webplatform_version()
        
        assert latest == 138  # Should detect 138 as the latest
    
    @patch('utils.release_monitor_core.requests.get')
    def test_detect_latest_webgpu_version(self, mock_get, monitor):
        """Test detecting latest WebGPU version from web."""
        # Mock HTML response with WebGPU versions
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = """
        <html>
        <body>
            <a href="/webgpu-134/">WebGPU 134</a>
            <a href="/webgpu-135/">WebGPU 135</a>
            <a href="/webgpu-136/">WebGPU 136</a>
        </body>
        </html>
        """
        mock_get.return_value = mock_response
        
        latest = monitor.detect_latest_webgpu_version()
        
        assert latest == 136  # Should detect 136 as the latest
    
    
    @patch('utils.release_monitor_core.requests.get')
    @patch('utils.release_monitor_core.html2text.html2text')
    def test_download_chrome_release(self, mock_html2text, mock_get, monitor, temp_dir):
        """Test downloading Chrome release notes."""
        # Mock HTML response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = "<html><body>Chrome 138 Release Notes</body></html>"
        mock_get.return_value = mock_response
        
        # Mock html2text conversion
        mock_html2text.return_value = "# Chrome 138 Release Notes\n\nContent here..."
        
        result = monitor.download_chrome_release(138, "stable")
        
        assert result["success"] is True
        assert result["version"] == 138
        assert result["channel"] == "stable"
        
        # Check file was created
        expected_file = temp_dir / "upstream_docs" / "release_notes" / "webplatform" / "chrome-138.md"
        assert expected_file.exists()
    
    @patch('utils.release_monitor_core.requests.get')
    @patch('utils.release_monitor_core.html2text.html2text')
    def test_download_chrome_release_beta(self, mock_html2text, mock_get, monitor, temp_dir):
        """Test downloading Chrome beta release notes."""
        # Mock HTML response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = "<html><body>Chrome 139 Beta Release Notes</body></html>"
        mock_get.return_value = mock_response
        
        # Mock html2text conversion
        mock_html2text.return_value = "# Chrome 139 Beta Release Notes\n\nContent here..."
        
        result = monitor.download_chrome_release(139, "beta")
        
        assert result["success"] is True
        assert result["version"] == 139
        assert result["channel"] == "beta"
        
        # Check file was created with beta suffix
        expected_file = temp_dir / "upstream_docs" / "release_notes" / "webplatform" / "chrome-139-beta.md"
        assert expected_file.exists()
    
    def test_update_version_tracking_with_locking(self, monitor, temp_dir):
        """Test version tracking update with file locking."""
        # Create versions file directory
        versions_dir = temp_dir / "upstream_docs" / "processed_releasenotes"
        versions_dir.mkdir(parents=True)
        
        # Update tracking for different types
        monitor.update_version_tracking("chrome", 138)
        monitor.update_version_tracking("chrome", 139)
        monitor.update_version_tracking("webgpu", 136)
        
        # Read the tracking file
        versions_file = versions_dir / "downloaded_versions.json"
        assert versions_file.exists()
        
        with open(versions_file) as f:
            data = json.load(f)
        
        assert 138 in data["chrome"]
        assert 139 in data["chrome"]
        assert 136 in data["webgpu"]
        assert "last_check" in data
    
    @patch('utils.release_monitor_core.fcntl.flock')
    def test_update_version_tracking_concurrent_access(self, mock_flock, monitor, temp_dir):
        """Test that file locking is properly used for concurrent access protection."""
        # Create versions file directory
        versions_dir = temp_dir / "upstream_docs" / "processed_releasenotes"
        versions_dir.mkdir(parents=True)
        
        # Update tracking
        monitor.update_version_tracking("chrome", 138)
        
        # Verify that flock was called with proper arguments
        assert mock_flock.called
        # Check that LOCK_EX was used for exclusive lock
        import fcntl
        lock_calls = [call for call in mock_flock.call_args_list if call[0][1] == fcntl.LOCK_EX]
        assert len(lock_calls) > 0


class TestReleaseMonitorTool:
    """Unit tests for ReleaseMonitorTool MCP wrapper."""
    
    @pytest.fixture
    def temp_dir(self):
        """Create a temporary directory for testing."""
        with tempfile.TemporaryDirectory() as tmpdir:
            yield Path(tmpdir)
    
    @pytest.fixture
    def tool(self, temp_dir):
        """Create a ReleaseMonitorTool instance."""
        return ReleaseMonitorTool(temp_dir)
    
    @pytest.mark.asyncio
    async def test_check_latest_releases_input_validation(self, tool):
        """Test input validation for channel and release_type parameters."""
        ctx = Mock()
        
        # Test invalid channel
        result = await tool.check_latest_releases(ctx, {"channel": "invalid"})
        data = json.loads(result)
        assert data["status"] == "error"
        assert "Unsupported channel" in data["error"]
        
        # Test invalid release_type
        result = await tool.check_latest_releases(ctx, {"release_type": "invalid"})
        data = json.loads(result)
        assert data["status"] == "error"
        assert "Unsupported release_type" in data["error"]
        
        # Test valid parameters
        with patch.object(tool.core, 'scan_existing_versions', return_value={"webplatform": set(), "webgpu": set()}):
            with patch.object(tool.core, 'detect_latest_webplatform_version', return_value=None):
                with patch.object(tool.core, 'detect_latest_webgpu_version', return_value=None):
                    result = await tool.check_latest_releases(ctx, {"channel": "stable", "release_type": "webplatform"})
                    data = json.loads(result)
                    assert data["status"] == "success"
    
    @pytest.mark.asyncio
    async def test_check_latest_releases_missing_stable_detection(self, tool):
        """Test that missing stable versions are properly reported."""
        ctx = Mock()
        
        with patch.object(tool.core, 'scan_existing_versions', return_value={"webplatform": {138}, "webgpu": set()}):
            with patch.object(tool.core, 'detect_missing_stable_versions', return_value=[139, 140]):
                with patch.object(tool.core, 'detect_latest_webplatform_version', return_value=140):
                    with patch.object(tool.core, 'detect_latest_webgpu_version', return_value=None):
                        result = await tool.check_latest_releases(ctx, {"channel": "stable", "release_type": "webplatform"})
                        data = json.loads(result)
                        
                        assert data["status"] == "success"
                        assert "missing_stable_with_beta" in data["webplatform"]
                        assert 139 in data["webplatform"]["missing_stable_with_beta"]
                        assert 140 in data["webplatform"]["missing_stable_with_beta"]
    
    @pytest.mark.asyncio
    async def test_crawl_missing_releases_requires_confirmation(self, tool):
        """Test that crawling requires user confirmation."""
        ctx = Mock()
        
        # Test without confirmation
        result = await tool.crawl_missing_releases(ctx, {"confirmed": False})
        data = json.loads(result)
        assert data["status"] == "error"
        assert "confirmation required" in data["error"].lower()
        
        # Test with confirmation but invalid parameters
        result = await tool.crawl_missing_releases(ctx, {"confirmed": True, "channel": "invalid"})
        data = json.loads(result)
        assert data["status"] == "error"
        assert "Unsupported channel" in data["error"]
    
    @pytest.mark.asyncio  
    async def test_crawl_missing_releases_with_confirmation(self, tool):
        """Test crawling with proper confirmation."""
        ctx = Mock()
        
        # Mock the check_latest_releases to return missing releases
        check_result = {
            "status": "success",
            "webplatform": {
                "chrome": {
                    "latest_available": 139,
                    "is_missing": True
                }
            }
        }
        
        with patch.object(tool, 'check_latest_releases', return_value=json.dumps(check_result)):
            with patch.object(tool.core, 'download_chrome_release', return_value={"success": True, "version": 139, "file": "chrome-139.md"}):
                result = await tool.crawl_missing_releases(ctx, {
                    "confirmed": True,
                    "release_type": "webplatform",
                    "channel": "stable"
                })
                data = json.loads(result)
                
                assert data["status"] == "success"
                assert len(data["downloaded"]) > 0
                assert "Chrome 139" in data["downloaded"][0]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])