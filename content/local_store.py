import os
import json
import time
import shutil
import hashlib
from pathlib import Path
from typing import Dict, Any, Tuple
from content.store import ContentStore, ContentConflictError, ContentNotFoundError

class LocalFileContentStore(ContentStore):
    def __init__(self, base_dir: str = None):
        if base_dir is None:
            # Locate backend/data/content relative to this file
            current_dir = Path(__file__).resolve().parent
            resolved_path = current_dir.parent / "data" / "content"
            if resolved_path.exists():
                self.base_dir = resolved_path
            else:
                self.base_dir = Path("data/content").resolve()
        else:
            self.base_dir = Path(base_dir).resolve()
        
        self.backup_dir = self.base_dir / "backups"
        
        # Ensure directories exist
        self.base_dir.mkdir(parents=True, exist_ok=True)
        self.backup_dir.mkdir(parents=True, exist_ok=True)

    def _get_file_path(self, filename: str) -> Path:
        # Prevent directory traversal
        clean_name = os.path.basename(filename)
        return self.base_dir / clean_name

    def _compute_git_sha(self, content_str: str) -> str:
        """Computes the Git blob SHA-1 of the content string."""
        data_bytes = content_str.encode('utf-8')
        header = f"blob {len(data_bytes)}\x00".encode('ascii')
        sha1 = hashlib.sha1()
        sha1.update(header)
        sha1.update(data_bytes)
        return sha1.hexdigest()

    def read(self, filename: str) -> Tuple[Dict[str, Any], str]:
        path = self._get_file_path(filename)
        if not path.exists():
            raise ContentNotFoundError(f"File {filename} not found in local store.")
        
        with open(path, "r", encoding="utf-8-sig") as f:
            raw_content = f.read()
        
        # Strip any residual BOM that might have slipped past utf-8-sig
        raw_content = raw_content.lstrip('\ufeff')
        
        content_dict = json.loads(raw_content)
        sha = self._compute_git_sha(raw_content)
        return content_dict, sha

    def write(self, filename: str, content: Dict[str, Any], sha: str, message: str) -> str:
        path = self._get_file_path(filename)
        
        # Verify SHA for optimistic concurrency check
        if path.exists() and sha:
            with open(path, "r", encoding="utf-8-sig") as f:
                existing_raw = f.read()
            existing_raw = existing_raw.lstrip('\ufeff')
            current_sha = self._compute_git_sha(existing_raw)
            if sha != current_sha:
                raise ContentConflictError(
                    f"Conflict: File {filename} has been modified (provided SHA {sha} != current SHA {current_sha})"
                )
        
        # Create backup if file already exists
        if path.exists():
            timestamp = int(time.time() * 1000)
            backup_path = self.backup_dir / f"{filename}.{timestamp}.bak"
            shutil.copy2(path, backup_path)
            
        # Write updated content (we normalize formatting to indent=2 to match portal/original style)
        new_raw = json.dumps(content, indent=2, ensure_ascii=False)
        with open(path, "w", encoding="utf-8") as f:
            f.write(new_raw)
            
        return self._compute_git_sha(new_raw)
