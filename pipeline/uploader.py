import os
from huggingface_hub import HfApi

def upload_dataset(dataset_dir='dataset', repo_id='Yash-kapse/synthetic-manuscripts', token=None):
    token = token or os.environ.get('HF_TOKEN')
    if not token:
        print("Error: HF_TOKEN not provided.")
        return False

    print(f"Uploading {dataset_dir} to {repo_id}...")
    api = HfApi(token=token)
    try:
        api.create_repo(repo_id=repo_id, repo_type="dataset", exist_ok=True, private=False)
        api.upload_folder(folder_path=dataset_dir, repo_id=repo_id, repo_type="dataset")
        print(f"Uploaded: https://huggingface.co/datasets/{repo_id}")
        return True
    except Exception as e:
        print(f"Upload failed: {e}")
        return False
