import os
from abc import ABC, abstractmethod
from typing import Tuple, Dict, Any

class ContentConflictError(Exception):
    """Exception raised when a write conflict is detected (optimistic concurrency check fails)."""
    pass

class ContentNotFoundError(Exception):
    """Exception raised when a file does not exist in the content store."""
    pass

class ContentStore(ABC):
    @abstractmethod
    def read(self, filename: str) -> Tuple[Dict[str, Any], str]:
        """Reads JSON content from the store.
        
        Args:
            filename: The name of the file (e.g. 'index.json')
            
        Returns:
            A tuple of (content_dict, sha_hash)
            
        Raises:
            ContentNotFoundError: If the file does not exist.
        """
        pass

    @abstractmethod
    def write(self, filename: str, content: Dict[str, Any], sha: str, message: str) -> str:
        """Writes JSON content to the store.
        
        Args:
            filename: The name of the file (e.g. 'index.json')
            content: The new JSON dict to write
            sha: The last known SHA of the file (for optimistic concurrency check)
            message: Commit message (used by GitHub store)
            
        Returns:
            The new SHA of the written file.
            
        Raises:
            ContentConflictError: If the provided SHA does not match the store's current SHA.
        """
        pass

def get_content_store() -> ContentStore:
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        # Avoid circular imports by lazy importing
        from content.github_store import GitHubContentStore
        return GitHubContentStore(
            token=token,
            owner=os.environ.get("GITHUB_REPO_OWNER", "rahulpar2103"),
            repo=os.environ.get("GITHUB_REPO_NAME", "ELEO-IIITD-chatbot"),
            branch=os.environ.get("GITHUB_BRANCH", "master"),
            data_dir_path=os.environ.get("GITHUB_DATA_DIR_PATH", "backend/data/content")
        )
    else:
        from content.local_store import LocalFileContentStore
        return LocalFileContentStore()
