package Repository

import Entity.hand
import org.springframework.data.jpa.repository.JpaRepository

interface HandDataRepository: JpaRepository<hand, Int>
{

}
