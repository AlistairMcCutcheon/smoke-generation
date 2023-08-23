import torch
from datasets import DatasetDict
from torch.utils.data import Dataset
from PIL import Image
import numpy as np
from utils.file_utils import list_image_files_recursively


class Preprocessor(object):
    def __init__(self, args, meta_args):
        self.args = args
        self.meta_args = meta_args

    def preprocess(self, raw_datasets: DatasetDict, cache_root: str):
        assert len(raw_datasets) == 3  # Not always.
        train_dataset = TrainDataset(
            self.args, self.meta_args, raw_datasets["train"], cache_root
        )
        dev_dataset = DevDataset(
            self.args, self.meta_args, raw_datasets["validation"], cache_root
        )

        return {
            "train": train_dataset,
            "dev": dev_dataset,
        }


class TrainDataset(Dataset):
    def __init__(self, args, meta_args, raw_datasets, cache_root):
        self.data = []

    def __getitem__(self, index):
        raise NotImplementedError()

    def __len__(self):
        return len(self.data)


class DevDataset(Dataset):
    def __init__(self, args, meta_args, raw_datasets, cache_root):
        self.root_dir = "../data/DFire/clean/test/empty"

        self.file_names = list_image_files_recursively(self.root_dir)

        self.data = [
            {
                "sample_id": torch.LongTensor([idx]).squeeze(0),
                "file_name": file_name,
                "model_kwargs": [
                    "sample_id",
                ],
            }
            for idx, file_name in enumerate(self.file_names)
        ]

    def __getitem__(self, index):
        data = {k: v for k, v in self.data[index].items()}

        # Add image.
        img = np.array(Image.open(data["file_name"])).transpose(2, 0, 1)

        # Add image.
        data["original_image"] = img
        data["model_kwargs"] = data["model_kwargs"] + [
            "original_image",
        ]

        return data

    def __len__(self):
        return len(self.data)
        # return 4
