from particles.particle import Particle, Vector


class RigidJoint:
    def __init__(self, particle1: Particle, particle2: Particle, distance: float):
        self.particle1 = particle1
        self.particle2 = particle2
        self.distance = distance

    def enforce_constraint(self):
        position1 = self.particle1.position
        position2 = self.particle2.position
        # Calculate the current distance between the particles
        current_distance = position1.subtract(position2).length()
        # print(f"current_distance: {current_distance}")

        # Calculate the difference between the current distance and the desired distance
        difference = self.distance - current_distance

        # Calculate the direction in which to move the particles
        direction = position1.subtract(position2).normalize()

        # Calculate the amount to move each particle
        move_amount = direction.multiply(difference)

        # Move the particles to maintain the desired distance
        # self.particle1.position = position1.add(move_amount)
        self.particle2.position = position2.subtract(move_amount)


class RigidChain:
    def __init__(self, particles: [Particle], distance: float):
        self.particles = particles
        self.joints = [
            RigidJoint(self.particles[i], self.particles[i + 1], distance)
            for i in range(len(self.particles) - 1)
        ]

    def update(self):
        # Update the positions of the particles
        for particle in self.particles:
            particle.update()

        # Enforce the constraints of the rigid joints
        for joint in self.joints:
            joint.enforce_constraint()


class SpringJoint:
    def __init__(
        self,
        particle1: Particle,
        particle2: Particle,
        rest_length: float,
        stiffness: float,
        damping: float = 0.1,
    ):
        self.particle1 = particle1
        self.particle2 = particle2
        self.rest_length = rest_length
        self.stiffness = stiffness
        self.damping = damping

    def current_length(self):
        return self.particle1.position.subtract(self.particle2.position).length()

    def apply_force(self):
        # Calculate the current length of the spring
        current_length = self.current_length()

        # Calculate the displacement of the spring from its rest length
        displacement = self.rest_length - current_length

        # Calculate the force exerted by the spring using Hooke's law
        spring_force = displacement * self.stiffness

        # Calculate the damping force
        relative_velocity = self.particle1.velocity.subtract(self.particle2.velocity)
        damping_force = relative_velocity.length() * self.damping

        # Calculate the total force
        total_force = spring_force - damping_force

        # Calculate the direction of the force
        direction = self.particle1.position.subtract(
            self.particle2.position
        ).normalize()

        # Apply the force to the particles
        self.particle1.apply_force(direction.multiply(total_force))
        self.particle2.apply_force(direction.multiply(-total_force))


class SpringChain:
    def __init__(self, particles: [Particle], rest_length, stiffness=0.1, damping=0.1):
        self.particles = particles
        self.springs = [
            SpringJoint(
                self.particles[i],
                self.particles[i + 1],
                rest_length,
                stiffness,
                damping,
            )
            for i in range(len(self.particles) - 1)
        ]

    def update(self):
        # Apply the forces exerted by the springs
        for spring in self.springs:
            spring.apply_force()

        # Update the positions of the particles
        for particle in self.particles:
            particle.update()
