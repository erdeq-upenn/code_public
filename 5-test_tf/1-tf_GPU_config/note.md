# using GPU
## 1. logging device placement
To find out which devices your operations and tensors are assigned to, put tf.debugging.set_log_device_placement(True) as the first statement of your program. Enabling device placement logging causes any Tensor allocations or operations to be printed.
## 2. limiting GPU memory growth
By default, TensorFlow maps nearly all of the GPU memory of all GPUs (subject to CUDA_VISIBLE_DEVICES) visible to the process.  
This is done to more efficiently use the relatively precious GPU memory resources on the devices by reducing memory fragmentation. To limit TensorFlow to a specific set of GPUs, use the tf.config.set_visible_devices method.
```
gpus = tf.config.list_physical_devices('GPU')
if gpus:
  # Restrict TensorFlow to only use the first GPU
  try:
    tf.config.set_visible_devices(gpus[0], 'GPU')
    logical_gpus = tf.config.list_logical_devices('GPU')
    print(len(gpus), "Physical GPUs,", len(logical_gpus), "Logical GPU")
  except RuntimeError as e:
    # Visible devices must be set before GPUs have been initialized
    print(e)


tf.debugging.set_log_device_placement(True)
tf.config.set_soft_device_placement(True)
```
