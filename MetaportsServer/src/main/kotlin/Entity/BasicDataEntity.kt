package Entity

import jakarta.persistence.Entity
import jakarta.persistence.GeneratedValue
import jakarta.persistence.GenerationType
import jakarta.persistence.Id

@Entity
class basic_data(
        @Id @GeneratedValue(strategy = GenerationType.IDENTITY)
        var play_id: Int = 0,
        var reaction_time: Float = 0.0F,
        var on_air: Float = 0.0F,
        var squat_jump: Int = 0,
        var knee_punch: Int = 0,
        var balance_test: Int = 0,
        var content_url: String = "",
        var content_name: String = ""
)