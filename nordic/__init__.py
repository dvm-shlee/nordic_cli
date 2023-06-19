import os
import gzip
import shutil
from typing import Optional, List
from .mrt import _pir

try:
    nrd = _pir.initialize_package()
    import matlab
except Exception as e:
    print("Error initializing nordic package\\n:{}".format(e))

def compress_file(input_file_path: str, output_file_path: str):
    with open(input_file_path, 'rb') as f_in:
        with gzip.open(output_file_path, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)

def run(magni_path: str,
        output_path: str,
        phase_path: Optional[str] = None,
        modality: Optional[str] = None,
        threshold_method: str = "NORDIC",
        kernel_size_gfactor: List[int] = [14, 14, 1],
        kernel_size_pca: Optional[List[int]] = None,
        verbose: bool = False,
        **kwargs
        ):
    """
    Executes the NORDIC algorithm on a NIFTI dataset. 

    Args:
        magni_path (str): Path to the input magnitude image file.
        output_path (str): Specifies the name of the output file. 
        phase_path (str, optional): Path to the input phase image file. If not provided, 
                                    the NORDIC algorithm runs with the 'magnitude_only' option. Defaults to None.
        modality (str, optional): Indicates the image modality - "fMRI" or "dMRI". If not specified, defaults to None.
        threshold_method (str, optional): Determines the thresholding method - 
                                          either "NORDIC" or "MP" (Marchenko-Pastur). Defaults to "NORDIC".
        kernel_size_gfactor (List[int], optional): Specifies the kernel size for the g-factor. Defaults to [14, 14, 1].
        kernel_size_pca (List[int], optional): Specifies the kernel size for PCA. If not provided, defaults to None.
        **kwargs (any) : All other options supported by MATLAB's NORDIC_NIFTI are case sensitive.

    Raises:
        FileNotFoundError: If the input image file does not exist.
        ValueError: If the provided modality or thresholding method or image format is not supported.
    """

    output_dir, output_file = os.path.split(output_path)
    output_list = output_file.split('.')
    output_filename = output_list[0]
    output_ext = ".".join(output_list[1:])
            
    # Initialize arguments
    args = {
        "DIROUT": f"{output_dir}/",
        "kernel_size_gfactor": matlab.int16(kernel_size_gfactor),
        "kernel_size_PCA": matlab.int16(kernel_size_pca) if isinstance(kernel_size_pca, list) else [],
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
        # prevent override input arguments
        if k in ["kernel_size_gfactor", "kernel_size_PCA"]:
            pass
        args[k] = v
    
    # Check if magnitude image exists
    if not os.path.exists(magni_path):
        raise FileNotFoundError(f"Input magnitude image file not found: {magni_path}")
    
    # Check if phase image exists
    if phase_path is None:
        phase_path = ""
        args["magnitude_only"] = 1
        args["use_magn_for_gfactor"] = 1
    elif not os.path.exists(phase_path):
        raise FileNotFoundError(f"Input phase image file not found: {phase_path}")

    if verbose:
        print("- Summary of input arguments (injected to MATLAB, NIFTI_NORDIC)")
        for k, v in args.items():
            print(f" {k} = {v}")
        print("\n")

    # Run NORDIC algorithm
    nrd.nordic(magni_path, phase_path, output_filename, args, nargout=0)
    
    # Compress output if required
    if output_ext == "nii.gz":
        print("compressing NORDIC output")
        temp_output = os.path.join(output_dir, "{}.nii".format(output_filename))
        compress_file(temp_output, output_path)
        os.unlink(temp_output)
    elif output_ext == "nii":
        pass
    else:
        raise ValueError(f"{output_ext} is not a supported image format")