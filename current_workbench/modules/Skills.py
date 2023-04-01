class Skills:
    """
    This class is used to manage the skills of a entity.
    """
    def __init__(self,
                 hp:int,
                 att_speed:int,
                 att_velocity:int,
                 damage:int,
                 piercing:int
                 ) -> None:
        """
        Initializes a new object of the Skills class.

        args:
            hp (int): the maximum hp that the entity can have.
            att_speed (int): the number of attack per second.
            att_velocity (int): the attack's velocity.
            damage (int): the attack's damage.
        """
        
        self.HP_max = hp
        self.att_speed = att_speed
        self.att_velocity = att_velocity
        self.damage = damage
        self.piercing = piercing