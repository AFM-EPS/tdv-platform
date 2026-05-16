from arcade.math import rand_in_circle
from arcade import particles

PARTICLE_SPEED_FAST = 2
DEFAULT_SCALE = 0.4
DEFAULT_ALPHA = 32
DEFAULT_EMIT_INTERVAL = 0.001
DEFAULT_EMIT_DURATION = 1.5

class TeleporterParticleSystem:
    def __init__(self, center_x, center_y, particle_path):

        self.emitter = particles.Emitter(
            center_xy = (center_x, center_y),
            emit_controller = particles.EmitterIntervalWithTime(
                DEFAULT_EMIT_INTERVAL,
                DEFAULT_EMIT_DURATION,
            ),
            particle_factory=lambda emitter: particles.LifetimeParticle(
                filename_or_texture = particle_path,
                change_xy = rand_in_circle((0.0, 0.0), PARTICLE_SPEED_FAST),
                lifetime = 1,
                scale = DEFAULT_SCALE,
                alpha = DEFAULT_ALPHA
            )
        )


    def update(self):
        self.emitter.update()


    def draw(self):
        self.emitter.draw()


    def is_finished(self):
        return self.emitter.can_reap()