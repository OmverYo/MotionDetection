package Entity

import jakarta.persistence.Entity
import jakarta.persistence.Id

@Entity
class recommend(
        @Id
        var user_id: Int = 0,
        var content_url: String = "",
        var content_name: String = ""
)