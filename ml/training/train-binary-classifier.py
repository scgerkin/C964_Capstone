from training.utils import (get_dx_labels,
                            get_img_metadata,
                            print_gpu_status,
                            )


print_gpu_status()

dx_labels = get_dx_labels()
print(f"Total diagnostic labels imported: {len(dx_labels)}")
img_metadata = get_img_metadata()
print(f"Total usable images: {len(img_metadata)}")

#%%
