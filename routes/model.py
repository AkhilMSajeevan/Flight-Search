from django.db import models


class AirportRoute(models.Model):
    """
    Represents an airport node in a binary tree structure.
    
    Attributes:
        parent_airport: Reference to parent airport (None for root)
        airport_code: Unique identifier for the airport
        position: Position relative to parent (Left/Right/Root)
        duration: Flight duration from parent to this airport (in minutes)
    """
    
    POSITION_CHOICES = [
        ('Left', 'Left'),
        ('Right', 'Right'),
        ('Root', 'Root'),
    ]
    
    parent_airport = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children',
        help_text='Parent airport in the tree structure'
    )
    
    airport_code = models.CharField(
        max_length=100,
        help_text='Airport identifier (e.g., Airport A, Airport B)'
    )
    
    position = models.CharField(
        max_length=10,
        choices=POSITION_CHOICES,
        help_text='Position relative to parent airport'
    )
    
    duration = models.IntegerField(
        default=0,
        help_text='Flight duration from parent airport (in minutes)'
    )
    
    class Meta:
        verbose_name = 'Airport Route'
        verbose_name_plural = 'Airport Routes'
        # Ensure no duplicate position for same parent
        unique_together = ['parent_airport', 'position']
    
    def __str__(self):
        """String representation showing airport code and duration"""
        return f"{self.airport_code} ({self.duration} min)"
    
    def get_total_duration(self):
        """
        Calculate total duration from root to this airport.
        
        Returns:
            int: Cumulative duration in minutes
        """
        total = 0
        current = self
        
        while current:
            total += current.duration
            current = current.parent_airport
        
        return total
    
    def get_path_from_root(self):
        """
        Get the complete path from root to this airport.
        
        Returns:
            list: List of airport codes from root to current
        """
        path = []
        current = self
        
        while current:
            path.insert(0, current.airport_code)
            current = current.parent_airport
        
        return path
    
    def get_depth(self):
        """
        Get the depth/level of this airport in the tree.
        
        Returns:
            int: Depth (root = 0, children of root = 1, etc.)
        """
        depth = 0
        current = self.parent_airport
        
        while current:
            depth += 1
            current = current.parent_airport
        
        return depth

