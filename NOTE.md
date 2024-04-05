## Announcement
Considering that many students suffer from a lack of computing resources, we provide several modifications to the base code and some hints to potentially improve the model's performance.


### Modification
#### Default training parameters
We have changed the default training parameters to prevent out-of-memory issues when training the base model on computers without a GPU. Specifically, we set self.training.batch_size = 16, self.validation.batch_size = 16, and self.test.batch_size = 16. Since the default training batch size is smaller, we have also adjusted the default learning rate from 1e-3 to 1e-4 to stabilize the training.


#### Pretrained Convolutional Neural Networks
Pretrained networks can generally accelerate training compared to training from scratch. We can use the pretrained MobileNet_v2 for image tasks and fine-tune it for the prediction task (see lines 64-69 in me292b/models/base_models.py). To further accelerate training, we also provide a pretrained MobileNet_v2 specifically for the prediction task (see lines 96-100 in me292b/models/base_models.py). This checkpoint of MobileNet_v2 is stored in extra_files/mn_pretrained.pkl.


Note that with the pretrained MobileNet_v2 stored in extra_files/mn_pretrained.pkl and suitable code modifications, you can achieve ADE of 0.7445 and MR of 0.5416 in just 1000 training steps, and ADE of 0.7284 and MR of 0.53 in 5000 training steps (see 'me292b-24sp-ta-ckpt1000' and 'me292b-24sp-ta-ckpt5000' on the leaderboard).


#### Accelerate the test process
We have also accelerated the testing process (see lines 100-102 in me292b/data/trajdata_datamodules.py). The related file is stored in extra_files/pred_ids.npy. In some cases, the testing process will be approximately 5 times faster.


### Hints
To improve prediction performance, introducing randomness into the training dataset is recommended, and incorporating vehicle dynamics will help accelerate the training since it constrains the feasible space of the trajectory.

### Monitor your training process
You can use tensorboard to monitor your training process.
```sh
tensorboard --logdir experiments/
```
An example is stored in extra_files/tb.png.

![tb](extra_files/tb.png)
