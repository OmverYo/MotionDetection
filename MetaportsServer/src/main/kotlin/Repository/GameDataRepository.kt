package Repository

import Entity.mt_training_result
import org.springframework.data.jpa.repository.JpaRepository

interface GameDataRepository: JpaRepository<mt_training_result, Int>
{

}