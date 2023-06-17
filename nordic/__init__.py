import os
from typing import Optional, List
import mrt

try:
    mrt = mrt.initialize()
except Exception as e:
    print("Error initializing nordic package\\n:{}".format(e))
    exit(1)

def nordic(mag_image_path: str, 
           phase_image_path: Optional[str] = None, 
           output_dir: Optional[str] = None,
           output_filename: Optional[str] = None, 
           output_ext: str = "nii.gz",
           modality: Optional[str] = None,
           threshold_method: str = "NORDIC",
           noise_volume_last: int = 0,
           factor_error: float = 1.0,
           full_dynamic_range: int = 0,
           kernel_size_gfactor: List[int] = [14, 14, 1],
           kernel_size_PCA: Optional[List[int]] = None,
           **kwargs
           ):
    """
    Runs the NORDIC algorithm on MRI data. 
    
    Args:
        mag_image_path (str): Path to the input magnitude image file.
        phase_image_path (str, optional): Path to the input phase image file. Defaults to None.
        output_dir (str, optional): Directory to save the output image. Defaults to None.
        output_filename (str, optional): Name of the output file. Defaults to None.
        output_ext (str, optional): Extension of the output file. Defaults to "nii.gz".
        modality (str, optional): Modality of the image, either "fMRI" or "dMRI". Defaults to None.
        threshold_method (str, optional): Thresholding method, either "NORDIC" or "MP" (Marchenko-Pastur). Defaults to "NORDIC".
        noise_volume_last (int, optional): Noise volume last parameter. Defaults to 0.
        factor_error (float, optional): Factor error parameter. Defaults to 1.0.
        full_dynamic_range (int, optional): Full dynamic range parameter. Defaults to 0.
        kernel_size_gfactor (List[int], optional): Kernel size for the g-factor. Defaults to [14, 14, 1].
        kernel_size_PCA (List[int], optional): Kernel size for PCA. Defaults to None.

    Raises:
        FileNotFoundError: If input image file does not exist.
        ValueError: If provided modality or thresholding method or image format is not supported.
    """
    
    # Initialize arguments
    args = {
        "DIROUT": output_dir if isinstance(output_dir, str) else '',
        "noise_volume_last": noise_volume_last,
        "factor_error": factor_error,
        "full_dynamic_range": full_dynamic_range,
        "kernel_size_gfactor": matlab.double(kernel_size_gfactor),
        "kernel_size_PCA": matlab.double(kernel_size_PCA) if isinstance(kernel_size_PCA, list) else matlab.double([]),
    }

    # Set modality specific parameters  
    if modality:
        if modality == "fMRI":
            args["temporal_phase"] = 1
            args["phase_filter_width"] = 10
        elif modality == "dMRI":
            args["temporal_phase"] = 3
            args["phase_filter_width"] = 3
        else:
            raise ValueError("{} is not supported modality".format(modality))
    
    # Set thresholding method
    if threshold_method == "NORDIC":
        args["NORDIC"] = 1
        args["MP"] = 0
    elif threshold_method == "MP":
        args["NORDIC"] = 0
        args["MP"] = 1
    else:
        raise ValueError("{} is not supported threshold method".format(threshold_method))

    # Additional keyword arguments
    for k, v in kwargs.items():
        args[k] = v
    
    # Check if magnitude image exists
    if not os.path.exists(mag_image_path):
        raise FileNotFoundError(f"Input magnitude image file not found: {mag_image_path}")
    
    # Check if phase image exists
    if phase_image_path is None:
        phase_image_path = ""
    elif not os.path.exists(phase_image_path):
        raise FileNotFoundError(f"Input phase image file not found: {phase_image_path}")
        args["magnitude_only"] = 1
    
    # Construct output file path
    output_filename = output_filename.split('.')[0]
    output_path = f"{output_filename}.nii"
    
    # Run NORDIC algorithm
    mrt.nordic(mag_image_path, phase_image_path, output_path, args)
    
    # Compress output if required
    if output_ext == "nii.gz":
        import nibabel as nib
        output_filepath = os.path.join(output_dir, output_path) if output_dir else output_path
        output_compressed = os.path.join(output_dir, f"{output_filename}.{output_ext}") if output_dir else f"{output_filename}.{output_ext}"
        nib.load(output_filepath).to_filename(output_compressed)
        os.remove(output_filepath)
    elif output_ext == "nii":
        pass
    else:
        raise ValueError(f"{output_ext} is not a supported image format")
