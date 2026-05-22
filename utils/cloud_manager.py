# a utility for managing clouds
# init once and there will always be 'n' clouds
from sprites.cloud import Cloud

class CloudManager:
    def __init__(self, game_state, numclouds):
        self.game_state = game_state

        for _ in range(numclouds):
            cloud = Cloud(game_state)

        # cloud regeneration code not required
        # as clouds automatically generate a new 
        # cloud as they are dying