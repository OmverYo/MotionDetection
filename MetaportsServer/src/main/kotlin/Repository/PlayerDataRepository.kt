package Repository

import Entity.player_data
import org.springframework.data.jpa.repository.JpaRepository

interface PlayerDataRepository: JpaRepository<player_data, Int>
{

}
