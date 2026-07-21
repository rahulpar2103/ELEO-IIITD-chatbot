import os
import sys
import shutil
import tempfile
import unittest
from fastapi.testclient import TestClient

# Ensure backend root is on sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from api.main import app
from content.local_store import LocalFileContentStore
from content.store import ContentConflictError, ContentNotFoundError

class TestContentStore(unittest.TestCase):
    def setUp(self):
        # Create a temporary directory for local store testing
        self.test_dir = tempfile.mkdtemp()
        self.store = LocalFileContentStore(base_dir=self.test_dir)
        
        # Write a sample file
        self.filename = "index.json"
        self.sample_data = {"announcements": [{"title": "Test notice"}]}
        
        # Write initial file
        self.initial_sha = self.store.write(
            self.filename, 
            self.sample_data, 
            sha=None, 
            message="Initial setup"
        )

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_read_success(self):
        content, sha = self.store.read(self.filename)
        self.assertEqual(content, self.sample_data)
        self.assertEqual(sha, self.initial_sha)

    def test_read_not_found(self):
        with self.assertRaises(ContentNotFoundError):
            self.store.read("nonexistent.json")

    def test_write_concurrency_success(self):
        updated_data = {"announcements": [{"title": "Test notice updated"}]}
        
        # Update using correct SHA should succeed
        new_sha = self.store.write(
            self.filename,
            updated_data,
            sha=self.initial_sha,
            message="Update successfully"
        )
        self.assertNotEqual(new_sha, self.initial_sha)
        
        # Read back and verify
        content, sha = self.store.read(self.filename)
        self.assertEqual(content, updated_data)
        self.assertEqual(sha, new_sha)

    def test_write_concurrency_conflict(self):
        updated_data = {"announcements": [{"title": "Test notice conflict"}]}
        
        # Try to write with stale/wrong SHA
        wrong_sha = "wrongsha1234567890"
        with self.assertRaises(ContentConflictError):
            self.store.write(
                self.filename,
                updated_data,
                sha=wrong_sha,
                message="This should fail"
            )

class TestContentApi(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)
        self.test_dir = tempfile.mkdtemp()
        
        # Mock get_content_store in the router and other modules to avoid real GitHub API calls
        import api.content_router
        import content
        import content.store
        
        self.original_router_store = api.content_router.get_content_store
        self.original_content_store = content.get_content_store
        self.original_store_store = content.store.get_content_store
        
        self.local_store = LocalFileContentStore(base_dir=self.test_dir)
        mock_func = lambda: self.local_store
        
        api.content_router.get_content_store = mock_func
        content.get_content_store = mock_func
        content.store.get_content_store = mock_func
        
        # Populate a valid test file
        self.local_store.write("index.json", {"test": "data"}, sha=None, message="init")

    def tearDown(self):
        import api.content_router
        import content
        import content.store
        
        api.content_router.get_content_store = self.original_router_store
        content.get_content_store = self.original_content_store
        content.store.get_content_store = self.original_store_store
        
        shutil.rmtree(self.test_dir)

    def test_get_content_list(self):
        resp = self.client.get("/content")
        self.assertEqual(resp.status_code, 200)
        self.assertIn({"name": "index.json"}, resp.json())

    def test_get_content_success(self):
        resp = self.client.get("/content/index.json")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json(), {"test": "data"})
        self.assertIn("ETag", resp.headers)
        self.assertIn("X-Content-SHA", resp.headers)

    def test_get_content_invalid_file(self):
        resp = self.client.get("/content/malicious_file.json")
        self.assertEqual(resp.status_code, 400)

    def test_put_content_success(self):
        # 1. GET to get the ETag
        get_resp = self.client.get("/content/index.json")
        sha = get_resp.headers["X-Content-SHA"]
        
        # 2. PUT to update
        put_resp = self.client.put(
            "/content/index.json",
            json={"test": "new data"},
            headers={"X-Content-SHA": sha}
        )
        self.assertEqual(put_resp.status_code, 200)
        self.assertTrue(put_resp.json()["success"])
        self.assertNotEqual(put_resp.json()["version"], sha)

    def test_put_content_conflict(self):
        resp = self.client.put(
            "/content/index.json",
            json={"test": "conflict data"},
            headers={"X-Content-SHA": "stalesha"}
        )
        self.assertEqual(resp.status_code, 409)
