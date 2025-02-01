"""Provides targets and tools for web requests."""

import uuid
from typing import Final

import requests

from embark.domain.tasks.task import (
    AbstractExecutionTarget,
    TaskExecutionContext
)
from embark.use_case.progress import ProgressReporter


_CHUNK_SIZE: Final = 4096


class DownloadFileTarget(AbstractExecutionTarget):
    """Target for file downloading."""

    def __init__(self, url: str, dst_file: str, timeout_s: int) -> None:
        """Create target."""
        self.url = url
        self.dst_file = dst_file
        self.timeout_s = timeout_s

    def execute(self, context: TaskExecutionContext) -> bool:  # noqa: WPS210
        variables = context.playbook_context.playbook.variables
        url = variables.format(self.url)
        dst = variables.format(self.dst_file)
        dst = context.playbook_context.file_path(dst)
        with (
            open(dst, "wb") as target_file,
            ProgressReporter(
                context.task.logger,
                str(uuid.uuid4()),
                f"Download {url}"
            ) as reporter
        ):
            response = requests.get(url, stream=True, timeout=self.timeout_s)
            total_length_str = response.headers.get('content-length')
            if total_length_str is None:
                target_file.write(response.content)
                return True
            total_length = int(total_length_str)
            dl = 0
            prev_progress: float = -1
            for chunk in response.iter_content(chunk_size=_CHUNK_SIZE):
                dl += len(chunk)
                target_file.write(chunk)
                progress = dl / total_length
                if int(progress * 100) != int(prev_progress * 100):
                    reporter.set_progress(progress)
                prev_progress = progress
        return True

    def get_display_name(self) -> str:
        return f"Download {self.url} -> {self.dst_file}"
