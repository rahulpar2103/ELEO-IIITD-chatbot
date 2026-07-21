import json
import base64
import urllib.request
import urllib.error
from typing import Dict, Any, Tuple
from content.store import ContentStore, ContentConflictError, ContentNotFoundError

class GitHubContentStore(ContentStore):
    def __init__(self, token: str, owner: str, repo: str, branch: str, data_dir_path: str):
        self.token = token
        self.owner = owner
        self.repo = repo
        self.branch = branch
        self.data_dir_path = data_dir_path.strip("/")

    def _get_url(self, filename: str) -> str:
        return f"https://api.github.com/repos/{self.owner}/{self.repo}/contents/{self.data_dir_path}/{filename}"

    def _get_headers(self) -> dict:
        return {
            "Authorization": f"token {self.token}",
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "ELEO-Chatbot-Backend"
        }

    def read(self, filename: str) -> Tuple[Dict[str, Any], str]:
        url = f"{self._get_url(filename)}?ref={self.branch}"
        req = urllib.request.Request(url, headers=self._get_headers())
        try:
            with urllib.request.urlopen(req) as response:
                data = json.loads(response.read().decode('utf-8'))
                
            sha = data.get("sha", "")
            content_b64 = data.get("content", "")
            # Clean up newlines in base64 payload from GitHub
            # Decode with utf-8-sig to strip any BOM from files edited on Windows
            content_str = base64.b64decode(content_b64.replace("\n", "")).decode('utf-8-sig')
            # Strip any residual BOM character
            content_str = content_str.lstrip('\ufeff')
            content_dict = json.loads(content_str)
            return content_dict, sha
        except urllib.error.HTTPError as e:
            if e.code == 404:
                raise ContentNotFoundError(f"File {filename} not found on GitHub.")
            raise Exception(f"GitHub API error during read: {e.read().decode('utf-8', errors='ignore')}")

    def write(self, filename: str, content: Dict[str, Any], sha: str, message: str) -> str:
        url = self._get_url(filename)
        
        # 1. Fetch current remote SHA to verify no external changes (optimistic concurrency check)
        remote_sha = ""
        try:
            req_get = urllib.request.Request(f"{url}?ref={self.branch}", headers=self._get_headers())
            with urllib.request.urlopen(req_get) as resp_get:
                data_get = json.loads(resp_get.read().decode('utf-8'))
                remote_sha = data_get.get("sha", "")
        except urllib.error.HTTPError as e:
            if e.code != 404:
                raise Exception(f"GitHub API error checking remote SHA: {e.read().decode('utf-8', errors='ignore')}")

        # Check for conflict before making the commit call
        if remote_sha and sha != remote_sha:
            raise ContentConflictError(
                f"Conflict: File {filename} was modified on GitHub by another user (provided SHA {sha} != remote SHA {remote_sha})"
            )

        # 2. Write new content
        content_str = json.dumps(content, indent=2, ensure_ascii=False)
        content_b64 = base64.b64encode(content_str.encode('utf-8')).decode('ascii')
        
        payload = {
            "message": message,
            "content": content_b64,
            "branch": self.branch
        }
        if remote_sha:
            payload["sha"] = remote_sha  # GitHub requires the current blob SHA to update

        payload_bytes = json.dumps(payload).encode('utf-8')
        
        req_put = urllib.request.Request(
            url, 
            data=payload_bytes, 
            headers={**self._get_headers(), "Content-Type": "application/json"},
            method="PUT"
        )
        
        try:
            with urllib.request.urlopen(req_put) as resp_put:
                data_put = json.loads(resp_put.read().decode('utf-8'))
                new_sha = data_put.get("content", {}).get("sha", "")
                return new_sha
        except urllib.error.HTTPError as e:
            if e.code == 409:
                raise ContentConflictError(
                    f"Conflict: GitHub returned 409 Conflict. The file {filename} may have been modified concurrently."
                )
            raise Exception(f"GitHub API error during write: {e.read().decode('utf-8', errors='ignore')}")
