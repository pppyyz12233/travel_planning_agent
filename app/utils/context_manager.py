"""上下文管理 —— 对话太长时自动裁剪"""

import tiktoken


class ContextManager:
    def __init__(self, max_tokens=4000):
        self.max_tokens = max_tokens
        self.encoder = tiktoken.get_encoding("cl100k_base")

    def count(self, messages: list[dict]) -> int:
        """算总 token 数"""
        text = "\n".join(m.get("content", "") or "" for m in messages)
        return len(self.encoder.encode(text))

    def compress(self, messages: list[dict]) -> list[dict]:
        """超过上限时，保留 system prompt + 最近的对话"""
        if self.count(messages) <= self.max_tokens:
            return messages

        system_msg = messages[0] if messages[0]["role"] == "system" else None

        # 从后往前保留
        kept = []
        for m in reversed(messages):
            if self.count(kept + [m]) > self.max_tokens:
                break
            kept.insert(0, m)

        if system_msg and system_msg not in kept:
            kept.insert(0, system_msg)

        return kept
