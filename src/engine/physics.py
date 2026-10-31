# src/engine/physics.py

class BoxCollider:
    """A lightweight 3D Axis-Aligned Bounding Box (AABB) collision detector."""
    def __init__(self, center, size):
        self.center = center  # (x, y, z)
        self.size = size      # (width, height, depth)

    def update_position(self, center):
        self.center = center

    def intersects(self, other_box):
        """Checks if this bounding box overlaps with another BoxCollider."""
        cx1, cy1, z1 = self.center
        sx1, sy1, sz1 = self.size
        
        cx2, cy2, z2 = other_box.center
        sx2, sy2, sz2 = other_box.size

        # Calculate half extents
        hx1, hy1, hz1 = sx1 / 2.0, sy1 / 2.0, sz1 / 2.0
        hx2, hy2, hz2 = sx2 / 2.0, sy2 / 2.0, sz2 / 2.0

        # Test overlap on X, Y, and Z axes
        overlap_x = abs(cx1 - cx2) < (hx1 + hx2)
        overlap_y = abs(cy1 - cy2) < (hy1 + hy2)
        overlap_z = abs(z1 - z2) < (hz1 + hz2)

        return overlap_x and overlap_y and overlap_z

def check_collision(player, obstacle):
    """Convenience helper to check AABB collision between player and an obstacle entity."""
    # Player origin adjustment (centered on feet, so center Y is offset by half height)
    p_center = (player.x, player.y + player.scale_y / 2.0, player.z)
    p_size = (player.scale_x, player.scale_y, player.scale_z)

    o_center = (obstacle.x, obstacle.y, obstacle.z)
    o_size = (obstacle.scale_x, obstacle.scale_y, obstacle.scale_z)

    player_box = BoxCollider(p_center, p_size)
    obstacle_box = BoxCollider(o_center, o_size)

    return player_box.intersects(obstacle_box)