import os
import numpy as np
from collections import defaultdict
from torch.utils.data import Dataset
import pytorch_lightning as pl
from torch.utils.data import DataLoader, Subset

from trajdata import AgentBatch, AgentType, UnifiedDataset

class UnifiedDataModule(pl.LightningDataModule):
    def __init__(self, algo_config, train_config):
        super(UnifiedDataModule, self).__init__()
        self._algo_config = algo_config
        self._train_config = train_config
        self.train_dataset = None
        self.valid_dataset = None
        self.test_dataset = None

    @property
    def modality_shapes(self):
        return dict(
            image=(3 + self._algo_config.history_num_frames + 1,  # semantic map + num_history + current
                   self._algo_config.raster_size,
                   self._algo_config.raster_size),
            static=(3,self._algo_config.raster_size,self._algo_config.raster_size),
            dynamic=(self._algo_config.history_num_frames + 1,self._algo_config.raster_size,self._algo_config.raster_size)

        )

    def setup(self, stage = None):
        data_cfg = self._algo_config
        future_sec = data_cfg.future_num_frames * data_cfg.step_time
        history_sec = data_cfg.history_num_frames * data_cfg.step_time
        neighbor_distance = data_cfg.max_agents_distance
        kwargs = dict(
            desired_data=["train"],
            centric="agent",
            desired_dt=0.1,
            history_sec=(0.9, 0.9),
            future_sec=(3.0, 3.0),
            only_predict=[AgentType.VEHICLE],
            agent_interaction_distances=defaultdict(lambda: 30.0),
            incl_robot_future=False,
            incl_raster_map=True,
            raster_map_params={
                "px_per_m": 2,
                "map_size_px": 224,
                "offset_frac_xy": (-0.5, 0.0),
            },
            num_workers=0,
            obs_format="x,y,xd,yd,xdd,ydd,s,c",
            verbose=True,
            data_dirs={  # Remember to change this to match your filesystem!
                "interaction_single":self._train_config.dataset_path
            },

            # first time true, then false
            save_index = False,
            # filter_fn = stationary_filter
        )
        # print(kwargs)
        self.train_dataset = UnifiedDataset(**kwargs)

        kwargs["desired_data"] = ["val"]
        kwargs["rebuild_cache"] = False
        self.valid_dataset = UnifiedDataset(**kwargs)
        
        kwargs["desired_data"] = ["test"]
        kwargs["rebuild_cache"] = False
        del kwargs["future_sec"]
        self.test_dataset = UnifiedDataset(**kwargs)

    def train_dataloader(self, return_dict = True):
        # Exploration:
        # You can choose the dataloader parameters. For instance, whether to shuffle.
        
        return DataLoader(
            dataset=self.train_dataset,
            shuffle=True,
            batch_size=self._train_config.training.batch_size,
            num_workers=self._train_config.training.num_data_workers,
            drop_last=True,
            collate_fn=self.train_dataset.get_collate_fn(return_dict=return_dict),
            persistent_workers=True if self._train_config.training.num_data_workers>0 else False
            
        )

    def val_dataloader(self, return_dict = True):
        return DataLoader(
            dataset=self.valid_dataset,
            shuffle=False,
            batch_size=self._train_config.validation.batch_size,
            num_workers=self._train_config.validation.num_data_workers,
            drop_last=True,
            collate_fn=self.valid_dataset.get_collate_fn(return_dict=return_dict),
            persistent_workers=True if self._train_config.validation.num_data_workers>0 else False
        )

    def test_dataloader(self, return_dict = True):
        pred_ids = np.load('extra_files/pred_ids.npy')
        pred_dataset= Subset(self.test_dataset, pred_ids)
        
        return DataLoader(
            dataset=pred_dataset,
            shuffle=False,
            batch_size=self._train_config.test.batch_size,
            num_workers=self._train_config.test.num_data_workers,
            drop_last=False,
            collate_fn=self.test_dataset.get_collate_fn(return_dict=return_dict),
            persistent_workers=True if self._train_config.test.num_data_workers>0 else False
        )

    def predict_dataloader(self):
        pass
    
    @staticmethod
    def stationary_filter(elem) -> bool:
        return elem.agent_meta_dict["is_stationary"]
