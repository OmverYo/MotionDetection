package Repository

import Entity.background
import org.springframework.data.jpa.repository.JpaRepository

interface BackgroundDataRepository: JpaRepository<background, Int>
{

}