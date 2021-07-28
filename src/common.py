import argparse
import attr
import functools
import types
import collections
import pdb
import logging

from pathlib import Path
from tqdm import tqdm

from typing import Union, Optional, Callable
from dataclasses import dataclass

import hydra
from omegaconf import DictConfig, OmegaConf
#import pytorch_lightning as pl
import numpy as np

def orig_cwd():
    return Path(hydra.utils.get_original_cwd())