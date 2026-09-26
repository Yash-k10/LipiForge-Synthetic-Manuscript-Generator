import os
import random

class CorpusManager:
    def __init__(self, data_dir='.'):
        self.files = {
            'devanagari': os.path.join(data_dir, 'devanagari_md.md'),
            'modi': os.path.join(data_dir, 'Modi_md.md'),
            'sharada': os.path.join(data_dir, 'sharada_md.md')
        }
        self.corpus = {}
        for script, path in self.files.items():
            if os.path.exists(path):
                with open(path, 'r', encoding='utf-8') as f:
                    self.corpus[script] = [l.strip() for l in f if l.strip()]
            else:
                self.corpus[script] = []

    def sample(self, script, n_lines=14):
        lines = self.corpus.get(script, [])
        if not lines:
            return []
        max_idx = max(0, len(lines) - n_lines)
        start = random.randint(0, max_idx)
        return lines[start : start + n_lines]
