package Entity

import jakarta.persistence.Entity
import jakarta.persistence.GeneratedValue
import jakarta.persistence.GenerationType
import jakarta.persistence.Id

@Entity
class background(
        @Id @GeneratedValue(strategy = GenerationType.IDENTITY)
        var user_id: Int = 0,
        var is_vr: Boolean = false,
        var bg_name: String = "",
        var coord_name: String = ""
)