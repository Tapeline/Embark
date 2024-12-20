"""
Provides targets and tools for web requests
"""

import sys

import requests

from embark.domain.tasks.task import AbstractExecutionTarget, TaskExecutionContext


class DownloadFileTarget(AbstractExecutionTarget):
    """Target for file downloading"""
    def __init__(self, url: str, dst_file: str, timeout_s: int):
        self.url = url
        self.dst_file = dst_file
        self.timeout_s = timeout_s

    def execute(self, context: TaskExecutionContext) -> bool:
        url = context.playbook_context.playbook.variables.format(self.url)
        dst = context.playbook_context.playbook.variables.format(self.dst_file)
        dst = context.playbook_context.file_path(dst)
        with open(dst, "wb") as f:
            response = requests.get(url, stream=True, timeout=self.timeout_s)
            total_length = response.headers.get('content-length')
            if total_length is None:
                f.write(response.content)
            else:
                dl = 0
                total_length = int(total_length)
                for data in response.iter_content(chunk_size=4096):
                    dl += len(data)
                    f.write(data)
                    done = int(50 * dl / total_length)
                    sys.stdout.write(f"\r[{'=' * done}{' ' * (50 - done)}]")
                    sys.stdout.flush()
        print()
        return True

    def get_display_name(self) -> str:
        return f"Download {self.url} -> {self.dst_file}"
