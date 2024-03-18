# Copyright (c) Hyggge. All rights reserved.
import mmcv
import os
import numpy as np
from mmcv.parallel import DataContainer as DC
from mmseg.datasets.builder import PIPELINES
from mmseg.datasets.pipelines.formatting import to_tensor



@PIPELINES.register_module()
class LoadLaneDetectGT(object):
    """Transfer gt_semantic_seg to binary mask and generate gt_labels."""
    def __init__(self, aux_gt_dirs, suffixs):
        self.aux_gt_dirs = aux_gt_dirs
        self.suffixs = suffixs
        self.file_client = mmcv.FileClient(backend='disk')

    def __call__(self, results):
        
        for i, (dir, suffix) in enumerate(zip(self.aux_gt_dirs, self.suffixs)):
            filename = os.path.join(dir, results['img_info']['filename'])
            filename = os.path.splitext(filename)[0] + suffix
            img_bytes = self.file_client.get(filename)
            aux_gt = mmcv.imfrombytes(
                img_bytes, flag='grayscale', backend='cv2').squeeze().astype(np.uint8)
            # convert to train ID
            aux_gt[aux_gt > 128] = 255
            aux_gt[aux_gt <= 128] = 0
            aux_gt[aux_gt == 255] = 1
            # aux_gt_list.append(aux_gt)
            results[f'aux_gt_{i+1}'] = aux_gt
            results['seg_fields'].append(f'aux_gt_{i+1}')
        
        # print(f"{results.keys()=}")
        # print(f"{results['img_info'].keys()=}")
        # print(results)
        return results

    def __repr__(self):
        return self.__class__.__name__ + \
               f'(ignore_index={self.ignore_index})'

@PIPELINES.register_module()
class LoadRoadMarkGT(object):
    """Transfer gt_semantic_seg to binary mask and generate gt_labels."""
    def __init__(self, aux_gt_dirs, suffixs):
        self.aux_gt_dirs = aux_gt_dirs
        self.suffixs = suffixs
        self.file_client = mmcv.FileClient(backend='disk')
        self.id_list = [0, 200, 204, 213, 209, 206, 207, 201, 203, 211, 208, 216, 217, 
            215, 218, 219, 210, 232, 214, 202, 220, 221, 222, 231, 224, 225, 
            226, 230, 228, 229, 233, 205, 212, 227, 223, 250, 249, 255]


    def __call__(self, results):
        
        for i, (dir, suffix) in enumerate(zip(self.aux_gt_dirs, self.suffixs)):
            filename = os.path.join(dir, results['img_info']['filename'])
            filename = os.path.splitext(filename)[0] + suffix
            img_bytes = self.file_client.get(filename)
            aux_gt = mmcv.imfrombytes(
                img_bytes, flag='grayscale', backend='cv2').squeeze().astype(np.uint8)
            # convert to train ID
            for target, ori in enumerate(self.id_list):
                if ori == 249:
                    # deal with noise and ignored label
                    aux_gt[aux_gt == ori] = 0
                elif ori == 255:
                    pass
                else:
                    aux_gt[aux_gt == ori] = target
            # aux_gt_list.append(aux_gt)
            results[f'aux_gt_{i+1}'] = aux_gt
            results['seg_fields'].append(f'aux_gt_{i+1}')
        
        # print(f"{results.keys()=}")
        # print(f"{results['img_info'].keys()=}")
        # print(results)
        return results

    def __repr__(self):
        return self.__class__.__name__ + \
               f'(ignore_index={self.ignore_index})'

@PIPELINES.register_module()
class LoadBinRoadMarkGT(object):
    """Transfer gt_semantic_seg to binary mask and generate gt_labels."""
    def __init__(self, aux_gt_dirs, suffixs):
        self.aux_gt_dirs = aux_gt_dirs
        self.suffixs = suffixs
        self.file_client = mmcv.FileClient(backend='disk')
        self.id_list = [0, 200, 204, 213, 209, 206, 207, 201, 203, 211, 208, 216, 217, 
            215, 218, 219, 210, 232, 214, 202, 220, 221, 222, 231, 224, 225, 
            226, 230, 228, 229, 233, 205, 212, 227, 223, 250, 249, 255]


    def __call__(self, results):
        
        for i, (dir, suffix) in enumerate(zip(self.aux_gt_dirs, self.suffixs)):
            filename = os.path.join(dir, results['img_info']['filename'])
            filename = os.path.splitext(filename)[0] + suffix
            img_bytes = self.file_client.get(filename)
            aux_gt = mmcv.imfrombytes(
                img_bytes, flag='grayscale', backend='cv2').squeeze().astype(np.uint8)
            # convert to train ID
            for target, ori in enumerate(self.id_list):
                if ori == 249:
                    # deal with noise and ignored label
                    aux_gt[aux_gt == ori] = 0
                elif ori == 255:
                    pass
                elif ori != 0:
                    aux_gt[aux_gt == ori] = 1
            # aux_gt_list.append(aux_gt)
            results[f'aux_gt_{i+1}'] = aux_gt
            results['seg_fields'].append(f'aux_gt_{i+1}')
        
        # print(f"{results.keys()=}")
        # print(f"{results['img_info'].keys()=}")
        # print(results)
        return results

    def __repr__(self):
        return self.__class__.__name__ + \
               f'(ignore_index={self.ignore_index})'

@PIPELINES.register_module()
class LoadCustomRoadMarkGT(object):
    """Transfer gt_semantic_seg to binary mask and generate gt_labels."""
    def __init__(self, aux_gt_dirs, suffixs, id_map=None):
        self.aux_gt_dirs = aux_gt_dirs
        self.suffixs = suffixs
        self.file_client = mmcv.FileClient(backend='disk')
        self.id_list = [0, 200, 204, 213, 209, 206, 207, 201, 203, 211, 208, 216, 217,
            215, 218, 219, 210, 232, 214, 202, 220, 221, 222, 231, 224, 225,
            226, 230, 228, 229, 233, 205, 212, 227, 223, 250, 249, 255]
        if id_map is None:
            self.id_map = {k : v for k, v in zip(self.id_list[1:-2], range(1, 36))}
            self.id_map[0] = 0
            self.id_map[249] = 0
            self.id_map[255] = 255

        else:
            self.id_map = id_map


    def __call__(self, results):
        for i, (dir, suffix) in enumerate(zip(self.aux_gt_dirs, self.suffixs)):
            filename = os.path.join(dir, results['img_info']['filename'])
            filename = os.path.splitext(filename)[0] + suffix
            img_bytes = self.file_client.get(filename)
            aux_gt = mmcv.imfrombytes(
                img_bytes, flag='grayscale', backend='cv2').squeeze().astype(np.uint8)
            # convert to train ID
            for k, v in self.id_map.items():
                aux_gt[aux_gt == k] = v
            # aux_gt_list.append(aux_gt)
            results[f'aux_gt_{i+1}'] = aux_gt
            results['seg_fields'].append(f'aux_gt_{i+1}')

        # print(f"{results.keys()=}")
        # print(f"{results['img_info'].keys()=}")
        # print(results)
        return results

    def __repr__(self):
        return self.__class__.__name__ + \
               f'(ignore_index={self.ignore_index})'