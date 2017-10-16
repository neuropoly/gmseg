import subprocess
import glob
import os
import nibabel as nib
import re
import numpy as np
from tqdm import tqdm

def make_filename(site_num, subject, rater=None):
    if rater is None:
        return "site{:d}-sc{:02d}-image.nii.gz".format(site_num,
                                                       subject)
    else:
        return "site{:d}-sc{:02d}-mask-r{:d}.nii.gz".format(site_num,
                                                            subject,
                                                            rater)
def run_main():
    # 1. fslmaths to remove wm class
    # fslmaths site2-sc05-mask-r4.nii.gz -uthr 1 new_mask.nii.gz

    dices = []
    for site in tqdm(xrange(1, 5), desc="Site   "):
        for subject in tqdm(xrange(1, 11), desc="Subject"):
            for rater in tqdm(xrange(1, 5), desc="Rater  "):
                mask_fname = make_filename(site, subject, rater)
                mask_fname_abs = os.path.join("training", mask_fname)
                
                gm_mask_fname = "gm_{}".format(mask_fname)
                gm_mask_fname_abs = os.path.join("training_masks", gm_mask_fname)
                
                prefix_image = "-".join(mask_fname.split("-")[0:2])
                image_name = "{}_csp.nii.gz".format(prefix_image)
                image_name = os.path.join("training_predictions", image_name)
                
                cmd = ["sct_dice_coefficient", "-i {}".format(gm_mask_fname_abs),
                       "-d {}".format(image_name)]
                output = subprocess.check_output(cmd)                  
                dice = float(re.findall("coefficient = (\d+\.\d+)", output)[0])
                dices.append(dice)
          
                avg = np.asarray(dices, dtype=np.float32).mean()
                tqdm.write("Dice: {:.6f} - Avg. [{:.6f}] [{}]".format(dice, avg, gm_mask_fname_abs))
                
                
    dices = np.asarray(dices, dtype=np.float32)
    print "Mean", dices.mean()
    



if __name__ == "__main__":
    run_main()
