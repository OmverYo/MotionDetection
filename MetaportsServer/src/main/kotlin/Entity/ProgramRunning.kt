package Entity

import jakarta.persistence.Entity
import jakarta.persistence.GeneratedValue
import jakarta.persistence.GenerationType
import jakarta.persistence.Id

@Entity
class program_running(
        @Id @GeneratedValue(strategy = GenerationType.IDENTITY)
        var program_id: Int = 0,
        var is_running: Boolean = true
)