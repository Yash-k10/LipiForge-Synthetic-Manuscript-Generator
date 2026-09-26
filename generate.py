import os
import argparse
import random
from PIL import Image
from pipeline.background import generate_background
from pipeline.renderer import render_folio
from pipeline.corpus import CorpusManager
from pipeline.uploader import upload_dataset

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--count', type=int, default=100)
    parser.add_argument('--output_dir', type=str, default='dataset')
    parser.add_argument('--push_to_hub', action='store_true')
    parser.add_argument('--hf_repo', type=str, default='Yash-kapse/synthetic-manuscripts')
    parser.add_argument('--hf_token', type=str, default=None)
    return parser.parse_args()

def generate_dataset(count=100, output_dir='dataset'):
    scripts = ['devanagari', 'modi', 'sharada']
    n_train = int(count * 0.85)
    n_val = int(count * 0.10)
    n_test = count - n_train - n_val

    splits = [
        ('train', n_train),
        ('validation', n_val),
        ('test', n_test)
    ]

    corpus = CorpusManager()
    styles = ['vibrant_ancient', 'classical_aged', 'palm_leaf', 'tea_patina']

    for script in scripts:
        print(f"Generating {script.upper()} ({count} folios)...")
        folio_idx = 1

        for split_name, split_count in splits:
            split_dir = os.path.join(output_dir, script, split_name)
            os.makedirs(split_dir, exist_ok=True)

            for _ in range(split_count):
                w = random.randint(1120, 1180)
                h = random.randint(580, 640)
                bg = generate_background(width=w, height=h, style=random.choice(styles))

                lines = corpus.sample(script, n_lines=14)
                img, gt = render_folio(bg, lines, script=script)

                name = f"folio_{folio_idx:03d}"
                Image.fromarray(img).save(os.path.join(split_dir, f"{name}.png"))
                with open(os.path.join(split_dir, f"{name}.md"), 'w', encoding='utf-8') as f:
                    f.write(gt)

                folio_idx += 1

            print(f"  {script}/{split_name}: {split_count} folios done.")

    print(f"\nFinished: 300 folios generated across 3 scripts in '{output_dir}'.")

def main():
    args = parse_args()
    generate_dataset(count=args.count, output_dir=args.output_dir)

    if args.push_to_hub:
        upload_dataset(
            dataset_dir=args.output_dir,
            repo_id=args.hf_repo,
            token=args.hf_token
        )

if __name__ == '__main__':
    main()
