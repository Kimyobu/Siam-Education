import diffusers

class Schedulers:
    scheduler_list = {
        "DEIS": diffusers.DEISMultistepScheduler,
        "DPM++ Inverse": diffusers.DPMSolverMultistepInverseScheduler,
        "DPM++ 2M": diffusers.DPMSolverMultistepScheduler,
        "DPM SDE": diffusers.DPMSolverSDEScheduler,
        "DPM++ SDE": diffusers.DPMSolverSinglestepScheduler,
        "DPM2": diffusers.KDPM2DiscreteScheduler,
        "DPM2 a": diffusers.KDPM2AncestralDiscreteScheduler,
        "Euler": diffusers.EulerDiscreteScheduler,
        "Euler a": diffusers.EulerAncestralDiscreteScheduler,
        "Heun": diffusers.HeunDiscreteScheduler,
        "LMS": diffusers.LMSDiscreteScheduler,
        "UniPC": diffusers.UniPCMultistepScheduler,
    }
    def __call__(self, name: str):
        if name in self.scheduler_list:
            return self.scheduler_list[name]
        else:
            return self.scheduler_list["DPM++ 2M"]