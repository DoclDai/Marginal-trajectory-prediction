from me292b.configs.config import Dict
from copy import deepcopy
import math

class TrainConfig(Dict):
    def __init__(self):
        super(TrainConfig, self).__init__()
        
        self.dataset_path = "MODIFY_ME"
        self.seed = 0
        self.logging.terminal_output_to_txt = True  # whether to log stdout to txt file
        self.logging.log_tb = True  # enable tensorboard logging
        self.logging.log_wandb = False  # enable wandb logging
        self.logging.log_every_n_steps = 10
        self.logging.flush_every_n_steps = 100

        ## save config - if and when to save model checkpoints ##
        self.save.enabled = True  # whether model saving should be enabled or disabled
        self.save.every_n_steps = 100  # save model every n epochs
        self.save.best_k = 5
        self.save.save_best_rollout = False
        self.save.save_best_validation = True

        ## evaluation rollout config ##
        self.rollout.save_video = True
        self.rollout.enabled = False  # enable evaluation rollouts
        self.rollout.every_n_steps = 1000  # do rollouts every @rate epochs
        self.rollout.warm_start_n_steps = 1  # number of steps to wait before starting rollouts

        # Exploration:
        # Adjust the training configuration
        # Choose the following parameters based on your GPUs. 
        
        ## training config
        self.training.batch_size = 32
        self.training.num_steps = 100000
        self.training.num_data_workers = 8

        ## validation config
        self.validation.enabled = True
        self.validation.batch_size = 32
        self.validation.num_data_workers = 8
        self.validation.every_n_steps = 1000
        self.validation.num_steps_per_epoch = 100
        
        ## test config
        self.test.enabled = True
        self.test.batch_size = 32
        self.test.num_data_workers = 8
        self.test.every_n_steps = 1000
        self.test.num_steps_per_epoch = 100
        

        ## Training parallelism (e.g., multi-GPU)
        self.parallel_strategy = "ddp_spawn"


class EnvConfig(Dict):
    def __init__(self):
        super(EnvConfig, self).__init__()
        self.name = "my_env"


class AlgoConfig(Dict):
    def __init__(self):
        super(AlgoConfig, self).__init__()
        self.name = "my_algo"
# ----------------------------config --------------------------------

class BehaviorCloningConfig(AlgoConfig):
    def __init__(self):
        super(BehaviorCloningConfig, self).__init__()
     
        self.name = "bc"
        self.raster_size = 224
        self.pixel_size = 0.5
          
        # Exploration:
        # Adjust the model structure
        
        self.model_architecture = "resnet18" #mobilenet_v2 resnet18
        self.map_feature_dim = 256
        self.history_num_frames = 9
        self.history_num_frames_ego = 9
        self.history_num_frames_agents = 9
        self.future_num_frames = 30
        self.step_time = 0.1
        self.render_ego_history = False
        self.decoder.layer_dims = () # you can make the decoder more complex
        self.decoder.state_as_input = True
        
   

        # Exploration:
        # You can choose whether to use dynamic layers
        
        self.dynamics.type = None
        
        # # This is an example of dynamic layer parameters
        # self.dynamics.type = "Unicycle"
        # self.dynamics.max_steer = 0.5
        # self.dynamics.max_yawvel = math.pi * 2.0
        # self.dynamics.acce_bound = (-10, 8)
        # self.dynamics.ddh_bound = (-math.pi * 2.0, math.pi * 2.0)
        # self.dynamics.max_speed = 40.0  # roughly 90mph


        # Exploration:
        # You can choose the weights of your loss function
        
        self.loss_weights.prediction_loss = 1.0
        self.loss_weights.goal_loss = 0.0
        self.loss_weights.yaw_reg_loss = 0.001


        # Exploration:
        # You can change the learning rate and its schedule.
        
        self.optim_params.predictor.learning_rate.initial = 1e-4  # predictor learning rate
        self.optim_params.predictor.learning_rate.decay_factor = (
            0.1  # factor to decay LR by (if epoch schedule non-empty)
        )
        self.optim_params.predictor.learning_rate.epoch_schedule = (
            []
        )  # epochs where LR decay occurs
        self.optim_params.predictor.regularization.L2 = 0.00  # L2 regularization strength
