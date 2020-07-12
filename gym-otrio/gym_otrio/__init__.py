from gym.envs.registration import register

register(
    id='otrio-v0',
    entry_point='gym_otrio.envs:OtrioEnv'
)
