package Entity

import jakarta.persistence.Entity
import jakarta.persistence.Id

@Entity
class hand(
        @Id
        var hand_id: Int = 1,
        var rx: Int = 0,
        var ry: Int = 0,
        var lx: Int = 0,
        var ly: Int = 0
)