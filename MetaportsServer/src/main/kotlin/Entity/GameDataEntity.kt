package Entity

import jakarta.persistence.Entity
import jakarta.persistence.GeneratedValue
import jakarta.persistence.GenerationType
import jakarta.persistence.Id

@Entity
class mt_training_result(
        @Id @GeneratedValue(strategy = GenerationType.IDENTITY)
        var play_id: Int = 0,
        var capture_time: Int = 0,
        var accuracy: Int = 0
)