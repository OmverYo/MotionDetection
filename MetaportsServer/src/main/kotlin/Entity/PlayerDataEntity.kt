package Entity

import jakarta.persistence.Entity
import jakarta.persistence.GeneratedValue
import jakarta.persistence.GenerationType
import jakarta.persistence.Id

@Entity
class player_data(
        @Id @GeneratedValue(strategy = GenerationType.IDENTITY)
        var play_id: Int = 0,
        var total: Int = 0,
        var perfect_frame: Int = 0,
        var awesome_frame: Int = 0,
        var good_frame: Int = 0,
        var ok_frame: Int = 0,
        var bad_frame: Int = 0
)